import streamlit as st

# Configura o título e o ícone na tela do celular
st.set_page_config(page_title="AgTech Açaí", page_icon="🌱", layout="centered")

st.title("🌱 AgTech - Sistema Agroflorestal")
st.subheader("Painel do Produtor: Monitoramento Autônomo")

# Função que simula o processamento dos artigos científicos dos pesquisadores
def processar_alerta(id_placa, categoria, duvida):
    solucoes = {
        "gafanhotos": "De acordo com o Manual de Manejo do Açaí (Embrapa), o ataque de gafanhotos em mudas exige a aplicação de óleo de neem a 1% ou extrato aquoso de fumo no fim da tarde.",
        "doentes": "Sintoma fitossanitário identificado. Estudos indicam estresse hídrico ou deficiência de Nitrogênio. Verifique se o sensor de solo está abaixo de 50% e aplique ureia se necessário.",
        "capivaras": "Presença de fauna invasora de grande porte registrada. O sistema acionou a resposta imediata de som e flash noturno na ESP32 física para afugentamento biológico.",
        "saudaveis": "Mudas identificadas como saudáveis pelo sensor de imagem. O ciclo de irrigação automática continua ativo e monitorando."
    }
    
    relatorio = f"""
    ### 📊 [RELATÓRIO CIENTÍFICO GERADO]
    * **Identificação do Dispositivo:** `{id_placa}`
    * **Diagnóstico da IA de Imagem:** `{categoria.upper()}`
    
    ➡️ **Manejo Recomendado (Base Científica):**
    {solucoes.get(categoria)}
    """
    
    if duvida:
        relatorio += f"\n\n💬 **Resposta à sua dúvida complementar ('{duvida}'):**\nPara essa ação específica, os artigos dos pesquisadores recomendam calibrar a dosagem biológica conforme o tamanho da muda."
        
    return relatorio

# Cria os campos visuais interativos
id_placa = st.text_input("ID da Placa ESP32", value="ESP32_VIVEIRO_01")
categoria = st.selectbox("O que a câmera da ESP32 registrou?", ["saudaveis", "doentes", "capivaras", "gafanhotos"], index=3)
duvida = st.text_input("Conversar com a IA (Faça uma pergunta complementar ao problema)")

if st.button("Processar Alerta e Buscar Solução", type="primary"):
    resultado = processar_alerta(id_placa, categoria, duvida)
    st.markdown(resultado)
