import streamlit as st
from streamlit.components.v1 import html

st.image("pages/image.png", use_container_width=True)

# Função de callback para salvar o comentário
def save_comment(card_id, comment_text):
    st.session_state[f"comment_{card_id}"] = comment_text
    st.session_state[f"editing_{card_id}"] = False
    # Para forçar a atualização da interface do Streamlit
    st.rerun()

def modal_card(card_id, title, preview_html, initial_modal_content_html):
    # Inicializa o estado do comentário e do modo de edição para cada card_id único
    if f"comment_{card_id}" not in st.session_state:
        st.session_state[f"comment_{card_id}"] = ""
    if f"editing_{card_id}" not in st.session_state:
        st.session_state[f"editing_{card_id}"] = False

    current_comment = st.session_state[f"comment_{card_id}"]

    # HTML/CSS/JS para o card e modal
    html_content = f"""
    <style>
    /* --- CARD COMPACTO --- */
    #{card_id}-card {{
        background-color: #1E1E1E;
        color: white;
        padding: 20px;
        border-radius: 12px;
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        transition: transform 0.2s ease;
    }}
    #{card_id}-card:hover {{
        transform: scale(1.02);
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    }}

    /* --- BACKDROP ESCURO --- */
    #{card_id}-modal {{
        display: none;
        position: fixed;
        z-index: 9999;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background-color: rgba(0,0,0,0.6);
    }}

    /* --- MODAL CONTEÚDO EXPANDIDO --- */
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

    .modal-title {{
        margin-top: 0;
        font-size: 22px;
        font-weight: bold;
    }}

    .edit-comment-btn, .save-comment-btn {{
        background-color: #007bff; /* Azul */
        color: white;
        padding: 8px 16px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
        margin-top: 10px;
    }}

    .save-comment-btn {{
        background-color: #28a745; /* Verde */
        margin-left: 10px;
    }}

    textarea {{
        width: calc(100% - 20px); /* Ajuste para padding */
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        box-sizing: border-box; /* Inclui padding e border na largura total */
        resize: vertical; /* Permite redimensionar verticalmente */
    }}
    </style>

    <div id="{card_id}-card" onclick="document.getElementById('{card_id}-modal').style.display='block'">
        <h4>{title}</h4>
        {preview_html}
    </div>

    <div id="{card_id}-modal" onclick="this.style.display='none'">
        <div id="{card_id}-modal-content" onclick="event.stopPropagation()">
            <button class="close-btn" onclick="document.getElementById('{card_id}-modal').style.display='none'">Fechar</button>
            <h3 class="modal-title">{title}</h3>
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
                    // Chamar a função Python para salvar o comentário e recarregar
                    fetch('/_stcore/scriptrunner/execute_callback', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            callback: 'save_comment', // Nome da função Python
                            args: ['{card_id}', commentText]
                        }})
                    }});
                    // Fecha o modal imediatamente após o clique em Salvar
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
    html(html_content, height=250)




### **Uso da Função `modal_card` Atualizada**


# ----------------------------
# USO
# ----------------------------

def boletin():
    st.title("📌 Histórico de Boletins")

    # Exemplo 1: Unidade 1
    modal_card(
        card_id="unidade1_card", # Use um ID único para cada card
        title="📋 Relatório - Unidade 1 - Casa Amarela - Recife",
        preview_html="""
            <p>🗓️ Última atualização: <b>09/07/2025</b></p>
            <p>📊 Status: <b>Aprovado</b></p>
        """,
        initial_modal_content_html="""
            <p><b>Resumo Geral:</b></p>
            <ul>
                <li>Atendimentos totais: 1.254</li>
                <li>Equipe ativa: 11 profissionais</li>
                <li>Integração SINAN concluída</li>
                <li>2 registros pendentes de regularização</li>
                <li>Boletins semanais em dia</li>
                <li>Relatórios enviados ao gestor municipal</li>
                <li>Pacientes com prioridade máxima: 3</li>
            </ul>
            <p><b>📎 Documentos:</b> <a href="#">Baixar PDF</a> | <a href="#">Ver Planilha</a></p>
        """
    )

    # Exemplo 2: Unidade 3 (Mude o card_id para ser único!)
    modal_card(
        card_id="unidade3_card", # ID único diferente do anterior
        title="📋 Relatório - Unidade 3 - Dois Irmãos - Recife",
        preview_html="""
            <p>🗓️ Última atualização: <b>10/07/2025</b></p>
            <p>📊 Status: <b>Aprovado</b></p>
        """,
        initial_modal_content_html="""
            <p><b>Resumo Geral:</b></p>
            <ul>
                <li>Atendimentos totais: 1.500</li>
                <li>Equipe ativa: 15 profissionais</li>
                <li>Integração SINAN concluída com sucesso</li>
                <li>Nenhum registro pendente</li>
                <li>Boletins diários em dia</li>
                <li>Relatórios consolidados enviados ao gestor estadual</li>
                <li>Pacientes com prioridade máxima: 5</li>
            </ul>
            <p><b>📎 Documentos:</b> <a href="#">Baixar PDF Relatório Completo</a> | <a href="#">Ver Dashboard</a></p>
        """
    )