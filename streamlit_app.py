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
    scary_or_normal = random.choice(["scary", "sad", "normal"])
    sentence_type = f" {random.choice([1,2])} sentence. Each with {random.choice([5,6])} word"
    print(sentence_type)
    age = random.choice([7,8])
    print(age)
    fear_factor = random.choice(["dark", "death", "blood", "fear", "sad", "lonely","neutral tone"])
    print(fear_factor)
    # third_person = random.choice(["use pronouns. Use \"])
    prompt_modifier = f"\"Don't use quotes. Give a {scary_or_normal} answer. Make it {sentence_type}. Make it sound like {age}-year old girl. Use {fear_factor} in your sentence. Use simple words that a child would use. Don't quote Chauncey"
    print(prompt_modifier)
    # prompt_openai = f"respond to \""+ prompt_user + "\" with a scary answer. make it {sentence_type} make it sound like a 8 year old girl. use death in your response. use words that kids use."
    prompt_openai = f"Assume you are an 8 year old girl. You have a cute but scary stuff toy named Chauncey. Chauncey is sinister and lonely. I want to talk to it through you. Tell me what Chauncey says to you if I ask Chauncey \" "+ prompt_user + " " + prompt_modifier
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