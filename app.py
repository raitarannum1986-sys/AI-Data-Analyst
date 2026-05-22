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
# CUSTOM UI
# =========================================
st.markdown("""
<style>
.stApp {
    background-color: #0b1c17;
    color: white;
}

.title {
    font-size: 48px;
    font-weight: 700;
    text-align: center;
    color: #1de9b6;
}

.subtitle {
    text-align: center;
    color: #7bd3c6;
    margin-bottom: 30px;
}

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
# HEADER
# =========================================
st.markdown('<div class="title">📊 DataMind AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload → Ask → Get Insights</div>', unsafe_allow_html=True)

# =========================================
# SIDEBAR CONFIG
# =========================================
st.sidebar.header("🔐 API Configuration")

api_mode = st.sidebar.radio("Choose API", ["OpenAI", "Azure OpenAI"])

openai_key = None
azure_key = None
azure_endpoint = None
deployment_name = None

# -------- OpenAI --------
if api_mode == "OpenAI":
    openai_key = st.sidebar.text_input("OpenAI API Key", type="password")

    if openai_key:
        st.sidebar.success("OpenAI key added ✅")

# -------- Azure --------
else:
    azure_endpoint = st.sidebar.text_input("Azure Endpoint")
    azure_key = st.sidebar.text_input("Azure API Key", type="password")
    deployment_name = st.sidebar.text_input("Deployment Name")

    if azure_key and azure_endpoint and deployment_name:
        st.sidebar.success("Azure config added ✅")

# =========================================
# FILE UPLOAD
# =========================================
uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    st.success("File uploaded successfully!")

    # Read file
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.dataframe(df.head())

    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    # =========================================
    # USER INPUT
    # =========================================
    user_query = st.text_input("Ask a question about your data")

    # =========================================
    # GENERATE INSIGHT
    # =========================================
    if st.button("Generate Insight"):

        if not user_query:
            st.warning("Please enter a question")
            st.stop()

        # Prepare data summary
        summary = df.describe(include="all").to_string()

        prompt = f"""
        You are a data analyst.

        Dataset summary:
        {summary}

        Question:
        {user_query}

        Give clear, useful insights.
        """

        # =========================================
        # OPENAI FLOW
        # =========================================
        if api_mode == "OpenAI":

            if not openai_key:
                st.error("Please enter OpenAI API key")
                st.stop()

            try:
                from openai import OpenAI
                client = OpenAI(api_key=openai_key)

                with st.spinner("Analyzing..."):
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}]
                    )

                st.success("Insight")
                st.write(response.choices[0].message.content)

            except Exception as e:
                st.error(f"Error: {e}")

        # =========================================
        # AZURE FLOW
        # =========================================
        else:

            if not azure_key or not azure_endpoint or not deployment_name:
                st.error("Please fill all Azure details")
                st.stop()

            try:
                from openai import AzureOpenAI

                client = AzureOpenAI(
                    api_key=azure_key,
                    api_version="2024-02-15-preview",
                    azure_endpoint=azure_endpoint
                )

                with st.spinner("Analyzing..."):
                    response = client.chat.completions.create(
                        model=deployment_name,
                        messages=[{"role": "user", "content": prompt}]
                    )

                st.success("Insight")
                st.write(response.choices[0].message.content)

            except Exception as e:
                st.error(f"Azure Error: {e}")
