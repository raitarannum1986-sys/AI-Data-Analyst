import streamlit as st

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="Care AI",
    page_icon="🩺",
    layout="wide"
)

# =========================================
# CUSTOM CSS (KEY PART)
# =========================================
st.markdown("""
<style>
body {
    background-color: #0b1c17;
    color: #e6f4f1;
}

.main {
    text-align: center;
}

.title {
    font-size: 48px;
    font-weight: 700;
    color: #1de9b6;
    margin-bottom: 10px;
}

.subtitle {
    font-size: 14px;
    letter-spacing: 2px;
    color: #7bd3c6;
    margin-bottom: 20px;
}

.desc {
    font-size: 16px;
    max-width: 700px;
    margin: auto;
    color: #b0cfc9;
    line-height: 1.6;
}

.chip {
    display: inline-block;
    padding: 10px 18px;
    margin: 8px;
    border-radius: 25px;
    background-color: #132f2a;
    color: #8fe3d4;
    font-size: 14px;
}

.footer {
    margin-top: 40px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# HERO SECTION
# =========================================
st.markdown('<div class="main">', unsafe_allow_html=True)

st.markdown('<div class="title">Care AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">HEALTHCARE & NUTRITION ASSISTANT</div>', unsafe_allow_html=True)

st.markdown("""
<div class="desc">
Your personalised AI health companion — get science-backed nutritional guidance 
tailored to your health goals, conditions, and lifestyle on a weekly, monthly, 
and quarterly basis.
</div>
""", unsafe_allow_html=True)

# =========================================
# FEATURES (CHIPS)
# =========================================
st.markdown("""
<div>
<span class="chip">● Weekly Plans</span>
<span class="chip">● Monthly Roadmaps</span>
<span class="chip">● Quarterly Goals</span>
<span class="chip">● Health Profiling</span>
<span class="chip">● Macro Insights</span>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# AUTH SECTION
# =========================================
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Sign In")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        st.success("Logged in successfully (dummy)")

with col2:
    st.subheader("Create Account")
    new_email = st.text_input("New Email")
    new_password = st.text_input("New Password", type="password")
    if st.button("Sign Up"):
        st.success("Account created (dummy)")

# =========================================
# FOOTER
# =========================================
st.markdown('<div class="footer">Built with ❤️ using Streamlit</div>', unsafe_allow_html=True)
