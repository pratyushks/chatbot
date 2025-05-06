import os
from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader

PDF_FOLDER = "./data/Insurance_PDFs/"

def load_documents():
    docs = []

    for filename in os.listdir(PDF_FOLDER):
        path = os.path.join(PDF_FOLDER, filename)
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(path)
        elif filename.endswith(".docx"):
            loader = UnstructuredWordDocumentLoader(path)
        else:
            continue
        docs.extend(loader.load())

    return docs

if __name__ == "__main__":
    all_docs = load_documents()
    print(f"Loaded {len(all_docs)} documents.")
