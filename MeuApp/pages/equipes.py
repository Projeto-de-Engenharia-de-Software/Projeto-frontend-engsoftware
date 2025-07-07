import pandas as pd
import streamlit as st

st.set_page_config(page_title="Nexus - Equipes", layout="centered") 



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

def remover(data, remover):
    busca = data[data['Usuário'] == 'remover']
    
    with st.container():
        st.warning(f"Tem certeza que deseja excluir '{remover}'?")
        col1, col2 = st.columns(2)

        with col1:
            confirmar = st.button("✅ Sim, excluir", key="confirmar")

        with col2:
            cancelar = st.button("❌ Cancelar", key="cancelar")

        if confirmar:
            st.success(f"'{nome_para_excluir}' foi excluído com sucesso.")
            data = data[data['Usuário'] != 'remover']

        elif cancelar:
            st.info("Operação cancelada.")

st.title("Equipes")
nomes = pd.DataFrame({
    'Membros': [
        'Juan Pabollo', 'Vitor Barros', 'Wellington Viana',
        'Ruan Rodrigues', 'Samara Accioly', 'Gabriel Farias'
    ],
    'Usuário': [
        "juansilva", "vBarros", "wViana03",
        "rodrigues01", "samaraaccioly", "gabrielF"
    ],
    'Status': [
        "Ativo", "Afastado", "Ativo",
        "Desligado", "Ativo", "Ativo"
    ],
    'Data de Ingresso': [
        "07-07-2020", "23-10-2020", "30-03-2019",
        "04-02-2021", "11-11-2022", "29-06-2023"
    ],
    'Especialidade': [
        "Agente de Saúde", "Enfermeiro", "Secretário de Saúde",
        "Enfemeiro", "Médico", "Médico"
    ],
    'Último Login': [
        "06-07-2025 12:05", "07-06-2025 16:32", "04-07-2025 07:21",
        "02-01-2025 11:53", "20-06-2025 19:43", "07-07-2025 15:12"
    ]
})

st.dataframe(nomes)
    

col1, col2, col3, col4 = st.columns([3,3,4,2])

with col1:
   if st.button("Adicionar membro"):
       st.switch_page("pages/adicionar_membro.py")
with col2:
    st.button("Remover membro")
with col3:
    st.button("Gerenciar Permissões")
with col4:
    if st.button("Voltar"):
        st.switch_page("pages/quadro_geral.py")
       