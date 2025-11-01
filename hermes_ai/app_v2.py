"""
Hermes Config Generator v2.0 - With ETL Transformation Support
Enhanced with natural language ETL transformation specification
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os

# Import agents
from agents import (
    SchemaAnalyzerAgent,
    ConfigGeneratorAgent,
    ValidationAgent,
    OptimizationAgent,
    OrchestratorAgent
)
from etl_transformation_agent import ETLTransformationAgent
from templates import get_template, list_templates
from git_integration import GitIntegration

# Page config
st.set_page_config(
    page_title="Hermes Config Generator v2.0",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'generated_config' not in st.session_state:
    st.session_state.generated_config = None
if 'generated_etl' not in st.session_state:
    st.session_state.generated_etl = None
if 'generated_sql' not in st.session_state:
    st.session_state.generated_sql = None
if 'source_schema' not in st.session_state:
    st.session_state.source_schema = None
if 'agent_logs' not in st.session_state:
    st.session_state.agent_logs = []

# Title
st.title("🤖 Hermes Config Generator v2.0")
st.markdown("**AI-Powered Configuration & ETL Transformation Generator**")
st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📝 Generate Config", 
    "🔄 ETL Transformations", 
    "🤖 Agent Activity", 
    "📚 Templates",
    "ℹ️ Help"
])

# ===== TAB 1: Generate Config =====
with tab1:
    st.header("Step 1: Upload Source Data File")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload CSV or JSON file",
            type=['csv', 'json'],
            help="Upload a sample of your source data file"
        )
    
    with col2:
        st.markdown("**Or use sample data:**")
        use_sample = st.selectbox(
            "Select sample dataset",
            ["None", "Trades Sample (CSV)", "Market Prices (JSON)"]
        )
    
    # Determine which file to use
    file_to_process = None
    if uploaded_file:
        file_to_process = uploaded_file
        st.success(f"✅ Uploaded: {uploaded_file.name}")
    elif use_sample != "None":
        sample_files = {
            "Trades Sample (CSV)": "sample_data/trades_sample.csv",
            "Market Prices (JSON)": "sample_data/market_prices_sample.json"
        }
        file_path = sample_files[use_sample]
        if os.path.exists(file_path):
            file_to_process = file_path
            st.info(f"📂 Using sample: {use_sample}")
    
    st.markdown("---")
    st.header("Step 2: Enter Feed Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        process_id = st.text_input(
            "Process ID *",
            value="HERMES_FEED_001",
            help="Unique identifier for this data feed"
        )
        
        feed_name = st.text_input(
            "Feed Name *",
            value="Sample Data Feed",
            help="Descriptive name for the feed"
        )
        
        source_system = st.text_input(
            "Source System *",
            value="External System",
            help="Name of the source system providing the data"
        )
    
    with col2:
        target_table = st.text_input(
            "Target Table *",
            value="gold.processed_data",
            help="Destination table name (schema.table)"
        )
        
        business_owner = st.text_input(
            "Business Owner",
            value="Data Team",
            help="Team or person responsible for this feed"
        )
        
        frequency = st.selectbox(
            "Feed Frequency",
            ["Daily", "Hourly", "Weekly", "Monthly", "Real-time"]
        )
    
    st.markdown("---")
    
    # Generate button
    if st.button("🚀 Generate Configuration", type="primary", use_container_width=True):
        if not file_to_process:
            st.error("❌ Please upload a file or select a sample dataset")
        elif not process_id or not feed_name or not source_system or not target_table:
            st.error("❌ Please fill in all required fields (*)")
        else:
            with st.spinner("🤖 AI Agents are working..."):
                # Save uploaded file temporarily if needed
                if uploaded_file:
                    temp_path = f"/tmp/{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    file_to_process = temp_path
                
                # Create orchestrator
                orchestrator = OrchestratorAgent()
                
                # Feed details
                feed_details = {
                    "process_id": process_id,
                    "feed_name": feed_name,
                    "source_system": source_system,
                    "target_table": target_table,
                    "business_owner": business_owner,
                    "frequency": frequency
                }
                
                # Generate config
                result = orchestrator.orchestrate_config_generation(
                    file_path=file_to_process,
                    feed_details=feed_details
                )
                
                # Store results
                st.session_state.generated_config = result["config"]
                st.session_state.source_schema = result.get("schema")
                st.session_state.agent_logs = orchestrator.get_all_agent_logs()
                
                # Display results
                if result["status"] == "completed":
                    st.success("✅ Configuration Generated Successfully!")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Validation Score", f"{result['validation_score']}/100")
                    with col2:
                        st.metric("Processing Steps", result["steps_completed"])
                    with col3:
                        status_color = "🟢" if result["status"] == "completed" else "🔴"
                        st.metric("Status", f"{status_color} {result['status'].upper()}")
                else:
                    st.error(f"❌ Generation Failed: {result.get('error', 'Unknown error')}")
    
    # Display generated config
    if st.session_state.generated_config:
        st.markdown("---")
        st.header("Generated Configuration")
        
        # JSON viewer
        st.json(st.session_state.generated_config)
        
        # Download button
        config_json = json.dumps(st.session_state.generated_config, indent=2)
        st.download_button(
            label="📥 Download Configuration JSON",
            data=config_json,
            file_name=f"{process_id}_config.json",
            mime="application/json",
            use_container_width=True
        )

# ===== TAB 2: ETL Transformations =====
with tab2:
    st.header("🔄 ETL Transformation Specification")
    
    if not st.session_state.source_schema:
        st.warning("⚠️ Please generate a configuration first in the 'Generate Config' tab to analyze the source schema.")
    else:
        st.success("✅ Source schema loaded from previous step")
        
        # Display source schema summary
        with st.expander("📊 View Source Schema"):
            schema = st.session_state.source_schema
            st.write(f"**File Type:** {schema.get('file_type', 'N/A')}")
            st.write(f"**Columns:** {schema.get('column_count', 0)}")
            
            # Display columns in a table
            if 'columns' in schema:
                cols_df = pd.DataFrame(schema['columns'])
                st.dataframe(cols_df[['name', 'dtype', 'null_count', 'unique_count']], use_container_width=True)
        
        st.markdown("---")
        st.header("Describe Your ETL Transformations")
        
        st.markdown("""
        **Tell the AI what transformations you need in plain English.** Be as detailed as possible!
        
        **Examples:**
        - "Convert trade_date from string to date format, calculate total_amount as price * quantity, filter out records where status is 'CANCELLED'"
        - "Rename customer_id to client_id, convert all currency amounts from cents to dollars by dividing by 100, add a new column called processing_date with today's date"
        - "Join with reference_data table on product_id, aggregate by customer and date to get daily totals, exclude test accounts"
        """)
        
        # Large text area for transformation description
        transformation_desc = st.text_area(
            "Transformation Requirements (Plain English)",
            height=200,
            placeholder="Example: Convert trade_date to DATE format, calculate total_value as price * quantity, filter out cancelled trades, add a column for processing_timestamp with current timestamp...",
            help="Describe all the transformations, calculations, filters, joins, and data quality rules you need"
        )
        
        # Target table
        etl_target_table = st.text_input(
            "Target Table Name",
            value=st.session_state.generated_config.get("target_table", "gold.target_table") if st.session_state.generated_config else "gold.target_table",
            help="Name of the destination table (schema.table)"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Generate ETL Transformation JSON button
            if st.button("🔄 Generate ETL Transformation JSON", type="primary", use_container_width=True):
                if not transformation_desc.strip():
                    st.error("❌ Please describe your transformation requirements")
                else:
                    with st.spinner("🤖 ETL Transformation Agent is working..."):
                        # Create ETL agent
                        etl_agent = ETLTransformationAgent()
                        
                        # Generate transformation
                        etl_json = etl_agent.generate_etl_transformation(
                            source_schema=st.session_state.source_schema,
                            target_table=etl_target_table,
                            transformation_description=transformation_desc
                        )
                        
                        # Store result
                        st.session_state.generated_etl = etl_json
                        
                        # Add ETL agent logs to the agent logs dictionary
                        if not isinstance(st.session_state.agent_logs, dict):
                            st.session_state.agent_logs = {}
                        st.session_state.agent_logs["etl_transformation"] = etl_agent.get_memory()
                        
                        st.success("✅ ETL Transformation JSON Generated!")
        
        with col2:
            # Generate SQL button
            if st.button("📝 Generate Executable SQL", type="secondary", use_container_width=True, disabled=not st.session_state.generated_etl):
                if st.session_state.generated_etl:
                    with st.spinner("🤖 Generating SQL..."):
                        etl_agent = ETLTransformationAgent()
                        sql = etl_agent.generate_sql_from_transformation(st.session_state.generated_etl)
                        st.session_state.generated_sql = sql
                        st.success("✅ SQL Generated!")
        
        # Display generated ETL JSON
        if st.session_state.generated_etl:
            st.markdown("---")
            st.header("Generated ETL Transformation JSON")
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Column Mappings", len(st.session_state.generated_etl.get("column_mappings", [])))
            with col2:
                st.metric("Derived Columns", len(st.session_state.generated_etl.get("derived_columns", [])))
            with col3:
                st.metric("Filters", len(st.session_state.generated_etl.get("filter_conditions", [])))
            with col4:
                st.metric("Quality Rules", len(st.session_state.generated_etl.get("data_quality_rules", [])))
            
            # JSON viewer with tabs
            etl_tab1, etl_tab2, etl_tab3 = st.tabs(["📋 Full JSON", "🗺️ Column Mappings", "🔍 Quality Rules"])
            
            with etl_tab1:
                st.json(st.session_state.generated_etl)
            
            with etl_tab2:
                if "column_mappings" in st.session_state.generated_etl:
                    mappings_df = pd.DataFrame(st.session_state.generated_etl["column_mappings"])
                    st.dataframe(mappings_df, use_container_width=True)
            
            with etl_tab3:
                if "data_quality_rules" in st.session_state.generated_etl:
                    rules_df = pd.DataFrame(st.session_state.generated_etl["data_quality_rules"])
                    st.dataframe(rules_df, use_container_width=True)
            
            # Download ETL JSON
            etl_json_str = json.dumps(st.session_state.generated_etl, indent=2)
            st.download_button(
                label="📥 Download ETL Transformation JSON",
                data=etl_json_str,
                file_name=f"{etl_target_table.replace('.', '_')}_etl_transformation.json",
                mime="application/json",
                use_container_width=True
            )
        
        # Display generated SQL
        if st.session_state.generated_sql:
            st.markdown("---")
            st.header("Generated Executable SQL")
            
            st.code(st.session_state.generated_sql, language="sql")
            
            # Download SQL
            st.download_button(
                label="📥 Download SQL File",
                data=st.session_state.generated_sql,
                file_name=f"{etl_target_table.replace('.', '_')}_etl.sql",
                mime="text/plain",
                use_container_width=True
            )

# ===== TAB 3: Agent Activity =====
with tab3:
    st.header("🤖 Agent Activity Monitor")
    st.markdown("Real-time view of AI agent actions and decisions")
    
    if not st.session_state.agent_logs:
        st.info("No agent activity yet. Generate a configuration to see agents in action!")
    else:
        # Flatten agent logs from all agents
        all_logs = []
        for agent_name, logs in st.session_state.agent_logs.items():
            for log in logs:
                if isinstance(log, dict):
                    log_entry = log.copy()
                    log_entry['agent'] = agent_name
                    all_logs.append(log_entry)
                else:
                    # Handle case where log might be a string
                    all_logs.append({
                        'agent': agent_name,
                        'action': str(log),
                        'timestamp': 'N/A',
                        'result': {}
                    })
        
        # Sort by timestamp if available
        try:
            all_logs.sort(key=lambda x: x.get('timestamp', ''))
        except:
            pass  # If sorting fails, keep original order
        
        for i, log in enumerate(all_logs):
            agent_name = log.get('agent', 'Unknown Agent')
            action = log.get('action', 'Unknown Action')
            with st.expander(f"Step {i+1}: [{agent_name}] {action}", expanded=(i == len(all_logs) - 1)):
                st.write(f"**Agent:** {agent_name}")
                st.write(f"**Timestamp:** {log.get('timestamp', 'N/A')}")
                st.write(f"**Action:** {action}")
                
                result = log.get('result', {})
                if isinstance(result, dict):
                    if 'error' in result:
                        st.error(f"❌ Error: {result['error']}")
                    else:
                        st.json(result)
                else:
                    st.write(result)

# ===== TAB 4: Templates =====
with tab4:
    st.header("📚 Configuration Templates")
    st.markdown("Pre-built templates for common data feed patterns")
    
    templates = list_templates()
    
    for template_info in templates:
        template_name = template_info.get("name", template_info["id"])
        with st.expander(f"📄 {template_name}"):
            template = get_template(template_info["id"])
            st.json(template)
            
            # Download button
            template_json = json.dumps(template, indent=2)
            st.download_button(
                label=f"Download {template_name}",
                data=template_json,
                file_name=f"{template_info['id']}.json",
                mime="application/json",
                key=f"download_{template_info['id']}"
            )

# ===== TAB 5: Help =====
with tab5:
    st.header("ℹ️ Help & Documentation")
    
    st.markdown("""
    ## How to Use This Tool
    
    ### Step 1: Generate Configuration
    1. Upload your source data file (CSV or JSON) or use a sample
    2. Fill in the feed details (Process ID, Feed Name, etc.)
    3. Click "Generate Configuration"
    4. Download the generated JSON configuration
    
    ### Step 2: Define ETL Transformations
    1. After generating the configuration, go to the "ETL Transformations" tab
    2. Describe your transformation requirements in plain English
    3. Click "Generate ETL Transformation JSON"
    4. Review the generated transformation specification
    5. Click "Generate Executable SQL" to get the SQL code
    6. Download both the ETL JSON and SQL files
    
    ## What the AI Agents Do
    
    ### Configuration Generation Agents:
    - **Schema Analyzer**: Analyzes your file structure and data types
    - **Config Generator**: Uses GPT-4 to create the configuration
    - **Validator**: Validates the configuration and scores it
    - **Optimizer**: Suggests performance improvements
    - **Orchestrator**: Coordinates all agents
    
    ### ETL Transformation Agent:
    - Converts your plain English requirements into executable JSON
    - Generates column mappings, transformations, filters, and quality rules
    - Creates executable SQL from the transformation specification
    
    ## Tips for Best Results
    
    ### For Configuration Generation:
    - Use descriptive Process IDs and Feed Names
    - Provide accurate source system information
    - Specify the correct target table name
    
    ### For ETL Transformations:
    - Be specific about data type conversions
    - Mention all calculations and derived columns
    - Specify any filters or conditions
    - Include data quality requirements
    - Mention any joins with other tables
    
    ## Example Transformation Descriptions
    
    **Simple:**
    ```
    Convert trade_date to DATE format, calculate total as price * quantity
    ```
    
    **Medium:**
    ```
    Rename customer_id to client_id, convert amounts from cents to dollars,
    filter out test accounts, add processing_timestamp with current time
    ```
    
    **Complex:**
    ```
    Convert trade_date from string to DATE, calculate total_value as price * quantity,
    add commission_amount as total_value * 0.02, filter out records where status = 'CANCELLED',
    join with reference_data on product_id to get product_name, aggregate by customer_id
    and trade_date to get daily totals, add data quality rule to reject null customer_ids
    ```
    
    ## Support
    
    For issues or questions, contact the Data Engineering team.
    """)

# Footer
st.markdown("---")
st.markdown("**Hermes Config Generator v2.0** | Powered by AI Agents | Built with ❤️ by the Data Team")
