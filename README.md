# 🎈 Blank app template

A simple Streamlit app template for you to modify!

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
import streamlit as st
from openai import OpenAI

# 🔑 Coloca aqui a tua API Key
client = OpenAI(api_key="SUA_API_KEY")

st.set_page_config(page_title="Avaliador de Negócios de Saúde")

st.title("🧠 Avaliador de Negócios de Saúde")
st.write("Insere uma ideia de negócio e recebe uma análise completa.")

# 📥 Input do utilizador
descricao = st.text_area("Descreve o negócio de saúde:", height=150)

if st.button("Avaliar negócio"):
    if descricao:
        with st.spinner("A analisar..."):

            prompt = f"""
            És um especialista em gestão de negócios na área da saúde em Portugal.

            Analisa o seguinte negócio:

            1. Pontos positivos
            2. Pontos negativos
            3. Riscos
            4. Viabilidade
            5. Sugestões
            6. Monetização
            7. Nota final de 1 a 10

            Negócio: {descricao}
            """

            resposta = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            resultado = resposta.choices[0].message.content

        st.subheader("📊 Resultado da análise:")
        st.write(resultado)

    else:
        st.warning("Por favor, escreve uma descrição do negócio.")
