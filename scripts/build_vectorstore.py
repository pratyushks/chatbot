import os
import sys
sys.path.append("./scripts")

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.document_loaders import TextLoader
from load_documents import load_documents

DATA_DIR = "./data/Angelone_scrapped"
VECTORSTORE_DIR = "./vectorstore"

def load_support_text_files():
    documents = []
    for fname in os.listdir(DATA_DIR):
        if fname.endswith(".txt"):
            path = os.path.join(DATA_DIR, fname)
            loader = TextLoader(path, encoding="utf-8")
            documents.extend(loader.load())
    return documents

def build_faiss_index():
    print("Loading insurance documents...")
    insurance_docs = load_documents()

    print("Loading scraped AngelOne content...")
    support_docs = load_support_text_files()

    all_docs = insurance_docs + support_docs
    print(f"Total documents before chunking: {len(all_docs)}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(all_docs)
    print(f"Total chunks after splitting: {len(chunks)}")

    print("Embedding and saving FAISS index...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(VECTORSTORE_DIR)

    print(f"FAISS vector index saved to: {VECTORSTORE_DIR}")

if __name__ == "__main__":
    build_faiss_index()
