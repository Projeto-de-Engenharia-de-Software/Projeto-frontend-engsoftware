import streamlit as st
import pandas as pd

st.set_page_config(page_title="Remover Membro", layout="centered")

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

st.title("Remover Membro")

if "nomes" not in st.session_state:
    st.error("Dados de membros não encontrados.")
    st.stop()

nomes = st.session_state["nomes"]

usuario = st.text_input("Digite o nome de usuário para remover")

col1, col2 = st.columns([2,2])

if 'modo_confirmar' not in st.session_state:
    st.session_state.modo_confirmar = False


with col1:
    if st.button("Remover"):
        st.session_state.modo_confirmar = True
        if usuario in nomes["Usuário"].values:
            st.session_state["confirm_delete"] = usuario
        else:
            st.warning("Usuário não encontrado.")

with col2:
    if st.button("Voltar"):
        st.switch_page("pages/equipes.py")



if "confirm_delete" in st.session_state:
    st.warning(f"Tem certeza que deseja excluir '{st.session_state.confirm_delete}'?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Sim, excluir"):
            df = st.session_state["nomes"]
            df = df[df["Usuário"] != st.session_state["confirm_delete"]]
            st.session_state["nomes"] = df
            st.session_state.nomes = df
            st.success(f"Usuário '{st.session_state.confirm_delete}' removido.")
            del st.session_state["confirm_delete"]
            st.session_state.modo_confirmar = False
            st.rerun()
    with col2:
        if st.button("❌ Cancelar"):
            del st.session_state["confirm_delete"]
            st.session_state.modo_confirmar = False
            st.rerun()
                