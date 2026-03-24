import streamlit as st
import google.generativeai as genai
from openai import OpenAI
import requests
from io import BytesIO

# Configuração da Interface
st.set_page_config(page_title="Nano Bet Pro - Arte Final", page_icon="🎨", layout="wide")
st.title("🎨 Nano Bet Pro - Gerador de Arte Final")
st.markdown("---")

# --- SUAS CHAVES (MANTIDAS) ---
GEMINI_KEY = "AIzaSyBY_fbe0_xFpkNWz0YAYxxZFYzW3VZ6uzs"
OPENAI_KEY = "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"

genai.configure(api_key=GEMINI_KEY)
openai_client = OpenAI(api_key=OPENAI_KEY)

# BANCO DE EXPERTS
EXPERTS = {
    "Herculano": {"cor": "#df3891"}, "Camillo": {"cor": "#00ff30"},
    "Bruno Karttos": {"cor": "#f9b61d"}, "Luisa Mendes": {"cor": "#8400ff"},
    "Raquel Maia": {"cor": "#22447f"}, "Neto Lima": {"cor": "#64e6f9"},
    "Nascimento": {"cor": "#37c200"}, "Nalanda Tips": {"cor": "#cd00ff"},
    "MD": {"cor": "#5acd51"}, "Luiz Royal": {"cor": "#00fffc"},
    "Danda": {"cor": "#00ff06"}, "Helder da Bet": {"cor": "#00ff1e"}
}

st.sidebar.header("⚙️ Configurações")
expert_sel = st.sidebar.selectbox("Expert", list(EXPERTS.keys()))
formato = st.sidebar.selectbox("Formato", ["9:16 Status", "1:1 Feed"])
briefing = st.text_area("✍️ Dados do Card", height=100)

if st.button("🚀 GERAR IMAGEM AGORA"):
    if not briefing:
        st.error("Digite os dados primeiro!")
    else:
        with st.spinner(f"Criando arte final..."):
            try:
                # CORREÇÃO DO MODELO AQUI: models/gemini-1.5-flash
                model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
                
                prompt_task = f"Create a high-quality professional betting card image prompt for DALL-E 3. Expert: {expert_sel}. Color: {EXPERTS[expert_sel]['cor']}. Data: {briefing}. Format: {formato}. Style: Premium, dark background, neon lights, 3D white text, 15% safe zone."
                
                gemini_res = model.generate_content(prompt_task)
                
                size = "1024x1792" if "9:16" in formato else "1024x1024"
                res_img = openai_client.images.generate(
                    model="dall-e-3",
                    prompt=gemini_res.text,
                    size=size,
                    quality="hd",
                    n=1
                )
                
                img_url = res_img.data[0].url
                st.image(img_url, caption=f"Arte Final - {expert_sel}")
                
                img_data = requests.get(img_url).content
                st.download_button(label="📥 Baixar em HD", data=BytesIO(img_data).read(), file_name=f"card_{expert_sel}.png", mime="image/png")

            except Exception as e:
                st.error(f"Erro técnico: {e}")
