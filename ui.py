import streamlit as st
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
import os

st.title("Policy Wordings Chatbot")

def initialize_vector_store(vector):
    ollamaEmbeddings = OllamaEmbeddings(model="llama3")
    vector_path = f"./vector/my_data/{vector}"

    new_vector_store_connection = Chroma(
        persist_directory=vector_path,
        embedding_function=ollamaEmbeddings,
    )
    return new_vector_store_connection

def get_response(vector_store_connection, question):
    chat_model = ChatOllama(model="llama3", temperature=0.5)

    template = """Use this context to answer the question. Do not imagine anything. Use the context to know the information, which you can use to then form sentences. If query not at all in context, say \"The question does not seem to be about the policy documents. Please rephrase the question and try again.\"
    {context}
    Question: {question}
    Helpful Answer:"""

    prompt = PromptTemplate.from_template(template)

    chain = (
            {
                "context": vector_store_connection.as_retriever(),
                "question": RunnablePassthrough(),
            }
            | prompt
            | chat_model
    )
    result = chain.invoke(question)
    return result.content

# Sidebar for PDF selection
def select_pdf():
    pdf_files = os.listdir("flattened_pdfs")
    selected_pdf = st.sidebar.selectbox("Choose the PDF you want to chat with:", pdf_files)
    return selected_pdf

if "selected_pdf" not in st.session_state:
    st.session_state.selected_pdf = select_pdf()
else:
    st.session_state.selected_pdf = st.sidebar.selectbox("Choose the PDF you want to chat with:", os.listdir("flattened_pdfs"), index=os.listdir("flattened_pdfs").index(st.session_state.selected_pdf))

vector_store_connection = initialize_vector_store(st.session_state.selected_pdf[:-4])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Chat with policy documents"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = get_response(vector_store_connection, prompt)
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})