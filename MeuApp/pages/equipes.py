# equipes.py
import pandas as pd
import streamlit as st
import requests
from pages.util import API_BASE_URL, make_authenticated_request
from pages._login import cookie

# Função para obter o tipo do usuário logado
def get_tipo_usuario():
    url = f"{API_BASE_URL}profiles/me/"
    response = make_authenticated_request("get", url)
    
    if response and response.status_code == 200:
        data = response.json()
        return data.get("perfil")
    else:
        return "perfil"

def get_equipes():
    token_cookie = cookie.get("auth_token")
    if token_cookie and 'auth_token' not in st.session_state:
        st.session_state.auth_token = token_cookie

    if 'auth_token' not in st.session_state:
        st.switch_page("pages/_login.py")

    url = f"{API_BASE_URL}equipes/"
    response = make_authenticated_request('get', url)

    if response and response.status_code == 200:
        data = response.json()

        # Retorna tabela vazia se não houver equipes
        if not data:
            return pd.DataFrame(columns=["Nome da Equipe", "Gestor", "Profissionais"])

        df_equipe = pd.DataFrame(data)
        df_equipe['gestor'] = df_equipe['gestor'].apply(
            lambda x: x['username'] if isinstance(x, dict) else x
        )
        df_equipe['profissionais'] = df_equipe['profissionais'].apply(
            lambda x: ', '.join([p['username'] for p in x]) if isinstance(x, list) else x
        )
        df_equipe.drop(columns=['id'], inplace=True)

        df_equipe.rename(columns={
            'nome': 'Nome da Equipe',
            'gestor': 'Gestor',
            'profissionais': 'Profissionais'
        }, inplace=True)

        return df_equipe
    else:
        st.error("Erro ao carregar equipes")
        return pd.DataFrame(columns=["Nome da Equipe", "Gestor", "Profissionais"])

def equipes(equipes):
    st.title("Equipes")
    st.dataframe(equipes, hide_index=True)

# Checar o tipo de usuário e exibir botões apropriados
    tipo_usuario = get_tipo_usuario()
    if tipo_usuario == "gestor":
        col1, col2, col3, col4 = st.columns([3,3,3,3])
        with col1:
            if st.button("Adicionar membro"):
                st.switch_page("pages/adicionar_membro.py")
        with col2:
            if st.button("Remover membro"):
                st.switch_page("pages/remover_membro.py")
        with col3:
            if st.button("Adicionar equipe"):
                st.switch_page("pages/adicionar_equipe.py")
        with col4:
            if st.button("Remover equipe"):
                st.switch_page("pages/remover_equipe.py")
    # elif tipo_usuario == "profissional":
    #     col1, _ = st.columns([3, 9])
    #     with col1:
    #         if st.button("Sair da equipe"):
    #             st.switch_page("pages/sair_equipe.py")