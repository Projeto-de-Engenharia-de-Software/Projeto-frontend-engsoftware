import streamlit as st
import requests

# Configurações da API
API_BASE_URL = "http://54.209.29.198:8000/api/" 

# Função para fazer requisições autenticadas
def make_authenticated_request(method, url, headers=None, params=None, json_data=None):
    if 'auth_token' not in st.session_state:
        st.error("Usuário não autenticado.")
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

        elif method.lower() == 'put':
            response = requests.put(url, headers=auth_headers, json=json_data)
        elif method.lower() == 'delete':
            response = requests.delete(url, headers=auth_headers)
        else:
            st.error(f"Método HTTP '{method}' não suportado.")
            return None  # Sai aqui, response não definido

        response.raise_for_status()
        return response

    except requests.exceptions.RequestException as e:
        st.error(f"Erro na requisição API: {e}")
        # Retorna a resposta para análise, se existir
        if 'response' in locals():
            return response
        return None

