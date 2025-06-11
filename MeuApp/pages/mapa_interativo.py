import streamlit as st

st.title("Mapa Interativo")

st.markdown("""
<style>
    div[data-testid="stSidebarNav"] ul li a[href*="_login.py"],
    div[data-testid="stSidebarNav"] ul li a[href*="_cadastrar.py"],
            div[data-testid="stSidebarNav"] ul li a[href*="Home.py"] {
        display: none !important;
    }
    
    div[data-testid="stSidebarNav"] ul li:nth-child(2),
    div[data-testid="stSidebarNav"] ul li:nth-child(4),
            div[data-testid="stSidebarNav"] ul li:nth-child(1) {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

homepage_btn = st.button("Homepage")
if homepage_btn:
      st.switch_page("pages/_homepage.py")