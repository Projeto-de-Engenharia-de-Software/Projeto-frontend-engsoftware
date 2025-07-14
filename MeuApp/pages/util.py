import streamlit as st
import requests

# Configurações da API
API_BASE_URL = "http://54.209.29.198:8000/api/" 

# Função para fazer requisições autenticadas
def make_authenticated_request(method, url, headers=None, params=None, json_data=None):
    if 'auth_token' not in st.session_state:
        return None # Não há token, a requisição não será autenticada
    
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
