import os
import streamlit as st
# from country_list import countries_for_language
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from answer import answer, top_5_ques
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate


st.set_page_config(
    page_title="ConstitutionBot",
    page_icon="\U0001F4D6",
    layout="wide"
)

st.header("Indian Constitution AI Assistant")
st.markdown("#### I am an AI assistant, here to help you understand, learn and query on India's Constitution!")
with st.sidebar:
    st.write("Top 10 question recommendations:")
    if st.button("click"):
        questions = top_5_ques('India')
        st.write(questions)
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant","content": "Ask anything about the Indian Constitution!"}
    ]

if "chat_memory" not in st.session_state.keys():
        st.session_state["chat_memory"] = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
memory = st.session_state["chat_memory"]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
user_prompt = st.chat_input()

if user_prompt is not None:
    st.session_state.messages.append({"role": "user","content": user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)


if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Loading..."):
            ai_response= answer(user_prompt,'India',memory)
            st.write(ai_response)
    new_ai_message = {"role":"assistant", "content":ai_response}
    st.session_state.messages.append(new_ai_message)