import streamlit as st
from openai import OpenAI
import random

st.title("Ask Chauncey")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         markdown_user = message["content"].replace("respond to \"", "")
#         markdown_user = markdown_user.replace("\" with a scary answer. make it into 2 5 word sentences. make it sound like a 8 year old girl. use death in your response. use words that kids use.", "")
#         # st.markdown(message["content"])
#         st.markdown(markdown_user)
#         print("*"*40, message["content"])

if prompt := st.chat_input("Hi"):
    prompt_user = prompt
    sentence_type = f" {random.choice([1,2])} sentence. Each with {random.choice([5,6,7])} word"
    print(sentence_type)
    age = random.choice([7,8,9])
    print(age)
    fear_factor = random.choice(["dark", "death", "blood", "fear", "sad", "lonely"])
    print(fear_factor)
    prompt_modifier = f"\" with a scary answer. Make it {sentence_type}. Make it sound like {age}-year old girl. Use {fear_factor} in your sentence. Use simple words that a child would use"
    print(prompt_modifier)
    # prompt_openai = f"respond to \""+ prompt_user + "\" with a scary answer. make it {sentence_type} make it sound like a 8 year old girl. use death in your response. use words that kids use."
    prompt_openai = f"Assume there's an 8 year old girl. She has a cute but scary stuff toy named Chauncey. I want to chat with it. Chauncey is sinister and lonely. Respond as the girl to \"Ask Chauncey "+ prompt_user + prompt_modifier
    print(prompt_openai)
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