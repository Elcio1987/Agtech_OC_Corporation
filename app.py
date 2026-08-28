import streamlit as st
import requests
import json
from PIL import Image
import io
import base64

# Configura o design do aplicativo móvel da sua AgTech com otimização de tráfego
st.set_page_config(page_title="AgTech Açaí - Local", page_icon="🌱", layout="centered")

st.title("🌱 AgTech - Consultor Agroflorestal")
st.caption("Monitoramento Autônomo & Inteligência Conectada (Powered by Seu PC Local & Llama)")

# --- CONFIGURAÇÃO INVISÍVEL VIA SECRETS DO STREAMLIT ---
try:
    URL_NGROK = st.secrets["URL_NGROK_LOCAL"]
    API_KEY = st.secrets["ANYTHINGLLM_API_KEY"]
except Exception:
    st.error("⚠️ Configuração pendente nos Secrets do Streamlit. Adicione URL_NGROK_LOCAL e ANYTHINGLLM_API_KEY em Settings > Secrets.")
    st.stop()

# Nome da sua pasta configurado de forma simples no AnythingLLM
SLUG_DA_SUA_PASTA = "agtech"

# Inicializa o histórico de conversa na memória do celular do produtor se não existir
if "historico_chat" not in st.session_state:
    st.session_state.historico_chat = []

# Função para converter e comprimir a imagem pesada do celular
def converter_imagem_para_base64(uploaded_file):
    image = Image.open(uploaded_file)
    max_size = (600, 600)
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
        with st.spinner("Enviando imagem para o seu computador e processando pelos artigos..."):
            try:
                img_base64 = converter_imagem_para_base64(foto_uploadeada)
                
                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                }
                
                # Prompt limpo e focado strictly nas regras da Embrapa
                prompt_comando = """
                Analise cuidadosamente a imagem que foi anexada a este atendimento e gere um relatório agroflorestal seguindo estas diretrizes obrigatórias:
                1. Faça uma avaliação crítica, fluida e interacional com o produtor (como um agrônomo de verdade conversando no campo).
                2. Apresente os resultados detalhando uma lista de no máximo 5 possíveis protocolos técnicos para corrigir o problema. Ordene-os por relevância científica.
                3. Cite obrigatoriamente de qual artigo ou manual da Embrapa você extraiu a informação e faça uma avaliação crítica se é um periódico sério ou cartilha educativa.
                4. Se não encontrar o problema nos artigos com certeza absoluta, diga estritamente que não encontrou na base de dados atual e que os desenvolvedores vão atualizar o sistema. Nunca invente dados falsos.
                """
                
                # AJUSTE DE ENGENHARIA MULTIMODAL: Passando o texto e os dados da imagem em estruturas separadas aceitas pela API
                payload = {
                    "message": prompt_comando,
                    "mode": "query",
                    "attachments": [
                        {
                            "name": "foto_campo.jpg",
                            "mimeType": "image/jpeg",
                            "content": img_base64
                        }
                    ]
                }
                
                # ROTA COMPATÍVEL COM O SISTEMA DESKTOP INDUSTRIAL
                url_final = f"{URL_NGROK.rstrip('/')}/api/v1/workspace/{SLUG_DA_SUA_PASTA}/chat"
                response = requests.post(url_final, headers=headers, json=payload, timeout=90)
                
                if response.status_code != 200:
                    raise Exception(f"O seu computador rejeitou a mensagem (Erro {response.status_code}). Detalhe: {response.text}")
                
                response_json = response.json()
                
                if "textResponse" in response_json:
                    texto_purificado = response_json["textResponse"]
                elif "response" in response_json:
                    texto_purificado = response_json["response"]
                else:
                    texto_purificado = str(response_json)
                
                st.session_state.historico_chat.append({
                    "autor": "assistant", 
                    "texto": texto_purificado,
                    "foto_usuario": foto_uploadeada
                })
                st.rerun()
            except Exception as e:
                st.error(f"Erro na comunicação com o seu PC: {str(e)}. Certifique-se de que o ngrok e o AnythingLLM estão ligados em casa.")

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
                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                }
                
                url_final = f"{URL_NGROK.rstrip('/')}/api/v1/workspace/{SLUG_DA_SUA_PASTA}/chat"
                payload_chat = {
                    "message": pergunta_complementar,
                    "mode": "query"
                }
                
                response = requests.post(url_final, headers=headers, json=payload_chat, timeout=90)
                response_json = response.json()
                
                if "textResponse" in response_json:
                    texto_purificado_chat = response_json["textResponse"]
                elif "response" in response_json:
                    texto_purificado_chat = response_json["response"]
                else:
                    texto_purificado_chat = str(response_json)
                
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
