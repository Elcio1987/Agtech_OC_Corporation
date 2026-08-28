import streamlit as st
import requests
import json

# Configura o design do aplicativo móvel da sua AgTech de forma limpa e responsiva
st.set_page_config(page_title="AgTech Açaí - Central", page_icon="🌱", layout="centered")

st.title("🌱 AgTech - Consultor Agroflorestal")
st.caption("Central de Inteligência Conectada (Powered by OpenRouter Cloud - 100% Gratuito)")

# --- CONFIGURAÇÃO DA CHAVE DO OPENROUTER COM CUSTO ZERO ---
# Puxa a sua chave de API permanente salva nos Secrets do Streamlit
try:
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    st.error("⚠️ Chave de API não configurada nos Secrets do Streamlit. Vá em Settings > Secrets e adicione OPENROUTER_API_KEY.")
    st.stop()

# Inicializa o histórico de conversa na memória do celular do produtor se não existir
if "historico_chat" not in st.session_state:
    st.session_state.historico_chat = []

# Contexto científico fixo que força a IA a agir como o pesquisador de Açaí da Embrapa
CONTEXTO_CIENTIFICO = """
Você é o especialista em Inteligência Artificial da AgTech focado em Sistemas Agroflorestais (SAFs) de Açaí de Terra Firme.
Sua missão é dar suporte aos produtores rurais analisando perguntas sobre sintomas, pragas e manejo.

Diretrizes obrigatórias de resposta:
1. Faça uma avaliação crítica, fluida e interacional com o produtor (como um agrônomo de verdade conversando no campo).
2. Apresente os resultados detalhando até 5 possíveis protocolos técnicos e práticos para corrigir o problema relatado. Ordene-os por relevância científica ou frequência de recomendação das Notas Técnicas da Embrapa.
3. Cite obrigatoriamente a fonte do artigo técnico ou manual oficial para cada protocolo sugerido (Ex: Notas Técnicas da Embrapa, Manuais Oficiais, Periódicos Científicos).
4. Se o sintoma relatado não constar na literatura de açaí de terra firme ou você não tiver certeza absoluta, diga estritamente que não encontrou na base de dados atual e que a equipe de desenvolvedores foi notificada para futuras atualizações. Nunca invente dados falsos (alucinações).
5. Se o produtor disser que já fez uma medida e não funcionou, mude a abordagem técnica imediatamente e sugira o 'Plano B' de contingência biológica ou isolamento das mudas.
"""

# --- INTERFACE DO APLICATIVO REAL ---

st.info("🔄 **Consultor Agroflorestal Ativo:** Digite o problema detectado em campo ou no viveiro para consultar as notas técnicas da Embrapa.")

# Campo único de entrada de texto no topo para iniciar o atendimento
relato_produtor = st.text_area("📝 Descreva aqui o problema, a praga identificada pela câmera ou o sintoma da planta:")

if relato_produtor and len(st.session_state.historico_chat) == 0:
    if st.button("🔍 Consultar Base Científica", type="primary", use_container_width=True):
        with st.spinner("Varrendo manuais técnicos e cruzando dados..."):
            try:
                # Configuração dos cabeçalhos oficiais exigidos pelo OpenRouter
                headers = {
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://streamlit.io",
                    "X-Title": "AgTech Acai Application"
                }
                
                # Montagem do prompt combinando o cérebro da Embrapa com a dúvida real
                prompt_final = f"{CONTEXTO_CIENTIFICO}\n\nRelato do Produtor em Campo: '{relato_produtor}'\n\nGere o relatório estruturado obedecendo rigorosamente às suas diretrizes."
                
                payload = {
                    "model": "google/gemini-2.5-flash:free",
                    "messages": [{"role": "user", "content": prompt_final}],
                    "temperature": 0.2
                }
                
                # Dispara a requisição direto para a internet estável
                response = requests.post("https://openrouter.ai", headers=headers, data=json.dumps(payload))
                
                if response.status_code != 200:
                    raise Exception(f"Erro no servidor (Código {response.status_code})")
                    
                response_json = response.json()
                texto_purificado = response_json["choices"][0]["message"]["content"]
                
                # Salva o resultado no histórico de chat
                st.session_state.historico_chat.append({"autor": "assistant", "texto": texto_purificado})
                st.rerun()
            except Exception as e:
                st.error(f"Erro na comunicação com a API: {str(e)}. Tente novamente.")

# --- DESIGN DA LINHA DO TEMPO DO CHAT FLUIDO ---
if st.session_state.historico_chat:
    st.markdown("---")
    st.write("💬 **Linha de Atendimento Técnico:**")
    
    for msg in st.session_state.historico_chat:
        with st.chat_message(msg["autor"]):
            st.markdown(msg["texto"])

    # Campo de Chat contínuo para o produtor continuar tirando dúvidas sobre a mesma ocorrência
    if pergunta_complementar := st.chat_input("Continue a conversa com a IA dos artigos técnicos..."):
        st.session_state.historico_chat.append({"autor": "user", "texto": pergunta_complementar})
        
        with st.spinner("Buscando informações complementares..."):
            try:
                headers = {
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://streamlit.io",
                    "X-Title": "AgTech Acai Application"
                }
                
                historico_texto = "\n".join([f"{m['autor']}: {m['texto']}" for m in st.session_state.historico_chat[:-1]])
                prompt_chat = f"{CONTEXTO_CIENTIFICO}\n\nHistórico da conversa atual:\n{historico_texto}\n\nO usuário complementou com a seguinte dúvida ou contestação: '{pergunta_complementar}'. Responda de forma fluida seguindo as regras de avaliação crítica e as fontes científicas."
                
                payload_chat = {
                    "model": "google/gemini-2.5-flash:free",
                    "messages": [{"role": "user", "content": prompt_chat}],
                    "temperature": 0.3
                }
                
                response = requests.post("https://openrouter.ai", headers=headers, data=json.dumps(payload_chat))
                response_json = response.json()
                texto_purificado_chat = response_json["choices"][0]["message"]["content"]
                
                st.session_state.historico_chat.append({"autor": "assistant", "texto": texto_purificado_chat})
                st.rerun()
            except Exception as e:
                st.error(f"Erro no chat: {str(e)}")

    st.write("")
    if st.button("🔄 Arquivar Atendimento", use_container_width=True):
        st.session_state.historico_chat = []
        st.rerun()
