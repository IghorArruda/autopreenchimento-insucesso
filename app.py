import streamlit as st
import re

# ============================================
# CONFIGURACAO DA PAGINA
# ============================================
st.set_page_config(
    page_title="AutoPreenchimento - Insucesso de Atividades",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================
# CSS CUSTOMIZADO
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        text-align: center;
        padding: 1rem 0 0.5rem 0;
    }

    .main-header h1 {
        color: #1f2937;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    .main-header p {
        color: #6b7280;
        font-size: 1rem;
        margin-top: 0;
    }

    .card-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #374151;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.8rem;
        border-bottom: 2px solid #f3f4f6;
        padding-bottom: 0.5rem;
    }

    .detected-field {
        background-color: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 0.6rem 0.8rem;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
        color: #1f2937;
    }

    .detected-label {
        font-size: 0.7rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.2rem;
    }

    .result-box {
        background-color: #111827;
        color: #e5e7eb;
        padding: 1.5rem;
        border-radius: 12px;
        font-family: 'Courier New', monospace;
        font-size: 0.95rem;
        line-height: 1.6;
        white-space: pre-wrap;
        border-left: 4px solid #ef4444;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .stButton>button[kind="primary"] {
        background-color: #dc2626;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        border: none;
        transition: all 0.2s;
    }

    .stButton>button[kind="primary"]:hover {
        background-color: #b91c1c;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
    }

    .success-toast {
        background-color: #d1fae5;
        color: #065f46;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #10b981;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNCAO DE PARSE DO TEXTO BRUTO
# ============================================
def parse_texto_bruto(texto):
    """Extrai dados do texto da rota usando regex."""
    dados = {}
    if not texto:
        return dados

    linhas = [l.strip() for l in texto.split('\n') if l.strip()]
    texto_flat = texto

    # Data
    m = re.search(r'(\d{2}/\d{2}/\d{4})', texto_flat)
    dados['data'] = m.group(1) if m else ''

    # Parada
    m = re.search(r'Parada\s+(\d+)', texto_flat)
    dados['parada'] = m.group(1) if m else ''

    # Cliente: linha apos o tipo de atividade
    dados['cliente'] = ''
    tipos_atividade = ['Instalacao', 'Chamado', 'Preventiva', 'Retirada', 'Chamado Modem']
    for i, linha in enumerate(linhas):
        if any(t.lower() in linha.lower() for t in tipos_atividade):
            if i + 1 < len(linhas):
                possivel = linhas[i + 1]
                if not any(k in possivel for k in ['Download', 'Mapa', 'Comentario', 'Modelo:', 'Chamado:', 'SAP:', 'Territorio:', 'Possui', 'ITENS:', 'R ', 'Av ', 'Avenida ', 'Rua ']):
                    if len(possivel) > 2 and not possivel.isdigit():
                        dados['cliente'] = possivel
                        break

    # Cidade
    dados['cidade'] = ''
    for i, linha in enumerate(linhas):
        if 'Download' in linha or 'NF' in linha:
            for j in range(max(0, i-3), i):
                possivel = linhas[j]
                if possivel and not any(k in possivel for k in ['Download', 'Mapa', 'Comentario', 'Modelo:', 'Chamado:', 'SAP:', 'Territorio:', 'Possui', 'ITENS:']):
                    if len(possivel) < 40 and len(possivel) > 2 and not possivel.startswith('R ') and not possivel.startswith('Av'):
                        if possivel != dados.get('cliente', ''):
                            dados['cidade'] = possivel
                            break
            break

    # PC / NF / ITENS
    m = re.search(r'(?:NF|ITENS:)\s*([A-Z0-9]+)', texto_flat)
    dados['pc'] = m.group(1) if m else ''

    # Endereco
    m = re.search(r'(R\s+[^,\n]+|Av\.?\s+[^,\n]+|Rua\s+[^,\n]+|Avenida\s+[^,\n]+)', texto_flat)
    dados['endereco'] = m.group(1).strip() if m else ''

    # Modelo
    m = re.search(r'Modelo:\s*(.+)', texto_flat)
    dados['modelo'] = m.group(1).strip() if m else ''

    # Chamado
    m = re.search(r'Chamado:\s*(\d+)', texto_flat)
    dados['chamado'] = m.group(1) if m else ''

    # SAP
    m = re.search(r'SAP:\s*(\d+)', texto_flat)
    dados['sap'] = m.group(1) if m else ''

    # Territorio
    m = re.search(r'Territorio:\s*(\S+)', texto_flat)
    dados['territorio'] = m.group(1) if m else ''

    # Telemetria
    m = re.search(r'Possui Telemetria:\s*(\S+)', texto_flat)
    dados['telemetria'] = m.group(1) if m else ''

    return dados

# ============================================
# HEADER
# ============================================
st.markdown("""
<div class="main-header">
    <h1>⚡ AutoPreenchimento</h1>
    <p>Gerador de Insucesso de Atividades</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ============================================
# SELETOR DE MODELO + BOTAO DEMO
# ============================================
col_tipo, col_demo = st.columns([2, 1])

with col_tipo:
    modelo = st.selectbox(
        "📋 Tipo de Atividade",
        ["Chamado", "Chamado Modem", "Preventiva", "Instalacao", "Retirada"],
        index=3,
        help="Selecione o tipo de atividade para gerar o texto formatado"
    )

with col_demo:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📋 Carregar Exemplo", type="secondary", help="Preenche com dados ficticios para demonstracao"):
        st.session_state.texto_bruto = """00/00/0000 - Parada 0\tEsconder
Instalacao
Empresa Demonstracao LTDA

Sao Paulo
Download NF 99A9999999
Download NF 99A9999999
Rua das Flores, 123 - Centro Sao Paulo SP
Mapa
Comentario:
COMENTARIO AGENDAMENTO: LEVAR ARMARIO
Modelo: EQP-2000 PRO
Chamado: 9999999
SAP: 8888888
ITENS: 99A9999999
Territorio: BRN8RJTEC02
Possui Telemetria: NAO."""
        st.session_state.solicitante = "Carlos Silva"
        st.session_state.motivo = "Cliente ausente no horario agendado. Aguardando reagendamento."
        st.session_state.contato_local = "Porteiro do predio"
        st.session_state.ligou_consultor = "Sim"
        st.rerun()

st.divider()

# ============================================
# COLUNAS PRINCIPAIS
# ============================================
col_input, col_manual = st.columns([1.1, 0.9])

# --- COLUNA ESQUERDA ---
with col_input:
    st.markdown('<div class="card-title">📥 Dados da Rota (Cole aqui)</div>', unsafe_allow_html=True)

    texto_bruto = st.text_area(
        "Texto da rota:",
        height=220,
        key="texto_bruto",
        placeholder="Cole o texto completo da rota do dia...",
        label_visibility="collapsed"
    )

    dados = parse_texto_bruto(texto_bruto)

    if dados:
        st.markdown('<div class="card-title">🔍 Detectado Automaticamente</div>', unsafe_allow_html=True)

        campos_detectados = [
            ('data', '📅 Data'), ('parada', '📍 Parada'), ('cliente', '🏢 Cliente'),
            ('cidade', '🌆 Cidade'), ('pc', '📦 PC/NF'), ('endereco', '📍 Endereco'),
            ('modelo', '🔧 Modelo'), ('chamado', '📞 Chamado'), ('sap', '📋 SAP'),
            ('territorio', '🗺️ Territorio'), ('telemetria', '📡 Telemetria')
        ]

        cols = st.columns(2)
        for i, (key, label) in enumerate(campos_detectados):
            with cols[i % 2]:
                valor = dados.get(key, '')
                cor = '#10b981' if valor else '#ef4444'
                st.markdown(
                    '<div class="detected-field">'
                    '<div class="detected-label">' + label + '</div>'
                    '<div style="color: ' + cor + '; font-weight: 600;">' + (valor if valor else 'Nao detectado') + '</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

# --- COLUNA DIREITA ---
with col_manual:
    st.markdown('<div class="card-title">✏️ Informacoes do Local</div>', unsafe_allow_html=True)

    solicitante = st.text_input(
        "👤 Solicitante",
        key="solicitante",
        placeholder="Nome do solicitante"
    )

    motivo = st.text_area(
        "📝 Motivo do Insucesso",
        key="motivo",
        height=100,
        placeholder="Descreva o motivo do insucesso..."
    )

    contato_local = st.text_input(
        "🗣️ Com quem falamos no local?",
        key="contato_local",
        placeholder="Nome do contato no local"
    )

    ligou_consultor = st.selectbox(
        "📞 O tecnico ligou para o consultor no ato da ocorrencia?",
        ["", "Sim", "Nao"],
        key="ligou_consultor"
    )

st.divider()

# ============================================
# GERACAO DO RESULTADO
# ============================================
gerar = st.button("⚡ GERAR TEXTO FORMATADO", type="primary", use_container_width=True)

if gerar:
    if not dados.get('cliente'):
        st.error("❌ Nao foi possivel detectar os dados do cliente. Verifique o texto colado.")
    else:
        texto_saida = (
            "❌️❌️ INSUCESSO NA (" + modelo.upper() + ") ❌️❌️\n\n"
            "*RAZAO:* " + dados.get('cliente', '') + "\n"
            "*PC:* " + dados.get('pc', '') + "\n"
            "*CHAMADO* " + dados.get('chamado', '') + "\n"
            "*SAP* " + dados.get('sap', '') + "\n"
            "*CIDADE* " + dados.get('cidade', '') + " \n"
            "*SOLICITANTE:* " + (solicitante if solicitante else '(  )') + "\n"
            "*MOTIVO* " + (motivo if motivo else '(  )') + "\n"
            "*COM QUEM FALAMOS NO LOCAL:* " + (contato_local if contato_local else '(  )') + "\n"
            "*O TECNICO LIGOU PARA O CONSULTOR NO ATO DA OCORRENCIA?* " + (ligou_consultor if ligou_consultor else '(  )')
        )

        st.markdown("<div class='success-toast'>✅ Texto gerado com sucesso! Selecione e copie abaixo.</div>", unsafe_allow_html=True)

        st.markdown("### 📋 Resultado para WhatsApp:")
        st.markdown('<div class="result-box">' + texto_saida.replace('\n', '<br>') + '</div>', unsafe_allow_html=True)

        st.markdown("**📎 Versao para copiar:**")
        st.code(texto_saida, language=None)

        st.info("💡 **Dica:** Clique no icone de copia no canto superior direito da caixa acima para copiar o texto.")

# ============================================
# FOOTER
# ============================================
st.divider()
st.markdown("""
<div style="text-align: center; color: #9ca3af; font-size: 0.8rem; padding: 1rem 0;">
    ⚡ AutoPreenchimento · Desenvolvido com Python + Streamlit · Projeto de Portfolio
</div>
""", unsafe_allow_html=True)
