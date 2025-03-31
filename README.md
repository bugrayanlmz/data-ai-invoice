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

### VS Code'da Çalıştırma

VS Code'da projeyi açtıktan sonra, ana dizindeki `run_app.py` dosyasını çalıştırın:

```bash
python run_app.py
```

### Jupyter Notebook'tan Çalıştırma

Jupyter Notebook kullanıcıları için, `src/` klasöründeki `.ipynb` dosyaları kullanılabilir.

```bash
jupyter notebook src/streamlit_app.ipynb
```

## Jupyter Notebook ve VS Code Arası Geçiş

Bu proje hem Jupyter Notebook hem de düz Python dosyaları olarak çalışabilir.

- `.ipynb` dosyalarını `.py` dosyalarına dönüştürmek için:

  ```bash
  jupyter nbconvert --to python dosya_adi.ipynb
  ```

- VS Code'da Jupyter Notebook desteği için Python eklentisini yükleyin.

## Notlar

- Google Document AI işlemcinizin doğru yapılandırıldığından emin olun
- Kimlik bilgilerinizi her zaman `.env` dosyasında saklayın ve bu dosyayı GitHub'a yüklemeyin
- Geniş belgeler için doküman işleme süresi daha uzun olabilir
