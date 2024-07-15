from langchain.chat_models import ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
import os


def chat_with(vector):
    print(f"Now chatting with the {vector}")
    print("Type pdf() at any time to select a different pdf")
    ollamaEmbeddings = OllamaEmbeddings(model="llama3")

    vector_path = f"./vector/my_data/{vector}"

    new_vector_store_connection = Chroma(
        persist_directory=vector_path,
        embedding_function=ollamaEmbeddings,
    )


    chat_model = ChatOllama(model="llama3", temperature=0.5)

    template = """Use this context to answer the question. Do not imagine anything. Use the context to know the information, which you can use to then form sentences. If query not at all in context, say \"The question does not seem to be about the policy documents. Please rephrase the question and try again.\"
    {context}
    Question: {question}
    Helpful Answer:"""

    prompt = PromptTemplate.from_template(template)

    chain = (
            {
                "context": new_vector_store_connection.as_retriever(),
                "question": RunnablePassthrough(),
            }
            | prompt
            | chat_model
    )

    while True:
        question = input("Enter question: ")

        if question == "pdf()":
            select_pdf()

        result = chain.invoke(question)
        print(result.content)


def select_pdf():
    i = 1
    pdf_dict = {}
    for pdf in os.listdir("flattened_pdfs"):
        pdf_dict[str(i)] = pdf[:-4]
        i += 1

    pdf_dict[str(i)] = "complete_text"[:-4]

    print("Choose the pdf you want to chat with:")
    for key, value in pdf_dict.items():
        print(f"{key}. {value}")
    print("Press any other key to exit")

    vector = input("Selection: ")

    if vector not in pdf_dict:
        print("Invalid Input, Exiting...")
        exit()

    vector = pdf_dict[vector]
    chat_with(vector)


select_pdf()