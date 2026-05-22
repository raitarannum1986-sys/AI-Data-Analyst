import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from openai import AzureOpenAI

st.set_page_config(page_title="DataMind AI", layout="wide")

# ─────────────────────────────
# 🔐 API CONFIG (NEW)
# ─────────────────────────────
with st.sidebar:
    st.markdown("### 🔐 API Configuration")

    use_custom = st.toggle("Use your own API")

    if use_custom:
        AZURE_ENDPOINT = st.text_input("Azure Endpoint")
        API_KEY = st.text_input("API Key", type="password")
        MODEL_NAME = st.text_input("Deployment Name")
        API_VERSION = st.text_input("API Version", value="2024-02-15-preview")
    else:
        try:
            AZURE_ENDPOINT = st.secrets["MODEL_ENDPOINT"]
            API_KEY = st.secrets["AZURE_OPENAI_API_KEY"]
            MODEL_NAME = st.secrets["CHAT_MODEL_NAME"]
            API_VERSION = st.secrets.get("API_VERSION", "2024-02-15-preview")
        except Exception:
            st.error("❌ Missing API configuration in secrets.")
            st.stop()

# Validation
if not AZURE_ENDPOINT or not API_KEY or not MODEL_NAME:
    st.warning("⚠️ Please provide API details to continue.")
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
# DATA AGENT
# ─────────────────────────────
def data_agent_llm(query, df):
    sample = df.head(10).to_string()

    prompt = f"""
You are a senior data analyst.

Dataset sample:
{sample}

User question:
{query}

Instructions:
- Provide structured insights
- Highlight trends
- Mention key observations
- Suggest insights clearly
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
# CHART
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

    st.markdown("### 💡 Try asking:")
    st.markdown("""
    - Show sales trend  
    - Which region performs best?  
    - Give key insights  
    - Compare revenue and profit  
    """)

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

        # Auto chart
        if any(word in query.lower() for word in ["trend", "chart", "plot"]):
            fig = generate_chart(df)
            if fig:
                st.subheader("📊 Chart")
                st.pyplot(fig)
            else:
                st.info("No numeric data available for chart.")
