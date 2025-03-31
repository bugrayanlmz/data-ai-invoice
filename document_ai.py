#!/usr/bin/env python
# coding: utf-8

# In[1]:


# src/document_ai.py
import os
from google.cloud import documentai_v1 as documentai

def process_document(file_path, project_id, location, processor_id):
    """
    Belgeyi Google Cloud Document AI ile işleyip dönen document nesnesini geri verir.
    
    Parametreler:
        file_path (str): İşlenecek PDF dosyasının tam yolu
        project_id (str): Google Cloud proje ID'si
        location (str): İşlemcinin bulunduğu bölge (örn. "eu", "us")
        processor_id (str): Document AI işlemci ID'si
        
    Dönüş:
        document: İşlenmiş belge nesnesi
    """
    # Kimlik bilgilerini kontrol et
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS ortam değişkeni ayarlanmamış. "
                               "Lütfen kimlik bilgilerinizi ayarlayın.")

    # Document AI client'ı oluştur
    client_options = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    # İşlemci adını oluştur
    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    # Dosya içeriğini oku
    with open(file_path, "rb") as f:
        file_content = f.read()

    # Raw document nesnesi oluştur (PDF formatı için)
    raw_document = documentai.RawDocument(content=file_content, mime_type="application/pdf")

    # Process request oluşturma
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    # İşlem yap ve sonucu al
    result = client.process_document(request=request)
    document = result.document
    return document

if __name__ == "__main__":
    # Dotenv'i kontrol et ve yükle
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("python-dotenv bulunamadı. Ortam değişkenleri .env dosyasından yüklenemedi.")
    
    # Test için örnek 
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "data-ai-invoice-454117")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "eu")
    processor_id = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID", "1e0be339e088cbdc")
    
    # Test dosyası yolu (gerekirse değiştirin)
    test_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                            "notebooks", "sample_invoice.pdf")
    
    if os.path.exists(test_file):
        print(f"Test dosyası işleniyor: {test_file}")
        try:
            doc = process_document(test_file, project_id, location, processor_id)
            print("İşleme başarılı!")
            print(f"Document metni: {doc.text[:100]}...")
            print(f"Entity sayısı: {len(doc.entities)}")
        except Exception as e:
            print(f"Hata: {e}")
    else:
        print(f"Test dosyası bulunamadı: {test_file}")


# In[ ]:



