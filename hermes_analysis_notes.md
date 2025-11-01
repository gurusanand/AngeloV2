# Hermes Framework Analysis - Working Notes

## Document Sources Analyzed
1. ExecutiveSummary.docx
2. Hermes.docx
3. Multiple presentation slides (WhatsApp images)
4. Architecture diagrams (PNG files)

## Key Findings from Documents

### Project Overview
- **Project Name**: Hermes Framework
- **Type**: Strategic framework build (not a migration)
- **Purpose**: Unified, metadata-driven ETL framework for data ingestion, transformation, and delivery

### Core Objectives
1. Standardize data ingestion, transformation, and settlement across multiple systems
2. Replace redundant feeds and legacy systems with unified, configurable framework
3. Enable automation, transparency, and scalability through metadata-driven approach
4. Reduce developer dependency and accelerate onboarding
5. Create self-service configuration utility

### Technical Architecture
- **Model**: Bronze → Silver → Gold layered architecture
- **Bronze Layer**: Raw data ingestion, auto-detect file format, schema validation
- **Silver Layer**: Cleaned, normalized data with business logic transformations
- **Gold Layer**: Final enriched and reconciled data for downstream systems

### Core Components
1. **Ingestion Service**: Detects and ingests multiple file types (CSV, JSON, XML, Pipe)
2. **Configuration Engine**: JSON-based logic definition for process ID, ETL steps, schema
3. **ETL Controller**: Executes standardized 10-step ETL flow via SQL logic
4. **Reconciliation Module**: Compares source vs. target for data integrity
5. **Monitoring Layer**: Tracks process status, control tables, error logs

### Technology Stack
- **Data Processing**: Spark / PySpark / SQL
- **Storage**: Hadoop / SQL Server / Redshift
- **Configuration**: JSON / Control Tables
- **Monitoring**: Batch Control, Process Logs

### Key Metrics
| Metric | Current | Target | Benefit |
|--------|---------|--------|---------|
| Onboarding Time | 8 weeks | 4 weeks | 50% faster |
| Developer Intervention | High (manual coding) | Low (config-driven) | Resource optimization |
| Feeds Supported | 200+ outbound | Unified framework | Simplified operations |
| Data Volume | Up to 7M records/day | Auto-optimized batch | Scalable pipeline |

### 10-Step ETL Framework Flow
1. File Arrival – Files parked in designated inbound location
2. Configuration Identification – Framework reads configuration using process/ETL ID
3. Format Detection – Automatically determines file type
4. Staging Table Mapping – Creates/validates target schema dynamically
5. Transformation – Executes SQL logic embedded in configuration
6. Business Logic Application – Applies conversions, joins, and normalization
7. Reconciliation & Validation – Auto-checks source vs. target counts and integrity
8. Archival & Control – Moves processed data, updates control tables
9. Notification/Monitoring – Logs process and raises alerts if needed
10. Output Feed Generation – Sends data to internal/external systems

### Governance & Ownership
- **Core Team**: Maintain framework, onboard new use cases
- **Stream Teams**: Manage configuration and daily operations
- **BA / Modeler**: Define and validate functional schema
- **QA / Control**: Monitor reconciliation and alerts
- **PMO**: Oversight, SOPs, and reporting

## Image Analysis Notes

### Architecture Diagrams to Review:
- arc.png - Overall architecture
- Config.png - Configuration structure
- Datadistribution.png - Data distribution model
- etl.png - ETL process flow
- MercuryFramework.png - Mercury framework relationship
- Migration.png - Migration approach

### Presentation Slides to Analyze:
- 100+ WhatsApp images containing presentation slides
- Need to extract: detailed technical flows, configuration examples, data models, integration points

## Next Steps
1. Analyze all architecture diagrams
2. Review presentation slides for additional technical details
3. Extract configuration examples and data models
4. Document integration points and system dependencies
5. Create comprehensive functional document


## Detailed Architecture Analysis from Diagrams

### 1. Overall System Architecture (arc.png)
**Hermes System Architecture - Multi-Environment Setup**

#### Data Sources (Trade Store & On-Prem Store):
- **Batch-based feed**: Data transfer through S3 API
- **Stream-based feed (Kafka)**: Streaming through Kafka/MQ
- **API-based feed**: Direct API integration

#### Clearwater Environment (AWS):
**Trade Account & Post Trade Domain Account:**
- **S3 Storage**: Blue gear icon - data transfer orchestration
- **Database**: Two green database icons (likely S3/Redshift)
- **MSK (Managed Streaming for Kafka)**: Purple icon for streaming data
- **Glue**: Purple icon for ETL orchestration
- **Lambda**: Orange icon for serverless processing
- **Glue Data Catalog**: Purple icon for metadata management
- **Column Level Data Catalog**: For fine-grained data governance
- **Tags**: For data classification and organization
- **Local Data Catalog**: Environment-specific metadata

#### EDP (Enterprise Data Platform):
- **AWS Account**: EDP Central Catalog Account
- **Alation Data Catalog**: Central metadata repository
- **Tags**: Enterprise-wide data classification
- **Central Data Catalog**: Unified metadata management
- **Lake Formation**: Data lake governance and security

#### Clearwater Governance:
- **Federated Governance Process**: Red icon for governance workflows
- Bidirectional sync between Clearwater and EDP environments

**Key Integration Points:**
1. Multiple ingestion methods (batch, stream, API)
2. Dual environment setup (Clearwater AWS + EDP)
3. Federated governance with centralized catalog
4. Data lineage tracking across environments

### 2. Mercury Framework - ETL Module (etl.png)

**Config Tables/Collections Layer:**
- **Process Config**: Defines ETL process parameters
- **ETL Steps**: Sequential transformation logic
- **Date Control**: Business date and execution scheduling
- **Holiday Calendar**: Business day calculations

**Python/Glue Based Framework Components:**
1. **ETL by Step Seq**: Sequential execution of transformation steps
2. **Reconciliation**: Source-to-target data validation
3. **Data Quality**: Data profiling and quality checks
4. **Intraday/Busday/Multiday Execution**: Flexible scheduling options
5. **Date Increment**: Business date progression logic
6. **Audit/Control**: Comprehensive logging and monitoring

**Use Cases Implemented:**
- Hermes Data Lake – Hadoop/Unix
- OMD – MS SQL Server/Unix
- Hermes Cloud

**Benefits:**
- ↑ Dev Efficiency by 40%
- ↑ Time to Market by 30%
- Standardization of ETL processes

### 3. Mercury Framework Flow - 12 Custom Features (MercuryFramework.png)

**Landing Layer (Left Hexagon Cluster):**
1. **File Watcher Process**: Monitors inbound file arrivals
2. **Housekeeping**: Cleanup and archival operations
3. **SOX Control**: Compliance and audit controls
4. **Mercury Framework Landing Layer**: Core ingestion engine
5. **Audit and Control**: Logging and tracking
6. **Date Control**: Business date management
7. **Integrity Check**: Data validation at ingestion

**Business Schema Layer (Right Hexagon Cluster):**
1. **Data Quality Check**: Validation rules execution
2. **Control Reporting**: Process status and metrics
3. **Transformation Process**: Business logic application
4. **Mercury Framework Business Schema Layer**: Core transformation engine
5. **Reconciliation**: Source vs. target validation
6. **Audit and Control**: Transformation logging
7. **Error Handling and Logging**: Exception management

**Data Flow:**
- Source Data (External DB, EDI/Flat) → Landing Layer → Business Schema Layer
- Bidirectional flow between layers for validation and reconciliation

### 4. Mercury Framework - Inbound Module (Config.png)

**Config Tables/Collections:**
- **Feed File Config**: File format and schema definitions
- **Date Control**: Execution scheduling
- **Process Control Config**: Workflow orchestration
- **Holiday Calendar**: Business day logic

**Python/Python Based Framework Components:**
1. **File Watcher**: Monitors file arrivals
2. **SOX Controls**: Compliance checks
3. **Processed Feed**: File processing status
4. **Load Trigger**: Initiates downstream processing
5. **Archival**: File retention management
6. **Date Increment**: Business date progression
7. **Audit/Control**: Comprehensive tracking

**Use Cases Implemented:**
- Hermes Data Lake – Hadoop/Unix
- Hercules – MongoDB/Unix
- Hermes ODS, Hermes Clear Water – MongoDB/Unix
- OMD – MS SQL Server/Unix

**Benefits:**
- ↑ Dev Efficiency by 40%
- ↑ Time to Market by 30%
- Standardization of feed ingestion

### 5. Mercury Framework - Data Distribution Module (Datadistribution.png)

**Config Tables/Collections:**
- **Process Config**: Distribution process parameters
- **File Pattern**: Output file format specifications
- **Extraction Steps**: Data extraction logic
- **Transfer**: File transfer protocols
- **Date Control**: Scheduling
- **Holiday Calendar**: Business day handling

**Python/Glue Based Framework Components:**
1. **Extraction Steps in Seq**: Sequential data extraction
2. **Feed creation on Pattern**: Template-based file generation
3. **File Control**: File validation and checksums
4. **Reconciliation**: Output validation
5. **Archival**: Output file retention
6. **Transfer**: Secure file transmission
7. **Date Increment**: Business date management
8. **Audit/Control**: Distribution tracking

**Use Cases Implemented:**
- Hermes Data Lake (Big data – Hive/Impala)
- Hermes ODS – (BCP, MongoDB)
- Hermes Clear Water – AWS Redshift
- OMD (MS SQL Server)

**Benefits:**
- ↑ Dev Efficiency by 40%
- ↑ Time to Market by 60%
- Support of 50+ different file formats & patterns

### 6. Upcoming Function Migrations (Migration.png)

**Planned Decommissioning Timeline:**

| Migration | Components | Timeline |
|-----------|-----------|----------|
| **COS Decommissioning** | Real time Hydration, Data Modelling, 90+ outbounds, API endpoints | 2026 |
| **BPS Decommissioning** | Inbound 70+ feeds, 300+ outbounds | 2026 |
| **FISS Decommissioning** | Real time Hydration, Data Modelling, outbounds, API endpoints | 2026-2027 |
| **SYSTR Decommissioning** | Batch Hydration, Data Modelling, outbounds, API endpoints | 2026-2028 |
| **Tech Debt** | Upgrading Unix servers from RHEL 7 to RHEL 8 and SQL server upgrades | Ongoing |
| **Astrid CV** | Real time Hydration, Data Modelling, outbounds, API endpoints | TBD |

**Key Migration Objectives:**
- Consolidate 400+ feeds (70+ inbound, 300+ outbound) into unified Hermes framework
- Migrate real-time and batch hydration processes
- Standardize data modeling across systems
- Modernize API endpoints
- Address technical debt through infrastructure upgrades
