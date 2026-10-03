# Invoice Data Extraction

A Python and Streamlit application that extracts structured information from PDF invoices using Google Cloud Document AI.

## Features

- Upload a PDF and inspect extracted entities and raw text.
- View confidence scores, summary metrics, and entity tables.
- Explore entity distributions with bar and pie charts.

Built with Streamlit, Google Cloud Document AI, Pandas, and Matplotlib.

## Run Locally

Requires Python, a Google Cloud project with the Document AI API enabled, an invoice processor, and service account credentials authorized to use it.

```bash
git clone https://github.com/bugrayanlmz/data-ai-invoice.git
cd data-ai-invoice
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

The activation command above is for macOS/Linux. Create a root `.env` file pointing to your service account JSON:

```env
GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/credentials.json
```

Create `.streamlit/secrets.toml` with your processor settings:

```toml
google_cloud_project_id = "your-project-id"
google_cloud_location = "eu"
google_document_ai_processor_id = "your-processor-id"
```

Set the location to your processor's region. Leave `GOOGLE_CLOUD_PROJECT_ID`, `GOOGLE_CLOUD_LOCATION`, and `GOOGLE_DOCUMENT_AI_PROCESSOR_ID` unset in your environment and `.env`: the current code replaces their values with hard-coded defaults when they are set. The Streamlit secrets configuration above avoids this issue.

```bash
streamlit run streamlit_app.py
```

Open the local URL printed by Streamlit and upload an invoice PDF. Keep credentials and secrets out of version control.
