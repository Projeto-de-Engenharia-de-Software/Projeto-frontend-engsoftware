import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from tema import aplicar_tema

# Oculta a barra lateral e menu padrão
st.set_page_config(page_title="Nexus", layout="centered")
aplicar_tema()
# Aplica estilo customizado (CSS)
st.markdown("""
    <style>
    body {
        background-color: white;
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

    .btn-login {
        background-color: black;
        color: white;
        padding: 10px 30px;
        margin: 10px 5px;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        cursor: pointer;
    }

    .btn-login:hover {
        background-color: #333;
    }

    </style>
""", unsafe_allow_html=True)


# Exibe a imagem no topo (ondas vermelhas/azuis)
st.image(r"C:\Users\ruang\Documents\aplicativos\NexusFrontEnd\MeuApp\pages\image.png", use_container_width=True)

# Título principal
st.markdown('<div class="title">Nexus</div>', unsafe_allow_html=True)
st.subheader("Cadastro")

col1, col2= st.columns(2)

# Caixa de login
with st.container():
  
    
    email = col1.text_input("E-mail", placeholder="Digite seu e-mail")
    senha = col1.text_input("Senha", type="password", placeholder="Digite sua senha")
    confirmar_senha = col1.text_input("Confirmar Senha", type= "password", placeholder="Confirme sua Senha")
    nome_completo = col2.text_input("Nome Completo", placeholder= "Digite Seu Nome Completo")
    Especialidade = col2.selectbox(label="Gestor", options= ["Gestor de Saúde","Agente de Saúde"])
    unidade_de_saude = col2.text_input("Unidade de Saúde", placeholder= "Selecione sua Unidade de Saúde")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Cadastrar"):
        st.switch_page("")
with col1:
    if st.button("Ja Possui Cadastro?"):
        st.warning("Redirecionar para Login")
        # lógica de recuperação...
