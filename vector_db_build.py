import os
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
import concatenator

for file in os.listdir("extracted_text"):
    if file == ".DS_Store":
        continue
    else:
        print(f"Now embedding {file}"[:-8]+"...")
        loaded = TextLoader(f"extracted_text/{file}")
        raw_doc = loaded.load()

        text_splitter = CharacterTextSplitter(chunk_size=1200, chunk_overlap=0.5)
        split_docs = text_splitter.split_documents(raw_doc)

        ollamaEmbeddings = OllamaEmbeddings(model="llama3")

        vectorstore = Chroma.from_documents(
            documents=split_docs,
            embedding=ollamaEmbeddings,
            persist_directory=f"./vector/my_data/{file}"[:-8],
        )

        vectorstore.persist()
        print("Done!")
