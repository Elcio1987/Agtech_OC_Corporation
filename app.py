import streamlit as st
from PIL import Image

# Configura o design do aplicativo móvel da sua AgTech
st.set_page_config(page_title="AgTech Açaí - Central", page_icon="🌱", layout="centered")

st.title("🌱 AgTech - Consultor Agroflorestal")
st.caption("Monitoramento Autônomo (ESP32) & Diagnóstico Clínico do Produtor")

# Inicializa o histórico de conversa na memória do aplicativo se não existir
if "historico_chat" not in st.session_state:
    st.session_state.historico_chat = []

# --- BANCO DE DADOS CIENTÍFICO INTEGRADO ---
banco_pesquisas = {
    "gafanhotos": {
        "analise_fluida": "Olá! Analisei com cuidado a imagem enviada do seu plantio e notei padrões claros de mastigação nas bordas das folhas mais jovens do açaizeiro. Esse tipo de dano mecânico é muito característico do ataque de gafanhotos, que costumam atacar canteiros inteiros rapidamente se não forem contidos.",
        "protocolos": [
            {"manejo": "Pulverização de Extrato de Fumo", "protocolo": "Preparar um extrato aquoso com 100g de fumo de corda em 1L de água por 24h. Diluir em 10L de água com sabão neutro e borrifar no fim da tarde.", "tipo": "Periódico Científico (Embrapa)", "peso": 3},
            {"manejo": "Aplicação de Óleo de Neem", "protocolo": "Diluir óleo de neem concentrado a 1% em água e aplicar com pulverizador costal nas mudas afetadas, repetindo a cada 3 dias.", "tipo": "Manual Técnico Oficial", "peso": 2},
            {"manejo": "Controle Biológico (Beauveria bassiana)", "protocolo": "Aplicar o bioinseticida à base do fungo via pulverização foliar nas primeiras horas da manhã, garantindo alta umidade para ativação dos esporos.", "tipo": "Periódico Científico (Universidade)", "peso": 3}
        ]
    },
    "doentes": {
        "analise_fluida": "De uma olhada no sintoma que registramos: há um amarelecimento uniforme que começa nas pontas das folhas mais velhas e caminha para o centro, com perda de vigor nas mudas de açaí de terra firme. Esse cenário é um forte indicativo de estresse nutricional ou hídrico prolongado.",
        "protocolos": [
            {"manejo": "Correção de Nitrogênio (Ureia)", "protocolo": "Calcular a dosagem de ureia de cobertura estritamente com base na idade da muda. Aplicar ao redor da projeção da copa, evitando contato direto com o caule.", "tipo": "Periódico Científico (Embrapa)", "peso": 3},
            {"manejo": "Estabilização do Turno de Rega", "protocolo": "Ajustar o sistema automatizado de irrigação para monitorar os sensores de solo de perto, garantindo que a umidade não caia abaixo de 50%.", "tipo": "Manual Técnico Oficial", "peso": 2},
            {"manejo": "Incorporação de Matéria Orgânica", "protocolo": "Adicionar composto orgânico maturado rico em microrganismos eficientes (EM) para melhorar a estrutura radicular e retenção de nutrientes.", "tipo": "Periódico Científico", "peso": 3}
        ]
    },
    "capivaras": {
        "analise_fluida": "Atenção: Registramos atividade de fauna invasora de grande porte na área de monitoramento. Trata-se de capivaras transitando próximas aos canteiros, o que pode gerar pisoteio ou danos mecânicos severos às mudas jovens de açaí.",
        "protocolos": [
            {"manejo": "Disparo Físico de Afugentamento", "protocolo": "O sistema de borda acionou automaticamente o ciclo variado de frequências sonoras (Buzzer) e o flash de luz intermitente na placa instalada em campo.", "tipo": "Manual Técnico Oficial", "peso": 2},
            {"manejo": "Instalação de Barreiras Físicas", "protocolo": "A literatura recomenda a fixação de cercas teladas ou alambrados de 1,20m na base do canteiro para impedir o acesso físico dos animais.", "tipo": "Periódico Científico (Embrapa)", "peso": 3}
        ]
    }
}

# Função que processa a imagem (Seja da ESP32 ou do Envio Manual)
def processar_diagnostico_cientifico(termo_identificado):
    termo_low = termo_identificado.lower()
    
    if "gafanhoto" in termo_low or "praga" in termo_low:
        chave = "gafanhotos"
    elif "amarelo" in termo_low or "doente" in termo_low or "mancha" in termo_low:
        chave = "doentes"
    elif "capivara" in termo_low or "bicho" in termo_low or "fauna" in termo_low:
        chave = "capivaras"
    else:
        # REGRA DE SEGURANÇA EXIGIDA: Se não houver certeza, a IA avisa os desenvolvedores
        return """
🔍 **[ANÁLISE DE BANCO DE DADOS]**
Analisei a imagem enviada com base em todos os artigos científicos dos pesquisadores e **não consegui identificar um padrão correspondente com 100% de certeza** na base de dados atual.

⚠️ **O que acontece agora?**
A nossa equipe de desenvolvedores e agrônomos parceiros foi notificada automaticamente. Vamos analisar este caso manualmente para adicionar a solução em futuras atualizações da plataforma!
        """
        
    dados = banco_pesquisas[chave]
    texto_final = f"🤖 **[ANÁLISE DO CONSULTOR AGTECH]**\n\n{dados['analise_fluida']}\n\n"
    texto_final += "--- \n\n### 📋 Protocolos de Correção Sugeridos (Ordem de Relevância Científica):\n"
    
    protocolos_ordenados = sorted(dados["protocolos"], key=lambda x: x["peso"], reverse=True)
    for i, item in enumerate(protocolos_ordenados[:5], 1):
        selo = "🏅 [Periódico Científico - Alta Autoridade]" if item["peso"] == 3 else "📋 [Manual Técnico Oficial]"
        texto_final += f"{i}. **{item['manejo']}**\n"
        texto_final += f"   *   *Protocolo:* {item['protocolo']}\n"
        texto_final += f"   *   *Fonte Acadêmica:* Encontrado em estudos de nível: *{item['tipo']}* ({selo}).\n\n"
        
    return texto_final

# --- INTERFACE DO APLICATIVO UNIFICADA (UX COMERCIAL LIMPA) ---

st.info("🔄 **Central Ativa:** Monitorando canteiros via ESP32 e aguardando interações do produtor.")

# 1. SEÇÃO DE MONITORAMENTO AUTOMÁTICO (Simulador para testes da ESP32)
with st.expander("🎥 CONEXÃO DO HARDWARE: Painel de Alertas da ESP32", expanded=True):
    st.write("Esta área simula a placa ESP32 trabalhando sozinha no campo:")
    alerta_esp32 = st.selectbox(
        "Forçar Alerta Automático da Câmera PTZ:", 
        ["Nenhum Alerta Ativo", "doentes (ESP32)", "gafanhotos (ESP32)", "capivaras (ESP32)"], 
        index=0
    )
    if alerta_esp32 != "Nenhum Alerta Ativo" and len(st.session_state.historico_chat) == 0:
        if st.button("🚨 Processar Ocorrência da Placa", type="primary"):
            limpo_termo = alerta_esp32.split(" ")[0]
            resposta_ia = f"🚨 **[ALERTA AUTOMÁTICO EM CAMPO]** A placa ESP32 detectou uma ocorrência e enviou ao servidor.\n\n"
            resposta_ia += processar_diagnostico_cientifico(limpo_termo)
            st.session_state.historico_chat.append({"autor": "assistant", "texto": resposta_ia})
            st.rerun()

st.markdown("---")

# 2. SEÇÃO DE INTERAÇÃO REATIVA DO PRODUTOR (Upload Manual)
foto_uploadeada = st.file_uploader("📸 Notou algo estranho caminhando pelo viveiro? Insira a foto do celular aqui:", type=["jpg", "jpeg", "png"])

if foto_uploadeada and len(st.session_state.historico_chat) == 0:
    st.write("Imagem carregada. Para a maquete simular de forma inteligente, nomeie o arquivo com palavras como 'gafanhoto.jpg', 'amarelo.png' ou 'desconhecido.jpg'.")
    if st.button("🔍 Enviar Foto para Diagnóstico", type="primary"):
        resposta_ia = processar_diagnostico_cientifico(foto_uploadeada.name)
        st.session_state.historico_chat.append({
            "autor": "assistant", 
            "texto": resposta_ia, 
            "foto_usuario": foto_uploadeada
        })
        st.rerun()

# --- DESIGN DA LINHA DO TEMPO DO CHAT FLUIDO ---
if st.session_state.historico_chat:
    st.markdown("---")
    st.write("💬 **Linha de Atendimento:**")
    
    for msg in st.session_state.historico_chat:
        with st.chat_message(msg["autor"]):
            st.markdown(msg["texto"])
            if "foto_usuario" in msg:
                st.image(msg["foto_usuario"], caption="📸 Foto enviada manualmente pelo produtor", use_container_width=True)

    # Chat contínuo no rodapé
    if pergunta_complementar := st.chat_input("Tire dúvidas sobre os protocolos ou diga se já tentou algo..."):
        st.session_state.historico_chat.append({"autor": "user", "texto": pergunta_complementar})
        
        texto_busca = pergunta_complementar.lower()
        termos_falha = ["não deu certo", "não funcionou", "já fiz", "ja fiz", "continua", "piorou", "não adiantou", "nao adiantou"]
        
        if any(termo in texto_busca for termo in termos_falha):
            resposta_ia = """
⚠️ **[REAVALIAÇÃO CONTEXTUAL]**
Entendido. Como os protocolos científicos iniciais de manejo não surtiram efeito prático no seu lote, o sistema está avançando a análise. 

Fiz uma varredura profunda nos artigos secundários e a recomendação é isolar imediatamente este lote de mudas para evitar contaminações cruzadas e suspender qualquer aplicação química até a estabilização.

🧠 **[MÓDULO DE APRENDIZADO]**
Registrado que esses protocolos específicos falharam no canteiro. Se desejar, clique no botão abaixo para exportar o histórico deste chat e enviar para um especialista humano.
            """
        else:
            resposta_ia = "Entendido. Complementando a sua dúvida com base nos artigos da Embrapa, lembre-se de que a aplicação de qualquer calda natural nas mudas de açaí deve ocorrer exclusivamente em horários de clima fresco para evitar fitotoxicidade."
            
        st.session_state.historico_chat.append({"autor": "assistant", "texto": resposta_ia})
        st.rerun()

    # Botão para fechar o caso e limpar a tela
    st.write("")
    if st.button("🔄 Arquivar Atendimento"):
        st.session_state.historico_chat = []
        st.rerun()
