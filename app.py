import streamlit as st

# Configura o título e o design do aplicativo móvel
st.set_page_config(page_title="AgTech Açaí", page_icon="🌱", layout="centered")

st.title("🌱 AgTech - Sistema Agroflorestal")
st.subheader("Central de Monitoramento e Diagnóstico")

# Inicializa o histórico de conversa se não existir
if "historico_chat" not in st.session_state:
    st.session_state.historico_chat = []

# Função avançada que simula a tomada de decisão da IA lendo os PDFs
def consultar_artigos(categoria, pergunta_usuario, e_primeira_msg=False):
    # Banco de conhecimento dos pesquisadores (Plano A e Plano B para cada praga)
    banco_conhecimento = {
        "gafanhotos": {
            "plano_A": "A aplicação biológica de óleo de neem a 1% ou extrato aquoso de fumo no fim da tarde. Fonte: [Embrapa Notas Técnicas](https://embrapa.br).",
            "plano_B": "Como o óleo de neem não resolveu, os artigos sugerem o controle mecânico rigoroso (catação) nas primeiras horas da manhã ou, em casos severos, a aplicação de bioinseticidas à base do fungo *Beauveria bassiana*. Evite defensivos químicos para não afetar o solo. Fonte: [Manual de Defesa Fitossanitária](https://embrapa.br)."
        },
        "doentes": {
            "plano_A": "Sintoma de Folhas Amarelas identificado. Estudos indicam estresse hídrico ou deficiência de Nitrogênio em terra firme. Verifique a irrigação e aplique ureia de cobertura se necessário. Fonte: [Manual de Nutrição do Açaizeiro](https://embrapa.br/busca-de-publicacoes).",
            "plano_B": "Se a adubação nitrogenada e a água não reverteram o amarelamento, os pesquisadores alertam para a possibilidade de nematoides ou fungos radiculares (como *Fusarium*). Recomenda-se suspender a adubação química e aplicar matéria orgânica rica em microrganismos benéficos para recuperar as raízes. Fonte: [Patologia do Açaizeiro](https://embrapa.br)."
        },
        "capivaras": {
            "plano_A": "Presença de fauna invasora registrada. O sistema acionou o som e o flash noturno intermitente na ESP32 física para afugentamento. Fonte: [Manejo de Fauna SAFs](https://embrapa.br).",
            "plano_B": "Se os animais se habituaram ao som e ao flash, a recomendação técnica dos artigos é a instalação física de cercas teladas na base do viveiro ou o uso de repelentes olfativos naturais nas bordas do plantio. Fonte: [Embrapa Manejo](https://embrapa.br)."
        },
        "saudaveis": {
            "plano_A": "Mudas identificadas como saudáveis. O ciclo de irrigação automática continua ativo. Fonte: [Manejo Hidrico do Açaí](https://embrapa.br).",
            "plano_B": "Tudo certo com as plantas. Continue acompanhando os relatórios gerados automaticamente pela ESP32."
        }
    }
    
    # 1. Se for o alerta inicial disparado pela câmera (Entrega o Plano A automaticamente)
    if e_primeira_msg:
        return f"""
📢 **[ALERTA DA CÂMERA]** Ocorrência registrada: `{categoria.upper()}`.

📚 **Recomendação Inicial dos Pesquisadores (Plano A):**
{banco_conhecimento[categoria]["plano_A"]}
        """
    
    # 2. Se for uma resposta do produtor conversando com a IA
    else:
        texto_pergunta = pergunta_usuario.lower()
        
        # Identifica se o produtor disse que a medida não deu certo ou já fez
        termos_negativos = ["não deu certo", "não funcionou", "já fiz", "ja fiz", "continua", "piorou", "nao resolveu"]
        reclamou_do_plano_A = any(termo in texto_pergunta for termo in termos_negativos)
        
        if reclamou_do_plano_A:
            return f"""
⚠️ **[AJUSTE DE ESTRATÉGIA COM BASE NO SEU FEEDBACK]**
Entendido. Como a primeira ação recomendada não resolveu o problema no campo, a IA buscou nos artigos científicos uma **alternativa secundária (Plano B)**:

📋 **Manejo de Contingência:**
{banco_conhecimento[categoria]["plano_B"]}

*💡 Caso os sintomas persistam por mais de 5 dias, o sistema sugere exportar o relatório para avaliação direta de um pesquisador parceiro.*
            """
        else:
            # Resposta comum para outras perguntas do chat
            return f"Entendido. Para complementar o manejo de `{categoria}`, certifique-se de que os sensores de solo estejam marcando acima de 50% de umidade e evite aplicar qualquer calda sob o sol quente. Fonte: [Repositório Técnico AgTech](https://embrapa.br)."

# --- INTERFACE GRÁFICA ---

st.info("📢 **Status do Sensor:** Monitorando área do produtor cadastrado.")
categoria_simulada = st.selectbox("Simular Registro da Câmera (Para Testes):", ["saudaveis", "doentes", "capivaras", "gafanhotos"], index=1)

# Inicializa a tela com o diagnóstico automático e a primeira solução (Plano A)
if len(st.session_state.historico_chat) == 0:
    alerta_inicial = consultar_artigos(categoria_simulada, "", e_primeira_msg=True)
    st.session_state.historico_chat.append({"autor": "assistant", "texto": alerta_inicial})

st.markdown("---")
st.write("💬 **Histórico de Atendimento:**")

# Desenha o chat linear na tela
for mensagem in st.session_state.historico_chat:
    with st.chat_message(mensagem["autor"]):
        st.markdown(mensagem["texto"])

# Campo de entrada de texto no rodapé estilo WhatsApp
if pergunta := st.chat_input("Converse com a IA (Ex: 'Já fiz isso e não deu certo' ou faça uma pergunta)..."):
    # Exibe a frase do produtor
    st.session_state.historico_chat.append({"autor": "user", "texto": pergunta})
    
    # Processa a resposta inteligente (Verifica se ele reclamou da primeira solução)
    resposta_ia = consultar_artigos(categoria_simulada, pergunta, e_primeira_msg=False)
    st.session_state.historico_chat.append({"autor": "assistant", "texto": resposta_ia})
    
    st.rerun()

# Botão para limpar o chat quando encerrar o chamado
if len(st.session_state.historico_chat) > 1:
    st.write("")
    if st.button("🔄 Encerrar Ocorrência (Limpar Atendimento)"):
        st.session_state.historico_chat = []
        st.rerun()


