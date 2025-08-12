import os, io, tempfile
import streamlit as st
from app.gobi_core import build_index, infer_paths_from_dir, retrieve, compose_answer
from app.emotion import detect_emotion, empathetic_prefix

st.set_page_config(page_title="GOBI", page_icon="🤖", layout="wide")
st.title("🤖 GOBI – Chatbot documental (MVP)")

# --- Sidebar: gestión de documentos
st.sidebar.header("📚 Documentos")
st.sidebar.write("Coloca PDFs/DOCX en `data/docs/` o súbelos aquí:")

uploaded = st.sidebar.file_uploader("Subir documentos", type=["pdf","docx","doc"], accept_multiple_files=True)
temp_paths = []
if uploaded:
    os.makedirs("data/docs", exist_ok=True)
    for up in uploaded:
        path = os.path.join("data/docs", up.name)
        with open(path, "wb") as f:
            f.write(up.read())
        temp_paths.append(path)
    st.sidebar.success(f"Guardados: {', '.join([os.path.basename(p) for p in temp_paths])}")

# --- Construcción de índice (cacheado)
@st.cache_resource(show_spinner=True)
def build_cached_index():
    paths = infer_paths_from_dir()
    return build_index(paths)

index = build_cached_index()

# --- Chat
if "history" not in st.session_state:
    st.session_state["history"] = []

with st.form("chat"):
    q = st.text_input("Escribe tu consulta (enter para enviar):")
    submitted = st.form_submit_button("Enviar")

if submitted and q.strip():
    emo = detect_emotion(q)
    hits = retrieve(q, index)
    result = compose_answer(q, hits)

    prefix = empathetic_prefix(emo)
    answer = prefix + result["answer"]
    st.session_state["history"].append(("Tú", q))
    st.session_state["history"].append(("Gobi", answer))

    # mostrar fuentes (links locales)
    st.markdown("**Fuentes:**")
    for s in result["sources"]:
        st.markdown(f"- [{s['name']}]({s['path']})")

# render historial
for who, msg in st.session_state["history"]:
    st.chat_message("user" if who=="Tú" else "assistant").write(msg)
