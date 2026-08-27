import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configura o design do aplicativo móvel da sua AgTech
st.set_page_config(page_title="AgTech Açaí - Central", page_icon="🌱", layout="centered")

st.title("🌱 AgTech - Consultor Agroflorestal")
st.caption("Monitoramento Autônomo & Inteligência Conectada (Powered by Gemini API)")

# --- CONFIGURAÇÃO DA CHAVE DO GEMINI REAl ---
# Substitua o texto abaixo pela chave que você copiou do Google AI Studio
GOOGLE_API_KEY = "AQ.Ab8RN6K189zHeh_cK_F78wLHa0aMnjCjRlMaG2wCpvQbrPtiXw"

genai.configure(api_key=GOOGLE_API_KEY)

# Inicializa o histórico de conversa na memória se não existir
if "historico_chat" not in st.session_state:
    st.session_state.historico_chat = []

# Contexto científico fixo que força a IA a agir como o pesquisador de Açaí da Embrapa
CONTEXTO_CIENTIFICO = """
Você é o especialista em Inteligência Artificial da AgTech focado em Sistemas Agroflorestais (SAFs) de Açaí de Terra Firme.
Sua missão é dar suporte aos produtores rurais analisando imagens de campo e perguntas.

Diretrizes obrigatórias de resposta:
1. Faça uma avaliação crítica, fluida e interacional com o produtor (como um agrônomo de verdade conversando no campo).
2. Apresente os resultados detalhando até 5 possíveis protocolos técnicos e práticos para corrigir o problema encontrado.
3. Cite obrigatoriamente a fonte do artigo técnico (Ex: Notas Técnicas da Embrapa, Manuais Oficiais, Periódicos Científicos).
4. Se o produtor enviar uma foto e você NÃO conseguir identificar a praga, doença ou animal com certeza absoluta com base na literatura de açaí, diga estritamente que não encontrou na base de dados atual e que a equipe de desenvolvedores foi notificada para futuras atualizações. Nunca invente dados falsos (alucinações).
5. Se o produtor disser que já fez uma medida e não funcionou, mude a abordagem técnica imediatamente e sugere o 'Plano B' de contingência biológica ou isolamento das mudas.
"""

# --- INTERFACE DO APLICATIVO REAL ---

st.info("🔄 **Central Ativa:** Aguardando fotos do campo ou comandos da ESP32.")

# Caixa única de Upload de Foto Real do Celular
foto_uploadeada = st.file_uploader("📸 Notou algo estranho ou tem uma dúvida? Insira a foto do celular aqui:", type=["jpg", "jpeg", "png"])

if foto_uploadeada and len(st.session_state.historico_chat) == 0:
    imagem_real = Image.open(foto_uploadeada)
    
    if st.button("🔍 Enviar Foto para Diagnóstico Real", type="primary"):
        with st.spinner("Analisando imagem com a base científica..."):
            try:
                # Aciona o modelo de visão avançado do Gemini (capaz de ver fotos e ler textos)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Monta a pergunta estruturada unindo a imagem aos critérios de negócio
                pergunta = [CONTEXTO_CIENTIFICO, "Analise esta foto tirada do viveiro de açaí e gere o relatório completo estruturado de acordo com as suas diretrizes.", imagem_real]
                
                response = model.generate_content(pergunta)
                
                # Salva o resultado real no histórico de chat
                st.session_state.historico_chat.append({
                    "autor": "assistant", 
                    "texto": response.text, 
                    "foto_usuario": foto_uploadeada
                })
                st.rerun()
            except Exception as e:
                st.error(f"Erro na comunicação com a API do Google: {e}")

# --- DESIGN DA LINHA DO TEMPO DO CHAT FLUIDO ---
if st.session_state.historico_chat:
    st.markdown("---")
    st.write("💬 **Linha de Atendimento:**")
    
    for msg in st.session_state.historico_chat:
        with st.chat_message(msg["autor"]):
            st.markdown(msg["texto"])
            if "foto_usuario" in msg:
                st.image(msg["foto_usuario"], caption="📸 Imagem analisada pela IA", use_container_width=True)

    # Campo de Chat contínuo para o produtor continuar tirando dúvidas sobre a mesma ocorrência
    if pergunta_complementar := st.chat_input("Continue a conversa com a IA dos artigos técnicos..."):
        st.session_state.historico_chat.append({"autor": "user", "texto": pergunta_complementar})
        
        with st.spinner("Buscando informações complementares..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Para manter o contexto da conversa vivo, passamos o histórico básico no prompt
                historico_texto = "\n".join([f"{m['autor']}: {m['texto']}" for m in st.session_state.historico_chat[:-1]])
                
                prompt_chat = f"{CONTEXTO_CIENTIFICO}\n\nHistórico da conversa atual:\n{historico_texto}\n\nO usuário complementou com a seguinte dúvida ou contestação: '{pergunta_complementar}'. Responda de forma fluida seguindo as regras de avaliação crítica e as fontes científicas."
                
                response = model.generate_content(prompt_chat)
                st.session_state.historico_chat.append({"autor": "assistant", "texto": response.text})
                st.rerun()
            except Exception as e:
                st.error(f"Erro no chat: {e}")

    # Botão para limpar a tela
    st.write("")
    if st.button("🔄 Arquivar Atendimento"):
        st.session_state.historico_chat = []
        st.rerun()
