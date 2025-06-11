import streamlit as st
st.set_page_config(page_title="Nexus - Login", layout="centered") 


# Aplica estilo customizado (CSS) - Mantenha este bloco ou mova-o para tema.py
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

st.image("pages/image.png", use_container_width=True) 
# Título principal
st.markdown('<div class="title">Recuperar Senha.</div>', unsafe_allow_html=True)
col1, col2, col3= st.columns(3)

# Caixa de login
with st.container():
  
    email = col1.text_input("E-mail", placeholder="Digite seu e-mail")
    nome_completo = col2.text_input("Nome Completo", placeholder= "Digite Seu Nome Completo")
    
    with col1:
        if st.button("Enviar"):
         st.switch_page("pages/_login.py")
 
    with col2:
        if st.button("Voltar"):
         st.switch_page("pages/_login.py")
 