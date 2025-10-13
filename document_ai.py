#!/usr/bin/env python
# coding: utf-8

# In[1]:


# src/document_ai.py
import os
from google.cloud import documentai_v1 as documentai

def process_document(file_path, project_id, location, processor_id):
    
    # Check credentials
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set. "
                               "Please configure your credentials.")

    # Create Document AI client
    client_options = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    # Create processor name
    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    # Read file content
    with open(file_path, "rb") as f:
        file_content = f.read()

    # Create raw document object (for PDF format)
    raw_document = documentai.RawDocument(content=file_content, mime_type="application/pdf")

    # Create process request
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    # Process and get result
    result = client.process_document(request=request)
    document = result.document
    return document

if __name__ == "__main__":
    # Check and load dotenv
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("python-dotenv not found. Environment variables could not be loaded from .env file.")
    
    # Example for testing 
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "data-ai-invoice-454117")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "eu")
    processor_id = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID", "1e0be339e088cbdc")
    
    # Test file path (change if necessary)
    test_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                            "notebooks", "sample_invoice.pdf")
    
    if os.path.exists(test_file):
        print(f"Processing test file: {test_file}")
        try:
            doc = process_document(test_file, project_id, location, processor_id)
            print("Processing successful!")
            print(f"Document text: {doc.text[:100]}...")
            print(f"Entity count: {len(doc.entities)}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"Test file not found: {test_file}")





