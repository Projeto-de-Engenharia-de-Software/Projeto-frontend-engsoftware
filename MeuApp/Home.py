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


st.title("Bem Vindo a NEXUS ")
st.write("Bem-vindo ao aplicativo Nexus!")

st.write("Use o menu lateral para navegar entre as páginas.")


if st.button("Não possuí cadastro?"):
   st.switch_page("2_Cadastrar")
