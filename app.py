import streamlit as st
import requests
import json
from PIL import Image
import io
import base64

# Configura o design do aplicativo móvel da sua AgTech com otimização de tráfego
st.set_page_config(page_title="AgTech Açaí - Local", page_icon="🌱", layout="centered")

st.title("🌱 AgTech - Consultor Agroflorestal")
st.caption("Monitoramento Autônomo & Inteligência Conectada (Powered by Llama 3.2 Vision)")

# --- CONFIGURAÇÃO INVISÍVEL VIA SECRETS DO STREAMLIT ---
try:
    URL_NGROK = st.secrets["URL_NGROK_LOCAL"]
except Exception:
    st.error("⚠️ Configuração pendente nos Secrets do Streamlit. Adicione URL_NGROK_LOCAL em Settings > Secrets.")
    st.stop()

# Inicializa o histórico de conversa na memória do celular do produtor se não existir
if "historico_chat" not in st.session_state:
    st.session_state.historico_chat = []

# Função para converter e comprimir a imagem pesada do celular
def converter_imagem_para_base64(uploaded_file):
    image = Image.open(uploaded_file)
    max_size = (512, 512) # Tamanho ideal focado em velocidade e nitidez para o Llama 3.2
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    buffered = io.BytesIO()
    image.convert("RGB").save(buffered, format="JPEG", quality=65)
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# --- INTERFACE DO APLICATIVO REAL ---

st.info("🔄 **Central Ativa:** Conectada ao Servidor Local. Aguardando fotos do campo.")

# Caixa única de Upload de Foto Real do Celular
foto_uploadeada = st.file_uploader("📸 Tire uma foto ou escolha da galeria do seu celular:", type=["jpg", "jpeg", "png"])

if foto_uploadeada and len(st.session_state.historico_chat) == 0:
    st.success("✅ Foto carregada na memória do aplicativo com sucesso!")
    
    if st.button("🔍 Enviar Foto para Diagnóstico Real no seu PC", type="primary", use_container_width=True):
        with st.spinner("Enviando imagem para o seu computador..."):
            try:
                img_base64_pura = converter_imagem_para_base64(foto_uploadeada)
                
                # ESTRUTURA OFICIAL E NATIVA DO OLLAMA VISION COMPLIENT 2026
                # Passa a imagem de forma nativa e pura pela API padrão do Llama
                payload = {
                    "model": "llama3.2-vision:latest",
                    "messages": [
                        {
                            "role": "user",
                            "content": "Analise cuidadosamente esta imagem do canteiro de açaí e gere um relatório técnico fluido e interacional com o produtor (como um agrônomo no campo). Apresente até 5 protocolos práticos baseados nas Notas Técnicas da Embrapa para corrigir o problema identificado e cite obrigatoriamente as fontes científicas.",
                            "images": [img_base64_pura]
                        }
                    ],
                    "stream": False,
                    "options": {
                        "temperature": 0.2
                    }
                }
                
                # ROTA DIRETA DA API DO OLLAMA: Envia direto para o motor de inteligência artificial
                url_final = f"{URL_NGROK.rstrip('/')}/api/chat"
                response = requests.post(url_final, json=payload, timeout=120)
                
                if response.status_code != 200:
                    raise Exception(f"O seu computador rejeitou a mensagem (Erro {response.status_code}). Detalhe: {response.text}")
                
                response_json = response.json()
                texto_purificado = response_json["message"]["content"]
                
                st.session_state.historico_chat.append({
                    "autor": "assistant", 
                    "texto": texto_purificado,
                    "foto_usuario": foto_uploadeada
                })
                st.rerun()
            except Exception as e:
                st.error(f"Erro na comunicação com o seu PC: {str(e)}. Certifique-se de que o ngrok está rodando na porta 11434.")

# --- DESIGN DA LINHA DO TEMPO DO CHAT FLUIDO ---
if st.session_state.historico_chat:
    st.markdown("---")
    st.write("💬 **Linha de Atendimento Técnico Local:**")
    
    for msg in st.session_state.historico_chat:
        with st.chat_message(msg["autor"]):
            st.markdown(msg["texto"])
            if "foto_usuario" in msg:
                st.image(msg["foto_usuario"], caption="📸 Imagem enviada ao servidor local", use_container_width=True)

    if pergunta_complementar := st.chat_input("Continue a conversa com o Llama do seu PC..."):
        st.session_state.historico_chat.append({"autor": "user", "texto": pergunta_complementar})
        
        with st.spinner("Consultando artigos locais..."):
            try:
                payload_chat = {
                    "model": "llama3.2-vision:latest",
                    "messages": [
                        {"role": "system", "content": "Você é o especialista em IA agroflorestal focado em Açaí de Terra Firme. Responda seguindo as diretrizes técnicas da Embrapa."},
                        {"role": "user", "content": pergunta_complementar}
                    ],
                    "stream": False,
                    "options": {
                        "temperature": 0.3
                    }
                }
                
                url_final = f"{URL_NGROK.rstrip('/')}/api/chat"
                response = requests.post(url_final, json=payload_chat, timeout=120)
                response_json = response.json()
                texto_purificado_chat = response_json["message"]["content"]
                
                st.session_state.historico_chat.append({
                    "autor": "assistant", 
                    "texto": texto_purificado_chat
                })
                st.rerun()
            except Exception as e:
                st.error(f"Erro no chat local: {str(e)}")

    st.write("")
    if st.button("🔄 Arquivar Atendimento", use_container_width=True):
        st.session_state.historico_chat = []
        st.rerun()
