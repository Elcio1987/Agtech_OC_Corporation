import streamlit as st
from PIL import Image

# Configura o design do aplicativo móvel da sua AgTech
st.set_page_config(page_title="AgTech Açaí - Central", page_icon="🌱", layout="centered")

st.title("🌱 AgTech - Consultor Agroflorestal")
st.caption("Monitoramento Autônomo & Diagnóstico Clínico do Produtor")

# Inicializa o histórico de conversa na memória do aplicativo se não existir
if "historico_chat" not in st.session_state:
    st.session_state.historico_chat = []

# --- BANCO DE CONHECIMENTO CIENTÍFICO SIMULADO (Com Pesos Acadêmicos e Frequência) ---
# Peso 3 = Periódico Científico Revisado por Pares (Ex: Embrapa Pesquisa)
# Peso 2 = Normas Técnicas Oficiais / Manuais de Zoneamento
# Peso 1 = Cartilhas Educativas / Manuais Práticos de Extensão
banco_pesquisas = {
    "gafanhotos": [
        {"manejo": "Aplicação de extrato aquoso de fumo no fim da tarde", "freq": 24, "tipo": "Periódico Científico (Embrapa)", "peso": 3},
        {"manejo": "Borrifação de óleo de neem concentrado a 1%", "freq": 18, "tipo": "Manual Técnico Oficial", "peso": 2},
        {"manejo": "Uso de bioinseticidas à base do fungo Beauveria bassiana", "freq": 11, "tipo": "Periódico Científico (Universidade)", "peso": 3},
        {"manejo": "Catação mecânica manual nas primeiras horas da manhã", "freq": 9, "tipo": "Cartilha Educativa (Emater)", "peso": 1},
        {"manejo": "Instalação de barreiras físicas (telas de proteção) nas mudas", "freq": 6, "tipo": "Cartilha Educativa", "peso": 1},
        {"manejo": "Aplicação de defensivo químico químico-sintético tradicional", "freq": 2, "tipo": "Nota Comercial (Não Recomendado)", "peso": 0} # Será filtrado por critério científico
    ],
    "doentes": [
        {"manejo": "Correção da adubação nitrogenada com ureia via cobertura", "freq": 31, "tipo": "Periódico Científico (Embrapa)", "peso": 3},
        {"manejo": "Estabilização do turno de rega (manter solo acima de 50% de umidade)", "freq": 22, "tipo": "Manual Técnico Oficial", "peso": 2},
        {"manejo": "Incorporação de matéria orgânica biológica com microrganismos eficientes (EM)", "freq": 14, "tipo": "Periódico Científico", "peso": 3},
        {"manejo": "Aplicação de biofertilizante líquido caseiro rico em potássio", "freq": 8, "tipo": "Cartilha Educativa", "peso": 1},
        {"manejo": "Poda sanitária imediata das folhas severamente amareladas", "freq": 5, "tipo": "Cartilha Educativa", "peso": 1},
        {"manejo": "Uso de fungicidas sistêmicos pesados direto no solo", "freq": 1, "tipo": "Nota Comercial (Evitar em SAFs)", "peso": 0}
    ],
    "pulgoes": [
        {"manejo": "Pulverização de calda de sabão neutro a 1% em água morna", "freq": 27, "tipo": "Manual Técnico Oficial", "tempo": 2},
        {"manejo": "Introdução biológica de predadores naturais (como joaninhas no viveiro)", "freq": 19, "tipo": "Periódico Científico (Embrapa)", "peso": 3},
        {"manejo": "Aplicação de extrato concentrado de alho e pimenta nas folhas", "freq": 15, "tipo": "Cartilha Educativa", "peso": 1},
        {"manejo": "Podas de condução para melhorar a circulação de ar entre as mudas", "freq": 12, "tipo": "Manual Técnico", "peso": 2},
        {"manejo": "Uso de armadilhas adesivas amarelas para captura de insetos alados", "freq": 7, "tipo": "Cartilha Educativa", "peso": 1}
    ]
}

# Função que executa a avaliação crítica e gera o Ranking de até 5 sugestões
def gerar_ranking_cientifico(categoria):
    if categoria not in banco_pesquisas:
        return "Nenhuma recomendação acadêmica encontrada para este quadro nos arquivos atuais."
    
    artigos = banco_pesquisas[categoria]
    
    # Avaliação Crítica: Filtra e ordena combinando a maior frequência com o maior peso acadêmico
    artigos_ordenados = sorted(artigos, key=lambda x: (x["peso"], x["freq"]), reverse=True)
    
    # Regra de Negócio: Limita rigidamente a exibição ao TOP 5 para evitar fadiga de decisão
    top_5 = artigos_ordenados[:5]
    
    texto_resposta = f"### 📚 Avaliação Crítica da Biblioteca de Pesquisas\n"
    texto_resposta += f"Varredura concluída. Foram analisados múltiplos documentos técnicos dos pesquisadores. Aqui estão as **5 principais estratégias testadas e recomendadas**, ordenadas por rigor científico e frequência de sucesso:\n\n"
    
    for i, item in enumerate(top_5, 1):
        # Destaca o peso acadêmico visualmente na lista
        selo = "🏅 [Alta Autoridade Acadêmica]" if item["peso"] == 3 else "📋 [Diretriz Técnica Oficial]" if item["peso"] == 2 else "🚜 [Prática de Extensão Rural]"
        texto_resposta += f"{i}. **{item['manejo']}**\n"
        texto_resposta += f"   *   *Fonte:* {item['tipo']} | *Frequência de Recomendação:* {item['freq']} artigos técnicos.\n"
        texto_resposta += f"   *   *Rigor:* {selo}\n\n"
        
    if len(artigos) > 5:
        texto_resposta += "💡 *Existem outras alternativas secundárias registradas nos PDFs. Caso necessite de mais opções à medida que o tratamento avance, basta solicitar aqui no chat.*"
        
    return texto_resposta

# --- INTERFACE DO APLICATIVO (UX LIMPA E TOTALMENTE REATIVA) ---

st.info("🔄 **Central Ativa:** Aguardando alertas da placa ou interações manuais do produtor.")

# Duas abas de entrada: Uma para os alertas mecânicos e outra para o produtor enviar do campo
aba_monitoramento, aba_envio_manual = st.tabs(["🎥 Alertas do Sensor (ESP32)", "📱 Envio Manual do Produtor"])

with aba_monitoramento:
    categoria_simulada = st.selectbox(
        "Simular Alerta Recebido da Câmera PTZ:", 
        ["Nenhum Alerta Ativo", "doentes", "gafanhotos", "pulgoes"], 
        index=0
    )
    if categoria_simulada != "Nenhum Alerta Ativo" and len(st.session_state.historico_chat) == 0:
        if st.button("🚨 Processar Alerta Automático da Placa", type="primary"):
            resposta_inicial = f"🚨 **[ALERTA AUTOMÁTICO EM CAMPO]** Câmera registrou ocorrência de `{categoria_simulada.upper()}`.\n\n"
            resposta_inicial += gerar_ranking_cientifico(categoria_simulada)
            st.session_state.historico_chat.append({"autor": "assistant", "texto": resposta_inicial})
            st.rerun()

with aba_envio_manual:
    st.write("Encontrou algo que a câmera não pegou enquanto andava pelo plantio? Registre aqui:")
    foto_uploadeada = st.file_uploader("Enviar foto da folha ou praga suspeita:", type=["jpg", "jpeg", "png"])
    
    # Se o produtor subir uma foto, simula a interação reativa com a IA de Imagem e de Texto juntas
    if foto_uploadeada and len(st.session_state.historico_chat) == 0:
        categoria_manual = st.radio("Selecione o sintoma visual aproximado para a IA analisar:", ["doentes", "gafanhotos", "pulgoes"])
        if st.button("🔍 Enviar Foto para Diagnóstico Científico"):
            imagem = Image.open(foto_uploadeada)
            
            resposta_manual = f"📱 **[DIAGNÓSTICO VIA SOLICITAÇÃO DO PRODUTOR]**\n"
            resposta_manual += f"Foto analisada com sucesso pela IA de Imagem. Quadro identificado como compatível com: `{categoria_manual.upper()}`.\n\n"
            resposta_manual += gerar_ranking_cientifico(categoria_manual)
            
            st.session_state.historico_chat.append({
                "autor": "assistant", 
                "texto": resposta_manual, 
                "foto_usuario": foto_uploadeada
            })
            st.rerun()

# --- DESIGN DA LINHA DO TEMPO DO CHAT ---
if st.session_state.historico_chat:
    st.markdown("---")
    st.write("💬 **Linha de Atendimento Técnico:**")
    
    for msg in st.session_state.historico_chat:
        with st.chat_message(msg["autor"]):
            st.markdown(msg["texto"])
            if "foto_usuario" in msg:
                st.image(msg["foto_usuario"], caption="📸 Foto enviada manualmente pelo produtor via aplicativo", use_container_width=True)

    # Chat contínuo no rodapé para novas perguntas baseadas no mesmo problema
    if pergunta_complementar := st.chat_input("Converse com a IA (Ex: 'Já fiz a primeira opção e não adiantou' ou faça uma pergunta)..."):
        st.session_state.historico_chat.append({"autor": "user", "texto": pergunta_complementar})
        
        texto_busca = pergunta_complementar.lower()
        termos_falha = ["não deu certo", "não funcionou", "já fiz", "ja fiz", "continua", "piorou", "não adiantou", "nao adiantou"]
        
        if any(termo in texto_busca for termo in termos_falha):
            # Traz um feedback dinâmico mostrando que está varrendo as alternativas abaixo do TOP 5
            resposta_ia = """
⚠️ **[REAVALIAÇÃO DE ESTRATÉGIA COM BASE NO SEU HISTÓRICO]**
Entendido. O sistema registrou que as principais linhas de tratamento falharam no seu lote. 

Fazendo uma varredura profunda nos artigos secundários da biblioteca, os pesquisadores alertam para manejo de resistência. Recomenda-se avançar para o uso de extratos combinados ou isolamento das mudas afetadas. 

🧠 **[MÓDULO DE APRENDIZADO CONTÍNUO]**
Esta falha foi computada para personalizar os próximos diagnósticos do seu canteiro. O sistema sugere gerar um PDF deste atendimento para enviar diretamente a um agrônomo parceiro.
            """
        else:
            resposta_ia = "Entendido. Para complementar essa dúvida específica, os artigos científicos da Embrapa recomendam que a umidade do solo esteja estabilizada e que qualquer aplicação de calda biológica ocorra exclusivamente sob condições de clima ameno (fim de tarde)."
            
        st.session_state.historico_chat.append({"autor": "assistant", "texto": resposta_ia})
        st.rerun()

    # Botão para fechar o caso e limpar a tela
    st.write("")
    if st.button("🔄 Arquivar Ocorrência (Limpar Painel)"):
        st.session_state.historico_chat = []
        st.rerun()
