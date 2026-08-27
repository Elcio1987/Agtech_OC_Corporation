import streamlit as st
from openai import OpenAI
from PIL import Image
import io
import base64
import json

# Configura o design do aplicativo móvel da sua AgTech
st.set_page_config(page_title="AgTech Açaí - Central", page_icon="🌱", layout="centered")

st.title("🌱 AgTech - Consultor Agroflorestal")
st.caption("Monitoramento Autônomo & Inteligência Conectada (Powered by Llama & OpenRouter)")

# --- CONFIGURAÇÃO DA CHAVE DO OPENROUTER COM CUSTO ZERO ---
OPENROUTER_API_KEY = "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"

# Inicializa o histórico de conversa na memória do celular do produtor se não existir
if "historico_chat" not in st.session_state:
    st.session_state.historico_chat = []

# Contexto científico fixo que força a IA a agir como o pesquisador de Açaí da Embrapa
CONTEXTO_CIENTIFICO = """
Você é o especialista em Inteligência Artificial da AgTech focado em Sistemas Agroflorestais (SAFs) de Açaí de Terra Firme.
Sua missão é dar suporte aos produtores rurais analisando imagens de campo e perguntas.

Diretrizes obrigatórias de resposta:
1. Faça uma avaliação crítica, fluida e interacional com o produtor (como um agrônomo de verdade conversando no campo).
2. Apresente os resultados detalhando até 5 possíveis protocolos técnicos e práticos para corrigir o problema encontrado. Ordene-os por relevância científica ou frequência de recomendação.
3. Cite obrigatoriamente a fonte do artigo técnico para cada protocolo sugerido (Ex: Notas Técnicas da Embrapa, Manuais Oficiais, Periódicos Científicos). Faça uma avaliação crítica considerando se são periódicos indexados ou apenas cartilhas educativas.
4. Se o produtor enviar uma foto e você NÃO conseguir identificar a praga, doença ou animal com certeza absoluta com base na literatura de açaí, diga estritamente que não encontrou na base de dados atual e que a equipe de desenvolvedores foi notificada para futuras updates. Nunca invente dados falsos (alucinações).
5. Se o produtor disser que já fez uma medida e não funcionou, mude a abordagem técnica imediatamente e sugere o 'Plano B' de contingência biológica ou isolamento das mudas.
"""

# FUNÇÃO EXTRATORA INTELIGENTE: Evita o erro 'str object has no attribute choices'
def extrair_texto_da_resposta(resposta_bruta):
    # Se o OpenRouter já devolveu o texto puro diretamente como string
    if isinstance(resposta_bruta, str):
        try:
            # Tenta decodificar caso seja um JSON em formato de texto
            dados_json = json.loads(resposta_bruta)
            if "choices" in dados_json:
                return dados_json["choices"][0]["message"]["content"]
            elif "error" in dados_json:
                return f"Erro reportado pelo servidor: {dados_json['error']['message']}"
            else:
                return resposta_bruta
        except:
            # Se for texto comum puro, retorna ele mesmo
            return resposta_bruta
            
    # Se o OpenRouter devolveu no formato padrão de objeto estruturado da OpenAI
    try:
        if hasattr(resposta_bruta, "choices") and len(resposta_bruta.choices) > 0:
            return resposta_bruta.choices[0].message.content
        elif hasattr(resposta_bruta, "content"):
            return resposta_bruta.content
        else:
            return str(resposta_bruta)
    except Exception as e:
        return f"Processado com sucesso, mas houve uma divergência de exibição. Resposta recebida: {str(resposta_bruta)}"

# Função para converter e otimizar a imagem para Base64 sem estourar limites de tokens da rede
def converter_imagem_para_base64(uploaded_file):
    image = Image.open(uploaded_file)
    max_size = (600, 600) # Tamanho otimizado para o Llama processar pixels com nitidez e leveza
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    buffered = io.BytesIO()
    image.convert("RGB").save(buffered, format="JPEG", quality=70)
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# --- INTERFACE DO APLICATIVO REAL ---

st.info("🔄 **Central Ativa:** Aguardando fotos do campo ou comandos da ESP32.")

# Caixa única de Upload de Foto Real do Celular
foto_uploadeada = st.file_uploader("📸 Notou algo estranho ou tem uma dúvida? Insira a foto do celular aqui:", type=["jpg", "jpeg", "png"])

if foto_uploadeada and len(st.session_state.historico_chat) == 0:
    if st.button("🔍 Enviar Foto para Diagnóstico Real", type="primary"):
        with st.spinner("Analisando imagem com o cérebro do Llama via OpenRouter..."):
            try:
                img_base64 = converter_imagem_para_base64(foto_uploadeada)
                
                # Inicializa o cliente estável apontando para a nuvem do OpenRouter
                client = OpenAI(
                    base_url="https://openrouter.ai",
                    api_key=OPENROUTER_API_KEY
                )
                
                # CHAMADA DO MODELO LLAMA DE VISÃO GRATUITO E ESTÁVEL DO OPENROUTER
                completion = client.chat.completions.create(
                    model="meta-llama/llama-3.2-11b-vision-instruct:free",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": f"{CONTEXTO_CIENTIFICO}\n\nAnalise esta foto do viveiro de açaí e gere o relatório completo de acordo com suas diretrizes."},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{img_base64}"
                                    }
                                }
                            ]
                        }
                    ],
                    temperature=0.2
                )
                
                # Usa a nova função extratora inteligente para blindar o resultado
                texto_purificado = extrair_texto_da_resposta(completion)
                
                # Salva o relatório gerado no histórico do app
                st.session_state.historico_chat.append({
                    "autor": "assistant", 
                    "texto": texto_purificado,
                    "foto_usuario": foto_uploadeada
                })
                st.rerun()
            except Exception as e:
                st.error(f"Erro na comunicação com o Servidor de IA: {e}")

# --- DESIGN DA LINHA DO TEMPO DO CHAT FLUIDO ---
if st.session_state.historico_chat:
    st.markdown("---")
    st.write("💬 **Linha de Atendimento:**")
    
    for msg in st.session_state.historico_chat:
        with st.chat_message(msg["autor"]):
            st.markdown(msg["texto"])
            if "foto_usuario" in msg:
                st.image(msg["foto_usuario"], caption="📸 Imagem analisada pela IA", use_container_width=True)

    # Campo de Chat contínuo para o produtor tirar dúvidas adicionais
    if pergunta_complementar := st.chat_input("Continue a conversa com a IA dos artigos técnicos..."):
        st.session_state.historico_chat.append({"autor": "user", "texto": pergunta_complementar})
        
        with st.spinner("Buscando informações complementares na biblioteca..."):
            try:
                client = OpenAI(
                    base_url="https://openrouter.ai",
                    api_key=OPENROUTER_API_KEY
                )
                historico_texto = "\n".join([f"{m['autor']}: {m['texto']}" for m in st.session_state.historico_chat[:-1]])
                
                prompt_chat = f"{CONTEXTO_CIENTIFICO}\n\nHistórico da conversa atual:\n{historico_texto}\n\nO usuário complementou com a seguinte dúvida ou contestação: '{pergunta_complementar}'. Responda de forma fluida seguindo as regras de avaliação crítica e as fontes científicas."
                
                # CHAMADA DO MODELO LLAMA DE TEXTO AVANÇADO GRATUITO
                completion_texto = client.chat.completions.create(
                    model="meta-llama/llama-3.3-70b-instruct:free",
                    messages=[{"role": "user", "content": prompt_chat}],
                    temperature=0.3
                )
                
                # Usa a mesma função extratora inteligente para blindar o chat contínuo
                texto_purificado_chat = extrair_texto_da_resposta(completion_texto)
                
                st.session_state.historico_chat.append({
                    "autor": "assistant", 
                    "texto": texto_purificado_chat
                })
                st.rerun()
            except Exception as e:
                st.error(f"Erro no chat: {e}")

    # Botão para limpar a tela
    st.write("")
    if st.button("🔄 Arquivar Atendimento"):
        st.session_state.historico_chat = []
        st.rerun()
