import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from openai import AzureOpenAI

# ─────────────────────────────
# PAGE CONFIG
# ─────────────────────────────
st.set_page_config(page_title="DataMind AI", layout="wide")

# ─────────────────────────────
# LOAD SECRETS (FIXED)
# ─────────────────────────────
try:
    AZURE_ENDPOINT = st.secrets["MODEL_ENDPOINT"]
    API_KEY = st.secrets["AZURE_OPENAI_API_KEY"]
    MODEL_NAME = st.secrets["CHAT_MODEL_NAME"]
    API_VERSION = st.secrets.get("API_VERSION", "2024-02-15-preview")
except Exception:
    st.error("❌ Missing API configuration. Please set Streamlit secrets.")
    st.stop()

# ─────────────────────────────
# INIT CLIENT
# ─────────────────────────────
client = AzureOpenAI(
    api_key=API_KEY,
    azure_endpoint=AZURE_ENDPOINT,
    api_version=API_VERSION
)

# ─────────────────────────────
# UI HEADER
# ─────────────────────────────
st.title("📊 DataMind AI")
st.caption("Upload data → Ask questions → Get AI insights")

# ─────────────────────────────
# FILE UPLOAD
# ─────────────────────────────
uploaded_file = st.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

# ─────────────────────────────
# LLM DATA AGENT
# ─────────────────────────────
def data_agent_llm(query, df):
    sample = df.head(10).to_string()

    prompt = f"""
You are a data analyst.

Here is a dataset sample:
{sample}

User question:
{query}

Instructions:
- Provide clear insights
- Explain patterns if possible
- Suggest trends or observations
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,  # IMPORTANT: Azure deployment name
        messages=[
            {"role": "system", "content": "You are a helpful data analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


# ─────────────────────────────
# CHART GENERATOR
# ─────────────────────────────
def generate_chart(df):
    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) == 0:
        return None

    col = numeric_cols[0]

    fig, ax = plt.subplots()
    df[col].plot(kind="line", ax=ax)
    ax.set_title(f"{col} Trend")

    return fig


# ─────────────────────────────
# MAIN FLOW
# ─────────────────────────────
if uploaded_file:

    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        st.stop()

    st.success("✅ File uploaded successfully!")

    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    # USER QUERY
    query = st.text_input("Ask a question about your data:")

    if query:

        with st.spinner("🧠 Analyzing data..."):
            try:
                answer = data_agent_llm(query, df)
            except Exception as e:
                st.error(f"❌ AI Error: {e}")
                st.stop()

        st.subheader("🧠 AI Insight")
        st.write(answer)

        # AUTO CHART (simple logic)
        if any(word in query.lower() for word in ["chart", "plot", "trend"]):
            fig = generate_chart(df)
            if fig:
                st.subheader("📊 Chart")
                st.pyplot(fig)
            else:
                st.info("No numeric data available for chart.")
