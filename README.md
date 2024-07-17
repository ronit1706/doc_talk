# DOC_TALK

This repository contains the code for doc_talk, a Retrieval-Augmented Generation (RAG) powered chatbot that utilizes the Llama 3 model. The chatbot can interact with users and answer questions by retrieving relevant information from a vector store of document embeddings.

## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Workflow](#workflow)
- [Technologies Used](#technologies-used)
- [Screenshots](#screenshots)


## Project Description

This project is designed to create an intelligent chatbot capable of answering questions by leveraging the Llama 3 model and a vector store. The chatbot retrieves relevant documents based on user queries, processes them to generate context-aware responses, and provides accurate answers.

## Features

- Load and preprocess PDF documents.
- Use OCR for flat pdfs
- Extract and split text from documents, properly managing table contents.
- Generate embeddings using the Ollama Embeddings model.
- Store embeddings in a vector store (ChromaDB).
- Retrieve relevant document chunks based on user queries.
- Generate responses using the Llama 3 model.
- Interactive chat interface for user queries.


## Workflow

Load PDF Documents: PDF documents are loaded from the flattened_pdfs directory.
	2.	Process PDFs: PDFs are processed to extract and split images using OpenCV.
	3.	Text Extraction: Extracted images are processed with OCR (using pytesseract) to extract text.
	4.	Embeddings Generation: Text chunks are converted into embeddings using the Ollama Embeddings model.
	5.	Store Embeddings: The generated embeddings are stored in a vector store (Chroma).
	6.	Retrieve Relevant Chunks: Based on user queries, relevant text chunks are retrieved from the vector store.
	7.	Generate Response: The Llama 3 model generates responses using the retrieved text chunks and the user query.
	8.	Interactive Chat: Users interact with the chatbot through a console interface.


## Technologies used

	•	Python
	•	OpenCV
	•	Tesseract-OCR
	•	pdf2image
	•	LangChain
	•	Ollama Embeddings
	•	Chroma Vector Store
	•	PlantUML

## Screenshots

![ui](https://github.com/user-attachments/assets/a22bb092-e67b-4a35-a3ce-2c722a7b67ec)
As seen in the image, the chatbot properly works for given context, but does not answer out of context questions (to avoid incorrect information)
