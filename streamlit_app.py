import os
import google.generativeai as genai
import streamlit as st

# 1. Configuração da página (DEVE SER A PRIMEIRA FUNÇÃO STREAMLIT)
st.set_page_config(
    page_title="Agente BlinkClinic", page_icon="🩺", layout="centered"
)

# 2. Configurar a API do Gemini de forma segura
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error(
        "❌ A variável de ambiente GEMINI_API_KEY não foi encontrada. "
        "Configura-a antes de correr a aplicação."
    )
    st.stop()  # Interrompe a execução se não houver API Key
else:
    genai.configure(api_key=api_key)

# 3. Inicializar o modelo e o histórico de chat na sessão do Streamlit
# Usamos o 'gemini-1.5-flash' que é ideal para respostas rápidas e chats
if "chat" not in st.session_state:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="Tu és o Agente BlinkClinic, um assistente virtual especializado em ajudar profissionais de saúde a treinar cenários clínicos e responder a dúvidas médicas com base em evidência.",
    )
    # Inicializa um chat com memória de contexto
    st.session_state.chat = model.start_chat(history=[])

# 4. Interface Utilizador (UI)
st.title("🩺 Agente BlinkClinic")
st.caption("Powered by Gemini 1.5 Flash")
st.write("Treina o agente fazendo perguntas ou simulando cenários clínicos.")

# Separador visual
st.markdown("---")

# 5. Mostrar o histórico de mensagens anteriores
for message in st.session_state.chat.history:
    # Converter o papel do modelo ('model' -> 'assistant') para o Streamlit
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 6. Caixa de Input estilo Chat (mais moderna que o text_area antigo)
if user_input := st.chat_input(
    "Escreve a tua pergunta ou cenário clínico aqui..."
):

    # Mostra imediatamente a mensagem do utilizador no ecrã
    with st.chat_message("user"):
        st.markdown(user_input)

    # Gera a resposta do modelo
    with st.chat_message("assistant"):
        with st.spinner("A analisar cenário..."):
            try:
                # Envia a mensagem mantendo o contexto da conversa
                response = st.session_state.chat.send_message(user_input)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"❌ Erro ao contactar o modelo: {e}")

# 7. Botão lateral para limpar o histórico, se necessário
with st.sidebar:
    st.header("Opções")
    if st.button("Limpar Histórico de Chat"):
        st.session_state.chat.history = []
        st.rerun()