import streamlit as st
import google.generativeai as genai
from openai import OpenAI
import requests
from io import BytesIO

# --- CONFIGURAÇÃO NANO BET DESIGN ---
st.set_page_config(page_title="Nano Bet Design", page_icon="🎨", layout="wide")

# CSS para Estética de App Nativo e Minimalista
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .stButton>button { background-color: #00ff30; color: black; border-radius: 8px; font-weight: bold; width: 100%; }
    .stSelectbox, .stTextArea, .stFileUploader { border-radius: 10px !important; }
    div[data-testid="stExpander"] { border: none; background: transparent; }
    </style>
    """, unsafe_allow_html=True)

# --- CHAVES ---
OPENAI_KEY = "SUA_CHAVE_AQUI"
GEMINI_KEY = "SUA_CHAVE_AQUI"

genai.configure(api_key=GEMINI_KEY)
openai_client = OpenAI(api_key=OPENAI_KEY)

# --- BANCO DE DADOS: OS 13 PROJETOS ---
PROJETOS = {
    "Camillo Joga10": {"cor": "#00ff30", "estilo": "Neon Vibrante e Fumaça"},
    "Luisa Mendes": {"cor": "#8400ff", "estilo": "Roxo Premium Luxury"},
    "Bruno Karttos": {"cor": "#f9b61d", "estilo": "Dourado e Amarelo Tech"},
    "Herculano": {"cor": "#df3891", "estilo": "Rosa Shock e Cyberpunk"},
    "Raquel Maia": {"cor": "#22447f", "estilo": "Azul Profundo e Lima"},
    "Neto Lima": {"cor": "#64e6f9", "estilo": "Ciano e Dark Mode"},
    "Nascimento": {"cor": "#37c200", "estilo": "Verde Bet Clássico"},
    "Nalanda Tips": {"cor": "#cd00ff", "estilo": "Magenta e Roxo"},
    "MD Oficial": {"cor": "#5acd51", "estilo": "Verde Gramado e Sport"},
    "Luiz Royal": {"cor": "#00fffc", "estilo": "Azul Royal e Neve"},
    "Danda Bet": {"cor": "#00ff06", "estilo": "Verde Elétrico"},
    "Helder Tips": {"cor": "#00ff1e", "estilo": "Verde Neon Dark"},
    "Nano Bet VIP": {"cor": "#ffffff", "estilo": "Branco e Prata Minimalista"}
}

# --- UI: PAINEL SUPERIOR ---
st.title("🎨 Nano Bet Design")
st.caption("Agente Especialista em Growth & Midia Esportiva")

# Linha de Atalhos (Dropdown de Clientes)
col_atalho, col_diretriz = st.columns([2, 1])

with col_atalho:
    projeto_sel = st.selectbox("🚀 Atalho de Projeto (Dropdown de Clientes)", list(PROJETOS.keys()))

with col_diretriz:
    modo_diretriz = st.toggle("Mesclar Regras da Marca", value=True, help="Se ativado, a IA prioriza o manual da marca selecionada.")

# --- UI: CAMPO DE PROMPT SIMPLIFICADO ---
col_upload, col_prompt = st.columns([1, 4])

with col_upload:
    foto_ref = st.file_uploader("", type=["jpg", "png"], label_visibility="collapsed")
    formato = st.radio("Formato", ["9:16 (Status)", "1:1 (Conversa)"], horizontal=True)

with col_prompt:
    briefing = st.text_area("", placeholder="O que vamos criar hoje? (Ex: Odd 5.0, Mês Março, Green)", height=100)
    tipo_card = st.selectbox("Tipo de Card", ["Resultado/Green", "Odd Alta", "Oferta Especial", "Feedback"])

# --- MOTOR DE EXECUÇÃO ---
if st.button("GERAR ARTE FINAL"):
    if not briefing:
        st.error("Diga-me o que criar!")
    else:
        with st.spinner("Refinando memória e renderizando arte..."):
            try:
                # O cérebro estratégico (Gemini) processa o DNA invisível
                dna_marca = f"Marca: {projeto_sel}. Cor: {PROJETOS[projeto_sel]['cor']}. Estilo: {PROJETOS[projeto_sel]['estilo']}." if modo_diretriz else ""
                
                model = genai.GenerativeModel('models/gemini-1.5-flash')
                prompt_task = f"""
                [ROLE]: Art Director, Growth Expert, Sports Media Agency Specialist.
                [CLIENT DNA]: {dna_marca}
                [SAFE ZONE]: 15% margins top/bottom are SACRED.
                [CARD TYPE]: {tipo_card}
                [INPUT]: {briefing}
                [TASK]: Create a prompt for DALL-E 3. HDR textures, 3D white bold fonts with black outline, dark premium background. If a photo was uploaded, create a digital faithful representation.
                """
                
                res_gemini = model.generate_content(prompt_task)
                
                # O executor (DALL-E) gera a imagem
                tamanho = "1024x1792" if "9:16" in formato else "1024x1024"
                img_gen = openai_client.images.generate(model="dall-e-3", prompt=res_gemini.text, size=tamanho, quality="hd")
                
                url = img_gen.data[0].url
                st.image(url, use_column_width=True)
                
                # Download
                btn_data = requests.get(url).content
                st.download_button("📥 BAIXAR ARTE FINAL HD", btn_data, f"arte_{projeto_sel}.png")

            except Exception as e:
                st.error(f"Erro: {e}")
