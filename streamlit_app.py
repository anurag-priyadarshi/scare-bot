import streamlit as st
from openai import OpenAI

st.title("Ask Chauncey")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        markdown_user = message["content"].replace("respond to \"", "")
        markdown_user = markdown_user.replace("\" with a scary answer. make it into 2 5 word sentences. make it sound like a 8 year old girl. use death in your response. use words that kids use.", "")
        # st.markdown(message["content"])
        st.markdown(markdown_user)
        print("*"*40, message["content"])

if prompt := st.chat_input("Hi"):
    prompt_user = prompt
    prompt_openai = "respond to \""+ prompt_user + "\" with a scary answer. make it into 2 5 word sentences. make it sound like a 8 year old girl. use death in your response. use words that kids use."
    st.session_state.messages.append({"role": "user", "content": prompt_openai})
    with st.chat_message("user"):
        st.markdown(prompt_user)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
        print("#"*40, st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response})