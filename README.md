# Fatura Veri Çıkarma ve Analiz Sistemi

Google Document AI kullanarak faturalardan otomatik veri çıkarma ve analiz yapan Streamlit tabanlı bir web uygulaması.

## Özellikler

- PDF formatındaki faturalardan otomatik veri çıkarma
- Çıkarılan verilerin tablo ve grafiklerle görselleştirilmesi
- Entity analizi ve dağılım grafikleri
- Güven skoru metrikleri
- Kullanıcı dostu arayüz

## Kurulum

### Gereksinimler

- Python 3.8+
- Google Cloud hesabı
- Document AI işlemcisi

### Paketleri Yükleme

```bash
pip install -r requirements.txt
```

### Ortam Değişkenleri

1. `.env.example` dosyasını `.env` olarak kopyalayın:

```bash
cp .env.example .env
```

2. `.env` dosyasını kendi bilgilerinizle düzenleyin
3. Google Cloud kimlik bilgilerini `credentials/` klasörüne yerleştirin

## Çalıştırma

### Doğrudan Streamlit ile Çalıştırma

```bash
streamlit run streamlit_app.py
```

## Notlar

- Google Document AI işlemcinizin doğru yapılandırıldığından emin olun
- Kimlik bilgilerinizi her zaman `.env` dosyasında saklayın ve bu dosyayı GitHub'a yüklemeyin
- Geniş belgeler için doküman işleme süresi daha uzun olabilir

## Streamlit Cloud Deployment

Bu uygulamayı Streamlit Cloud üzerinden deploy etmek için:

1. GitHub repository'nizi Streamlit Cloud'a bağlayın.
2. Servis hesabı kimlik bilgilerinizi Streamlit Cloud'da ayarlayın:

   - `.streamlit/secrets.toml.example` dosyasını `.streamlit/secrets.toml` olarak kopyalayın
   - Google Cloud servis hesabı JSON kimlik bilgilerinizi `google_credentials` değişkenine ekleyin
   - Diğer parametreleri (project_id, location, processor_id) kendi değerlerinizle güncelleyin

3. Streamlit Cloud'da app ayarlarından "Secrets" bölümüne gidin ve aşağıdaki formatta kimlik bilgilerinizi ekleyin:

```toml
google_credentials = '''
{
  "type": "service_account",
  "project_id": "your-project-id",
  ... (Servis hesabı JSON içeriğinin tamamı)
}
'''
google_cloud_project_id = "data-ai-invoice-454117"
google_cloud_location = "eu"
google_document_ai_processor_id = "1e0be339e088cbdc"
```

4. Google Cloud servis hesabınıza Document AI API ve Document AI için gerekli izinleri verdiğinizden emin olun.

5. **ÖNEMLİ**: Deploy sırasında "Main file path" olarak `streamlit_app.py` belirtin.
