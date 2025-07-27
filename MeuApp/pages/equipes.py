import pandas as pd
import streamlit as st
from pages.util import API_BASE_URL, make_authenticated_request

def get_equipes():
    url = f"{API_BASE_URL}equipes/"
    response = make_authenticated_request('get', url)

    if response and response.status_code == 200:
        df_equipe = pd.DataFrame(response.json())
        df_equipe['gestor'] = df_equipe['gestor'].apply(lambda x: x['username'] if isinstance(x, dict) else x)
        df_equipe['profissionais'] = df_equipe['profissionais'].apply(lambda x: ', '.join([p['username'] for p in x]) if isinstance(x, list) else x)
        df_equipe.drop(columns=['id'], inplace=True)

        df_equipe.rename(columns = {
            'nome': 'Nome da Equipe',
            'gestor': 'Gestor',
            'profissionais': 'Profissionais'
        }, inplace=True)

        return df_equipe
    else:
        st.error("Erro ao carregar equipes")
        return pd.DataFrame



def equipes(equipes):
    st.title("Equipes")
    st.dataframe(equipes, hide_index=True)

    col1, col2, col3, col4 = st.columns([3,3,4,2])

    with col1:
        if st.button("Adicionar membro"):
            st.switch_page("pages/adicionar_membro.py")
    with col2:
        if st.button("Remover membro"):
            st.switch_page("pages/remover_membro.py")
    with col3:
        st.button("Gerenciar Permissões")
