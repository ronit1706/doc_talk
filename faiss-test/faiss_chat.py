import os
import faiss
import numpy as np
from langchain.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough

# Load FAISS index
index = faiss.read_index("faiss_index.index")

# Load document texts
embedding_dir = "embeddings"
docs = []
for file in os.listdir(embedding_dir):
    if file.endswith("_docs.txt"):
        with open(os.path.join(embedding_dir, file), 'r') as f:
            docs.extend(f.readlines())


def chat_with_faiss():
    print("Now chatting with the FAISS index...")
    print("Type pdf() at any time to select a different pdf")

    chat_model = ChatOllama(model="llama3", temperature=0.5)

    template = """Use this context to answer the question. Do not imagine anything. Use the context to know the information, which you can use to then form sentences. If query not at all in context, say "The question does not seem to be about the policy documents. Please rephrase the question and try again."
    {context}
    Question: {question}
    Helpful Answer:"""

    prompt = PromptTemplate.from_template(template)

    def retrieve_context(question):
        # Generate embedding for the question
        question_embedding = ollamaEmbeddings.embed_document([question])

        # Perform FAISS search
        D, I = index.search(np.array(question_embedding), k=3)

        # Retrieve corresponding documents
        context = "\n".join([docs[i] for i in I[0]])
        return context

    chain = (
            {
                "context": retrieve_context,
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
    print("FAISS index is already selected for chatting.")
    chat_with_faiss()


select_pdf()