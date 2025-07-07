import streamlit as st

st.set_page_config(page_title="Nexus - Adicionar", layout="centered") 



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

st.title("Adicionar Membro para a Equipe")



col1, col2 = st.columns([2,2])

with col1:
    st.text_input("Nome de Usuário")
    
    

cl1, cl2, cl3, cl4 = st.columns([2,6,2,2])

with cl1:
    st.button("Adicionar")
    
with cl2:
    if st.button("Voltar"):
        st.switch_page("pages/equipes.py")