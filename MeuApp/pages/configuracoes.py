import streamlit as st



left, center, right = st.columns([3, 5, 2])


with center:
        st.title("Configurações")

nova_senha = st.text_input("Nova Senha")

confirmar_senha = st.text_input("Confirmar Nova Senha")

novo_user = st.text_input("Novo Usuário")

salvar_btn = st.button("Salvar")

homepage_btn = st.button("Homepage")


st.markdown("""
        <style>
        div.stButton > button {
            background-color: black;
            color: white;
            border-radius: 10px;
            height: 30px;
            width: 23%;
            font-size: 14px;
            font-color: white;
        }
            .stButton.active {
        background-color: blue !important;
        color: white !important;
    }
        </style>
    """, unsafe_allow_html=True)


