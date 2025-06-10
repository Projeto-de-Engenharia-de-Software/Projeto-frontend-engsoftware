# tema.py
import streamlit as st

def aplicar_tema():
    # Obter o estado do tema da sessão
    if "modo_escuro" not in st.session_state:
        st.session_state.modo_escuro = True #
       
    # Botão de alternância no canto superior direito
    col1, col2, col3 = st.columns([8, 1, 1])
    with col3:
        
        modo = st.toggle("🌙", value=st.session_state.modo_escuro, help="Alternar tema escuro")

    st.session_state.modo_escuro = modo

    # Estilos para cada tema (o resto do código aqui permanece o mesmo que discutimos antes)
    if st.session_state.modo_escuro:
        st.markdown("""
        <style>
        body {
            background-color: #0e1117;
            color: white;
        }
        .stApp {
            background-color: #0e1117;
            color: white;
        }
        .stTextInput label, .stTextArea label, .stSelectbox label, .stDateInput label {
            color: white;
        }
        .stTextInput input::placeholder, .stTextArea textarea::placeholder,
        .stNumberInput input::placeholder, .stDateInput input::placeholder {
            color: white;
        }
        .stTextInput input, .stTextArea textarea, .stNumberInput input, .stDateInput input {
            color: white;
        }
        .btn-login {
            background-color: black;
            color: white;
        }
        .btn-login:hover {
            background-color: #333;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        body {
            background-color: white;
            color: black;
        }
        .stApp {
            background-color: white;
            color: black;
        }
        .stTextInput label, .stTextArea label, .stSelectbox label, .stDateInput label {
            color: black;
        }
        .stTextInput input::placeholder, .stTextArea textarea::placeholder,
        .stNumberInput input::placeholder, .stDateInput input::placeholder {
            color: white;
        }
        .stTextInput input, .stTextArea textarea, .stNumberInput input, .stDateInput input {
            color: black;
        }
        .btn-login {
            background-color: black;
            color: white;
        }
        .btn-login:hover {
            background-color: #333;
        }
        </style>
        """, unsafe_allow_html=True)