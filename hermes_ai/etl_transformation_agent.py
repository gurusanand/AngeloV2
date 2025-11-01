"""
ETL Transformation Agent
Converts natural language transformation descriptions into executable ETL JSON
"""

import json
from typing import Dict, List, Any
from datetime import datetime
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()


class ETLTransformationAgent:
    """Agent responsible for generating ETL transformation specifications from natural language"""
    
    def __init__(self):
        self.name = "ETL Transformation Agent"
        self.role = "Converts natural language ETL requirements into executable JSON specifications"
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
    
    def generate_etl_transformation(self, 
                                   source_schema: Dict[str, Any],
                                   target_table: str,
                                   transformation_description: str) -> Dict[str, Any]:
        """
        Generate ETL transformation JSON from natural language description
        
        Args:
            source_schema: Schema of the source data (from Schema Analyzer)
            target_table: Name of the destination table
            transformation_description: Natural language description of transformations
        
        Returns:
            Complete ETL transformation JSON with mappings and SQL logic
        """
        
        # Prepare detailed prompt for LLM
        prompt = f"""You are an expert ETL developer. Generate a comprehensive ETL transformation specification in JSON format.

SOURCE SCHEMA:
{json.dumps(source_schema, indent=2)}

TARGET TABLE: {target_table}

USER'S TRANSFORMATION REQUIREMENTS:
{transformation_description}

Generate a complete ETL transformation JSON that includes:

1. **column_mappings**: Array of source-to-target column mappings with:
   - source_column: Name of source column
   - target_column: Name of target column (can be renamed)
   - data_type: Target data type (STRING, INTEGER, DECIMAL, DATE, TIMESTAMP, BOOLEAN)
   - transformation_type: Type of transformation (DIRECT, CAST, CONCAT, SUBSTRING, CASE_WHEN, CALCULATION, LOOKUP, CUSTOM)
   - transformation_logic: SQL expression or logic for the transformation
   - is_nullable: Whether the target column can be null
   - default_value: Default value if source is null
   - description: Brief description of the transformation

2. **derived_columns**: Array of new columns created from calculations:
   - column_name: Name of the new column
   - data_type: Data type
   - calculation_logic: SQL expression to calculate the value
   - description: What this column represents

3. **filter_conditions**: Array of filter conditions to apply:
   - condition_name: Name of the filter
   - sql_where_clause: SQL WHERE clause condition
   - description: What records this filter includes/excludes

4. **aggregations**: Array of aggregation operations (if needed):
   - group_by_columns: Columns to group by
   - aggregate_functions: Array of aggregation functions (SUM, COUNT, AVG, MIN, MAX)
   - having_conditions: Optional HAVING clause conditions

5. **data_quality_rules**: Array of data quality validations:
   - rule_name: Name of the rule
   - rule_type: Type (NOT_NULL, UNIQUE, RANGE, PATTERN, CUSTOM)
   - column_name: Column to validate
   - validation_logic: SQL expression for validation
   - action_on_failure: What to do if validation fails (REJECT, FLAG, DEFAULT)

6. **join_specifications**: Array of joins with other tables (if mentioned):
   - join_type: Type of join (INNER, LEFT, RIGHT, FULL)
   - source_table: Source table name
   - target_table: Table to join with
   - join_condition: ON clause condition
   - columns_to_select: Columns to select from joined table

7. **pre_processing_steps**: Array of steps to execute before main transformation:
   - step_order: Order of execution
   - step_type: Type (DEDUPLICATION, CLEANSING, STANDARDIZATION, VALIDATION)
   - step_logic: SQL or description of the step

8. **post_processing_steps**: Array of steps to execute after main transformation:
   - step_order: Order of execution
   - step_type: Type (RECONCILIATION, AUDIT, NOTIFICATION, ARCHIVAL)
   - step_logic: SQL or description of the step

9. **sql_generation_metadata**: Metadata for SQL generation:
   - source_table_name: Name of the source staging table
   - target_table_name: Name of the target table
   - target_schema: Target database schema
   - partition_columns: Columns to partition by (if any)
   - sort_columns: Columns to sort by (if any)
   - incremental_load: Whether this is incremental or full load
   - incremental_key_column: Column to use for incremental load (e.g., last_modified_date)

Return ONLY valid JSON without any markdown formatting or explanations.

IMPORTANT: 
- Be specific and detailed in transformation_logic
- Generate actual SQL expressions that can be executed
- Handle all source columns mentioned in the schema
- If user doesn't specify a transformation for a column, use DIRECT mapping
- Be smart about data type conversions
- Include sensible data quality rules
"""

        try:
            # Call LLM
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert ETL developer. Generate detailed, executable ETL transformation specifications in JSON format. Be specific and include actual SQL logic."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.2,  # Low temperature for consistency
                max_tokens=3000   # Increased for detailed transformations
            )
            
            # Extract and parse JSON
            etl_text = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if etl_text.startswith("```"):
                etl_text = etl_text.split("```")[1]
                if etl_text.startswith("json"):
                    etl_text = etl_text[4:]
            
            etl_json = json.loads(etl_text)
            
            # Add metadata
            etl_json["metadata"] = {
                "generated_at": datetime.now().isoformat(),
                "generated_by": "ETL Transformation Agent",
                "source_columns_count": len(source_schema.get("columns", [])),
                "transformation_description": transformation_description
            }
            
            self.log_action("generate_etl_transformation", {
                "success": True, 
                "target_table": target_table,
                "mappings_count": len(etl_json.get("column_mappings", []))
            })
            
            return etl_json
            
        except Exception as e:
            error_result = {
                "error": str(e),
                "fallback_transformation": self._generate_fallback_transformation(
                    source_schema, target_table
                )
            }
            self.log_action("generate_etl_transformation_error", error_result)
            return error_result["fallback_transformation"]
    
    def _generate_fallback_transformation(self, source_schema: Dict, target_table: str) -> Dict:
        """Generate basic transformation if LLM fails"""
        columns = source_schema.get("columns", [])
        
        return {
            "column_mappings": [
                {
                    "source_column": col["name"],
                    "target_column": col["name"],
                    "data_type": self._infer_target_type(col["dtype"]),
                    "transformation_type": "DIRECT",
                    "transformation_logic": col["name"],
                    "is_nullable": True,
                    "default_value": None,
                    "description": f"Direct mapping of {col['name']}"
                }
                for col in columns
            ],
            "derived_columns": [],
            "filter_conditions": [],
            "aggregations": {},
            "data_quality_rules": [
                {
                    "rule_name": "check_not_null_primary_key",
                    "rule_type": "NOT_NULL",
                    "column_name": columns[0]["name"] if columns else "id",
                    "validation_logic": f"{columns[0]['name']} IS NOT NULL",
                    "action_on_failure": "REJECT"
                }
            ],
            "join_specifications": [],
            "pre_processing_steps": [
                {
                    "step_order": 1,
                    "step_type": "DEDUPLICATION",
                    "step_logic": f"Remove duplicates based on {columns[0]['name']}"
                }
            ],
            "post_processing_steps": [
                {
                    "step_order": 1,
                    "step_type": "RECONCILIATION",
                    "step_logic": "Compare source and target counts"
                }
            ],
            "sql_generation_metadata": {
                "source_table_name": "staging_table",
                "target_table_name": target_table,
                "target_schema": "gold",
                "partition_columns": [],
                "sort_columns": [],
                "incremental_load": False,
                "incremental_key_column": None
            },
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "generated_by": "ETL Transformation Agent (Fallback)",
                "note": "Basic transformation generated due to LLM error"
            }
        }
    
    def _infer_target_type(self, pandas_dtype: str) -> str:
        """Infer target SQL data type from pandas dtype"""
        dtype_lower = pandas_dtype.lower()
        
        if 'int' in dtype_lower:
            return 'INTEGER'
        elif 'float' in dtype_lower or 'double' in dtype_lower:
            return 'DECIMAL'
        elif 'bool' in dtype_lower:
            return 'BOOLEAN'
        elif 'date' in dtype_lower or 'time' in dtype_lower:
            return 'TIMESTAMP'
        else:
            return 'STRING'
    
    def generate_sql_from_transformation(self, etl_json: Dict[str, Any]) -> str:
        """
        Generate executable SQL from ETL transformation JSON
        
        Args:
            etl_json: ETL transformation specification
        
        Returns:
            Executable SQL INSERT statement
        """
        try:
            metadata = etl_json.get("sql_generation_metadata", {})
            source_table = metadata.get("source_table_name", "staging_table")
            target_table = metadata.get("target_table_name", "target_table")
            target_schema = metadata.get("target_schema", "gold")
            
            # Build SELECT clause
            select_clauses = []
            
            # Column mappings
            for mapping in etl_json.get("column_mappings", []):
                logic = mapping.get("transformation_logic", mapping["source_column"])
                target_col = mapping.get("target_column", mapping["source_column"])
                select_clauses.append(f"    {logic} AS {target_col}")
            
            # Derived columns
            for derived in etl_json.get("derived_columns", []):
                col_name = derived["column_name"]
                calc_logic = derived["calculation_logic"]
                select_clauses.append(f"    {calc_logic} AS {col_name}")
            
            # Build WHERE clause
            where_clauses = []
            for filter_cond in etl_json.get("filter_conditions", []):
                where_clauses.append(filter_cond["sql_where_clause"])
            
            # Build JOIN clause
            join_clauses = []
            for join_spec in etl_json.get("join_specifications", []):
                join_type = join_spec["join_type"]
                join_table = join_spec["target_table"]
                join_condition = join_spec["join_condition"]
                join_clauses.append(f"{join_type} JOIN {join_table} ON {join_condition}")
            
            # Construct SQL
            select_clause_str = ',\n'.join(select_clauses)
            sql = f"""-- Generated ETL SQL
-- Target: {target_schema}.{target_table}
-- Generated at: {datetime.now().isoformat()}

INSERT INTO {target_schema}.{target_table}
SELECT
{select_clause_str}
FROM {source_table}"""
            
            # Add JOINs
            if join_clauses:
                sql += "\n" + "\n".join(join_clauses)
            
            # Add WHERE
            if where_clauses:
                where_clause_str = "\n    AND ".join(where_clauses)
                sql += f"\nWHERE\n    {where_clause_str}"
            
            sql += ";"
            
            self.log_action("generate_sql", {"success": True, "target_table": target_table})
            return sql
            
        except Exception as e:
            error_sql = f"-- Error generating SQL: {str(e)}\n-- Please review the ETL transformation JSON"
            self.log_action("generate_sql_error", {"error": str(e)})
            return error_sql


# Convenience function
def generate_etl_transformation_json(source_schema: Dict[str, Any],
                                    target_table: str,
                                    transformation_description: str) -> Dict[str, Any]:
    """
    Main entry point for generating ETL transformations
    
    Args:
        source_schema: Schema from Schema Analyzer Agent
        target_table: Name of destination table
        transformation_description: Natural language transformation requirements
    
    Returns:
        Complete ETL transformation JSON
    """
    agent = ETLTransformationAgent()
    return agent.generate_etl_transformation(source_schema, target_table, transformation_description)
