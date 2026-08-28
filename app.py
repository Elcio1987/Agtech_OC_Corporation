import streamlit as st
import requests
import json

# Configura o design do aplicativo móvel da sua AgTech de forma limpa e responsiva
st.set_page_config(page_title="AgTech Açaí - Central", page_icon="🌱", layout="centered")

st.title("🌱 AgTech - Consultor Agroflorestal")
st.caption("Central de Inteligência Conectada (Powered by OpenRouter Cloud)")

# --- CONFIGURAÇÃO DA CHAVE DO OPENROUTER COM CUSTO ZERO ---
try:
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    st.error("⚠️ Chave de API não configurada nos Secrets do Streamlit. Vá em Settings > Secrets e adicione OPENROUTER_API_KEY.")
    st.stop()

# Inicializa o histórico de conversa na memória do celular do produtor se não existir
if "historico_chat" not in st.session_state:
    st.session_state.historico_chat = []

# Contexto científico rígido que força a IA a priorizar periódicos revisados por pares
CONTEXTO_CIENTIFICO = """
Você é o especialista sênior em Inteligência Artificial Agroflorestal focado em SAFs de Açaí de Terra Firme.
Sua missão é dar suporte crítico e prático aos produtores rurais com base em literatura científica de alta autoridade.

Diretrizes obrigatórias de resposta:
1. Adote um tom fluido, interacional e altamente profissional (como um agrônomo experiente conversando diretamente com o produtor no campo). Evite respostas cruas ou em tópicos simplórios de uma única linha.
2. Apresente os resultados detalhando protocolos técnicos e práticos profundos, porém objetivos, para mitigar o problema identificado pela câmera da ESP32.
3. Ordene as recomendações estritamente pelo peso científico das fontes: dê prioridade máxima para artigos publicados em periódicos indexados e revisados por pares (Ex: Revistas Científicas de Renome, Pesquisas de Universidades Federais). Em seguida, liste cartilhas educativas ou manuais de campo (Ex: Manuais Técnicos da Embrapa), fazendo uma avaliação crítica e clara sobre o peso de cada fonte citada.
4. Se o problema ou comportamento detectado não constar na literatura científica de açaí com certeza absoluta, informe estritamente que o evento não foi localizado na base de dados acadêmica atual e que a equipe de engenharia da AgTech foi notificada para futuras atualizações na IA. Nunca invente dados (alucinações).
5. Se o produtor relatar que uma medida preventiva falhou, mude a abordagem técnica imediatamente, sugerindo o 'Plano B' de contingência biológica, manejo integrado ou isolamento imediato do lote de mudas.
"""

# --- SIMULADOR DE GATILHO DA ESP32 EM CAMPO ---
st.markdown("### 📡 Central de Alertas de Campo (Simulador ESP32 Cam)")
st.write("Abaixo estão as ocorrências em tempo real detectadas pela IA de visão computacional instalada nos viveiros.")

col1, col2, col3 = st.columns(3)
with col1:
    gatilho_pulgão = st.button("🪲 Alerta: Pulgão Detectado", use_container_width=True)
with col2:
    gatilho_mancha = st.button("🍂 Alerta: Mancha Foliar", use_container_width=True)
with col3:
    gatilho_animal = st.button("🐖 Alerta: Invasão de Animais", use_container_width=True)

# Define o problema com base no botão clicado pela placa/simulador
problema_detectado = ""
if gatilho_pulgão:
    problema_detectado = "A câmera da ESP32 identificou foco de infestação de pulgões (insetos sugadores) nas folhas jovens do lote de mudas de açaí."
elif gatilho_mancha:
    problema_detectado = "A câmera da ESP32 identificou lesões necróticas marrons com halos amarelados compatíveis com ataque de fungos (Mancha Foliar) no viveiro de açaí."
elif gatilho_animal:
    problema_detectado = "A câmera da ESP32 detectou a presença de animais invasores de médio porte quebrando e pisoteando as linhas de plantio do sistema agroflorestal."

# Executa o processamento científico se a ESP32 disparar um alerta e o chat estiver vazio
if problema_detectado and len(st.session_state.historico_chat) == 0:
    st.warning(f"🚨 **Notificação Enviada ao Produtor:** {problema_detectado}")
    with st.spinner("IA processando relatório com base nos periódicos revisados por pares..."):
        try:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://streamlit.io",
                "X-Title": "AgTech Acai Application"
            }
            
            prompt_final = f"{CONTEXTO_CIENTIFICO}\n\n🚨 ALERTA DA ESP32 EM CAMPO: '{problema_detectado}'\n\nGere o relatório agroflorestal completo e estruturado obedecendo rigorosamente às diretrizes de peso científico e fontes."
            
            payload = {
                "model": "google/gemini-2.5-flash:free",
                "messages": [{"role": "user", "content": prompt_final}],
                "temperature": 0.2
            }
            
            response = requests.post("https://openrouter.ai", headers=headers, data=json.dumps(payload))
            
            if response.status_code != 200:
                raise Exception(f"Erro no servidor do OpenRouter (Código {response.status_code})")
                
            response_json = response.json()
            texto_purificado = response_json["choices"][0]["message"]["content"]
            
            st.session_state.historico_chat.append({"autor": "assistant", "texto": texto_purificado})
            st.rerun()
        except Exception as e:
            st.error(f"Erro na comunicação com a API: {str(e)}. Verifique se a sua chave nos Secrets está correta.")

# --- LINHA DO TEMPO INTERATIVA DO ATENDIMENTO ---
if st.session_state.historico_chat:
    st.markdown("---")
    st.write("💬 **Linha de Atendimento Agroflorestal Ativa:**")
    
    for msg in st.session_state.historico_chat:
        with st.chat_message(msg["autor"]):
            st.markdown(msg["texto"])

    # Permite o produtor conversar de forma fluida para tirar mais dúvidas com o especialista
    if pergunta_complementar := st.chat_input("Tire suas dúvidas ou conteste o plano de manejo com o consultor científico..."):
        st.session_state.historico_chat.append({"autor": "user", "texto": pergunta_complementar})
        
        with st.spinner("Consultando literatura acadêmica complementar..."):
            try:
                headers = {
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://streamlit.io",
                    "X-Title": "AgTech Acai Application"
                }
                
                historico_texto = "\n".join([f"{m['autor']}: {m['texto']}" for m in st.session_state.historico_chat[:-1]])
                prompt_chat = f"{CONTEXTO_CIENTIFICO}\n\nHistórico da ocorrência atual:\n{historico_texto}\n\nO produtor rural complementou com a seguinte dúvida ou contestação técnica: '{pergunta_complementar}'. Responda de forma fluida seguindo as regras de avaliação crítica e pesos científicos das fontes."
                
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
    if st.button("🔄 Arquivar Ocorrência e Limpar Tela", use_container_width=True):
        st.session_state.historico_chat = []
        st.rerun()
