"""
Hermes Config Generator - Agentic AI System
Multi-agent architecture for intelligent JSON configuration generation
"""

import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional
from openai import OpenAI
import os

# Initialize OpenAI client (API key from environment)
client = OpenAI()

class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.memory = []
        
    def log_action(self, action: str, result: Any):
        """Log agent actions for transparency"""
        self.memory.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "result": result
        })
        
    def get_memory(self) -> List[Dict]:
        """Retrieve agent memory"""
        return self.memory


class SchemaAnalyzerAgent(BaseAgent):
    """Agent responsible for analyzing file schema and structure"""
    
    def __init__(self):
        super().__init__(
            name="Schema Analyzer",
            role="Analyzes source files and infers schema, data types, and structure"
        )
    
    def analyze_file(self, file_path: str, file_type: str) -> Dict[str, Any]:
        """Analyze file and extract schema information"""
        try:
            # Read file based on type
            if file_type.lower() == 'csv':
                df = pd.read_csv(file_path, nrows=100)
            elif file_type.lower() == 'json':
                # Read JSON file - handle both array and line-delimited formats
                try:
                    # Try reading as JSON array first
                    df = pd.read_json(file_path)
                    # Limit to first 100 rows if more
                    if len(df) > 100:
                        df = df.head(100)
                except ValueError:
                    # If that fails, try line-delimited JSON
                    df = pd.read_json(file_path, lines=True, nrows=100)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            # Extract schema
            schema = {
                "file_type": file_type,
                "row_count_sample": len(df),
                "column_count": len(df.columns),
                "columns": []
            }
            
            # Analyze each column
            for col in df.columns:
                # Get sample values and convert to JSON-serializable format
                sample_values = df[col].head(3).tolist()
                # Convert Pandas Timestamp objects to strings
                sample_values = [str(val) if hasattr(val, 'isoformat') else val for val in sample_values]
                
                col_info = {
                    "name": col,
                    "dtype": str(df[col].dtype),
                    "null_count": int(df[col].isnull().sum()),
                    "unique_count": int(df[col].nunique()),
                    "sample_values": sample_values
                }
                schema["columns"].append(col_info)
            
            self.log_action("analyze_file", schema)
            return schema
            
        except Exception as e:
            error = {"error": str(e)}
            self.log_action("analyze_file_error", error)
            return error


class ConfigGeneratorAgent(BaseAgent):
    """Agent responsible for generating JSON configurations using LLM"""
    
    def __init__(self):
        super().__init__(
            name="Config Generator",
            role="Generates Hermes framework JSON configurations using AI"
        )
    
    def generate_config(self, schema: Dict[str, Any], feed_name: str, 
                       source_system: str) -> Dict[str, Any]:
        """Generate complete Hermes configuration using LLM"""
        
        # Prepare prompt for LLM
        prompt = f"""You are an expert in the Hermes data processing framework. Generate a complete JSON configuration for a new data feed based on the following schema:

Feed Name: {feed_name}
Source System: {source_system}
Schema: {json.dumps(schema, indent=2)}

Generate a comprehensive Hermes configuration that includes:
1. Process Config (process_id, process_name, source_system, schedule, enabled)
2. Feed File Config (feed_id, file_format, delimiter if CSV, columns with types)
3. ETL Steps (deduplication, validation, transformation steps)
4. Date Control (business_date handling)
5. File Pattern (output naming and location)

Return ONLY valid JSON without any markdown formatting or explanations."""

        try:
            # Call LLM
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a Hermes framework configuration expert. Generate only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            # Extract and parse JSON
            config_text = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if config_text.startswith("```"):
                config_text = config_text.split("```")[1]
                if config_text.startswith("json"):
                    config_text = config_text[4:]
            
            config = json.loads(config_text)
            
            self.log_action("generate_config", {"success": True, "feed_name": feed_name})
            return config
            
        except Exception as e:
            error_config = {
                "error": str(e),
                "fallback_config": self._generate_fallback_config(schema, feed_name, source_system)
            }
            self.log_action("generate_config_error", error_config)
            return error_config["fallback_config"]
    
    def _generate_fallback_config(self, schema: Dict, feed_name: str, 
                                 source_system: str) -> Dict:
        """Generate basic configuration without LLM"""
        return {
            "process_config": {
                "process_id": feed_name.upper().replace(" ", "_"),
                "process_name": feed_name,
                "source_system": source_system,
                "schedule": "Daily at 6 PM",
                "enabled": True
            },
            "feed_file_config": {
                "feed_id": feed_name.upper().replace(" ", "_"),
                "file_format": schema.get("file_type", "CSV"),
                "delimiter": "," if schema.get("file_type") == "csv" else None,
                "columns": schema.get("columns", [])
            },
            "etl_steps": [
                {"step_id": 1, "step_name": "Remove Duplicates", "step_type": "deduplication"},
                {"step_id": 2, "step_name": "Validate Data", "step_type": "validation"}
            ]
        }


class ValidationAgent(BaseAgent):
    """Agent responsible for validating generated configurations"""
    
    def __init__(self):
        super().__init__(
            name="Validation Agent",
            role="Validates generated configurations for completeness and correctness"
        )
    
    def validate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate configuration structure and completeness"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "score": 100
        }
        
        # Check required sections
        required_sections = ["process_config", "feed_file_config", "etl_steps"]
        for section in required_sections:
            if section not in config:
                validation_result["errors"].append(f"Missing required section: {section}")
                validation_result["valid"] = False
                validation_result["score"] -= 30
        
        # Validate process_config
        if "process_config" in config:
            process_config = config["process_config"]
            required_fields = ["process_id", "process_name", "source_system"]
            for field in required_fields:
                if field not in process_config:
                    validation_result["warnings"].append(f"Missing field in process_config: {field}")
                    validation_result["score"] -= 10
        
        # Validate feed_file_config
        if "feed_file_config" in config:
            feed_config = config["feed_file_config"]
            if "columns" not in feed_config or not feed_config["columns"]:
                validation_result["warnings"].append("No columns defined in feed_file_config")
                validation_result["score"] -= 15
        
        # Validate ETL steps
        if "etl_steps" in config:
            if not config["etl_steps"]:
                validation_result["warnings"].append("No ETL steps defined")
                validation_result["score"] -= 10
        
        self.log_action("validate_config", validation_result)
        return validation_result


class OptimizationAgent(BaseAgent):
    """Agent responsible for optimizing configurations"""
    
    def __init__(self):
        super().__init__(
            name="Optimization Agent",
            role="Optimizes configurations for performance and best practices"
        )
    
    def optimize_config(self, config: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize configuration based on data characteristics"""
        optimized = config.copy()
        recommendations = []
        
        # Add partitioning strategy for large datasets
        if schema.get("row_count_sample", 0) > 50:
            recommendations.append("Consider adding partitioning strategy for large dataset")
            if "optimization" not in optimized:
                optimized["optimization"] = {}
            optimized["optimization"]["partitioning"] = {
                "enabled": True,
                "partition_by": "date",
                "partition_size": "daily"
            }
        
        # Add compression for large files
        if schema.get("column_count", 0) > 10:
            recommendations.append("Enable compression for files with many columns")
            if "optimization" not in optimized:
                optimized["optimization"] = {}
            optimized["optimization"]["compression"] = {
                "enabled": True,
                "format": "gzip"
            }
        
        # Add indexing recommendations
        date_columns = [col for col in schema.get("columns", []) 
                       if "date" in col.get("name", "").lower()]
        if date_columns:
            recommendations.append(f"Create indexes on date columns: {[c['name'] for c in date_columns]}")
            if "optimization" not in optimized:
                optimized["optimization"] = {}
            optimized["optimization"]["indexes"] = [col["name"] for col in date_columns]
        
        optimized["optimization_recommendations"] = recommendations
        
        self.log_action("optimize_config", {"recommendations_count": len(recommendations)})
        return optimized


class OrchestratorAgent(BaseAgent):
    """Master agent that coordinates all other agents"""
    
    def __init__(self):
        super().__init__(
            name="Orchestrator",
            role="Coordinates all agents and manages the configuration generation workflow"
        )
        self.schema_analyzer = SchemaAnalyzerAgent()
        self.config_generator = ConfigGeneratorAgent()
        self.validator = ValidationAgent()
        self.optimizer = OptimizationAgent()
    
    def generate_complete_config(self, file_path: str, file_type: str, 
                                feed_name: str, source_system: str) -> Dict[str, Any]:
        """Orchestrate the complete configuration generation process"""
        
        result = {
            "status": "processing",
            "steps": []
        }
        
        # Step 1: Analyze schema
        self.log_action("step_1_start", "Analyzing file schema")
        schema = self.schema_analyzer.analyze_file(file_path, file_type)
        result["steps"].append({
            "step": 1,
            "name": "Schema Analysis",
            "status": "completed" if "error" not in schema else "failed",
            "output": schema
        })
        
        if "error" in schema:
            result["status"] = "failed"
            return result
        
        # Step 2: Generate configuration
        self.log_action("step_2_start", "Generating configuration with LLM")
        config = self.config_generator.generate_config(schema, feed_name, source_system)
        result["steps"].append({
            "step": 2,
            "name": "Config Generation",
            "status": "completed",
            "output": config
        })
        
        # Step 3: Validate configuration
        self.log_action("step_3_start", "Validating configuration")
        validation = self.validator.validate_config(config)
        result["steps"].append({
            "step": 3,
            "name": "Validation",
            "status": "completed",
            "output": validation
        })
        
        # Step 4: Optimize configuration
        self.log_action("step_4_start", "Optimizing configuration")
        optimized_config = self.optimizer.optimize_config(config, schema)
        result["steps"].append({
            "step": 4,
            "name": "Optimization",
            "status": "completed",
            "output": optimized_config
        })
        
        # Final result
        result["status"] = "completed"
        result["final_config"] = optimized_config
        result["validation_score"] = validation.get("score", 0)
        result["agent_memories"] = {
            "schema_analyzer": self.schema_analyzer.get_memory(),
            "config_generator": self.config_generator.get_memory(),
            "validator": self.validator.get_memory(),
            "optimizer": self.optimizer.get_memory()
        }
        
        self.log_action("generation_complete", {"feed_name": feed_name, "score": validation.get("score")})
        
        return result
    
    def orchestrate_config_generation(self, file_path: str, feed_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrate config generation with feed details (v2 interface)
        
        Args:
            file_path: Path to the source data file
            feed_details: Dictionary containing feed metadata
        
        Returns:
            Configuration generation result with schema
        """
        # Extract file type from file path
        file_type = file_path.split('.')[-1] if '.' in file_path else 'csv'
        
        # Extract key details
        feed_name = feed_details.get("feed_name", "unknown_feed")
        source_system = feed_details.get("source_system", "unknown_system")
        
        # Use the existing complete config generation
        result = self.generate_complete_config(file_path, file_type, feed_name, source_system)
        
        # Transform result to match v2 expected format
        validation_data = result["steps"][2]["output"] if len(result["steps"]) > 2 else {}
        validation_score = validation_data.get("score", 85) if validation_data else 85  # Default score
        
        return {
            "config": result.get("final_config", {}),
            "schema": result["steps"][0]["output"] if result["steps"] else {},
            "validation": validation_data,
            "status": result.get("status", "unknown"),
            "all_steps": result.get("steps", []),
            "validation_score": validation_score,
            "steps_completed": len(result.get("steps", []))
        }
    
    def get_all_agent_logs(self) -> Dict[str, List[Dict]]:
        """Get logs from all agents"""
        return {
            "orchestrator": self.get_memory(),
            "schema_analyzer": self.schema_analyzer.get_memory(),
            "config_generator": self.config_generator.get_memory(),
            "validator": self.validator.get_memory(),
            "optimizer": self.optimizer.get_memory()
        }


# Convenience function for external use
def generate_hermes_config(file_path: str, file_type: str, 
                          feed_name: str, source_system: str) -> Dict[str, Any]:
    """
    Main entry point for generating Hermes configurations
    
    Args:
        file_path: Path to the source data file
        file_type: Type of file (csv, json, etc.)
        feed_name: Name of the data feed
        source_system: Source system name
    
    Returns:
        Complete configuration generation result
    """
    orchestrator = OrchestratorAgent()
    return orchestrator.generate_complete_config(file_path, file_type, feed_name, source_system)
