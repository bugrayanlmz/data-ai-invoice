#!/usr/bin/env python
# coding: utf-8

# In[8]:


# src/streamlit_app.py

import os
import streamlit as st
import pandas as pd
import tempfile
import matplotlib.pyplot as plt
import nbimporter

# Dotenv yüklü değilse atlayacak şekilde düzenleme
try:
    from dotenv import load_dotenv
    # .env dosyasını yükle (varsa)
    load_dotenv()
    print("Ortam değişkenleri .env dosyasından yüklendi")
except ImportError:
    print("python-dotenv bulunamadı. Ortam değişkenleri .env dosyasından yüklenemedi.")

from src.document_ai import process_document
from src.data_processing import extract_entities, clean_entities

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="Fatura Analiz Sistemi",
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

# Ortam değişkenini kontrol et
credential_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not credential_path:
    # Yedek yöntem
    default_path = "/Users/bugrayanlmz/Desktop/data-ai-project/data-ai-invoice/credentials/data-ai-invoice-454117-86bae93a14c4.json"
    st.sidebar.warning(f"⚠️ GOOGLE_APPLICATION_CREDENTIALS ortam değişkeni bulunamadı. Varsayılan kimlik dosyası kullanılıyor.")
    credential_path = default_path

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path

# Ana başlık
st.title("📄 Fatura/Makbuz Otomatik Veri Çıkarma ve Analizi")

# Sidebar bilgileri
with st.sidebar:
    st.header("ℹ️ Bilgi")
    st.info("""
    Bu uygulama, faturalarınızı otomatik olarak analiz eder ve önemli bilgileri çıkarır.
    
    Desteklenen formatlar:
    - PDF
    
    İşlem adımları:
    1. Faturanızı yükleyin
    2. Sistem otomatik olarak analiz eder
    3. Sonuçları görüntüleyin
    """)

# Ana içerik
col1, col2 = st.columns([1, 2])

with col1:

    st.subheader("📤 Dosya Yükleme")
    uploaded_file = st.file_uploader("PDF dosyanızı buraya sürükleyin veya seçin", type=["pdf"])
    if uploaded_file:
        st.success("✅ Dosya başarıyla yüklendi!")
    st.markdown('</div>', unsafe_allow_html=True)

# Google Cloud proje bilgileri
project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "data-ai-invoice-454117")
location = os.getenv("GOOGLE_CLOUD_LOCATION", "eu")
processor_id = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID", "1e0be339e088cbdc")

if uploaded_file is not None:
    with st.spinner("🔄 Dosya işleniyor..."):
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
            
            # Entity verilerini işle
            df_entities = extract_entities(document)
            df_clean = clean_entities(df_entities)
            

            st.subheader("📊 Analiz Sonuçları")
            
            # Önemli bilgileri göster
            cols = st.columns(3)
            with cols[0]:
                st.metric("Toplam Entity Sayısı", len(df_clean))
            with cols[1]:
                st.metric("Benzersiz Entity Türleri", df_clean["Entity Türü"].nunique())
            with cols[2]:
                st.metric("Güven Skoru (Ort.)", f"{df_clean['Güven Skoru'].mean():.2%}")
            
            # Entity tablosu
            st.subheader("📋 Tespit Edilen Bilgiler")
            try:
                # Gradient ile dataframe gösterimi dene
                st.dataframe(
                    df_clean.style.background_gradient(subset=['Güven Skoru'], cmap='YlGn'),
                    use_container_width=True
                )
            except Exception as e:
                # Hata durumunda normal dataframe göster
                st.warning(f"Tabloyu stilize ederken bir hata oluştu: {str(e)}")
                st.dataframe(df_clean, use_container_width=True)
            
            # Görselleştirmeler
            st.subheader("📈 Entity Dağılımı")
            entity_counts = df_clean["Entity Türü"].value_counts()
            
            col3, col4 = st.columns(2)
            with col3:
                st.bar_chart(entity_counts)
            with col4:
                # Manuel pasta grafiği oluştur
                fig, ax = plt.subplots()
                ax.pie(entity_counts.values, labels=entity_counts.index, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')  # Pasta grafiğinin daire şeklinde olmasını sağlar
                st.pyplot(fig)
            
            # Ham metin
            with st.expander("📝 Ham Metin"):
                st.text(document.text)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Bir hata oluştu: {str(e)}")
            st.error("Lütfen dosyanızı kontrol edip tekrar deneyin.")


# In[ ]:




