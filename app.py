import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from openai import AzureOpenAI
import os

st.set_page_config(page_title="DataMind AI", layout="wide")

# ─────────────────────────────
# LOAD ENV (or use st.secrets)
# ─────────────────────────────
AZURE_ENDPOINT = st.secrets["MODEL_ENDPOINT"]
API_KEY = st.secrets["AZURE_OPENAI_API_KEY"]
MODEL_NAME = st.secrets["CHAT_MODEL_NAME"]
API_VERSION = st.secrets.get("API_VERSION", "2024-02-15-preview")

client = AzureOpenAI(
    api_key=API_KEY,
    azure_endpoint=AZURE_ENDPOINT,
    api_version=API_VERSION
)

# ─────────────────────────────
# UI
# ─────────────────────────────
st.title("📊 DataMind AI")
st.caption("AI-powered Data Analyst")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel",
    type=["csv", "xlsx"]
)

# ─────────────────────────────
# LLM DATA AGENT
# ─────────────────────────────
def data_agent_llm(query, df):

    # Limit data preview (important)
    sample = df.head(10).to_string()

    prompt = f"""
You are a data analyst.

Here is a dataset sample:
{sample}

User question:
{query}

Instructions:
- Answer clearly
- If analysis is needed, explain insights
- Suggest chart if relevant
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful data analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


# ─────────────────────────────
# SIMPLE CHART GENERATOR
# ─────────────────────────────
def generate_chart(df):
    num_cols = df.select_dtypes(include="number").columns

    if len(num_cols) == 0:
        return None

    col = num_cols[0]

    fig, ax = plt.subplots()
    df[col].plot(kind="line", ax=ax)
    ax.set_title(f"{col} Trend")

    return fig


# ─────────────────────────────
# MAIN FLOW
# ─────────────────────────────
if uploaded_file:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("File uploaded successfully!")

    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    query = st.text_input("Ask a question about your data:")

    if query:

        with st.spinner("Analyzing data..."):

            answer = data_agent_llm(query, df)

        st.subheader("🧠 AI Insight")
        st.write(answer)

        # Optional chart
        if "chart" in query.lower() or "trend" in query.lower():
            fig = generate_chart(df)
            if fig:
                st.subheader("📊 Chart")
                st.pyplot(fig)
