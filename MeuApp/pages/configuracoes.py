import streamlit as st
from pages.util import make_authenticated_request, API_BASE_URL

def config():
    st.title("Configurações")

    st.subheader("Alterar Senha")

    old_password = st.text_input("Senha Atual", type="password")
    new_password = st.text_input("Nova Senha", type="password")
    confirm_new_password = st.text_input("Confirmar Nova Senha", type="password")

    #st.subheader("Alterar Nome de Usuário")
    #novo_user = st.text_input("Novo Usuário")  # Ainda não implementado

    salvar_btn = st.button("Salvar")
    logout_btn = st.button("Fazer Logoff")

    if logout_btn:
        st.session_state.auth_token = False
        st.cache_data.clear()
        st.switch_page("pages/_login.py")
        st.rerun()

    if salvar_btn:
        if not all([old_password, new_password, confirm_new_password]):
            st.warning("Preencha todos os campos de senha.")
            return

        if new_password != confirm_new_password:
            st.warning("As senhas novas não coincidem.")
            return

        payload = {
            "old_password": old_password,
            "new_password": new_password,
            "confirm_new_password": confirm_new_password
        }

        response = make_authenticated_request(
            method="put",
            url=f"{API_BASE_URL}profile/change-password/",
            json_data=payload
        )

        if response is None:
            st.error("Falha na requisição. Sem resposta da API.")
            return

        if response.status_code == 200:
            st.success("Senha alterada com sucesso!")
        else:
            # Tenta mostrar o erro detalhado da API
            try:
                error_json = response.json()
                error_message = "Erro ao alterar senha:"
                for field, errors in error_json.items():
                    error_message += f"\n- {field}: {', '.join(errors)}"
                st.error(error_message)
            except Exception:
                st.error(f"Erro inesperado. Status code: {response.status_code}")
