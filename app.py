import streamlit as st
import google.generativeai as genai
from openai import OpenAI
import requests
from io import BytesIO

# Configuração da Interface (Visual de Elite)
st.set_page_config(page_title="Nano Bet Pro - Arte Final", page_icon="🎨", layout="wide")
st.title("🎨 Nano Bet Pro - Gerador de Arte Final")
st.subheader("Criação de Cards de Alta Conversão")
st.markdown("---")

# --- SUAS CHAVES INTEGRADAS ---
GEMINI_KEY = "AIzaSyBY_fbe0_xFpkNWz0YAYxxZFYzW3VZ6uzs"
OPENAI_KEY = "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"

# Inicializar os Motores
genai.configure(api_key=GEMINI_KEY)
openai_client = OpenAI(api_key=OPENAI_KEY)

# --- BANCO DE DADOS DE BRANDING (12 EXPERTS) ---
EXPERTS = {
    "Herculano": {"cor": "#df3891", "estilo": "Rosa Barbie e Verde Neon"},
    "Camillo": {"cor": "#00ff30", "estilo": "Verde Intenso e Escuro"},
    "Bruno Karttos": {"cor": "#f9b61d", "estilo": "Amarelo e Dourado Premium"},
    "Luisa Mendes": {"cor": "#8400ff", "estilo": "Roxo Vibrante"},
    "Raquel Maia": {"cor": "#22447f", "estilo": "Azul e Verde Lima"},
    "Neto Lima": {"cor": "#64e6f9", "estilo": "Ciano Tech"},
    "Nascimento": {"cor": "#37c200", "estilo": "Verde Clássico Bet"},
    "Nalanda Tips": {"cor": "#cd00ff", "estilo": "Roxo e Magenta"},
    "MD": {"cor": "#5acd51", "estilo": "Verde Esportivo"},
    "Luiz Royal": {"cor": "#00fffc", "estilo": "Ciano Royal"},
    "Danda": {"cor": "#00ff06", "estilo": "Verde Limão Agressivo"},
    "Helder da Bet": {"cor": "#00ff1e", "estilo": "Verde Neon Puro"}
}

# --- BARRA LATERAL DE CONFIGURAÇÃO ---
st.sidebar.header("⚙️ Configurações do Card")
expert_sel = st.sidebar.selectbox("Escolha o Expert", list(EXPERTS.keys()))
formato = st.sidebar.selectbox("Formato do WhatsApp", ["9:16 Status", "1:1 Feed"])
tipo_card = st.sidebar.selectbox("Tipo de Card", ["Resultado/Green", "Odd Alta", "Oferta Especial", "Feedback"])

# Entrada do Briefing
briefing = st.text_area("✍️ Dados do Card (Ex: ODD 4.5, Lucro R$ 500, Março)", height=100)

if st.button("🚀 GERAR IMAGEM AGORA"):
    if not briefing:
        st.error("Por favor, digite os dados do card antes de gerar.")
    else:
        with st.spinner(f"O Diretor de Arte está criando a peça para {expert_sel}..."):
            try:
                # FASE 1: O Gemini (Estrategista) cria o prompt ultra-detalhado
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt_task = f"""
                Create a high-quality professional betting card image prompt for DALL-E 3.
                EXPERT: {expert_sel}
                MAIN COLOR: {EXPERTS[expert_sel]['cor']} ({EXPERTS[expert_sel]['estilo']})
                FORMAT: {formato}
                DATA: {briefing}
                TYPE: {tipo_card}
                
                VISUAL RULES:
                - Dark, premium background with smoke and glowing particles.
                - Bold, 3D white typography with heavy black outlines.
                - Centralize the main numbers (ODD/Profit).
                - SAFE ZONE: Keep 15% margin at the top and bottom.
                - High contrast, HDR lighting, realistic textures.
                - Professional betting aesthetic.
                """
                gemini_res = model.generate_content(prompt_task)
                
                # FASE 2: O DALL-E 3 (Ilustrador) gera a imagem final
                size = "1024x1792" if "9:16" in formato else "1024x1024"
                res_img = openai_client.images.generate(
                    model="dall-e-3",
                    prompt=gemini_res.text,
                    size=size,
                    quality="hd",
                    n=1
                )
                
                img_url = res_img.data[0].url
                
                # Exibição e Download
                st.image(img_url, caption=f"Arte Final - Expert {expert_sel}")
                
                img_data = requests.get(img_url).content
                st.download_button(label="📥 Baixar Arte em HD", data=BytesIO(img_data).read(), file_name=f"card_{expert_sel}.png", mime="image/png")

            except Exception as e:
                st.error(f"Ocorreu um erro técnico: {e}")
