import streamlit as st
import openai

st.title("Chatbot with OpenAI GPT")
st.caption("Made by wisdom")

with st.sidebar:
    st.markdown("[Get an OpenAI API key](http://platform.openai.com/account/api-key)")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
#st.write(st.secrets["nonexistent_key"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "g[t-3.5-turbo]"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "| ")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})