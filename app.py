import streamlit as st
from openai import OpenAI

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="DataMind AI",
    page_icon="📊",
    layout="wide"
)

# =========================================
# LOAD OPENAI CLIENT
# =========================================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# =========================================
# CUSTOM CSS
# =========================================
st.markdown("""
<style>
.stApp {
    background-color: #0b1c17;
    color: white;
}

.title {
    font-size: 50px;
    font-weight: bold;
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
}
</style>
""", unsafe_allow_html=True)

# =========================================
# HEADER
# =========================================
st.markdown('<div class="title">📊 DataMind AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload data → Ask questions → Get AI insights</div>', unsafe_allow_html=True)

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
    import pandas as pd

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.write("Preview:")
    st.dataframe(df.head())

    # =========================================
    # USER QUERY
    # =========================================
    user_query = st.text_input("Ask a question about your data")

    # =========================================
    # GENERATE INSIGHT
    # =========================================
    if st.button("Generate Insight"):
        if not user_query:
            st.warning("Please enter a question first.")
        else:
            with st.spinner("Analyzing your data..."):

                # Convert dataframe summary (IMPORTANT)
                data_summary = df.describe(include="all").to_string()

                prompt = f"""
                You are a data analyst.

                Here is the dataset summary:
                {data_summary}

                User question:
                {user_query}

                Provide clear insights.
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )

                answer = response.choices[0].message.content

                st.success("Insight:")
                st.write(answer)
