# rag.py

import requests
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import glob
import os
import logging

# Setup logging for this module
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def load_pdfs():
    pdf_files = glob.glob("./pdfs/*.pdf")
    try:
        with open("example.txt", "r") as f:
            recorded_files = set(f.read().splitlines())
    except FileNotFoundError:
        recorded_files = set()

    docs = []
    new_files = []

    for file_path in pdf_files:
        if file_path not in recorded_files:
            loader = PyPDFLoader(file_path)
            docs.extend(loader.load())
            new_files.append(file_path)

    if new_files:
        with open("example.txt", "a") as f:
            for new_file in new_files:
                f.write(new_file + "\n")

        logging.info(f"Processed {len(new_files)} new PDF(s): {new_files}")
    else:
        logging.info("No new PDFs to process.")

    return docs

def return_chunks(data):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(data)
    logging.info(f"Generated {len(chunks)} new chunks.")
    return chunks

def update_vector_store(new_chunks, index_path="vectorstores/my_faiss_index"):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    if os.path.exists(os.path.join(index_path, "index.faiss")):
        db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        db.add_documents(new_chunks)
        logging.info("Added new chunks to existing FAISS index.")
    else:
        db = FAISS.from_documents(new_chunks, embeddings)
        logging.info("Created new FAISS index with new chunks.")

    db.save_local(index_path)
    logging.info(f"Saved FAISS index to {index_path}")

def load_database():
    index_path = "vectorstores/my_faiss_index"
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    logging.info(f"Loaded FAISS index from {index_path}")
    return db

def retrive_context(query, db):
    retrived = db.similarity_search(query, k=3)
    logging.info(f"Retrieved {len(retrived)} chunks for query: '{query}'")
    context_text = "\n\n".join([chunk.page_content for chunk in retrived])
    return context_text

def initial_setup():
    data = load_pdfs()
    new_chunks = return_chunks(data)

    if new_chunks:
        update_vector_store(new_chunks)

    db = load_database()
    return db

def handle_user_query(query, db):
    context = retrive_context(query, db)

    prompt = f"""
You are a helpful assistant representing the PM Accelerator team.
Use the context below to answer the user's question accurately.
If the question is irrelevant or if answer not found in context, politely decline and ask them to contact the team.
The team details are (if in case):
main members to contact: Anil Thomas, Marla in discord groups.

Context:
{context}

Question: {query}

Answer:
"""

    payload = {
        "model": "mistral:7b-instruct",
        "prompt": prompt,
        "stream": False
        
    }

    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        response.raise_for_status()
        result = response.json()
        logging.info("Successfully got LLM response.")
        return result.get("response")
    except requests.exceptions.RequestException as e:
        logging.error(f"LLM request failed: {e}")
        return None
