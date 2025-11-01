# Hermes Framework: Source, Target & Control Tables Explained
## A Layman's Guide

**Author**: Manus AI  
**Date**: 2025-10-31  
**Purpose**: Simple explanations for non-technical readers

---

## The Restaurant Kitchen Analogy 🍳

Think of the Hermes framework like a **restaurant kitchen** that processes food orders:

---

## 1. SOURCE (The Ingredients Coming In) 📦

### What is a Source?

**Simple Definition**: A **source** is where your raw data comes from—like ingredients arriving at a restaurant.

### In the Hermes Framework:

**Sources are the INPUT files or data feeds** that arrive from various systems, in different formats.

### Real-World Examples:

| Source Type | What It Is | Restaurant Analogy |
|-------------|------------|-------------------|
| **CSV File** | Trade data from trading system | Box of vegetables from supplier |
| **JSON Feed** | Market prices from Bloomberg | Fresh fish delivery |
| **XML File** | Customer data from CRM | Meat order from butcher |
| **Database Table** | Historical records from legacy system | Ingredients from storage room |
| **API Stream** | Real-time stock prices | Fresh herbs from garden |

### Key Characteristics:

✅ **You don't control the format** - Sources come "as-is" from external systems  
✅ **Different formats** - CSV, JSON, XML, Excel, databases, APIs  
✅ **Different schedules** - Some daily, some hourly, some real-time  
✅ **Different quality** - Some clean, some messy  
✅ **Different structures** - Each source has its own column names and data types

### Example:
```
Source File: trades_2025_10_31.csv
From: Trading System
Format: CSV with 50 columns
Contains: Today's stock trades (10,000 rows)
Arrives: Every day at 6 PM
```

---

## 2. TARGET (Where the Processed Data Goes) 🎯

### What is a Target?

**Simple Definition**: A **target** is where your cleaned, transformed, and organized data ends up—like plated dishes going to customers.

### In the Hermes Framework:

**Targets are the OUTPUT destinations** where processed data is delivered after going through the ETL pipeline.

### Real-World Examples:

| Target Type | What It Is | Restaurant Analogy |
|-------------|------------|-------------------|
| **Data Warehouse Table** | Redshift table for analytics | Plated dish for dine-in customer |
| **Output File** | CSV file for downstream system | Takeout order in container |
| **API Endpoint** | REST API for other applications | Food delivery to customer's home |
| **Dashboard** | Tableau/PowerBI visualization | Display case showing desserts |
| **Database** | MongoDB collection for applications | Buffet table for self-service |

### Key Characteristics:

✅ **You DO control the format** - Targets follow your standardized structure  
✅ **Standardized** - All targets use consistent column names and data types  
✅ **Clean and validated** - Only quality data reaches targets  
✅ **Business-ready** - Organized for easy consumption  
✅ **Multiple targets** - One source can feed many targets

### Example:
```
Target Table: gold.trades_summary
Location: AWS Redshift Data Warehouse
Format: Standardized schema (15 columns)
Contains: Cleaned and aggregated trade data
Used by: Finance team dashboards, Risk reports, Compliance audits
```

---

## 3. The Journey: Source → Processing → Target

### The Complete Flow:

```
┌─────────────────┐
│   SOURCE        │  Raw ingredients arrive
│  (Raw Data)     │  - trades_2025_10_31.csv
│                 │  - Messy, inconsistent
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   BRONZE LAYER  │  Store exactly as received
│  (Raw Storage)  │  - Historical record
│                 │  - No changes made
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   SILVER LAYER  │  Clean and standardize
│  (Cleaned Data) │  - Remove duplicates
│                 │  - Fix data types
│                 │  - Validate quality
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   GOLD LAYER    │  Business-ready data
│  (Enriched)     │  - Aggregated
│                 │  - Calculated fields
│                 │  - Joined with other data
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   TARGET        │  Delivered to consumers
│  (Final Output) │  - Dashboard
│                 │  - Reports
│                 │  - Other systems
└─────────────────┘
```

### Restaurant Analogy:

1. **SOURCE**: Raw ingredients arrive (vegetables, meat, spices)
2. **BRONZE**: Store in refrigerator exactly as received
3. **SILVER**: Wash, peel, chop, measure ingredients
4. **GOLD**: Cook, season, plate beautifully
5. **TARGET**: Serve to customer's table

---

## 4. CONTROL TABLES (The Recipe Books & Instructions) 📚

### What are Control Tables?

**Simple Definition**: **Control tables** are like recipe books and instruction manuals that tell the Hermes framework HOW to process data from sources to targets.

### Why Do We Need Them?

Instead of writing custom code for every data feed, Hermes uses **configuration files** (stored in control tables) that describe:
- Where data comes from (source)
- How to process it (transformations)
- Where to send it (target)

### Restaurant Analogy:

| Control Table | What It Contains | Restaurant Equivalent |
|---------------|------------------|----------------------|
| **Process Config** | Which feeds to process, when to run | Daily menu & cooking schedule |
| **Feed File Config** | File format, column definitions | Recipe card (ingredients list) |
| **ETL Steps** | Transformation logic, business rules | Cooking instructions (step-by-step) |
| **Date Control** | Business dates, holidays | Restaurant calendar (open/closed days) |
| **File Pattern** | Output file naming, format | Plating instructions (how to serve) |
| **Transfer Config** | Where to send output files | Delivery addresses |

---

## 5. Control Tables in Detail

### Control Table #1: Process Config

**What it does**: Defines each data processing job

**Example Entry:**
```json
{
  "process_id": "TRADE_DAILY",
  "process_name": "Daily Trade Processing",
  "source_system": "Trading Platform",
  "schedule": "Daily at 6 PM",
  "enabled": true
}
```

**Layman Translation:**
> "There's a job called 'Daily Trade Processing' that runs every day at 6 PM. It's currently turned on."

---

### Control Table #2: Feed File Config

**What it does**: Describes the structure of incoming files

**Example Entry:**
```json
{
  "feed_id": "TRADE_CSV",
  "file_format": "CSV",
  "delimiter": ",",
  "columns": [
    {"name": "trade_id", "type": "string"},
    {"name": "amount", "type": "decimal"},
    {"name": "trade_date", "type": "date"}
  ]
}
```

**Layman Translation:**
> "The trade file is a CSV with commas separating values. It has three columns: trade_id (text), amount (number with decimals), and trade_date (date)."

---

### Control Table #3: ETL Steps

**What it does**: Defines the transformation logic

**Example Entry:**
```json
{
  "step_id": 1,
  "step_name": "Remove Duplicates",
  "step_type": "deduplication",
  "logic": "Remove rows with duplicate trade_id"
},
{
  "step_id": 2,
  "step_name": "Calculate Total",
  "step_type": "calculation",
  "logic": "total_amount = quantity * price"
}
```

**Layman Translation:**
> "Step 1: Remove any duplicate trades. Step 2: Calculate the total amount by multiplying quantity times price."

---

### Control Table #4: Date Control

**What it does**: Manages business dates and scheduling

**Example Entry:**
```json
{
  "business_date": "2025-10-31",
  "is_holiday": false,
  "process_date": "2025-10-31",
  "next_run_date": "2025-11-01"
}
```

**Layman Translation:**
> "Today is October 31, 2025. It's not a holiday, so we'll process data. Tomorrow we'll run again on November 1st."

---

### Control Table #5: File Pattern

**What it does**: Defines output file naming and format

**Example Entry:**
```json
{
  "output_pattern": "trades_{business_date}.csv",
  "output_format": "CSV",
  "output_location": "s3://bucket/output/"
}
```

**Layman Translation:**
> "Create an output file named 'trades_2025_10_31.csv' and save it to the S3 bucket in the output folder."

---

## 6. Why This Approach is Powerful 💪

### Traditional Approach (Without Control Tables):

```
❌ Write custom Python code for each feed
❌ Hard-coded logic (difficult to change)
❌ Takes 4-8 weeks to onboard new feed
❌ Requires developer for every change
❌ Code breaks when source format changes
```

### Hermes Approach (With Control Tables):

```
✅ Just fill in configuration (no coding)
✅ Change config, not code (easy updates)
✅ Takes 2-4 weeks to onboard new feed
✅ Business analysts can make changes
✅ Framework adapts automatically
```

---

## 7. Real-World Example: Trade Processing

### Scenario:
Your company receives daily trade files from the trading system and needs to create reports for the finance team.

### The Players:

**SOURCE**: 
- File: `trades_2025_10_31.csv`
- From: Trading System
- Format: CSV with 50 columns
- Contains: 10,000 trades
- Arrives: Daily at 6 PM

**CONTROL TABLES**:
- **Process Config**: "Run trade processing daily at 6:30 PM"
- **Feed File Config**: "CSV file, comma-separated, 50 columns defined"
- **ETL Steps**: 
  1. Remove duplicates
  2. Validate trade amounts
  3. Calculate totals
  4. Aggregate by trader
- **Date Control**: "Today is 2025-10-31, not a holiday, process normally"
- **File Pattern**: "Output as trades_summary_2025_10_31.csv"

**TARGET**:
- Table: `gold.trades_summary` in Redshift
- File: `trades_summary_2025_10_31.csv` sent to finance team
- Dashboard: Updated PowerBI report

### The Process:

1. **6:00 PM**: Source file arrives → Saved to Bronze layer (raw)
2. **6:30 PM**: Hermes reads Process Config → "Time to process trades!"
3. **6:31 PM**: Reads Feed File Config → "This is a CSV with 50 columns"
4. **6:32 PM**: Executes ETL Steps → Clean, validate, transform
5. **6:35 PM**: Reads File Pattern → "Create output file with this name"
6. **6:36 PM**: Writes to Target → Redshift table + output file
7. **6:37 PM**: Updates Date Control → "Done! Next run tomorrow"

---

## 8. Summary Table

| Concept | Simple Definition | Restaurant Analogy | Technical Term |
|---------|-------------------|-------------------|----------------|
| **SOURCE** | Where raw data comes from | Ingredients arriving | Input data feed |
| **TARGET** | Where processed data goes | Plated dish to customer | Output destination |
| **BRONZE** | Raw data storage | Refrigerator storage | Raw data lake |
| **SILVER** | Cleaned data | Prepped ingredients | Cleansed data |
| **GOLD** | Business-ready data | Cooked dish | Curated data |
| **CONTROL TABLES** | Configuration & instructions | Recipe books | Metadata repository |

---

## 9. Key Takeaways 🎯

**SOURCE**:
- ✅ You receive it (don't control format)
- ✅ Can be files, databases, APIs, streams
- ✅ Often messy and inconsistent

**TARGET**:
- ✅ You create it (control format)
- ✅ Standardized and clean
- ✅ Ready for business use

**CONTROL TABLES**:
- ✅ Configuration, not code
- ✅ Tell Hermes HOW to process
- ✅ Easy to change without programming

**The Magic**:
> Instead of writing code for every data feed, you just fill in configuration in control tables. Hermes does the rest automatically!

---

## 10. Why This Matters for Your MVP

When building the **Automated Config Generator** (Low-Hanging Fruit #2), you're creating a tool that:

1. **Analyzes the SOURCE** (incoming file)
2. **Generates CONTROL TABLE entries** (configuration)
3. **Defines the TARGET** (output structure)

**Without the tool**: Developer spends 4-8 hours writing JSON configs manually

**With the tool**: Upload source file → AI generates configs → 5 minutes done!

---

**Hope this makes it crystal clear! Think of it as a restaurant kitchen: ingredients come in (source), recipes guide the cooking (control tables), and finished dishes go out (target).** 🍽️

---

**Document End**
