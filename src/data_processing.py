#!/usr/bin/env python
# coding: utf-8

# In[2]:


# src/data_processing.py

import pandas as pd

def extract_entities(document):
    """
    Document AI tarafından işlenen belge nesnesindeki entity'leri çekip,
    bir pandas DataFrame'ine dönüştürür.
    
    Parametre:
      document: Document AI'den dönen işlenmiş belge nesnesi
      
    Dönüş:
      df: Entity'leri içeren pandas DataFrame'i
    """
    data = []
    for entity in document.entities:
        data.append({
            "Entity Türü": entity.type_,
            "Metin": entity.mention_text,
            "Güven Skoru": entity.confidence
        })
    
    # DataFrame oluşturma
    df = pd.DataFrame(data)
    return df

def clean_entities(df):
    """
    Basit veri temizleme işlemlerini gerçekleştirir.
    Örneğin, boş değerlerin kontrolü veya metin üzerinde düzenlemeler yapabilirsiniz.
    
    Parametre:
      df: Entity'leri içeren DataFrame
      
    Dönüş:
      df_clean: Temizlenmiş DataFrame
    """
    # Örnek: Güven skoru 0 olan satırları filtrele
    df_clean = df[df["Güven Skoru"] > 0]
    # Metin sütununu strip ile temizleme (başındaki/sonundaki boşlukları kaldırma)
    df_clean["Metin"] = df_clean["Metin"].str.strip()
    return df_clean

if __name__ == "__main__":
    # Burada test amaçlı örnek bir document nesnesi ile çalışabilirsiniz.
    # Örneğin, document_ai.py'den aldığınız işlenmiş belge nesnesini burada import edebilirsiniz:
    #
    # from document_ai import process_document
    # document = process_document("notebooks/sample_invoice.pdf", "your-project-id", "eu", "your-processor-id")
    # df_entities = extract_entities(document)
    # df_clean = clean_entities(df_entities)
    # print(df_clean.head())
    
    pass


# In[ ]:



