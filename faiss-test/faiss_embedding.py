import os
import numpy as np
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter

# Directory for extracted text files
extracted_text_dir = "extracted_text"
embedding_dir = "embeddings"
os.makedirs(embedding_dir, exist_ok=True)

# Initialize the embedding model
ollamaEmbeddings = OllamaEmbeddings(model="llama3")

# Iterate through each file in the directory
for file in os.listdir(extracted_text_dir):
    # Skip system files and any other irrelevant files
    if file == ".DS_Store":
        continue

    print(f"Now embedding {file[:-8]}...")

    # Load the text document
    loaded = TextLoader(os.path.join(extracted_text_dir, file))
    raw_doc = loaded.load()

    # Split the document into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1200, chunk_overlap=50)
    split_docs = text_splitter.split_documents(raw_doc)

    # Generate embeddings for each chunk
    embeddings = ollamaEmbeddings.embed_documents(split_docs)

    # Save embeddings and document IDs
    np.save(os.path.join(embedding_dir, f"{file[:-8]}_embeddings.npy"), embeddings)
    with open(os.path.join(embedding_dir, f"{file[:-8]}_docs.txt"), 'w') as f:
        for doc in split_docs:
            f.write(f"{doc.page_content}\n")

    print("Done!")