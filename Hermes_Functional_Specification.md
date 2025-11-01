

> # Hermes Framework Functional Specification
> **Author**: Manus AI
> **Version**: 1.0
> **Date**: 2025-10-31

## 1. Introduction

This document provides a detailed functional and technical overview of the Hermes framework, a strategic initiative designed to modernize and standardize the data processing ecosystem. The Hermes framework is a unified, metadata-driven ETL (Extract, Transform, Load) solution built to replace a complex landscape of legacy systems and redundant data feeds. By leveraging a configuration-driven approach, Hermes aims to significantly reduce manual coding, accelerate the onboarding of new data sources, and establish a scalable, transparent, and automated data processing pipeline.

The development of the Hermes framework is a strategic build, not a simple migration. It represents a fundamental shift from code-based ETL scripts to a centralized, reusable, and self-service model. This new paradigm empowers data teams to configure and manage their own data pipelines through a standardized set of tools and utilities, minimizing their reliance on a central development team.

### 1.1. Purpose and Scope

The primary purpose of the Hermes framework is to standardize data ingestion, transformation, and distribution across the organization. The framework is designed to handle a wide variety of data formats and sources, providing a single, consistent process for managing data from its point of origin to its final destination. The scope of the Hermes framework encompasses the entire data lifecycle, from initial ingestion and validation to transformation, reconciliation, and final delivery to downstream systems.

The key objectives of the Hermes framework are as follows:

- **Standardize Data Processing**: To establish a single, consistent process for data ingestion, transformation, and distribution across all business units and asset classes.
- **Reduce Complexity**: To decommission redundant data feeds and legacy systems, simplifying the overall data architecture.
- **Increase Automation**: To automate the end-to-end data processing workflow, reducing the need for manual intervention.
- **Improve Scalability**: To build a scalable and elastic data processing platform that can handle growing data volumes and evolving business requirements.
- **Enhance Transparency**: To provide a clear and comprehensive view of the entire data processing lifecycle, from data lineage to processing status.
- **Empower Data Teams**: To provide data teams with the tools and utilities they need to manage their own data pipelines, reducing their dependence on a central development team.

### 1.2. References

This document is based on the analysis of the following materials:

- [1] ExecutiveSummary.docx
- [2] Hermes.docx
- [3] Architecture Diagrams (arc.png, etl.png, MercuryFramework.png, Config.png, Datadistribution.png, Migration.png)
- [4] Presentation Slides (99 images)

## 2. System Architecture

The Hermes framework is built upon a modern, multi-layered data architecture that promotes separation of concerns and facilitates a clear and organized data flow. The architecture is designed to be both scalable and flexible, leveraging a combination of on-premises and cloud-based technologies to meet the diverse needs of the organization. The system is divided into several key architectural components, including the data processing layers, the underlying technology stack, and the integration with the broader enterprise data platform.

### 2.1. High-Level Architecture

The high-level architecture of the Hermes framework is based on a three-layered model, commonly referred to as the Bronze, Silver, and Gold layers. This layered approach ensures that data is progressively cleaned, transformed, and enriched as it moves through the system, culminating in a high-quality, business-ready dataset. The framework also incorporates a robust governance and monitoring layer that provides visibility and control over the entire data processing lifecycle.

The overall system architecture, as depicted in the provided diagrams [3], consists of several interconnected environments, including the operational data stores, the Clearwater processing environment, and the Enterprise Data Platform (EDP). Data is ingested from a variety of sources, including batch feeds, streaming data, and APIs, and is then processed through the various layers of the Hermes framework.

![Overall System Architecture](/home/ubuntu/upload/arc.png)

### 2.2. Data Processing Layers

The Hermes framework utilizes a medallion architecture, which organizes data into three distinct layers: Bronze, Silver, and Gold. This layered approach provides a clear and structured data flow, ensuring that data is progressively refined and enriched as it moves through the system.

| Layer | Description | Tools/Logic |
|---|---|---|
| **Bronze** | Raw data ingestion and staging | Auto-detects file format, schema validation |
| **Silver** | Cleaned, normalized data | Business logic transformations |
| **Gold** | Final, enriched and reconciled data | Output feeds to downstream systems |

**Bronze Layer**: The Bronze layer is the initial entry point for all data entering the Hermes framework. Data in this layer is in its raw, unprocessed state. The primary function of the Bronze layer is to ingest data from various sources and perform initial validation checks, such as file format detection and schema validation. This layer acts as a historical archive of all source data, providing a complete and auditable record of all incoming information.

**Silver Layer**: The Silver layer contains data that has been cleaned, transformed, and enriched. In this layer, business logic is applied to the raw data to normalize data formats, handle missing values, and perform other data quality improvements. The data in the Silver layer is structured and queryable, making it suitable for a variety of analytical and reporting purposes.

**Gold Layer**: The Gold layer contains the final, business-ready data that is consumed by downstream systems and applications. The data in this layer has been fully transformed, reconciled, and aggregated to meet the specific needs of the business. The Gold layer provides a single source of truth for all key business metrics and KPIs.

### 2.3. Technology Stack

The Hermes framework leverages a modern, cloud-native technology stack that is designed to be both scalable and cost-effective. The framework is built primarily on Amazon Web Services (AWS) and utilizes a variety of managed services to minimize operational overhead and maximize flexibility. The core technology stack includes the following components:

| Layer | Technology |
|---|---|
| **Data Processing** | Spark / PySpark / SQL |
| **Storage** | Hadoop / SQL Server / Redshift / S3 |
| **Configuration** | JSON / Control Tables |
| **Monitoring** | Batch Control, Process Logs |
| **Streaming** | MSK (Managed Streaming for Kafka) |
| **Orchestration** | AWS Glue |
| **Serverless** | AWS Lambda |
| **Data Catalog** | Alation / AWS Glue Data Catalog |
| **Governance** | AWS Lake Formation |

## 3. ETL Framework and Process Flow

The Hermes framework is built around a standardized, 10-step ETL process that ensures consistency and reliability across all data pipelines. This process is orchestrated by the ETL Controller, which reads the configuration for each pipeline and executes the required steps in the correct sequence. The entire process is designed to be highly automated, with minimal need for manual intervention.

The ETL process flow is divided into three main stages: Ingestion, Transformation, and Distribution. Each stage consists of a series of steps that are executed in a predefined order. The following diagram provides a high-level overview of the ETL process flow:

![ETL Process Flow](/home/ubuntu/upload/etl.png)

### 3.1. 10-Step ETL Framework Flow

The standardized 10-step ETL flow is the backbone of the Hermes framework. This process ensures that all data is ingested, processed, and delivered in a consistent and reliable manner. The following table provides a detailed description of each step in the ETL process:

| Step | Description |
|---|---|
| **1. File Arrival** | Files are parked in a designated inbound location. The File Watcher process monitors this location for new arrivals. |
| **2. Configuration Identification** | The framework reads the configuration for the incoming file using the process/ETL ID. |
| **3. Format Detection** | The framework automatically determines the file type (e.g., CSV, JSON, XML, Pipe). |
| **4. Staging Table Mapping** | The framework creates or validates the target schema for the data in the staging area. |
| **5. Transformation** | The framework executes the SQL logic embedded in the configuration to transform the data. |
| **6. Business Logic Application** | The framework applies any additional business logic, such as conversions, joins, and normalization. |
| **7. Reconciliation & Validation** | The framework automatically checks the source vs. target counts and performs other data integrity checks. |
| **8. Archival & Control** | The framework moves the processed data to an archival location and updates the control tables. |
| **9. Notification/Monitoring** | The framework logs the process status and raises alerts if any issues are detected. |
| **10. Output Feed Generation** | The framework sends the processed data to the appropriate internal or external systems. |

### 3.2. Mercury Framework Integration

The Hermes framework is closely integrated with the Mercury framework, which provides a set of reusable components and services for data processing. The Mercury framework is composed of several modules, including the Inbound Module, the ETL Module, and the Data Distribution Module. These modules provide a standardized set of tools and utilities for managing the end-to-end data processing lifecycle.

The following diagram illustrates the high-level flow of the Mercury framework:

![Mercury Framework Flow](/home/ubuntu/upload/MercuryFramework.png)

As shown in the diagram, the Mercury framework is divided into two main layers: the Landing Layer and the Business Schema Layer. The Landing Layer is responsible for ingesting data from various sources and performing initial validation checks. The Business Schema Layer is responsible for applying business logic, transforming the data, and preparing it for consumption by downstream systems.

## 4. Configuration and Automation

A core principle of the Hermes framework is **Configuration over Code**. This approach is designed to minimize manual script development and empower data teams to manage their own ETL pipelines through a self-service model. The framework leverages a JSON-based configuration system, which allows developers to define the entire ETL process, from ingestion to distribution, in a declarative manner.

### 4.1. Configuration-Driven Logic

Instead of writing custom Spark or Python code for each new data feed, developers define the ETL logic in a standardized JSON format. The Hermes framework then reads this configuration and dynamically generates the necessary SQL and Spark jobs to execute the pipeline. This approach has several key benefits:

- **Reduced Development Time**: Eliminates the need to write boilerplate code for each new pipeline.
- **Increased Consistency**: Ensures that all pipelines adhere to the same standards and best practices.
- **Simplified Maintenance**: Centralizes the ETL logic in a single, easy-to-understand format.
- **Empowered Data Teams**: Allows data teams to manage their own pipelines without requiring deep expertise in Spark or Python.

The following is a conceptual example of the JSON configuration structure:

```json
{
  "process_id": "HERMES001",
  "source": "STAGING_FEED",
  "target": "SETTLEMENT_TABLE",
  "steps": [
    {"validate": "schema_check"},
    {"transform": "business_logic"},
    {"reconcile": "source_vs_target"}
  ]
}
```

### 4.2. Configuration Management

The configuration for the Hermes framework is managed through a set of control tables and collections. These tables store the metadata for each ETL process, including the process configuration, ETL steps, date control, and holiday calendar. This centralized approach to configuration management ensures that all pipelines are managed in a consistent and auditable manner.

The following diagram illustrates the configuration components of the Mercury Inbound Module, which is a key part of the Hermes framework:

![Configuration Components](/home/ubuntu/upload/Config.png)

As shown in the diagram, the configuration is divided into several key areas:

- **Feed File Config**: Defines the format and schema for each inbound data feed.
- **Date Control**: Manages the business date and execution schedule for each pipeline.
- **Process Control Config**: Orchestrates the overall workflow for each ETL process.
- **Holiday Calendar**: Provides a centralized source for business day calculations.
## 5. Governance and Ownership

Effective governance is a critical component of the Hermes framework. The framework is designed to provide a clear and comprehensive view of the entire data processing lifecycle, from data lineage to processing status. This is achieved through a federated governance model that balances the need for centralized control with the desire to empower individual data teams.

### 5.1. Roles and Responsibilities

The governance model for the Hermes framework is based on a clear division of roles and responsibilities. The following table outlines the key roles and their corresponding responsibilities:

| Role | Responsibilities |
|---|---|
| **Core Team** | Maintain and enhance the framework, onboard new use cases, and provide support to the stream teams. |
| **Stream Teams** | Manage the configuration and daily operations of their own data pipelines. |
| **BA / Modeler** | Define and validate the functional schema for each data feed. |
| **QA / Control** | Monitor the reconciliation and alerting processes to ensure data integrity. |
| **PMO** | Provide oversight and governance for the entire Hermes framework. |

### 5.2. Federated Governance Model

The Hermes framework utilizes a federated governance model that combines a centralized data catalog with local data catalogs in each environment. This approach allows for a single, unified view of all data assets, while still providing the flexibility for individual teams to manage their own data. The central data catalog is managed by the Enterprise Data Platform (EDP) and is powered by Alation. The local data catalogs are managed by AWS Glue and provide a more detailed view of the data within each environment.

The following diagram illustrates the federated governance process:

![Federated Governance](/home/ubuntu/upload/arc.png)

As shown in the diagram, there is a bidirectional synchronization between the central and local data catalogs. This ensures that all data is consistently tagged and classified across all environments. The framework also leverages AWS Lake Formation to enforce fine-grained security policies and control access to sensitive data.

## 6. Migration and Decommissioning

The Hermes framework is a key enabler of the organization's broader data modernization strategy. A key goal of the Hermes initiative is to decommission a large number of legacy systems and redundant data feeds, simplifying the overall data architecture and reducing operational costs. The migration to the Hermes framework will be a multi-year effort, with a phased approach that prioritizes the most critical systems and data feeds.

### 6.1. Migration Roadmap

The following table outlines the planned decommissioning timeline for the key legacy systems that will be replaced by the Hermes framework:

| Migration | Components | Timeline |
|---|---|---|
| **COS Decommissioning** | Real time Hydration, Data Modelling, 90+ outbounds, API endpoints | 2026 |
| **BPS Decommissioning** | Inbound 70+ feeds, 300+ outbounds | 2026 |
| **FISS Decommissioning** | Real time Hydration, Data Modelling, outbounds, API endpoints | 2026-2027 |
| **SYSTR Decommissioning** | Batch Hydration, Data Modelling, outbounds, API endpoints | 2026-2028 |
| **Tech Debt** | Upgrading Unix servers from RHEL 7 to RHEL 8 and SQL server upgrades | Ongoing |
| **Astrid CV** | Real time Hydration, Data Modelling, outbounds, API endpoints | TBD |

![Migration Timeline](/home/ubuntu/upload/Migration.png)

### 6.2. Key Migration Objectives

The migration to the Hermes framework is designed to achieve several key objectives:

- **Consolidate Data Feeds**: Consolidate over 400 data feeds (70+ inbound and 300+ outbound) into the unified Hermes framework.
- **Standardize Data Processing**: Migrate both real-time and batch hydration processes to the new framework.
- **Modernize Data Modeling**: Standardize data modeling across all systems and asset classes.
- **Upgrade API Endpoints**: Modernize and standardize all API endpoints.
- **Address Technical Debt**: Address long-standing technical debt through infrastructure upgrades and system consolidation.

## 7. Benefits and Metrics

The adoption of the Hermes framework is expected to deliver significant benefits across the organization, including increased efficiency, faster time to market, and improved data quality. The framework's success will be measured against a set of key performance indicators (KPIs) that track these improvements over time.

### 7.1. Quantified Benefits

The Hermes framework is projected to deliver substantial improvements in several key areas. The following table summarizes the expected benefits, as outlined in the provided documentation [1, 2, 4]:

| Metric | Current State | Target State | Benefit |
|---|---|---|---|
| **Onboarding Time** | 8 weeks | 4 weeks | 50% faster delivery |
| **Developer Intervention** | High (manual coding) | Low (config-driven) | Resource optimization |
| **Time to Market (Distribution)** | N/A | N/A | 60% improvement |
| **Feed Duplication** | 200+ outbound feeds | Unified framework | Simplified operations |
| **Data Volume** | Up to 7M records/day | Auto-optimized batch processing | Scalable pipeline |
| **Supported Formats** | Limited | 50+ file formats & patterns | Increased flexibility |

These metrics highlight the transformative impact of the Hermes framework. By automating manual processes and standardizing the data processing workflow, the framework will enable the organization to deliver new data products and services to the market more quickly and efficiently.

### 7.2. Key Success Factors

The success of the Hermes framework is dependent on a number of key factors. These include:

- **Configuration-Driven Approach**: The shift from code-based to configuration-based ETL is the cornerstone of the Hermes framework. This approach is critical for achieving the desired levels of automation and self-service.
- **Metadata Management**: A centralized and well-managed metadata repository is essential for providing a clear and comprehensive view of the entire data processing lifecycle.
- **Automated Reconciliation**: Automated reconciliation is key to ensuring data integrity and building trust in the data.
- **Modular Design**: The modular design of the framework allows for the reuse of components across multiple use cases, which accelerates development and reduces maintenance costs.
- **Cloud-Native Architecture**: The use of cloud-native technologies provides the scalability, flexibility, and cost-effectiveness required to meet the evolving needs of the business.
- **Federated Governance**: The federated governance model provides the right balance of centralized control and decentralized autonomy, empowering data teams while still ensuring compliance with enterprise standards.

## 8. Detailed Module Specifications

The Hermes framework is composed of three primary modules, each responsible for a specific stage of the data processing lifecycle. These modules are the Inbound Module, the ETL Module, and the Data Distribution Module. Each module is built on the same core principles of configuration-driven automation and metadata management.

### 8.1. Inbound Module

The Inbound Module is responsible for ingesting data from a variety of sources and performing initial validation checks. This module is designed to handle a wide range of file formats, including CSV, JSON, XML, and pipe-delimited files. The module automatically detects the file format and validates the schema against the configuration.

**Key Components:**

- **File Watcher**: Monitors designated inbound locations for new file arrivals. When a new file is detected, the File Watcher triggers the ingestion process.
- **SOX Controls**: Performs compliance checks to ensure that all data is handled in accordance with regulatory requirements.
- **Processed Feed**: Tracks the status of each file as it moves through the ingestion process.
- **Load Trigger**: Initiates the downstream processing of the data once it has been successfully ingested and validated.
- **Archival**: Moves the processed files to a designated archival location for long-term retention.
- **Date Increment**: Manages the business date progression for each data feed.
- **Audit/Control**: Logs all ingestion activities and provides comprehensive tracking of the data lineage.

**Process Flow:**

1. File arrives in the designated inbound location.
2. File Watcher detects the new file and retrieves the configuration.
3. The system performs format detection and schema validation.
4. SOX controls are executed to ensure compliance.
5. The data is loaded into the staging area.
6. The processed feed status is updated.
7. The file is archived.
8. The business date is incremented.
9. All activities are logged in the audit/control tables.

**Benefits:**

- Development efficiency increased by 40%
- Time to market improved by 30%
- Standardization of feed ingestion across all systems

### 8.2. ETL Module

The ETL Module is the core of the Hermes framework, responsible for transforming raw data into business-ready information. This module executes the standardized 10-step ETL process, applying business logic, performing data quality checks, and reconciling the data to ensure accuracy and completeness.

**Key Components:**

- **ETL by Step Seq**: Executes the transformation steps in the correct sequence, as defined in the configuration.
- **Reconciliation**: Compares the source and target data to ensure that all records have been processed correctly.
- **Data Quality**: Performs a variety of data quality checks, including null value detection, data type validation, and referential integrity checks.
- **Intraday/Busday/Multiday Execution**: Supports flexible scheduling options to accommodate different business requirements.
- **Date Increment**: Manages the business date progression for each ETL process.
- **Audit/Control**: Logs all transformation activities and provides comprehensive tracking of the data lineage.

**Process Flow:**

1. The ETL Controller retrieves the configuration for the process.
2. The system executes the ETL steps in the defined sequence.
3. Business logic is applied to transform the data.
4. Data quality checks are performed.
5. The data is reconciled against the source.
6. The business date is incremented.
7. All activities are logged in the audit/control tables.

**Benefits:**

- Development efficiency increased by 40%
- Time to market improved by 30%
- Standardization of ETL processes across all systems

### 8.3. Data Distribution Module

The Data Distribution Module is responsible for generating output feeds and distributing them to downstream systems. This module supports a wide variety of file formats and transfer protocols, providing a flexible and scalable solution for data distribution.

![Data Distribution Module](/home/ubuntu/upload/Datadistribution.png)

**Key Components:**

- **Extraction Steps in Seq**: Executes the data extraction steps in the correct sequence, as defined in the configuration.
- **Feed Creation on Pattern**: Generates output files based on predefined templates and patterns.
- **File Control**: Validates the output files and generates checksums to ensure data integrity.
- **Reconciliation**: Compares the output data against the source to ensure that all records have been processed correctly.
- **Archival**: Moves the output files to a designated archival location for long-term retention.
- **Transfer**: Securely transfers the output files to the target systems using a variety of protocols, including SFTP, S3, and API.
- **Date Increment**: Manages the business date progression for each distribution process.
- **Audit/Control**: Logs all distribution activities and provides comprehensive tracking of the data lineage.

**Process Flow:**

1. The Distribution Controller retrieves the configuration for the process.
2. The system executes the extraction steps in the defined sequence.
3. Output files are generated based on the file pattern templates.
4. File control checks are performed.
5. The data is reconciled against the source.
6. The output files are archived.
7. The files are transferred to the target systems.
8. The business date is incremented.
9. All activities are logged in the audit/control tables.

**Benefits:**

- Development efficiency increased by 40%
- Time to market improved by 60%
- Support for 50+ different file formats and patterns

## 9. Implementation Use Cases

The Hermes framework has been successfully implemented across a variety of use cases, demonstrating its flexibility and scalability. The following table summarizes the key implementation use cases:

| Use Case | Description | Technology |
|---|---|---|
| **Hermes Data Lake** | Large-scale data lake for analytical processing | Hadoop / Unix / Hive / Impala |
| **Hermes ODS** | Operational Data Store for real-time data access | MongoDB / Unix / BCP |
| **Hermes Clear Water** | Cloud-based data warehouse for analytics | AWS Redshift |
| **OMD** | Operational Market Data system | MS SQL Server / Unix |
| **Hercules** | Document-based data store | MongoDB / Unix |

These use cases demonstrate the versatility of the Hermes framework and its ability to support a wide range of data processing requirements, from large-scale batch processing to real-time data streaming.

## 10. Mercury Framework - 12 Custom Features

The Mercury framework, which is integrated with Hermes, provides 12 custom features that are essential for managing the end-to-end data processing lifecycle. These features are organized into two main layers: the Landing Layer and the Business Schema Layer.

**Landing Layer Features:**

1. **File Watcher Process**: Monitors inbound file arrivals and triggers the ingestion process.
2. **Housekeeping**: Performs cleanup and archival operations to maintain system performance.
3. **SOX Control**: Ensures compliance with regulatory requirements.
4. **Mercury Framework Landing Layer**: Core ingestion engine that orchestrates the entire ingestion process.
5. **Audit and Control**: Logs all ingestion activities and provides comprehensive tracking.
6. **Date Control**: Manages business date progression and scheduling.
7. **Integrity Check**: Validates data integrity at the point of ingestion.

**Business Schema Layer Features:**

1. **Data Quality Check**: Executes validation rules to ensure data quality.
2. **Control Reporting**: Provides process status and metrics.
3. **Transformation Process**: Applies business logic to transform the data.
4. **Mercury Framework Business Schema Layer**: Core transformation engine that orchestrates the entire transformation process.
5. **Reconciliation**: Validates data against the source to ensure accuracy.
6. **Audit and Control**: Logs all transformation activities and provides comprehensive tracking.
7. **Error Handling and Logging**: Manages exceptions and provides detailed error logs.

These 12 features work together to provide a comprehensive and robust data processing platform that is both flexible and scalable.

## 11. Conclusion

The Hermes framework represents a significant advancement in the organization's data processing capabilities. By shifting from a code-based to a configuration-driven approach, the framework enables a more agile, efficient, and scalable data processing environment. The framework's modular design, combined with its robust governance and monitoring capabilities, provides a solid foundation for the organization's data modernization strategy.

The benefits of the Hermes framework are substantial, including a 50% reduction in onboarding time, a 40% increase in development efficiency, and support for over 50 different file formats and patterns. These improvements will enable the organization to deliver new data products and services to the market more quickly and efficiently, while also reducing operational costs and complexity.

The migration to the Hermes framework will be a multi-year effort, but the long-term benefits are clear. By decommissioning legacy systems and consolidating redundant data feeds, the organization will simplify its data architecture and create a more sustainable and scalable data processing platform. The Hermes framework is not just a technology solution; it is a strategic enabler that will empower the organization to achieve its data-driven business objectives.

## 12. Action Items and Next Steps

The following action items have been identified to ensure the successful implementation and adoption of the Hermes framework:

| # | Action Item | Owner | Priority | Status |
|---|---|---|---|---|
| 1 | Finalize JSON configuration schema and parameter list | Core Dev Team | High | In progress |
| 2 | Build common utility to auto-generate configuration files | Engineering | High | Planned |
| 3 | Define canonical data model for all asset classes | BA & Data Modeler | Medium | Ongoing |
| 4 | Identify redundant feeds for decommissioning | Business Stream | Medium | In progress |
| 5 | Implement reconciliation module (source vs target) | QA / Control | High | Planned |
| 6 | Establish monitoring and error-logging framework | Core Dev Team | Medium | Planned |
| 7 | Validate onboarding efficiency improvements (pilot phase) | Project Manager | Medium | Pending pilot results |
| 8 | Document variant logic for regional settlements | BA / Data Modeler | Medium | Planned |
| 9 | Schedule framework dry-run with sample dataset | Core Dev + QA | High | To be scheduled |
| 10 | Prepare governance SOP for process ownership | PMO | Low | Drafting |

**Next Steps:**

1. Create Hermes Phase 1 Report Deck summarizing framework design and outcomes.
2. Conduct pilot deployment on selected data mart.
3. Measure onboarding and reconciliation metrics post-implementation.
4. Prepare Phase 2 proposal for end-to-end automation and observability integration.

---

## References

[1] ExecutiveSummary.docx - Hermes Project Executive Summary  
[2] Hermes.docx - Hermes Framework Technical Documentation  
[3] Architecture Diagrams - System Architecture, ETL Module, Mercury Framework, Configuration, Data Distribution, Migration  
[4] Presentation Slides - 99 detailed presentation slides covering all aspects of the Hermes framework implementation

---

**Document End**
