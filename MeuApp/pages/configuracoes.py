import streamlit as st


st.set_page_config(page_title="Nexus", layout="centered", initial_sidebar_state="collapsed")

st.image("pages/image.png", use_container_width=True)

left, center, right = st.columns([3, 5, 2])


with center:
        
        st.title("Configurações")

with st.container():

    nova_senha = st.text_input("Nova Senha")

    confirmar_senha = st.text_input("Confirmar Nova Senha")

    novo_user = st.text_input("Novo Usuário")

salvar_btn = st.button("Salvar")

homepage_btn = st.button("Homepage")

logout_btn = st.button("Fazer Logoff")

if logout_btn:
      st.session_state.auth_token = False
      st.switch_page("pages/_login.py")
      st.rerun()
if homepage_btn:
      
      st.switch_page("pages/_homepage.py")
