#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
VS Code için başlatma dosyası
"""

import os
import subprocess
import sys

def main():
    """Streamlit uygulamasını başlatır"""
    print("Fatura Analiz Uygulaması başlatılıyor...")
    
    # Uygulama yolu
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "streamlit_app.py")
    
    # Streamlit uygulamasını başlat
    subprocess.run([sys.executable, "-m", "streamlit", "run", app_path])

if __name__ == "__main__":
    main() 