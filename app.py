
import streamlit as st

st.set_page_config(page_title="Spiritual Translator", layout="wide")

st.title("🧘‍♂️ 360° Spiritual Translator Console")

st.markdown("Upload documents and compare translations across 4 columns.")

uploaded_file = st.file_uploader("Upload your document (TXT or DOCX)", type=["txt", "docx"])

if uploaded_file:
    st.success("File uploaded. Translation preview not yet implemented in this version.")
