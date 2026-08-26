import streamlit as st

# Configura o título e o design do aplicativo móvel
st.set_page_config(page_title="AgTech Açaí", page_icon="🌱", layout="centered")

st.title("🌱 AgTech - Sistema Agroflorestal")
st.subheader("Central de Monitoramento e Diagnóstico")

# --- SIMULAÇÃO DE BANCO DE DADOS INVISÍVEL ---
# O ID da placa agora roda escondido no sistema, vinculado ao cadastro do produtor
ID_PLACA_OCULTO = "ESP32_VIVEIRO_PRODUTOR_JOAO"

# Inicializa o histórico de conversa na memória do celular do produtor se não existir
if "historico_chat" not in st.session_state:
    st.session_state.historico_chat = []

# Função que simula a busca científica nos artigos dos pesquisadores
def consultar_artigos(categoria, pergunta_usuario):
    solucoes = {
        "gafanhotos": "De acordo com o Manual de Manejo do Açaí (Embrapa), o ataque de gafanhotos em mudas exige a aplicação de óleo de neem a 1% ou extrato aquoso de fumo no fim da tarde. Fonte: [Embrapa Notas Técnicas](https://embrapa.br).",
        "doentes": "Sintoma fitossanitário identificado (Folhas Amarelas). Estudos da Embrapa indicam estresse hídrico ou deficiência de Nitrogênio em terra firme. Fonte: [Manual de Nutrição do Açaizeiro](https://embrapa.br).",
        "capivaras": "Presença de fauna invasora de grande porte registrada. O sistema acionou a resposta imediata de som e flash noturno na ESP32 física para afugentamento biológico. Fonte: [Manejo de Fauna SAFs](https://embrapa.br).",
        "saudaveis": "Mudas identificadas como saudáveis pelo sensor de imagem. O ciclo de irrigação automática continua ativo e monitorando. Fonte: [Manejo Hidrico do Açaí](https://embrapa.br)."
    }
    
    # Se for a primeira mensagem, traz o diagnóstico da câmera + solução do artigo
    if not st.session_state.historico_chat:
        resposta_inicial = f"""
        🤖 **[DIAGNÓSTICO DA CÂMERA EM TEMPO REAL]**
        A IA de imagem registrou uma ocorrência de: `{categoria.upper()}`.
        
        📚 **Recomendação dos Pesquisadores:**
        {solucoes.get(categoria)}
        """
        return resposta_inicial
    
    # Se for uma pergunta de continuação do chat:
    else:
        # Aqui no futuro o Llama 3.2 usará os metadados e os PDFs para responder contextualmente
        return f"Com base nos artigos científicos da sua biblioteca, para responder à sua dúvida sobre *'{pergunta_usuario}'*, recomenda-se seguir rigidamente as dosagens recomendadas pelos pesquisadores para evitar a fitotoxicidade na muda jovem de açaí. Fonte consultada: [Repositório Técnico AgTech](https://embrapa.br)."

# --- INTERFACE GRÁFICA SEM ID DA PLACA (UX LIMPA) ---

# Simulador do Alerta da ESP32 (Fica no topo como contexto)
st.info(f"📢 **Status do Sensor:** Monitorando área do produtor cadastrado.")
categoria = st.selectbox("Simular Registro da Câmera (Para Testes):", ["saudaveis", "doentes", "capivaras", "gafanhotos"], index=3)

st.markdown("---")
st.write("💬 **Conversa com o Especialista Científico:**")

# Exibe todo o histórico da conversa na tela como se fosse um chat de mensagens
for mensagem in st.session_state.historico_chat:
    with st.chat_message(mensagem["autor"]):
        st.markdown(mensagem["texto"])

# Campo de texto estilo chat no rodapé para o usuário continuar perguntando
if pergunta := st.chat_input("Faça uma pergunta ou tire uma dúvida sobre o problema..."):
    
    # Se for a PRIMEIRA interação, gera o relatório do artigo antes
    if not st.session_state.historico_chat:
        resposta_diagnostico = consultar_artigos(categoria, "")
        st.session_state.historico_chat.append({"autor": "assistant", "texto": resposta_diagnostico})
    
    # Adiciona a pergunta do produtor ao chat
    st.session_state.historico_chat.append({"autor": "user", "texto": pergunta})
    
    # Puxa a resposta contextualizada da IA lendo os artigos
    resposta_ia = consultar_artigos(categoria, pergunta)
    st.session_state.historico_chat.append({"autor": "assistant", "texto": resposta_ia})
    
    # Atualiza a tela para exibir as novas mensagens imediatamente
    st.rerun()

# Botão auxiliar para o produtor resetar o chat quando resolver o problema
if st.session_state.historico_chat:
    st.write("")
    if st.button("🔄 Encerrar Ocorrência (Limpar Histórico)"):
        st.session_state.historico_chat = []
        st.rerun()

