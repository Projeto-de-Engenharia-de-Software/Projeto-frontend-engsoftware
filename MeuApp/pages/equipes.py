import pandas as pd
import streamlit as st

from pages import quadro_geral

st.set_page_config(page_title="Nexus - Equipes", layout="centered") 

st.markdown("""
    <style>
    body {
        font-family: 'sans-serif';
    }

    .title {
        font-size: 60px;
        font-weight: bold;
        text-align: center;
        margin-top: -30px;
        margin-bottom: 0;
    }

    .login-box {
        max-width: 400px;
        margin: auto;
        padding: 30px;
        background-color: white;
        border-radius: 10px;
        text-align: center;
    }


            section[data-testid="stSidebar"] {
        display: none !important;
    }

    /* Remove o botão de recolher/expandir a sidebar (☰) */
    div[data-testid="collapsedControl"] {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

if "nomes" not in st.session_state:
    st.session_state["nomes"] = quadro_geral.nomes

st.title("Equipes")
st.dataframe(st.session_state["nomes"])

col1, col2, col3, col4 = st.columns([3,3,4,2])

with col1:
   if st.button("Adicionar membro"):
       st.switch_page("pages/adicionar_membro.py")
with col2:
    if st.button("Remover membro"):
        st.switch_page("pages/remover_membro.py")
with col3:
    st.button("Gerenciar Permissões")
with col4:
    if st.button("Voltar"):
        st.switch_page("pages/quadro_geral.py")