import streamlit as st
import requests
import extra_streamlit_components as stx

# Configurações iniciais da página
st.set_page_config(page_title="Nexus - Login", layout="centered", initial_sidebar_state="collapsed")

cookie = stx.CookieManager()
API_BASE_URL = "http://54.209.29.198:8000/api/"

def validar_token(token):
    """
    Verifica se o token ainda é válido na API.
    Retorna True se válido, False caso contrário.
    """
    if not token:
        return False
    try:
        resp = requests.get(f"{API_BASE_URL}auth/check/", headers={"Authorization": f"Token {token}"})
        return resp.status_code == 200
    except requests.exceptions.RequestException:
        return False

def fazer_login(username, password):
    """
    Faz login na API. Se bem-sucedido, salva token na sessão e cookie.
    """
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
            # cookie de sessão: some ao fechar o navegador
            cookie.set("auth_token", token)
            st.switch_page("pages/quadro_geral.py")
        else:
            st.error("Token não recebido. Verifique a resposta da API.")
    except requests.exceptions.RequestException as e:
        try:
            error = response.json()
            st.error(f"Erro no login: {error.get('non_field_errors', ['Verifique usuário e senha.'])[0]}")
        except:
            st.error("Erro ao tentar se conectar. Verifique seu backend.")

# ===== CSS e Layout =====
st.markdown("""
    <style>
    body { font-family: 'sans-serif'; }
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
    section[data-testid="stSidebar"] { display: none !important; }
    div[data-testid="collapsedControl"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# Imagem e título
st.image("pages/image.png", use_container_width=True)
st.markdown('<div class="title">Nexus</div>', unsafe_allow_html=True)
st.subheader("Login")

# Verifica se já há token válido
token_cookie = cookie.get("auth_token")
if token_cookie and validar_token(token_cookie):
    st.session_state.auth_token = token_cookie
    st.switch_page("pages/quadro_geral.py")

# Campos de login
with st.container():
    username = st.text_input("Usuário", placeholder="Digite seu Usuário")
    senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")

col1, col2, col3 = st.columns([1, 2, 4])

# Botão Entrar
if col1.button("Entrar", key="btn_entrar_login"):
    if username and senha:
        fazer_login(username, senha)
    else:
        st.warning("Por favor, preencha usuário e senha.", icon="⚠️")

# Cadastro
with col2:
    if st.button("Não possui cadastro?", key="btn_cadastro_login"):
        st.switch_page("pages/_cadastrar.py")
