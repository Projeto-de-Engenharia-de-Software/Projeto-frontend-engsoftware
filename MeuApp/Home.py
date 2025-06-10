import streamlit as st

# Oculta a barra lateral e menu padrão
st.set_page_config(page_title="Nexus", layout="centered")

# Aplica estilo customizado (CSS)
st.markdown("""
            
    <style>
            
    body {
        background-color: white;
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


st.image("pages/image.png", use_container_width=True)

st.markdown('<br><br>', unsafe_allow_html=True)

st.markdown('<h1 class="title">Bem Vindo ao Nexus</h1>', unsafe_allow_html=True)
st.markdown('<br><br><br>', unsafe_allow_html=True)

left,center,right = st.columns([8,6,2])

with left:
    if st.button("Não Possui Cadastro?"):
        st.switch_page("pages/_cadastrar.py")
with right:

    if st.button("Entrar"):
        st.switch_page("pages/_login.py")