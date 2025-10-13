#!/usr/bin/env python
# coding: utf-8

# In[8]:


# src/streamlit_app.py

import os
import streamlit as st
import pandas as pd
import tempfile
import matplotlib.pyplot as plt

# Skip if dotenv is not installed
try:
    from dotenv import load_dotenv
    # Load .env file (if exists)
    load_dotenv()
    print("Environment variables loaded from .env file")
except ImportError:
    print("python-dotenv not found. Environment variables could not be loaded from .env file.")

# Fix relative import paths
try:
    # When running in Streamlit Cloud environment
    from document_ai import process_document
    from data_processing import extract_entities, clean_entities
except ImportError:
    # When running in local development environment
    try:
        from src.document_ai import process_document
        from src.data_processing import extract_entities, clean_entities
    except ImportError:
        # Last resort: try direct import
        import sys
        import os
        # Add module path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        if parent_dir not in sys.path:
            sys.path.append(parent_dir)
        if current_dir not in sys.path:
            sys.path.append(current_dir)
        from document_ai import process_document
        from data_processing import extract_entities, clean_entities

# Page configuration
st.set_page_config(
    page_title="Invoice Analysis System",
    page_icon="📄",
    layout="wide"
)

# CSS stilleri
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #2c3e50;
        font-size: 2.5rem !important;
        padding-bottom: 2rem;
    }
    .stAlert {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .upload-section {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 1rem;
        margin: 1rem 0;
    }
    .results-section {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Check environment variable
credential_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not credential_path:
    # Use secrets for Streamlit Cloud
    import tempfile
    
    # Check credentials from Streamlit secrets
    if hasattr(st, "secrets") and "google_credentials" in st.secrets:
        # Write credentials defined as secrets in Streamlit Cloud to temporary file
        credentials_content = st.secrets["google_credentials"]
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp:
            temp.write(credentials_content)
            credential_path = temp.name
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path
            st.sidebar.success("✅ Google credentials loaded from secrets")
    else:
        st.sidebar.error("❌ Google credentials not found! Please configure Streamlit secrets or environment variables.")
        st.stop()
else:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path

# Google Cloud project information - get from secrets or env
project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
if not project_id and hasattr(st, "secrets") and "google_cloud_project_id" in st.secrets:
    project_id = st.secrets["google_cloud_project_id"]
else:
    # Default value
    project_id = "data-ai-invoice-454117"

location = os.getenv("GOOGLE_CLOUD_LOCATION")
if not location and hasattr(st, "secrets") and "google_cloud_location" in st.secrets:
    location = st.secrets["google_cloud_location"]
else:
    # Default value
    location = "eu"

processor_id = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID")
if not processor_id and hasattr(st, "secrets") and "google_document_ai_processor_id" in st.secrets:
    processor_id = st.secrets["google_document_ai_processor_id"]
else:
    # Default value
    processor_id = "1e0be339e088cbdc"

# Main title
st.title("📄 Invoice/Receipt Automatic Data Extraction and Analysis")

# Sidebar information
with st.sidebar:
    st.header("ℹ️ Information")
    st.info("""
    This application automatically analyzes your invoices and extracts important information.
    
    Supported formats:
    - PDF
    
    Processing steps:
    1. Upload your invoice
    2. The system automatically analyzes it
    3. View the results
    """)

# Main content
col1, col2 = st.columns([1, 2])

with col1:

    st.subheader("📤 File Upload")
    uploaded_file = st.file_uploader("Drag and drop your PDF file here or select", type=["pdf"])
    if uploaded_file:
        st.success("✅ File uploaded successfully!")
    st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    with st.spinner("🔄 Processing file..."):
        file_content = uploaded_file.read()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        
        try:
            document = process_document(
                file_path=temp_file_path,
                project_id=project_id,
                location=location,
                processor_id=processor_id
            )
            
            # Process entity data
            df_entities = extract_entities(document)
            df_clean = clean_entities(df_entities)
            

            st.subheader("📊 Analysis Results")
            
            # Display key information
            cols = st.columns(3)
            with cols[0]:
                st.metric("Total Entity Count", len(df_clean))
            with cols[1]:
                st.metric("Unique Entity Types", df_clean["Entity Type"].nunique())
            with cols[2]:
                st.metric("Confidence Score (Avg.)", f"{df_clean['Confidence Score'].mean():.2%}")
            
            # Entity table
            st.subheader("📋 Detected Information")
            try:
                # Try showing dataframe with gradient
                st.dataframe(
                    df_clean.style.background_gradient(subset=['Confidence Score'], cmap='YlGn'),
                    use_container_width=True
                )
            except Exception as e:
                # Show normal dataframe in case of error
                st.warning(f"An error occurred while styling the table: {str(e)}")
                st.dataframe(df_clean, use_container_width=True)
            
            # Visualizations
            st.subheader("📈 Entity Distribution")
            entity_counts = df_clean["Entity Type"].value_counts()
            
            col3, col4 = st.columns(2)
            with col3:
                st.bar_chart(entity_counts)
            with col4:
                # Create manual pie chart
                fig, ax = plt.subplots()
                ax.pie(entity_counts.values, labels=entity_counts.index, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')  # Ensures the pie chart is circular
                st.pyplot(fig)
            
            # Raw text
            with st.expander("📝 Raw Text"):
                st.text(document.text)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.error("Please check your file and try again.")





