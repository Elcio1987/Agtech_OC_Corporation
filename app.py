import streamlit as st
from PIL import Image

# Configura o design do aplicativo móvel da sua AgTech
st.set_page_config(page_title="AgTech Açaí - Central", page_icon="🌱", layout="centered")

st.title("🌱 AgTech - Consultor Agroflorestal")
st.caption("Monitoramento Autônomo & Diagnóstico Clínico do Produtor")

# Inicializa o histórico de conversa na memória do aplicativo se não existir
if "historico_chat" not in st.session_state:
    st.session_state.historico_chat = []

# --- BANCO DE DADOS CIENTÍFICO INTEGRADO (Simulando a IA real processando a foto de forma invisível) ---
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
    }
}

# Função que gera a resposta fluida + ranking de protocolos
def processar_imagem_de_forma_autonoma(nome_arquivo):
    # Na IA real, o processador de imagem decide a praga sozinho pelo nome do arquivo ou conteúdo.
    # Criamos esse filtro apenas para a simulação ficar inteligente de acordo com o teste.
    nome_low = nome_arquivo.lower()
    
    if "gafanhoto" in nome_low or "inseto" in nome_low or "praga" in nome_low:
        chave = "gafanhotos"
    elif "amarelo" in nome_low or "doente" in nome_low or "mancha" in nome_low:
        chave = "doentes"
    else:
        # REGRA DE SEGURANÇA EXIGIDA: Se não houver certeza, a IA não força nenhuma resposta falsa
        return """
🔍 **[ANÁLISE DE BANCO DE DADOS]**
Analisei a imagem enviada com base em todos os artigos científicos dos pesquisadores e **não consegui identificar um padrão correspondente com 100% de certeza** na base de dados atual.

⚠️ **O que acontece agora?**
A nossa equipe de desenvolvedores e agrônomos parceiros foi notificada automaticamente. Vamos analisar este caso manualmente para adicionar a solução em futuras atualizações da plataforma!
        """
        
    dados = banco_pesquisas[chave]
    
    # 1. Monta a explicação fluida e interacional com o produtor
    texto_final = f"🤖 **[ANÁLISE DO CONSULTOR AGTECH]**\n\n{dados['analise_fluida']}\n\n"
    texto_final += "--- \n\n### 📋 Protocolos de Correção Sugeridos (Ordem de Relevância Científica):\n"
    
    # 2. Organiza e lista os protocolos detalhados e os artigos encontrados (Limitado ao Top 5)
    protocolos_ordenados = sorted(dados["protocolos"], key=lambda x: x["peso"], reverse=True)
    
    for i, item in enumerate(protocolos_ordenados[:5], 1):
        selo = "🏅 [Periódico Científico - Alta Autoridade]" if item["peso"] == 3 else "📋 [Manual Técnico Oficial]"
        texto_final += f"{i}. **{item['manejo']}**\n"
        texto_warning = f"   *   *Protocolo:* {item['protocolo']}\n"
        texto_final += f"   *   *Fonte Acadêmica:* Encontrado em estudos de nível: *{item['tipo']}* ({selo}).\n\n"
        
    return texto_final

# --- INTERFACE DO APLICATIVO EXTREMAMENTE LIMPA (UX SEM BOTÕES DE CATEGORIAS) ---

st.info("🔄 **Central Ativa:** Aguardando fotos do campo para análise científica.")

# Caixa única de Upload de Foto - Sem abas, sem seletores complexos
foto_uploadeada = st.file_uploader("📸 Encontrou um problema ou dúvida no viveiro? Insira a foto aqui:", type=["jpg", "jpeg", "png"])

if foto_uploadeada and len(st.session_state.historico_chat) == 0:
    # Mostra a foto enviada pelo produtor na interface na hora
    imagem = Image.open(foto_uploadeada)
    
    # Para o teste da maquete ser inteligente: Diga aos seus amigos para renomearem a foto no celular
    # Exemplo de nomes de arquivo para testar: "gafanhoto.jpg", "folha_amarela.png" ou "desconhecido.jpg"
    if st.button("🔍 Enviar Foto para Diagnóstico", type="primary"):
        resposta_ia = processar_imagem_de_forma_autonoma(foto_uploadeada.name)
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
                st.image(msg["foto_usuario"], caption="📸 Foto enviada pelo produtor", use_container_width=True)

    # Chat contínuo no rodapé para continuar a conversa fiada
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
