Este repositorio fue hecho para razones de estudio. Si algún usario desea utilizarlo y tiene sugerencias para mejorar la aplicación y/o sus funciones, puede contactarme a mi correo "rommel.solisb23@gmail.com".
Muchas gracias por el apoyo.

# GOBI – Chatbot documental (MVP)

Lee PDFs/DOCX locales, busca con TF-IDF, responde con límite de 300 palabras y lista fuentes.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
mkdir -p data/docs
# coloca aquí tus PDFs/DOCX
streamlit run app/main.py
