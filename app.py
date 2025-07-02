
import streamlit as st
import docx
import openai
import pandas as pd

openai.api_key = st.secrets["OPENAI_API_KEY"]

def extract_paragraphs(uploaded_file):
    doc = docx.Document(uploaded_file)
    return [para.text.strip() for para in doc.paragraphs if para.text.strip()]

def translate_with_commentary(telugu, english_ref):
    prompt = f"""
    You are a spiritual translator following a strict 360° Rulebook.
    1. Preserve literal meaning
    2. Maintain spiritual and philosophical depth
    3. Use clear global spiritual language and Sanskrit formatting

    Compare the following Telugu and English Reference. Output:
    Column 3: Final global translation (literal + clear)
    Column 4: Commentary (glossary, diagnostics, insight)

    Telugu: {telugu}
    English Reference: {english_ref}

    Output:
    Column 3:
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    output = response.choices[0].message.content.split("Column 4:")
    return output[0].strip(), output[1].strip() if len(output) > 1 else ""

st.set_page_config(page_title="Spiritual Tablet Translator", layout="wide")
st.title("📖 Spiritual Tablet Translator Console")

col1, col2 = st.columns(2)
with col1:
    telugu_doc = st.file_uploader("📄 Upload Telugu Document", type=["docx"])
with col2:
    english_doc = st.file_uploader("📝 Upload English Notes Document", type=["docx"])

if telugu_doc and english_doc:
    telugu_paras = extract_paragraphs(telugu_doc)
    english_paras = extract_paragraphs(english_doc)
    max_len = max(len(telugu_paras), len(english_paras))
    data = []

    with st.spinner("🔄 Translating..."):
        for i in range(max_len):
            telugu_text = telugu_paras[i] if i < len(telugu_paras) else ""
            english_text = english_paras[i] if i < len(english_paras) else ""
            col3, col4 = translate_with_commentary(telugu_text, english_text)
            data.append({
                "Telugu (C1)": telugu_text,
                "English Ref (C2)": english_text,
                "GPT Translation (C3)": col3,
                "Commentary (C4)": col4
            })

    df = pd.DataFrame(data)
    st.success("✅ Translation Complete!")
    st.dataframe(df, use_container_width=True)
    st.download_button("⬇️ Download Excel", df.to_excel(index=False), "Spiritual_Tablet_4_Column.xlsx")
