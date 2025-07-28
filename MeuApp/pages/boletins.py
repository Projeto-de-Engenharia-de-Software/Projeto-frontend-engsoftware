import streamlit as st
import pandas as pd
from streamlit.components.v1 import html

st.image("pages/image.png", use_container_width=True)

# ----------------------
# FUNÇÕES AUXILIARES
# ----------------------

def status_color(status):
    return {
        "Aprovado": "#28a745",
        "Pendente": "#ffc107",
        "Rejeitado": "#dc3545"
    }.get(status, "#6c757d")  # cinza padrão

# Função para salvar comentário (sem funcionalidade backend aqui)
def save_comment(card_id, comment_text):
    st.session_state[f"comment_{card_id}"] = comment_text
    st.session_state[f"editing_{card_id}"] = False
    st.rerun()

def modal_card(card_id, title, preview_html, initial_modal_content_html):
    if f"comment_{card_id}" not in st.session_state:
        st.session_state[f"comment_{card_id}"] = ""
    if f"editing_{card_id}" not in st.session_state:
        st.session_state[f"editing_{card_id}"] = False

    current_comment = st.session_state[f"comment_{card_id}"]

    html_content = f"""
    <style>
    #{card_id}-card {{
        background-color: #1E1E1E;
        color: white;
        padding: 20px;
        border-radius: 12px;
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        transition: transform 0.2s ease;
        margin-bottom: 15px;
    }}
    #{card_id}-card:hover {{
        transform: scale(1.02);
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    }}
    #{card_id}-modal {{
        display: none;
        position: fixed;
        z-index: 9999;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background-color: rgba(0,0,0,0.6);
    }}
    #{card_id}-modal-content {{
        background-color: white;
        color: black;
        margin: 5% auto;
        padding: 30px;
        border-radius: 10px;
        width: 80%;
        max-width: 900px;
        max-height: 70vh;
        overflow-y: auto;
        box-shadow: 0 6px 18px rgba(0,0,0,0.3);
        animation: zoomIn 0.3s ease;
    }}
    @keyframes zoomIn {{
        from {{ opacity: 0; transform: scale(0.85); }}
        to   {{ opacity: 1; transform: scale(1); }}
    }}
    .close-btn {{
        background-color: #dc3545;
        color: white;
        padding: 8px 16px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
        float: right;
    }}
    .edit-comment-btn, .save-comment-btn {{
        background-color: #007bff;
        color: white;
        padding: 8px 16px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
        margin-top: 10px;
    }}
    .save-comment-btn {{ background-color: #28a745; margin-left: 10px; }}
    textarea {{
        width: calc(100% - 20px);
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        resize: vertical;
    }}
    </style>

    <div id="{card_id}-card" onclick="document.getElementById('{card_id}-modal').style.display='block'">
        <h4>{title}</h4>
        {preview_html}
    </div>

    <div id="{card_id}-modal" onclick="this.style.display='none'">
        <div id="{card_id}-modal-content" onclick="event.stopPropagation()">
            <button class="close-btn" onclick="document.getElementById('{card_id}-modal').style.display='none'">Fechar</button>
            <h3>{title}</h3>
            <hr>
            {initial_modal_content_html}

            <p><b>📝 Comentário:</b></p>
            <div id="{card_id}-comment-display" style="display: {'none' if st.session_state[f'editing_{card_id}'] else 'block'};">
                <p>{current_comment if current_comment else "Nenhum comentário adicionado."}</p>
                <button class="edit-comment-btn" onclick="
                    document.getElementById('{card_id}-comment-display').style.display = 'none';
                    document.getElementById('{card_id}-edit-section').style.display = 'block';
                    document.getElementById('{card_id}-comment-textarea').value = `{current_comment}`;
                ">Editar Comentário</button>
            </div>

            <div id="{card_id}-edit-section" style="display: {'block' if st.session_state[f'editing_{card_id}'] else 'none'};">
                <textarea id="{card_id}-comment-textarea" rows="4" placeholder="Adicione seu comentário aqui..."></textarea>
                <button class="save-comment-btn" onclick="
                    var commentText = document.getElementById('{card_id}-comment-textarea').value;
                    alert('Comentário salvo localmente. Integração com backend pode ser feita aqui.');
                    document.getElementById('{card_id}-modal').style.display='none';
                ">Salvar Comentário</button>
                <button class="edit-comment-btn" onclick="
                    document.getElementById('{card_id}-comment-display').style.display = 'block';
                    document.getElementById('{card_id}-edit-section').style.display = 'none';
                ">Cancelar</button>
            </div>
        </div>
    </div>
    """
    html(html_content, height=260)


# ----------------------
# PÁGINA PRINCIPAL
# ----------------------

def boletin():
    st.title("📌 Histórico de Boletins")

    # Filtro por status
    filtro_status = st.selectbox("📊 Filtrar por status", ["Todos", "Aprovado", "Pendente", "Rejeitado"])
    busca_unidade = st.text_input("🔎 Buscar por unidade")

    # Dados fictícios dos boletins
    boletins = [
        {
            "id": "unidade1_card",
            "titulo": "📋 Relatório - Unidade 1 - Casa Amarela - Recife",
            "data": "09/07/2025",
            "status": "Aprovado",
            "resumo": """
                <ul>
                    <li>Atendimentos: 1.254</li>
                    <li>Equipe: 11 profissionais</li>
                    <li>Integração SINAN concluída</li>
                    <li>2 registros pendentes</li>
                </ul>
            """,
            "documentos": '<a href="#">PDF</a> | <a href="#">Planilha</a>'
        },
        {
            "id": "unidade3_card",
            "titulo": "📋 Relatório - Unidade 3 - Dois Irmãos - Recife",
            "data": "10/07/2025",
            "status": "Aprovado",
            "resumo": """
                <ul>
                    <li>Atendimentos: 1.500</li>
                    <li>Equipe: 15 profissionais</li>
                    <li>Integração SINAN concluída</li>
                    <li>Nenhum registro pendente</li>
                </ul>
            """,
            "documentos": '<a href="#">Relatório Completo</a> | <a href="#">Dashboard</a>'
        },
        {
            "id": "unidade4_card",
            "titulo": "📋 Relatório - Unidade 4 - Ibura - Recife",
            "data": "11/07/2025",
            "status": "Pendente",
            "resumo": """
                <ul>
                    <li>Atendimentos: 980</li>
                    <li>Equipe: 9 profissionais</li>
                    <li>Integração SINAN pendente</li>
                    <li>5 registros aguardando análise</li>
                </ul>
            """,
            "documentos": '<a href="#">Rascunho PDF</a>'
        }
    ]

    # Aplicar filtros
    for boletim in boletins:
        if (filtro_status != "Todos" and boletim["status"] != filtro_status):
            continue
        if busca_unidade and busca_unidade.lower() not in boletim["titulo"].lower():
            continue

        modal_card(
            card_id=boletim["id"],
            title=boletim["titulo"],
            preview_html=f"""
                <p>🗓️ Atualizado: <b>{boletim['data']}</b></p>
                <p>📊 Status: <b style='color:{status_color(boletim['status'])}'>{boletim['status']}</b></p>
            """,
            initial_modal_content_html=f"""
                <p><b>Resumo:</b></p>{boletim['resumo']}
                <p><b>📎 Documentos:</b> {boletim['documentos']}</p>
            """
        )

# Chamada da página
boletin()
