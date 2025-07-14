import streamlit as st
import requests, json

def make_authenticated_request(method, url, headers=None, params=None, json_data=None):

    if 'auth_token' not in st.session_state:

        return None 
    
    auth_headers = {

        "Authorization": f"Token {st.session_state.auth_token}",
        "Content-Type": "application/json"

    }

    if headers: 

        auth_headers.update(headers)

    try:

        if method.lower() == 'get':

            response = requests.get(url, headers=auth_headers, params=params)

        elif method.lower() == 'post':

            response = requests.post(url, headers=auth_headers, json=json_data)
        

        response.raise_for_status() 

        return response
    
    except requests.exceptions.RequestException as e:

        st.error(f"Erro na requisição API: {e}")

        return None
    
def fazer_login(username, password):

    login_url = f"{API_BASE_URL}auth/token/"

    try:

        response = requests.post(login_url, json={
            "username": username,
            "password": password   
        })

        response.raise_for_status()  

        token = response.json().get("token")

        if token:

            st.session_state.auth_token = token 
            st.switch_page("pages/quadro_geral.py")  

        else:

            st.error("Token não recebido. Verifique a resposta da API.")

        return True
    
    except requests.exceptions.RequestException as e:

        try:

            error = response.json()
            st.error(f"Erro no login: {error.get('non_field_errors', ['Verifique usuário e senha.'])[0]}")

        except:

            st.error("Erro ao tentar se conectar. Verifique seu backend.")

        return False

API_BASE_URL = "http://54.209.29.198:8000/api/" 

st.set_page_config(page_title="Nexus - Login", layout="centered", initial_sidebar_state="collapsed")

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

st.markdown('<div class="title">Nexus</div>', unsafe_allow_html=True)
st.subheader("Login")


with st.container():

    username = st.text_input("Usuário", placeholder="Digite seu Usuário")
    senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")

col1, col2, col3 = st.columns([1,2,4])



if col1.button("Entrar", key="btn_entrar_login"):

    sucesso = fazer_login(username,senha)

    if sucesso:

        st.success("Login realizado com sucesso!")
        

    else:

        st.warning("Corrija seus dados :)", icon="⚠️")

with col2:

    if st.button("Esqueci minha senha", key="btn_esqueci_login"):

        st.switch_page("pages/_recuperacao_senha.py")

with col3:
    
    if st.button("Não possui cadastro?", key="btn_cadastro_login"): 
     
        st.switch_page("pages/_cadastrar.py") 