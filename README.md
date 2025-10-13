# Invoice Data Extraction and Analysis System

A Streamlit-based web application for automatic data extraction and analysis from invoices using Google Document AI.

## Features

- Automatic data extraction from PDF invoices
- Visualization of extracted data with tables and charts
- Entity analysis and distribution graphs
- Confidence score metrics
- User-friendly interface

## Installation

### Requirements

- Python 3.8+
- Google Cloud account
- Document AI processor

### Installing Packages

```bash
pip install -r requirements.txt
```

### Environment Variables

1. Copy `.env.example` file as `.env`:

```bash
cp .env.example .env
```

2. Edit the `.env` file with your own information
3. Place your Google Cloud credentials in the `credentials/` folder

## Running the Application

### Running Directly with Streamlit

```bash
streamlit run streamlit_app.py
```

## Notes

- Make sure your Google Document AI processor is properly configured
- Always store your credentials in the `.env` file and do not upload this file to GitHub
- Document processing time may be longer for large documents

## Streamlit Cloud Deployment

To deploy this application on Streamlit Cloud:

1. Connect your GitHub repository to Streamlit Cloud.
2. Configure your service account credentials in Streamlit Cloud:

   - Copy `.streamlit/secrets.toml.example` file as `.streamlit/secrets.toml`
   - Add your Google Cloud service account JSON credentials to the `google_credentials` variable
   - Update other parameters (project_id, location, processor_id) with your own values

3. Go to the "Secrets" section in Streamlit Cloud app settings and add your credentials in the following format:

```toml
google_credentials = '''
{
  "type": "service_account",
  "project_id": "your-project-id",
  ... (Complete service account JSON content)
}
'''
google_cloud_project_id = "data-ai-invoice-454117"
google_cloud_location = "eu"
google_document_ai_processor_id = "1e0be339e088cbdc"
```

4. Make sure your Google Cloud service account has the necessary permissions for Document AI API.

5. **IMPORTANT**: Specify `streamlit_app.py` as the "Main file path" during deployment.
