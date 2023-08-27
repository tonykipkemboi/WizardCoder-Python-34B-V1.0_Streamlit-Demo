import random
import time
import streamlit as st
from gradio_client import Client


@st.cache_data
def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon.

    Args:
        emoji (str): name of the emoji, i.e. ":balloon:"
    """

    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


# --- UI Configurations --- #
st.set_page_config(page_title="WizardCoder-Python-34B-V1.0 Streamlit Demo 🎈",
                   page_icon=":llama:",
                   layout="wide")

icon(":llama:")

# Initialize your Gradio client
client = Client("http://47.103.63.15:50085/")

# Streamlit UI
st.title(':red[WizardCoder Streamlit Demo]', anchor=False)
st.caption(
    """
    :rainbow[No 🧢, it's hella slow but worth trying!]  | :rainbow[Follow me on 𝕏 [@tonykipkemboi](https://twitter.com/tonykipkemboi)]

    """
)
with st.expander(":red[About this app]"):
    col1, col2 = st.columns([1.5, 2])
    col2.write("""
            - WizardCoder 34B is based on Code Llama.
            
            - This Streamlit app using this [API](http://47.103.63.15:50085/).
             
            - WizardCoder-34B surpasses GPT-4, ChatGPT-3.5 and Claude-2 on HumanEval with 73.2% pass@1

            🖥️ [Gradio Demo](http://47.103.63.15:50085/)
             
            🏇 [Model Weights](https://huggingface.co/WizardLM/WizardCoder-Python-34B-V1.0)
            
            🏇 [Github](https://github.com/nlpxucan/WizardLM/tree/main/WizardCoder)

   
            """
               )
    col1.image("llama.png", width=300)

with st.expander(":red[Settings for :blue[Temperature] and :orange[Max_Tokens]]"):
    col1, col2 = st.columns(2)
    temperature = col1.slider(
        'Temperature', min_value=0.0, max_value=1.0, value=0.0, step=0.1)
    max_tokens = col2.slider('Max Tokens', min_value=1,
                             max_value=2048, value=2048, step=1)
st.divider()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if instruction := st.chat_input('Write Python code to...'):
    st.session_state.messages.append({"role": "user", "content": instruction})
    with st.chat_message("user"):
        st.markdown(instruction)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
    # Display assistant response in chat message container
    with st.status(":red[Running prediction...]", expanded=True) as status:
        st.write(":rainbow[This might take a few minutes...]")
        result = client.predict(
            instruction,
            temperature,
            max_tokens,
            api_name="/predict"
        )
        st.write(":rainbow[Appending output for display...]")
        full_response += result
        st.write(":rainbow[Done! 🎉]")
        if result:
            status.update(label="Complete!",
                          state="complete", expanded=False)
    message_placeholder.markdown(full_response)
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response})
else:
    st.info(':red[Enter your prompt]', icon="👇🏾")
