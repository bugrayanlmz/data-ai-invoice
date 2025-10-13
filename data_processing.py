#!/usr/bin/env python
# coding: utf-8

# In[2]:


# src/data_processing.py

import pandas as pd

def extract_entities(document):
    data = []
    for entity in document.entities:
        data.append({
            "Entity Type": entity.type_,
            "Text": entity.mention_text,
            "Confidence Score": entity.confidence
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    return df

def clean_entities(df):
    # Example: Filter rows with confidence score of 0
    df_clean = df[df["Confidence Score"] > 0]
    # Clean text column with strip (remove leading/trailing spaces)
    df_clean["Text"] = df_clean["Text"].str.strip()
    return df_clean

if __name__ == "__main__":

    
    pass
