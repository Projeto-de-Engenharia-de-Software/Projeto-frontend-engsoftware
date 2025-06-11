import streamlit as st
import requests
import json

# Configurações da API
API_BASE_URL = "http://127.0.0.1:8000/api/" 

def make_authenticated_request(method, url, headers=None, params=None, json_data=None):
    if 'auth_token' not in st.session_state:
        return None # Não há token, a requisição não será autenticada
    
    auth_headers = {
        "Authorization": f"Token {st.session_state.auth_token}",
        "Content-Type": "application/json"
    }
    if headers: # Mescla com headers adicionais se houver
        auth_headers.update(headers)

    try:
        if method.lower() == 'get':
            response = requests.get(url, headers=auth_headers, params=params)
        elif method.lower() == 'post':
            response = requests.post(url, headers=auth_headers, json=json_data)
        # ... outras requisições (put, delete) ...

        response.raise_for_status() # Lança erro para status 4xx/5xx
        return response
    except requests.exceptions.RequestException as e:
        st.error(f"Erro na requisição API: {e}")
        return None

def registrar_usuario(data):
    try:
        # A API de registro não precisa de autenticação inicial
        response = requests.post(f"{API_BASE_URL}register/", json=data) 
        response.raise_for_status() # Lança erro para status 4xx/5xx

        st.rerun() # Recarrega a página
    except requests.exceptions.RequestException as e:
        error_message = "Erro no cadastro. Por favor, tente novamente."
        if response is not None:
            try:
                error_details = response.json()
                for field, errors in error_details.items():
                    error_message += f"\n- {field}: {', '.join(errors)}"
            except json.JSONDecodeError:
                error_message += f"\nDetalhes: {response.text}"
        st.error(error_message)


# Oculta a barra lateral e menu padrão
st.set_page_config(page_title="Nexus, Cadastro", layout="centered", initial_sidebar_state="collapsed")

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
       section[data-testid="stSidebar"] {
        display: none !important;
    }

    div[data-testid="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0px !important;
        width: 0px !important;
        position: fixed !important;
        top: -100px !important;
        left: -100px !important;
        z-index: -9999 !important;
    }
    </style>
""", unsafe_allow_html=True)


# Exibe a imagem no topo (ondas vermelhas/azuis)
st.image("pages\image.png", use_container_width=True)

# Título principal
st.markdown('<div class="title">Nexus</div>', unsafe_allow_html=True)
st.subheader("Cadastro")

col1, col2= st.columns(2)
dados = {}

# Caixa de login
with st.container():
  
    email = col1.text_input("E-mail", placeholder="Digite seu e-mail")
    username = col1.text_input("Nome de Usuário", placeholder="Digite seu Nome de Usuário")
    senha = col1.text_input("Senha", type="password", placeholder="Digite sua senha")
    confirmar_senha = col1.text_input("Confirmar Senha", type= "password", placeholder="Confirme sua Senha")
    nome_completo = col2.text_input("Nome Completo", placeholder= "Digite seu Nome Completo")
    perfil = col2.selectbox(label="Perfil", options= ["Gestor de Saúde","Agente de Saúde"])
    unidade_de_saude = col2.text_input("Unidade de Saúde", placeholder= "Selecione sua Unidade de Saúde")
    especialidade = col2.text_input("Especialidade", placeholder="Digite a sua Especialidade")

    dados = {
        "username": username,
        "password": senha,
        "confirm_password": confirmar_senha,
        "full_name": nome_completo,
        "especialidade": especialidade,
        "unidade_de_saude": unidade_de_saude,
        "email": email,
        "perfil": perfil
        }


col1, col2, col3 = st.columns([1,2,3])

if col1.button("Cadastrar"):
    try: 
        registrar_usuario(dados)
        st.switch_page("pages/quadro_geral.py")
    except:
        st.warning('Corrija seus dados :)', icon="⚠️")
        
        

with col2:
    if st.button("Já Possui Cadastro?"):
         st.switch_page("pages/_login.py")

        