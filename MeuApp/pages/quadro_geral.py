import streamlit as st

import streamlit as st

st.set_page_config(
    page_title="Quadro Geral de Casos",
    page_icon=":chart_with_upwards_trend:",
)


st.markdown("<h1 style='text-align: center;'>Quadro Geral de Casos</h1>", unsafe_allow_html=True)

st.sidebar.title("Seções")

slider = st.slider("Período", min_value = 2015, max_value = 2024, value = 2015)

if st.sidebar.button("Mapa Interativo"):
    st.switch_page("sidebar_quadro/mapa_interativo.py")


