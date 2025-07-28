import streamlit as st
from pages.util import API_BASE_URL, make_authenticated_request
from pages._login import cookie

st.set_page_config(page_title="Remover Membro", layout="centered", initial_sidebar_state="collapsed")

# Estilo customizado
st.markdown("""
    <style>
    body {
        font-family: 'sans-serif';
    }

    .title {
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        margin-top: -30px;
        margin-bottom: 20px;
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

    div[data-testid="collapsedControl"] {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Autenticação via cookie
token_cookie = cookie.get("auth_token")
if token_cookie and 'auth_token' not in st.session_state:
    st.session_state.auth_token = token_cookie

if 'auth_token' not in st.session_state:
    st.switch_page("pages/_login.py")

# Título
st.markdown("<div class='title'>Remover Membro</div>", unsafe_allow_html=True)

# Buscar equipes
response = make_authenticated_request("get", f"{API_BASE_URL}equipes/")
if response and response.status_code == 200:
    equipes = response.json()
    equipe_opcoes = {f"{eq['nome']} (ID {eq['id']})": eq for eq in equipes}

    equipe_selecionada = st.selectbox("Selecione a equipe", list(equipe_opcoes.keys()))
    equipe_dados = equipe_opcoes[equipe_selecionada]
    profissionais = [p['username'] for p in equipe_dados.get("profissionais", [])]

    if profissionais:
        username = st.text_input("Digite o nome de usuário a remover")

        col1, col2 = st.columns([1, 1])

        if 'modo_confirmar' not in st.session_state:
            st.session_state.modo_confirmar = False

        with col1:
            if st.button("Remover"):
                if username.strip() in profissionais:
                    st.session_state.modo_confirmar = True
                    st.session_state["confirm_delete"] = username
                else:
                    st.warning("Usuário não encontrado na equipe selecionada.")

        # Confirmação
        if st.session_state.get("modo_confirmar") and st.session_state.get("confirm_delete"):
            st.warning(f"Tem certeza que deseja remover '{st.session_state.confirm_delete}'?")
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Sim, remover"):
                    url = f"{API_BASE_URL}equipes/{equipe_dados['id']}/remover-profissional/"
                    body = {"username": st.session_state.confirm_delete}
                    post_response = make_authenticated_request("post", url, json_data=body)

                    if post_response and post_response.status_code in [200, 201]:
                        st.success(f"Usuário '{st.session_state.confirm_delete}' removido com sucesso!")
                    elif post_response and post_response.status_code == 400:
                        try:
                            erro = post_response.json()
                            if "username" in erro:
                                st.warning("Usuário não encontrado na equipe.")
                            else:
                                st.error(f"Erro: {erro}")
                        except Exception:
                            st.error("Erro ao remover o profissional.")
                    else:
                        st.error("Erro ao remover o profissional.")

                    # Limpa estado
                    st.session_state.modo_confirmar = False
                    del st.session_state["confirm_delete"]
                    st.rerun()
            with col2:
                if st.button("Cancelar"):
                    st.session_state.modo_confirmar = False
                    del st.session_state["confirm_delete"]
                    st.rerun()
    else:
        st.info("Esta equipe não possui profissionais para remover.")
else:
    st.error("Erro ao carregar equipes.")

st.divider()
if st.button("Voltar para Equipes"):
    st.session_state.page = "Equipes"
    st.switch_page("pages/quadro_geral.py")