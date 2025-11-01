# Hermes Config Generator - Agent System Explained

## 🤖 Multi-Agent Architecture Overview

The Hermes Config Generator uses a **sophisticated multi-agent AI system** where five specialized agents work together to generate perfect configurations. Each agent has a specific role, capabilities, and uses intelligent prompts to accomplish its tasks.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  ORCHESTRATOR AGENT                     │
│         (Coordinates all other agents)                  │
└───────────┬─────────────────────────────────────────────┘
            │
            ├──► 1. Schema Analyzer Agent
            │    └─► Analyzes file structure
            │
            ├──► 2. Config Generator Agent (LLM)
            │    └─► Generates JSON using GPT-4
            │
            ├──► 3. Validation Agent
            │    └─► Validates configuration
            │
            └──► 4. Optimization Agent
                 └─► Optimizes for performance
```

---

## 🔍 Agent 1: Schema Analyzer Agent

### Role
**"Analyzes source files and infers schema, data types, and structure"**

### Capabilities
- Reads CSV and JSON files
- Extracts column names and data types
- Identifies null values and unique counts
- Samples data for analysis
- Detects data patterns

### How It Works

**Input**: File path and file type

**Process**:
1. Reads first 100 rows of the file (sample)
2. Uses Pandas to analyze structure
3. For each column, extracts:
   - Column name
   - Data type (string, int, float, date, etc.)
   - Null count (missing values)
   - Unique count (distinct values)
   - Sample values (first 3 rows)

**Output**: Schema dictionary with complete structure

### Example Output
```json
{
  "file_type": "csv",
  "row_count_sample": 20,
  "column_count": 5,
  "columns": [
    {
      "name": "trade_id",
      "dtype": "object",
      "null_count": 0,
      "unique_count": 20,
      "sample_values": ["T001", "T002", "T003"]
    },
    {
      "name": "symbol",
      "dtype": "object",
      "null_count": 0,
      "unique_count": 5,
      "sample_values": ["AAPL", "GOOGL", "MSFT"]
    },
    {
      "name": "quantity",
      "dtype": "int64",
      "null_count": 0,
      "unique_count": 15,
      "sample_values": [100, 250, 50]
    }
  ]
}
```

### Code Location
Lines 37-83 in `agents.py`

### No LLM Prompt
This agent uses **pure data analysis** with Pandas - no AI model needed!

---

## 🤖 Agent 2: Config Generator Agent (LLM-Powered)

### Role
**"Generates Hermes framework JSON configurations using AI"**

### Capabilities
- Uses OpenAI GPT-4.1-mini model
- Understands Hermes framework structure
- Generates complete, valid JSON configurations
- Applies best practices automatically
- Falls back to basic config if LLM fails

### How It Works

**Input**: Schema (from Agent 1), feed name, source system

**Process**:
1. Constructs detailed prompt for GPT-4
2. Sends schema and requirements to LLM
3. Receives generated JSON configuration
4. Parses and validates JSON
5. Returns complete configuration

**Output**: Complete Hermes JSON configuration

---

### 🎯 THE ACTUAL LLM PROMPT (Lines 99-112)

```python
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
```

### System Prompt (Line 119)
```python
"You are a Hermes framework configuration expert. Generate only valid JSON."
```

---

### LLM Configuration

**Model**: `gpt-4.1-mini` (OpenAI)  
**Temperature**: `0.3` (low randomness for consistency)  
**Max Tokens**: `2000` (enough for complete config)  
**Role**: System + User messages

### Example LLM Call
```python
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "system", 
            "content": "You are a Hermes framework configuration expert. Generate only valid JSON."
        },
        {
            "role": "user", 
            "content": prompt  # The detailed prompt above
        }
    ],
    temperature=0.3,
    max_tokens=2000
)
```

---

### Example Generated Configuration

**Input**:
- Feed Name: "Daily Trade Feed"
- Source System: "Trading Platform"
- Schema: 5 columns (trade_id, symbol, quantity, price, trade_date)

**Output** (Generated by GPT-4):
```json
{
  "process_config": {
    "process_id": "DAILY_TRADE_FEED",
    "process_name": "Daily Trade Feed",
    "source_system": "Trading Platform",
    "schedule": "Daily at 6 PM",
    "enabled": true,
    "retry_count": 3,
    "timeout_minutes": 30
  },
  "feed_file_config": {
    "feed_id": "TRADE_CSV",
    "file_format": "CSV",
    "delimiter": ",",
    "header_row": true,
    "encoding": "utf-8",
    "columns": [
      {
        "name": "trade_id",
        "type": "string",
        "nullable": false,
        "primary_key": true
      },
      {
        "name": "symbol",
        "type": "string",
        "nullable": false
      },
      {
        "name": "quantity",
        "type": "integer",
        "nullable": false
      },
      {
        "name": "price",
        "type": "decimal",
        "nullable": false
      },
      {
        "name": "trade_date",
        "type": "date",
        "nullable": false
      }
    ]
  },
  "etl_steps": [
    {
      "step_id": 1,
      "step_name": "Remove Duplicates",
      "step_type": "deduplication",
      "key_columns": ["trade_id"]
    },
    {
      "step_id": 2,
      "step_name": "Validate Amounts",
      "step_type": "validation",
      "rule": "price > 0 AND quantity > 0"
    },
    {
      "step_id": 3,
      "step_name": "Calculate Total",
      "step_type": "calculation",
      "formula": "total_amount = quantity * price"
    }
  ],
  "date_control": {
    "business_date_column": "trade_date",
    "date_format": "%Y-%m-%d",
    "timezone": "UTC"
  },
  "file_pattern": {
    "output_pattern": "trades_{business_date}.csv",
    "output_format": "CSV",
    "output_location": "s3://bucket/output/trades/"
  }
}
```

### Fallback Mechanism

If LLM fails (API error, timeout, invalid JSON), the agent generates a **basic fallback configuration** without AI (lines 148-169).

### Code Location
Lines 85-169 in `agents.py`

---

## ✅ Agent 3: Validation Agent

### Role
**"Validates generated configurations for completeness and correctness"**

### Capabilities
- Checks for required sections
- Validates field presence
- Scores configuration (0-100)
- Generates errors and warnings
- Ensures deployment readiness

### How It Works

**Input**: Generated configuration (from Agent 2)

**Process**:
1. Check for required sections (process_config, feed_file_config, etl_steps)
2. Validate each section has required fields
3. Check for columns definition
4. Verify ETL steps exist
5. Calculate validation score

**Output**: Validation result with score, errors, and warnings

---

### Validation Rules

| Check | Penalty | Type |
|-------|---------|------|
| Missing required section | -30 points | Error |
| Missing process_config field | -10 points | Warning |
| No columns defined | -15 points | Warning |
| No ETL steps | -10 points | Warning |

**Perfect Score**: 100 (no errors or warnings)  
**Minimum Score**: 0 (multiple critical errors)

---

### Example Validation Output

**Perfect Configuration**:
```json
{
  "valid": true,
  "errors": [],
  "warnings": [],
  "score": 100
}
```

**Configuration with Issues**:
```json
{
  "valid": true,
  "errors": [],
  "warnings": [
    "Missing field in process_config: schedule",
    "No ETL steps defined"
  ],
  "score": 80
}
```

**Invalid Configuration**:
```json
{
  "valid": false,
  "errors": [
    "Missing required section: feed_file_config"
  ],
  "warnings": [],
  "score": 70
}
```

### Code Location
Lines 172-221 in `agents.py`

### No LLM Prompt
This agent uses **rule-based validation** - no AI model needed!

---

## ⚡ Agent 4: Optimization Agent

### Role
**"Optimizes configurations for performance and best practices"**

### Capabilities
- Analyzes data characteristics
- Suggests partitioning strategies
- Recommends compression
- Identifies indexing opportunities
- Adds optimization metadata

### How It Works

**Input**: Configuration (from Agent 2) + Schema (from Agent 1)

**Process**:
1. Analyze dataset size (row count)
2. Check column count
3. Identify date columns
4. Generate optimization recommendations
5. Add optimization section to config

**Output**: Optimized configuration with recommendations

---

### Optimization Rules

| Condition | Recommendation | Action |
|-----------|----------------|--------|
| Row count > 50 | Add partitioning | Partition by date, daily |
| Column count > 10 | Enable compression | Use gzip compression |
| Date columns exist | Create indexes | Index date columns |

---

### Example Optimization Output

**Input**: Large dataset (100 rows, 15 columns, has date columns)

**Added to Configuration**:
```json
{
  "optimization": {
    "partitioning": {
      "enabled": true,
      "partition_by": "date",
      "partition_size": "daily"
    },
    "compression": {
      "enabled": true,
      "format": "gzip"
    },
    "indexes": ["trade_date", "created_date"]
  },
  "optimization_recommendations": [
    "Consider adding partitioning strategy for large dataset",
    "Enable compression for files with many columns",
    "Create indexes on date columns: ['trade_date', 'created_date']"
  ]
}
```

### Code Location
Lines 224-271 in `agents.py`

### No LLM Prompt
This agent uses **heuristic analysis** - no AI model needed!

---

## 🎯 Agent 5: Orchestrator Agent

### Role
**"Coordinates all agents and manages the configuration generation workflow"**

### Capabilities
- Manages agent lifecycle
- Coordinates workflow steps
- Aggregates results
- Maintains transparency
- Handles errors gracefully

### How It Works

**Input**: File path, file type, feed name, source system

**Process**:
1. **Step 1**: Call Schema Analyzer Agent → Get schema
2. **Step 2**: Call Config Generator Agent → Generate config
3. **Step 3**: Call Validation Agent → Validate config
4. **Step 4**: Call Optimization Agent → Optimize config
5. Aggregate all results and agent memories

**Output**: Complete result with all steps, final config, and agent logs

---

### Workflow Steps

```
Step 1: Schema Analysis
├─► Schema Analyzer Agent
└─► Output: File schema

Step 2: Config Generation
├─► Config Generator Agent (GPT-4)
└─► Output: JSON configuration

Step 3: Validation
├─► Validation Agent
└─► Output: Validation score (0-100)

Step 4: Optimization
├─► Optimization Agent
└─► Output: Optimized configuration
```

---

### Complete Output Structure

```json
{
  "status": "completed",
  "steps": [
    {
      "step": 1,
      "name": "Schema Analysis",
      "status": "completed",
      "output": { /* schema */ }
    },
    {
      "step": 2,
      "name": "Config Generation",
      "status": "completed",
      "output": { /* config */ }
    },
    {
      "step": 3,
      "name": "Validation",
      "status": "completed",
      "output": { /* validation result */ }
    },
    {
      "step": 4,
      "name": "Optimization",
      "status": "completed",
      "output": { /* optimized config */ }
    }
  ],
  "final_config": { /* complete optimized configuration */ },
  "validation_score": 98,
  "agent_memories": {
    "schema_analyzer": [ /* action logs */ ],
    "config_generator": [ /* action logs */ ],
    "validator": [ /* action logs */ ],
    "optimizer": [ /* action logs */ ]
  }
}
```

### Code Location
Lines 274-353 in `agents.py`

### No LLM Prompt
This agent uses **workflow orchestration** - no AI model needed!

---

## 🧠 Agent Memory System

Every agent has a **memory system** that logs all actions for transparency and debugging.

### Memory Structure

```python
{
  "timestamp": "2025-10-31T12:34:56.789",
  "action": "analyze_file",
  "result": { /* action result */ }
}
```

### Example Agent Memory

```json
[
  {
    "timestamp": "2025-10-31T12:34:56.123",
    "action": "analyze_file",
    "result": {
      "file_type": "csv",
      "column_count": 5
    }
  },
  {
    "timestamp": "2025-10-31T12:34:57.456",
    "action": "generate_config",
    "result": {
      "success": true,
      "feed_name": "Daily Trade Feed"
    }
  }
]
```

---

## 📊 Agent Comparison Table

| Agent | Uses LLM? | Input | Output | Purpose |
|-------|-----------|-------|--------|---------|
| **Schema Analyzer** | ❌ No | File path | Schema | Analyze data structure |
| **Config Generator** | ✅ Yes (GPT-4) | Schema | JSON config | Generate configuration |
| **Validation** | ❌ No | Config | Score + errors | Validate correctness |
| **Optimization** | ❌ No | Config + schema | Optimized config | Improve performance |
| **Orchestrator** | ❌ No | All inputs | Complete result | Coordinate workflow |

---

## 🔑 Key Design Principles

### 1. **Separation of Concerns**
Each agent has ONE specific responsibility

### 2. **Transparency**
All agent actions are logged in memory

### 3. **Fail-Safe**
Fallback mechanisms if LLM fails

### 4. **Composability**
Agents can be used independently or together

### 5. **Extensibility**
Easy to add new agents without changing existing ones

---

## 💡 Why This Architecture?

### Traditional Approach (Single LLM Call)
```
User Input → LLM → Output
```
**Problems**:
- Black box (no visibility)
- Hard to debug
- All-or-nothing (no partial results)
- Can't optimize individual steps

### Multi-Agent Approach (Our System)
```
User Input → Agent 1 → Agent 2 → Agent 3 → Agent 4 → Output
              ↓         ↓         ↓         ↓
           Memory    Memory    Memory    Memory
```
**Benefits**:
- ✅ Full transparency (see each step)
- ✅ Easy debugging (check agent memories)
- ✅ Partial results (even if one agent fails)
- ✅ Optimized (each agent does one thing well)
- ✅ Testable (test each agent independently)

---

## 🎯 Real-World Example: Complete Flow

### Input
- File: `trades.csv`
- Feed Name: "Daily Trade Feed"
- Source System: "Trading Platform"

### Agent 1: Schema Analyzer
**Action**: Reads CSV, analyzes structure  
**Output**: 
```json
{
  "file_type": "csv",
  "column_count": 5,
  "columns": [
    {"name": "trade_id", "dtype": "object"},
    {"name": "symbol", "dtype": "object"},
    {"name": "quantity", "dtype": "int64"},
    {"name": "price", "dtype": "float64"},
    {"name": "trade_date", "dtype": "object"}
  ]
}
```

### Agent 2: Config Generator (GPT-4)
**Action**: Sends schema to GPT-4 with prompt  
**Prompt**: "Generate Hermes config for Daily Trade Feed..."  
**Output**: Complete JSON configuration (see example above)

### Agent 3: Validator
**Action**: Validates generated config  
**Checks**: Required sections, fields, structure  
**Output**: 
```json
{
  "valid": true,
  "score": 100,
  "errors": [],
  "warnings": []
}
```

### Agent 4: Optimizer
**Action**: Analyzes data characteristics  
**Recommendations**: Partitioning, compression, indexing  
**Output**: Optimized config with recommendations

### Agent 5: Orchestrator
**Action**: Coordinates all agents, aggregates results  
**Output**: Complete result with all steps and final config

---

## 🔧 Technical Implementation Details

### Base Agent Class (Lines 16-34)

All agents inherit from `BaseAgent`:
- `name`: Agent identifier
- `role`: Agent description
- `memory`: Action log
- `log_action()`: Records actions
- `get_memory()`: Retrieves logs

### OpenAI Client Initialization (Line 14)
```python
client = OpenAI()  # Uses OPENAI_API_KEY from environment
```

### Main Entry Point (Lines 357-372)
```python
def generate_hermes_config(file_path, file_type, feed_name, source_system):
    orchestrator = OrchestratorAgent()
    return orchestrator.generate_complete_config(...)
```

---

## 📚 Summary

### Agents Overview

1. **Schema Analyzer** - Analyzes data structure (no LLM)
2. **Config Generator** - Generates JSON using GPT-4 (LLM)
3. **Validator** - Validates configuration (no LLM)
4. **Optimizer** - Optimizes for performance (no LLM)
5. **Orchestrator** - Coordinates everything (no LLM)

### Only ONE Agent Uses LLM
**Config Generator Agent** uses OpenAI GPT-4.1-mini with:
- Detailed prompt about Hermes framework
- Schema and requirements
- Temperature 0.3 for consistency
- Max 2000 tokens for complete config

### All Other Agents
Use **deterministic algorithms**:
- Pandas for data analysis
- Rule-based validation
- Heuristic optimization
- Workflow orchestration

---

## 🎓 Learning Resources

### To Understand This System
1. **Multi-Agent Systems**: How agents collaborate
2. **LLM Prompting**: Crafting effective prompts
3. **Data Analysis**: Pandas schema inference
4. **Validation**: Rule-based checking
5. **Optimization**: Performance heuristics

### To Extend This System
- Add new agents (e.g., SecurityAgent, CostAgent)
- Enhance prompts for better LLM output
- Add more validation rules
- Implement advanced optimization strategies
- Create agent communication protocols

---

**This multi-agent architecture makes the Hermes Config Generator intelligent, transparent, and reliable!** 🤖✨
