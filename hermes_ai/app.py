"""
Hermes Config Generator - Streamlit Frontend
LLM-powered agentic AI system for automatic JSON configuration generation
"""

import streamlit as st
import json
import os
from pathlib import Path
import pandas as pd
from agents import generate_hermes_config
import time

# Page configuration
st.set_page_config(
    page_title="Hermes Config Generator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1976D2;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🤖 Hermes Config Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Automatic JSON Configuration Generation</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/artificial-intelligence.png", width=80)
    st.title("About")
    st.info("""
    **Hermes Config Generator** uses advanced AI agents to automatically generate 
    JSON configurations for the Hermes data processing framework.
    
    **Features:**
    - 🔍 Schema Analysis
    - 🤖 LLM-Powered Generation
    - ✅ Automatic Validation
    - ⚡ Performance Optimization
    """)
    
    st.title("How It Works")
    st.markdown("""
    1. **Upload** your source data file
    2. **Provide** feed details
    3. **AI agents** analyze and generate config
    4. **Download** ready-to-use JSON
    """)
    
    st.title("Sample Data")
    st.markdown("""
    Try with our sample datasets:
    - 📊 Trade Data (CSV)
    - 💹 Market Prices (JSON)
    """)

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["📤 Generate Config", "🤖 Agent Activity", "📚 Templates", "ℹ️ Help"])

with tab1:
    st.header("Generate Configuration")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Step 1: Upload Source File")
        
        # File upload options
        upload_option = st.radio(
            "Choose data source:",
            ["Upload your file", "Use sample data"],
            horizontal=True
        )
        
        uploaded_file = None
        file_path = None
        file_type = None
        
        if upload_option == "Upload your file":
            uploaded_file = st.file_uploader(
                "Choose a CSV or JSON file",
                type=["csv", "json"],
                help="Upload your source data file for analysis"
            )
            
            if uploaded_file:
                # Save uploaded file
                file_path = f"/tmp/{uploaded_file.name}"
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                file_type = uploaded_file.name.split(".")[-1]
                st.success(f"✅ File uploaded: {uploaded_file.name}")
                
        else:
            # Sample data selection
            sample_files = {
                "Trade Data (CSV)": "/home/ubuntu/hermes_ai/sample_data/trades_sample.csv",
                "Market Prices (JSON)": "/home/ubuntu/hermes_ai/sample_data/market_prices_sample.json"
            }
            
            selected_sample = st.selectbox(
                "Select sample dataset:",
                list(sample_files.keys())
            )
            
            file_path = sample_files[selected_sample]
            file_type = "csv" if "CSV" in selected_sample else "json"
            st.info(f"📁 Using sample: {selected_sample}")
        
        # Show file preview
        if file_path and os.path.exists(file_path):
            st.subheader("File Preview")
            try:
                if file_type == "csv":
                    df = pd.read_csv(file_path, nrows=5)
                else:
                    df = pd.read_json(file_path, lines=False)
                    if isinstance(df, pd.Series):
                        df = df.to_frame()
                    df = df.head(5)
                
                st.dataframe(df, use_container_width=True)
                st.caption(f"Showing first 5 rows of {len(df.columns)} columns")
            except Exception as e:
                st.error(f"Error reading file: {e}")
        
        st.divider()
        
        st.subheader("Step 2: Provide Feed Details")
        
        feed_name = st.text_input(
            "Feed Name",
            value="Daily Trade Feed",
            help="Enter a descriptive name for this data feed"
        )
        
        source_system = st.text_input(
            "Source System",
            value="Trading Platform",
            help="Enter the name of the source system"
        )
        
        st.divider()
        
        # Generate button
        if st.button("🚀 Generate Configuration", type="primary", use_container_width=True):
            if not file_path:
                st.error("❌ Please upload a file or select sample data first")
            elif not feed_name or not source_system:
                st.error("❌ Please provide feed name and source system")
            else:
                # Show progress
                with st.spinner("🤖 AI Agents are working..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Simulate agent progress
                    status_text.text("🔍 Schema Analyzer Agent: Analyzing file structure...")
                    progress_bar.progress(25)
                    time.sleep(1)
                    
                    status_text.text("🤖 Config Generator Agent: Generating configuration with LLM...")
                    progress_bar.progress(50)
                    time.sleep(1)
                    
                    status_text.text("✅ Validation Agent: Validating configuration...")
                    progress_bar.progress(75)
                    time.sleep(1)
                    
                    status_text.text("⚡ Optimization Agent: Optimizing for performance...")
                    progress_bar.progress(90)
                    
                    # Generate config
                    try:
                        result = generate_hermes_config(
                            file_path=file_path,
                            file_type=file_type,
                            feed_name=feed_name,
                            source_system=source_system
                        )
                        
                        progress_bar.progress(100)
                        status_text.text("✅ Configuration generated successfully!")
                        
                        # Store in session state
                        st.session_state['result'] = result
                        st.session_state['generated'] = True
                        
                        time.sleep(0.5)
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error generating configuration: {e}")
                        progress_bar.empty()
                        status_text.empty()
    
    with col2:
        st.subheader("Quick Stats")
        
        if file_path and os.path.exists(file_path):
            try:
                if file_type == "csv":
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_json(file_path, lines=False)
                
                st.metric("Total Rows", f"{len(df):,}")
                st.metric("Total Columns", len(df.columns))
                st.metric("File Size", f"{os.path.getsize(file_path) / 1024:.1f} KB")
                
                # Data quality indicators
                st.subheader("Data Quality")
                null_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
                st.progress(max(0, 100 - null_pct) / 100)
                st.caption(f"Completeness: {100 - null_pct:.1f}%")
                
            except Exception as e:
                st.warning(f"Could not analyze file: {e}")
    
    # Show results if generated
    if st.session_state.get('generated', False):
        st.divider()
        st.header("✅ Configuration Generated Successfully!")
        
        result = st.session_state['result']
        
        # Validation score
        score = result.get('validation_score', 0)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Validation Score", f"{score}/100", 
                     delta="Excellent" if score >= 90 else "Good" if score >= 70 else "Needs Review")
        
        with col2:
            st.metric("Processing Steps", len(result.get('steps', [])))
        
        with col3:
            st.metric("Status", result.get('status', 'Unknown').upper())
        
        # Show final configuration
        st.subheader("Generated Configuration")
        
        final_config = result.get('final_config', {})
        
        # Pretty print JSON
        config_json = json.dumps(final_config, indent=2)
        st.code(config_json, language="json", line_numbers=True)
        
        # Download button
        st.download_button(
            label="📥 Download Configuration JSON",
            data=config_json,
            file_name=f"{feed_name.lower().replace(' ', '_')}_config.json",
            mime="application/json",
            type="primary",
            use_container_width=True
        )
        
        # Show validation details
        if result.get('steps'):
            validation_step = next((s for s in result['steps'] if s['name'] == 'Validation'), None)
            if validation_step:
                validation_output = validation_step.get('output', {})
                
                if validation_output.get('warnings'):
                    st.warning("⚠️ **Warnings:**")
                    for warning in validation_output['warnings']:
                        st.markdown(f"- {warning}")
                
                if validation_output.get('errors'):
                    st.error("❌ **Errors:**")
                    for error in validation_output['errors']:
                        st.markdown(f"- {error}")
        
        # Show optimization recommendations
        if 'optimization_recommendations' in final_config:
            st.subheader("⚡ Optimization Recommendations")
            for rec in final_config['optimization_recommendations']:
                st.info(f"💡 {rec}")

with tab2:
    st.header("🤖 Agent Activity Monitor")
    st.markdown("Real-time view of AI agent actions and decisions")
    
    if st.session_state.get('generated', False):
        result = st.session_state['result']
        
        # Show each step
        for step in result.get('steps', []):
            with st.expander(f"Step {step['step']}: {step['name']}", expanded=True):
                st.markdown(f"**Status:** {step['status'].upper()}")
                
                if step['name'] == 'Schema Analysis':
                    schema = step['output']
                    st.json(schema)
                
                elif step['name'] == 'Config Generation':
                    st.markdown("**LLM-Generated Configuration:**")
                    st.json(step['output'])
                
                elif step['name'] == 'Validation':
                    validation = step['output']
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Valid", "✅ Yes" if validation.get('valid') else "❌ No")
                    with col2:
                        st.metric("Score", f"{validation.get('score', 0)}/100")
                    
                    if validation.get('warnings'):
                        st.warning("Warnings: " + ", ".join(validation['warnings']))
                
                elif step['name'] == 'Optimization':
                    optimized = step['output']
                    if 'optimization' in optimized:
                        st.json(optimized['optimization'])
        
        # Agent memories
        st.subheader("Agent Memory Logs")
        memories = result.get('agent_memories', {})
        
        for agent_name, memory in memories.items():
            with st.expander(f"📝 {agent_name.replace('_', ' ').title()}"):
                for entry in memory:
                    st.markdown(f"**{entry['timestamp']}**")
                    st.json(entry)
    else:
        st.info("👆 Generate a configuration first to see agent activity")

with tab3:
    st.header("📚 Configuration Templates")
    st.markdown("Pre-built templates for common data patterns")
    
    templates = {
        "CSV Trade Data": {
            "description": "Standard CSV file with trade transactions",
            "use_case": "Daily trade files from trading systems",
            "file_format": "CSV",
            "typical_columns": ["trade_id", "symbol", "quantity", "price", "trade_date"]
        },
        "JSON Market Data": {
            "description": "JSON feed with market prices and volumes",
            "use_case": "Real-time or batch market data feeds",
            "file_format": "JSON",
            "typical_columns": ["symbol", "price", "volume", "timestamp"]
        },
        "Customer Data": {
            "description": "Customer information from CRM systems",
            "use_case": "Customer master data synchronization",
            "file_format": "CSV/JSON",
            "typical_columns": ["customer_id", "name", "email", "registration_date"]
        }
    }
    
    for template_name, template_info in templates.items():
        with st.expander(f"📄 {template_name}"):
            st.markdown(f"**Description:** {template_info['description']}")
            st.markdown(f"**Use Case:** {template_info['use_case']}")
            st.markdown(f"**File Format:** {template_info['file_format']}")
            st.markdown(f"**Typical Columns:** {', '.join(template_info['typical_columns'])}")

with tab4:
    st.header("ℹ️ Help & Documentation")
    
    st.subheader("What is Hermes Config Generator?")
    st.markdown("""
    Hermes Config Generator is an AI-powered tool that automatically generates JSON configuration 
    files for the Hermes data processing framework. It uses multiple specialized AI agents to:
    
    - **Analyze** your source data files
    - **Generate** complete configurations using LLM
    - **Validate** configurations for correctness
    - **Optimize** for performance and best practices
    """)
    
    st.subheader("How to Use")
    st.markdown("""
    1. **Upload your data file** (CSV or JSON) or select a sample dataset
    2. **Provide feed details** (feed name and source system)
    3. **Click Generate** and watch the AI agents work
    4. **Download** the generated JSON configuration
    5. **Deploy** to your Hermes framework
    """)
    
    st.subheader("AI Agents")
    st.markdown("""
    - **Schema Analyzer Agent**: Analyzes file structure and infers data types
    - **Config Generator Agent**: Uses LLM to generate comprehensive configurations
    - **Validation Agent**: Validates configurations for completeness and correctness
    - **Optimization Agent**: Suggests performance optimizations
    - **Orchestrator Agent**: Coordinates all agents and manages the workflow
    """)
    
    st.subheader("Supported File Types")
    st.markdown("""
    - **CSV**: Comma-separated values with headers
    - **JSON**: JSON arrays or objects
    - **More formats** coming soon (XML, Parquet, Avro)
    """)
    
    st.subheader("Configuration Sections")
    st.markdown("""
    Generated configurations include:
    - **Process Config**: Job scheduling and execution settings
    - **Feed File Config**: File format and column definitions
    - **ETL Steps**: Data transformation and validation steps
    - **Date Control**: Business date handling
    - **File Pattern**: Output file naming and location
    - **Optimization**: Performance tuning recommendations
    """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p><strong>Hermes Config Generator</strong> | Powered by AI Agents & LLM</p>
    <p>Built for Low-Hanging Fruit MVP #2 | 2025</p>
</div>
""", unsafe_allow_html=True)
