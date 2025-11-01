"""
Hermes Config Generator - Template Library
Pre-built templates for common data feed types
"""

import json
from typing import Dict, List, Any

class TemplateLibrary:
    """Library of pre-built configuration templates"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Dict]:
        """Load all pre-built templates"""
        return {
            "csv_trade_data": self._csv_trade_template(),
            "json_market_data": self._json_market_template(),
            "xml_customer_data": self._xml_customer_template(),
            "pipe_delimited_transaction": self._pipe_transaction_template(),
            "csv_financial_report": self._csv_financial_template(),
            "json_api_feed": self._json_api_template(),
            "csv_inventory_data": self._csv_inventory_template(),
            "json_user_activity": self._json_user_activity_template(),
            "csv_sales_data": self._csv_sales_template(),
            "xml_order_data": self._xml_order_template(),
            "csv_employee_data": self._csv_employee_template(),
            "json_iot_sensor": self._json_iot_template()
        }
    
    def get_template(self, template_id: str) -> Dict[str, Any]:
        """Get a specific template by ID"""
        return self.templates.get(template_id, {})
    
    def list_templates(self) -> List[Dict[str, str]]:
        """List all available templates"""
        template_list = []
        for tid, template in self.templates.items():
            template_list.append({
                "id": tid,
                "name": template.get("metadata", {}).get("name", tid),
                "description": template.get("metadata", {}).get("description", ""),
                "file_format": template.get("metadata", {}).get("file_format", ""),
                "use_case": template.get("metadata", {}).get("use_case", "")
            })
        return template_list
    
    def _csv_trade_template(self) -> Dict:
        return {
            "metadata": {
                "name": "CSV Trade Data",
                "description": "...",
                "file_format": "CSV",
                "use_case": "...",
                "typical_columns": ["trade_id", "symbol", "quantity", "price", "trade_date"]
            },
            "process_config": {
                "process_id": "TRADE_DAILY",
                "process_name": "Daily Trade Processing",
                "source_system": "Trading Platform",
                "schedule": "Daily at 6 PM",
                "enabled": True,
                "retry_count": 3,
                "timeout_minutes": 30
            },
            "feed_file_config": {
                "feed_id": "TRADE_CSV",
                "file_format": "CSV",
                "delimiter": ",",
                "header_row": True,
                "encoding": "utf-8",
                "columns": [
                    {"name": "trade_id", "type": "string", "nullable": False, "primary_key": True},
                    {"name": "symbol", "type": "string", "nullable": False},
                    {"name": "quantity", "type": "integer", "nullable": False},
                    {"name": "price", "type": "decimal", "nullable": False},
                    {"name": "trade_date", "type": "date", "nullable": False}
                ]
            },
            "etl_steps": [
                {"step_id": 1, "step_name": "Remove Duplicates", "step_type": "deduplication", "key_columns": ["trade_id"]},
                {"step_id": 2, "step_name": "Validate Amounts", "step_type": "validation", "rule": "price > 0 AND quantity > 0"},
                {"step_id": 3, "step_name": "Calculate Total", "step_type": "calculation", "formula": "total_amount = quantity * price"},
                {"step_id": 4, "step_name": "Aggregate by Symbol", "step_type": "aggregation", "group_by": ["symbol", "trade_date"]}
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
    
    def _json_market_template(self) -> Dict:
        return {
            "metadata": {
                "name": "JSON Market Data",
                "description": "JSON feed with market prices and volumes",
                "file_format": "JSON",
                "use_case": "Real-time or batch market data feeds",
                "typical_columns": ["symbol", "price", "volume", "timestamp"]
            },
            "process_config": {
                "process_id": "MARKET_DATA_HOURLY",
                "process_name": "Hourly Market Data Processing",
                "source_system": "Market Data Provider",
                "schedule": "Hourly",
                "enabled": True,
                "retry_count": 5,
                "timeout_minutes": 15
            },
            "feed_file_config": {
                "feed_id": "MARKET_JSON",
                "file_format": "JSON",
                "json_type": "array",
                "columns": [
                    {"name": "symbol", "type": "string", "nullable": False},
                    {"name": "price", "type": "decimal", "nullable": False},
                    {"name": "volume", "type": "integer", "nullable": True},
                    {"name": "timestamp", "type": "timestamp", "nullable": False}
                ]
            },
            "etl_steps": [
                {"step_id": 1, "step_name": "Parse Timestamp", "step_type": "transformation", "action": "convert_to_datetime"},
                {"step_id": 2, "step_name": "Validate Prices", "step_type": "validation", "rule": "price > 0"},
                {"step_id": 3, "step_name": "Calculate VWAP", "step_type": "calculation", "formula": "vwap = sum(price * volume) / sum(volume)"}
            ],
            "date_control": {
                "business_date_column": "timestamp",
                "date_format": "%Y-%m-%dT%H:%M:%SZ",
                "timezone": "UTC"
            },
            "file_pattern": {
                "output_pattern": "market_data_{business_date}_{hour}.json",
                "output_format": "JSON",
                "output_location": "s3://bucket/output/market/"
            }
        }
    
    def _xml_customer_template(self) -> Dict:
        return {
            "metadata": {
                "name": "XML Customer Data",
                "description": "Customer information from CRM systems",
                "file_format": "XML",
                "use_case": "Customer master data synchronization",
                "typical_columns": ["customer_id", "name", "email", "registration_date"]
            },
            "process_config": {
                "process_id": "CUSTOMER_DAILY",
                "process_name": "Daily Customer Sync",
                "source_system": "CRM System",
                "schedule": "Daily at 2 AM",
                "enabled": True,
                "retry_count": 3,
                "timeout_minutes": 45
            },
            "feed_file_config": {
                "feed_id": "CUSTOMER_XML",
                "file_format": "XML",
                "root_element": "customers",
                "record_element": "customer",
                "columns": [
                    {"name": "customer_id", "type": "string", "nullable": False, "primary_key": True},
                    {"name": "name", "type": "string", "nullable": False},
                    {"name": "email", "type": "string", "nullable": True},
                    {"name": "registration_date", "type": "date", "nullable": False}
                ]
            },
            "etl_steps": [
                {"step_id": 1, "step_name": "Remove Duplicates", "step_type": "deduplication", "key_columns": ["customer_id"]},
                {"step_id": 2, "step_name": "Validate Email", "step_type": "validation", "rule": "email LIKE '%@%.%'"},
                {"step_id": 3, "step_name": "Standardize Names", "step_type": "transformation", "action": "title_case"}
            ],
            "date_control": {
                "business_date_column": "registration_date",
                "date_format": "%Y-%m-%d",
                "timezone": "UTC"
            },
            "file_pattern": {
                "output_pattern": "customers_{business_date}.csv",
                "output_format": "CSV",
                "output_location": "s3://bucket/output/customers/"
            }
        }
    
    def _pipe_transaction_template(self) -> Dict:
        return {
            "metadata": {
                "name": "Pipe-Delimited Transaction Data",
                "description": "Transaction records with pipe delimiter",
                "file_format": "Pipe-Delimited",
                "use_case": "Legacy system transaction exports",
                "typical_columns": ["transaction_id", "account_id", "amount", "transaction_date"]
            },
            "process_config": {
                "process_id": "TRANSACTION_BATCH",
                "process_name": "Batch Transaction Processing",
                "source_system": "Legacy Banking System",
                "schedule": "Daily at 11 PM",
                "enabled": True,
                "retry_count": 3,
                "timeout_minutes": 60
            },
            "feed_file_config": {
                "feed_id": "TRANSACTION_PIPE",
                "file_format": "CSV",
                "delimiter": "|",
                "header_row": True,
                "encoding": "utf-8",
                "columns": [
                    {"name": "transaction_id", "type": "string", "nullable": False, "primary_key": True},
                    {"name": "account_id", "type": "string", "nullable": False},
                    {"name": "amount", "type": "decimal", "nullable": False},
                    {"name": "transaction_date", "type": "timestamp", "nullable": False}
                ]
            },
            "etl_steps": [
                {"step_id": 1, "step_name": "Remove Duplicates", "step_type": "deduplication", "key_columns": ["transaction_id"]},
                {"step_id": 2, "step_name": "Validate Amount", "step_type": "validation", "rule": "amount != 0"},
                {"step_id": 3, "step_name": "Calculate Daily Total", "step_type": "aggregation", "group_by": ["account_id", "transaction_date"]}
            ],
            "date_control": {
                "business_date_column": "transaction_date",
                "date_format": "%Y-%m-%d %H:%M:%S",
                "timezone": "UTC"
            },
            "file_pattern": {
                "output_pattern": "transactions_{business_date}.csv",
                "output_format": "CSV",
                "output_location": "s3://bucket/output/transactions/"
            }
        }
    
    def _csv_financial_template(self) -> Dict:
        return {
            "metadata": {
                "name": "CSV Financial Report",
                "description": "Financial statements and reports",
                "file_format": "CSV",
                "use_case": "Monthly/Quarterly financial reporting",
                "typical_columns": ["account_code", "account_name", "amount", "period"]
            },
            "process_config": {
                "process_id": "FINANCIAL_MONTHLY",
                "process_name": "Monthly Financial Report",
                "source_system": "ERP System",
                "schedule": "Monthly on 1st at 8 AM",
                "enabled": True,
                "retry_count": 2,
                "timeout_minutes": 90
            },
            "feed_file_config": {
                "feed_id": "FINANCIAL_CSV",
                "file_format": "CSV",
                "delimiter": ",",
                "header_row": True,
                "encoding": "utf-8",
                "columns": [
                    {"name": "account_code", "type": "string", "nullable": False},
                    {"name": "account_name", "type": "string", "nullable": False},
                    {"name": "amount", "type": "decimal", "nullable": False},
                    {"name": "period", "type": "string", "nullable": False}
                ]
            },
            "etl_steps": [
                {"step_id": 1, "step_name": "Validate Account Codes", "step_type": "validation", "rule": "account_code MATCHES '^[0-9]{4,6}$'"},
                {"step_id": 2, "step_name": "Calculate Subtotals", "step_type": "aggregation", "group_by": ["account_code", "period"]},
                {"step_id": 3, "step_name": "Format Currency", "step_type": "transformation", "action": "round_to_2_decimals"}
            ],
            "date_control": {
                "business_date_column": "period",
                "date_format": "%Y-%m",
                "timezone": "UTC"
            },
            "file_pattern": {
                "output_pattern": "financial_report_{period}.csv",
                "output_format": "CSV",
                "output_location": "s3://bucket/output/financial/"
            }
        }
    
    def _json_api_template(self) -> Dict:
        return {
            "metadata": {
                "name": "JSON API Feed",
                "description": "REST API JSON responses",
                "file_format": "JSON",
                "use_case": "API data ingestion",
                "typical_columns": ["id", "data", "timestamp"]
            },
            "process_config": {
                "process_id": "API_REALTIME",
                "process_name": "Real-time API Data Ingestion",
                "source_system": "External API",
                "schedule": "Every 5 minutes",
                "enabled": True,
                "retry_count": 5,
                "timeout_minutes": 5
            },
            "feed_file_config": {
                "feed_id": "API_JSON",
                "file_format": "JSON",
                "json_type": "object",
                "columns": [
                    {"name": "id", "type": "string", "nullable": False, "primary_key": True},
                    {"name": "data", "type": "json", "nullable": True},
                    {"name": "timestamp", "type": "timestamp", "nullable": False}
                ]
            },
            "etl_steps": [
                {"step_id": 1, "step_name": "Parse JSON Data", "step_type": "transformation", "action": "flatten_json"},
                {"step_id": 2, "step_name": "Remove Duplicates", "step_type": "deduplication", "key_columns": ["id"]},
                {"step_id": 3, "step_name": "Enrich with Metadata", "step_type": "enrichment", "action": "add_ingestion_timestamp"}
            ],
            "date_control": {
                "business_date_column": "timestamp",
                "date_format": "%Y-%m-%dT%H:%M:%S.%fZ",
                "timezone": "UTC"
            },
            "file_pattern": {
                "output_pattern": "api_data_{business_date}_{timestamp}.json",
                "output_format": "JSON",
                "output_location": "s3://bucket/output/api/"
            }
        }
    
    def _csv_inventory_template(self) -> Dict:
        return {
            "metadata": {
                "name": "CSV Inventory Data",
                "description": "Product inventory levels",
                "file_format": "CSV",
                "use_case": "Daily inventory snapshots",
                "typical_columns": ["product_id", "quantity", "location", "snapshot_date"]
            },
            "process_config": {
                "process_id": "INVENTORY_DAILY",
                "process_name": "Daily Inventory Snapshot",
                "source_system": "Warehouse Management System",
                "schedule": "Daily at 11:59 PM",
                "enabled": True,
                "retry_count": 3,
                "timeout_minutes": 30
            },
            "feed_file_config": {
                "feed_id": "INVENTORY_CSV",
                "file_format": "CSV",
                "delimiter": ",",
                "header_row": True,
                "encoding": "utf-8",
                "columns": [
                    {"name": "product_id", "type": "string", "nullable": False},
                    {"name": "quantity", "type": "integer", "nullable": False},
                    {"name": "location", "type": "string", "nullable": False},
                    {"name": "snapshot_date", "type": "date", "nullable": False}
                ]
            },
            "etl_steps": [
                {"step_id": 1, "step_name": "Validate Quantity", "step_type": "validation", "rule": "quantity >= 0"},
                {"step_id": 2, "step_name": "Aggregate by Product", "step_type": "aggregation", "group_by": ["product_id", "snapshot_date"]},
                {"step_id": 3, "step_name": "Flag Low Stock", "step_type": "calculation", "formula": "low_stock = quantity < 10"}
            ],
            "date_control": {
                "business_date_column": "snapshot_date",
                "date_format": "%Y-%m-%d",
                "timezone": "UTC"
            },
            "file_pattern": {
                "output_pattern": "inventory_{snapshot_date}.csv",
                "output_format": "CSV",
                "output_location": "s3://bucket/output/inventory/"
            }
        }
    
    def _json_user_activity_template(self) -> Dict:
        return {
            "metadata": {
                "name": "JSON User Activity",
                "description": "User behavior and activity logs",
                "file_format": "JSON",
                "use_case": "User analytics and tracking",
                "typical_columns": ["user_id", "action", "timestamp", "metadata"]
            },
            "process_config": {
                "process_id": "USER_ACTIVITY_HOURLY",
                "process_name": "Hourly User Activity Processing",
                "source_system": "Web Application",
                "schedule": "Hourly",
                "enabled": True,
                "retry_count": 3,
                "timeout_minutes": 20
            },
            "feed_file_config": {
                "feed_id": "USER_ACTIVITY_JSON",
                "file_format": "JSON",
                "json_type": "array",
                "columns": [
                    {"name": "user_id", "type": "string", "nullable": False},
                    {"name": "action", "type": "string", "nullable": False},
                    {"name": "timestamp", "type": "timestamp", "nullable": False},
                    {"name": "metadata", "type": "json", "nullable": True}
                ]
            },
            "etl_steps": [
                {"step_id": 1, "step_name": "Parse Metadata", "step_type": "transformation", "action": "flatten_json"},
                {"step_id": 2, "step_name": "Sessionize", "step_type": "calculation", "formula": "session_id = generate_session_id(user_id, timestamp)"},
                {"step_id": 3, "step_name": "Aggregate by User", "step_type": "aggregation", "group_by": ["user_id", "action"]}
            ],
            "date_control": {
                "business_date_column": "timestamp",
                "date_format": "%Y-%m-%dT%H:%M:%S.%fZ",
                "timezone": "UTC"
            },
            "file_pattern": {
                "output_pattern": "user_activity_{business_date}_{hour}.json",
                "output_format": "JSON",
                "output_location": "s3://bucket/output/user_activity/"
            }
        }
    
    def _csv_sales_template(self) -> Dict:
        return {
            "metadata": {
                "name": "CSV Sales Data",
                "description": "Sales transactions and orders",
                "file_format": "CSV",
                "use_case": "Daily sales reporting",
                "typical_columns": ["order_id", "customer_id", "product_id", "amount", "order_date"]
            },
            "process_config": {
                "process_id": "SALES_DAILY",
                "process_name": "Daily Sales Processing",
                "source_system": "E-commerce Platform",
                "schedule": "Daily at 1 AM",
                "enabled": True,
                "retry_count": 3,
                "timeout_minutes": 45
            },
            "feed_file_config": {
                "feed_id": "SALES_CSV",
                "file_format": "CSV",
                "delimiter": ",",
                "header_row": True,
                "encoding": "utf-8",
                "columns": [
                    {"name": "order_id", "type": "string", "nullable": False, "primary_key": True},
                    {"name": "customer_id", "type": "string", "nullable": False},
                    {"name": "product_id", "type": "string", "nullable": False},
                    {"name": "amount", "type": "decimal", "nullable": False},
                    {"name": "order_date", "type": "timestamp", "nullable": False}
                ]
            },
            "etl_steps": [
                {"step_id": 1, "step_name": "Remove Duplicates", "step_type": "deduplication", "key_columns": ["order_id"]},
                {"step_id": 2, "step_name": "Validate Amount", "step_type": "validation", "rule": "amount > 0"},
                {"step_id": 3, "step_name": "Calculate Daily Revenue", "step_type": "aggregation", "group_by": ["order_date"]}
            ],
            "date_control": {
                "business_date_column": "order_date",
                "date_format": "%Y-%m-%d %H:%M:%S",
                "timezone": "UTC"
            },
            "file_pattern": {
                "output_pattern": "sales_{business_date}.csv",
                "output_format": "CSV",
                "output_location": "s3://bucket/output/sales/"
            }
        }
    
    def _xml_order_template(self) -> Dict:
        return {
            "metadata": {
                "name": "XML Order Data",
                "description": "Purchase orders from suppliers",
                "file_format": "XML",
                "use_case": "Supplier order management",
                "typical_columns": ["order_id", "supplier_id", "order_date", "total_amount"]
            },
            "process_config": {
                "process_id": "ORDER_BATCH",
                "process_name": "Batch Order Processing",
                "source_system": "Procurement System",
                "schedule": "Daily at 3 AM",
                "enabled": True,
                "retry_count": 3,
                "timeout_minutes": 40
            },
            "feed_file_config": {
                "feed_id": "ORDER_XML",
                "file_format": "XML",
                "root_element": "orders",
                "record_element": "order",
                "columns": [
                    {"name": "order_id", "type": "string", "nullable": False, "primary_key": True},
                    {"name": "supplier_id", "type": "string", "nullable": False},
                    {"name": "order_date", "type": "date", "nullable": False},
                    {"name": "total_amount", "type": "decimal", "nullable": False}
                ]
            },
            "etl_steps": [
                {"step_id": 1, "step_name": "Remove Duplicates", "step_type": "deduplication", "key_columns": ["order_id"]},
                {"step_id": 2, "step_name": "Validate Total", "step_type": "validation", "rule": "total_amount > 0"},
                {"step_id": 3, "step_name": "Aggregate by Supplier", "step_type": "aggregation", "group_by": ["supplier_id", "order_date"]}
            ],
            "date_control": {
                "business_date_column": "order_date",
                "date_format": "%Y-%m-%d",
                "timezone": "UTC"
            },
            "file_pattern": {
                "output_pattern": "orders_{business_date}.csv",
                "output_format": "CSV",
                "output_location": "s3://bucket/output/orders/"
            }
        }
    
    def _csv_employee_template(self) -> Dict:
        return {
            "metadata": {
                "name": "CSV Employee Data",
                "description": "Employee master data",
                "file_format": "CSV",
                "use_case": "HR data synchronization",
                "typical_columns": ["employee_id", "name", "department", "hire_date"]
            },
            "process_config": {
                "process_id": "EMPLOYEE_WEEKLY",
                "process_name": "Weekly Employee Sync",
                "source_system": "HR System",
                "schedule": "Weekly on Monday at 6 AM",
                "enabled": True,
                "retry_count": 2,
                "timeout_minutes": 30
            },
            "feed_file_config": {
                "feed_id": "EMPLOYEE_CSV",
                "file_format": "CSV",
                "delimiter": ",",
                "header_row": True,
                "encoding": "utf-8",
                "columns": [
                    {"name": "employee_id", "type": "string", "nullable": False, "primary_key": True},
                    {"name": "name", "type": "string", "nullable": False},
                    {"name": "department", "type": "string", "nullable": True},
                    {"name": "hire_date", "type": "date", "nullable": False}
                ]
            },
            "etl_steps": [
                {"step_id": 1, "step_name": "Remove Duplicates", "step_type": "deduplication", "key_columns": ["employee_id"]},
                {"step_id": 2, "step_name": "Standardize Names", "step_type": "transformation", "action": "title_case"},
                {"step_id": 3, "step_name": "Calculate Tenure", "step_type": "calculation", "formula": "tenure_years = (current_date - hire_date) / 365"}
            ],
            "date_control": {
                "business_date_column": "hire_date",
                "date_format": "%Y-%m-%d",
                "timezone": "UTC"
            },
            "file_pattern": {
                "output_pattern": "employees_{business_date}.csv",
                "output_format": "CSV",
                "output_location": "s3://bucket/output/employees/"
            }
        }
    
    def _json_iot_template(self) -> Dict:
        return {
            "metadata": {
                "name": "JSON IoT Sensor Data",
                "description": "IoT device sensor readings",
                "file_format": "JSON",
                "use_case": "IoT data ingestion and monitoring",
                "typical_columns": ["device_id", "sensor_type", "reading", "timestamp"]
            },
            "process_config": {
                "process_id": "IOT_REALTIME",
                "process_name": "Real-time IoT Data Processing",
                "source_system": "IoT Platform",
                "schedule": "Every minute",
                "enabled": True,
                "retry_count": 5,
                "timeout_minutes": 2
            },
            "feed_file_config": {
                "feed_id": "IOT_JSON",
                "file_format": "JSON",
                "json_type": "array",
                "columns": [
                    {"name": "device_id", "type": "string", "nullable": False},
                    {"name": "sensor_type", "type": "string", "nullable": False},
                    {"name": "reading", "type": "decimal", "nullable": False},
                    {"name": "timestamp", "type": "timestamp", "nullable": False}
                ]
            },
            "etl_steps": [
                {"step_id": 1, "step_name": "Validate Reading", "step_type": "validation", "rule": "reading IS NOT NULL"},
                {"step_id": 2, "step_name": "Detect Anomalies", "step_type": "calculation", "formula": "anomaly = reading > (avg + 3 * stddev)"},
                {"step_id": 3, "step_name": "Aggregate by Device", "step_type": "aggregation", "group_by": ["device_id", "sensor_type"]}
            ],
            "date_control": {
                "business_date_column": "timestamp",
                "date_format": "%Y-%m-%dT%H:%M:%S.%fZ",
                "timezone": "UTC"
            },
            "file_pattern": {
                "output_pattern": "iot_data_{business_date}_{timestamp}.json",
                "output_format": "JSON",
                "output_location": "s3://bucket/output/iot/"
            }
        }


# Convenience function
def get_template_library() -> TemplateLibrary:
    """Get the template library instance"""
    return TemplateLibrary()

# Convenience functions for direct access
_template_library = TemplateLibrary()

def get_template(template_id: str) -> Dict[str, Any]:
    """Get a specific template by ID"""
    return _template_library.get_template(template_id)

def list_templates() -> List[Dict[str, str]]:
    """List all available templates"""
    return _template_library.list_templates()
