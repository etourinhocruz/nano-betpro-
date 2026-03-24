import streamlit as st
import google.generativeai as genai
from openai import OpenAI
import requests
from io import BytesIO

# Configuração da Interface
st.set_page_config(page_title="Nano Bet Design - Arte Final", page_icon="🎨", layout="wide")
st.title("🎨 Nano Bet Design - Gerador de Arte Final")
st.markdown("---")

# --- SUAS CHAVES INTEGRADAS ---
OPENAI_KEY = "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"
GEMINI_KEY = "AIzaSyBY_fbe0_xFpkNWz0YAYxxZFYzW3VZ6uzs" 

# --- INICIALIZAÇÃO ---
genai.configure(api_key=GEMINI_KEY)
openai_client = OpenAI(api_key=OPENAI_KEY)

# --- BANCO DE DADOS DE BRANDING ---
EXPERTS = {
    "Herculano": {"cor": "#df3891"},
    "Camillo": {"cor": "#00ff30"},
    "Bruno Karttos": {"cor": "#f9b61d"},
    "Luisa Mendes": {"cor": "#8400ff"},
    "Raquel Maia": {"cor": "#22447f"},
    "Neto Lima": {"cor": "#64e6f9"},
    "Nascimento": {"cor": "#37c200"},
    "Nalanda Tips": {"cor": "#cd00ff"},
    "MD": {"cor": "#5acd51"},
    "Luiz Royal": {"cor": "#00fffc"},
    "Danda": {"cor": "#00ff06"},
    "Helder da Bet": {"cor": "#00ff1e"}
}

# --- INTERFACE ---
st.sidebar.header("Configurações do Card")
expert_sel = st.sidebar.selectbox("Expert", list(EXPERTS.keys()))
formato = st.sidebar.selectbox("Formato", ["9:16 Status (WhatsApp)", "1:1 Feed"])
tipo_card = st.sidebar.selectbox("Tipo de Card", ["Resultado", "Odd Alta", "Oferta", "Feedback"])

briefing = st.text_area("Dados do Card (Ex: Odd 5.0, Mês Março, Green)", height=100)

if st.button("🚀 GERAR ARTE FINAL"):
    if not briefing:
        st.error("Digite os dados primeiro!")
    else:
        with st.spinner(f"Gerando arte final para {expert_sel}..."):
            try:
                # O Gemini cria o prompt visual baseado nas regras
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt_task = f"Create a professional high-conversion betting card image prompt for DALL-E 3. Expert: {expert_sel}. Main Color: {EXPERTS[expert_sel]['cor']}. Format: {formato}. Data: {briefing}. Style: Dark background, premium neon lights, 3D typography, 15% safe zone margins on top and bottom. High contrast."
                gemini_res = model.generate_content(prompt_task)
                
                # O DALL-E 3 gera a imagem final
                size = "1024x1792" if "9:16" in formato else "1024x1024"
                res_img = openai_client.images.generate(
                    model="dall-e-3",
                    prompt=gemini_res.text,
                    size=size,
                    quality="hd",
                    n=1
                )
                
                img_url = res_img.data[0].url
                st.image(img_url, caption=f"Arte de {expert_sel} pronta!")
                
                # Download
                btn_data = requests.get(img_url).content
                st.download_button("📥 Baixar Imagem", btn_data, f"{expert_sel}_card.png", "image/png")
                
            except Exception as e:
                st.error(f"Erro técnico: {e}. Verifique se a chave do Gemini começa com AIzaSy.")
