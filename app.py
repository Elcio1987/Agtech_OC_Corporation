import streamlit as st
import requests
import json
from PIL import Image
import io
import base64

# Configura o design do aplicativo móvel da sua AgTech
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

# --- ATENÇÃO PRODUTOR: CONFIGURAÇÃO DO NOME DA PASTA ---
# Substitua o texto abaixo pelo nome interno (slug) que você viu na engrenagem da sua pasta
# Exemplos comuns: "manejo-acai", "manejo_acai", "acai", "agtech"
SLUG_DA_SUA_PASTA = "agtech"

# Inicializa o histórico de conversa na memória do celular do produtor se não existir
if "historico_chat" not in st.session_state:
    st.session_state.historico_chat = []

# Função para converter e otimizar a imagem para enviar ao seu computador
def converter_imagem_para_base64(uploaded_file):
    image = Image.open(uploaded_file)
    max_size = (600, 600)
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    buffered = io.BytesIO()
    image.convert("RGB").save(buffered, format="JPEG", quality=75)
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# --- INTERFACE DO APLICATIVO REAL ---

st.info("🔄 **Central Ativa:** Conectada ao Servidor Local. Aguardando fotos do campo.")

# Caixa única de Upload de Foto Real do Celular
foto_uploadeada = st.file_uploader("📸 Encontrou algo estranho no viveiro? Insira a foto do celular aqui:", type=["jpg", "jpeg", "png"])

if foto_uploadeada and len(st.session_state.historico_chat) == 0:
    if st.button("🔍 Enviar Foto para Diagnóstico Real no seu PC", type="primary"):
        with st.spinner("Enviando imagem para o seu computador e processando pelos artigos..."):
            try:
                img_base64 = converter_imagem_para_base64(foto_uploadeada)
                
                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                }
                
                prompt_comando = f"""
                [Análise de Imagem anexada via Base64: data:image/jpeg;base64,{img_base64}]
                
                Instruções obrigatórias para sua resposta:
                1. Faça uma avaliação crítica, fluida e interacional com o produtor com base na foto e nos artigos de açaí.
                2. Apresente os resultados detalhando uma lista de no máximo 5 possíveis protocolos técnicos para corrigir o problema.
                3. Cite obrigatoriamente de qual artigo ou manual da Embrapa você extraiu a informação e faça uma avaliação crítica se é um periódico sério ou cartilha educativa.
                4. Se não encontrar o problema nos artigos com certeza absoluta, diga estritamente que não encontrou na base de dados atual e que os desenvolvedores vão atualizar o sistema. Nunca invente dados falsos.
                """
                
                payload = {
                    "message": prompt_comando,
                    "mode": "query"
                }
                
                # ROTA DE WORKSPACE RÍGIDA: Garante o direcionamento correto para os PDFs
                url_final = f"{URL_NGROK.rstrip('/')}/api/v1/workspaces/{SLUG_DA_SUA_PASTA}/chat"
                response = requests.post(url_final, headers=headers, json=payload, timeout=60)
                
                if response.status_code != 200:
                    raise Exception(f"O seu computador rejeitou a mensagem (Erro {response.status_code}). Detalhe: {response.text}")
                
                response_json = response.json()
                
                # Captura de forma flexível as variações de resposta do AnythingLLM Desktop
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
                
                url_final = f"{URL_NGROK.rstrip('/')}/api/v1/workspaces/{SLUG_DA_SUA_PASTA}/chat"
                payload_chat = {
                    "message": pergunta_complementar,
                    "mode": "query"
                }
                
                response = requests.post(url_final, headers=headers, json=payload_chat, timeout=60)
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
    if st.button("🔄 Arquivar Atendimento"):
        st.session_state.historico_chat = []
        st.rerun()
