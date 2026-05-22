import streamlit as st
import pandas as pd

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="DataMind AI",
    page_icon="📊",
    layout="wide"
)

# =========================================
# SIDEBAR (API INPUT)
# =========================================
st.sidebar.header("🔐 API Configuration")

use_api = st.sidebar.toggle("Use your own API", value=True)

api_key = None

if use_api:
    api_key = st.sidebar.text_input(
        "Enter OpenAI API Key",
        type="password",
        placeholder="sk-xxxx..."
    )

    if api_key:
        st.sidebar.success("API key added ✅")
    else:
        st.sidebar.warning("Please enter API key")

# =========================================
# HEADER
# =========================================
st.title("📊 DataMind AI")
st.caption("Upload data → Ask questions → Get AI insights")

# =========================================
# FILE UPLOAD
# =========================================
uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

# =========================================
# AFTER UPLOAD
# =========================================
if uploaded_file:
    st.success("File uploaded successfully!")

    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.dataframe(df.head())

    # =========================================
    # USER QUERY
    # =========================================
    user_query = st.text_input("Ask a question about your data")

    # =========================================
    # GENERATE INSIGHT
    # =========================================
    if st.button("Generate Insight"):

        if not api_key:
            st.error("❌ Please enter your API key in sidebar")

        elif not user_query:
            st.warning("Please enter a question")

        else:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)

            with st.spinner("Analyzing your data..."):

                summary = df.describe(include="all").to_string()

                prompt = f"""
                You are a data analyst.

                Dataset summary:
                {summary}

                Question:
                {user_query}

                Give clear insights.
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )

                answer = response.choices[0].message.content

                st.success("Insight")
                st.write(answer)
