import streamlit as st

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="DataMind AI",
    page_icon="📊",
    layout="wide"
)

# =========================================
# FORCE FULL WIDTH + REMOVE DEFAULT PADDING
# =========================================
st.markdown("""
<style>

/* Remove default padding */
.block-container {
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* Background */
.stApp {
    background-color: #0b1c17;
    color: white;
}

/* Center everything */
.centered {
    text-align: center;
    margin-top: 60px;
}

/* Title */
.title {
    font-size: 60px;
    font-weight: 700;
    color: #1de9b6;
}

/* Subtitle */
.subtitle {
    font-size: 18px;
    color: #7bd3c6;
    margin-top: 10px;
}

/* Upload box styling */
[data-testid="stFileUploader"] {
    background-color: #132f2a;
    border-radius: 15px;
    padding: 30px;
}

/* Button styling */
.stButton > button {
    background-color: #1de9b6;
    color: black;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# HERO SECTION
# =========================================
st.markdown('<div class="centered">', unsafe_allow_html=True)

st.markdown('<div class="title">📊 DataMind AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload data → Ask questions → Get AI insights</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.write("")  # spacing

# =========================================
# FILE UPLOAD SECTION (CENTERED)
# =========================================
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    uploaded_file = st.file_uploader(
        "Upload CSV or Excel file",
        type=["csv", "xlsx"]
    )

# =========================================
# AFTER UPLOAD
# =========================================
if uploaded_file:
    st.success("File uploaded successfully!")

    st.text_input("Ask a question about your data")

    if st.button("Generate Insight"):
        st.info("Processing... (connect your LLM here)")
