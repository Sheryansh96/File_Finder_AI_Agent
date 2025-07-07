# pdf_indexer.py
import os
import PyPDF2
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain_huggingface import HuggingFaceEmbeddings

PDF_DIR = "/Users/shreyas/Desktop/Test"

def extract_chunks():
    chunks = []
    for file in os.listdir(PDF_DIR):
        if not file.endswith(".pdf"):
            continue
        path = os.path.join(PDF_DIR, file)
        try:
            reader = PyPDF2.PdfReader(open(path, "rb"))
            text = ""
            for page in reader.pages[:3]:
                text += page.extract_text() or ""
            chunks.append(Document(page_content=text, metadata={"source": file}))
        except Exception as e:
            print(f"Skipping {file}: {e}")
    return chunks

def index_pdfs():
    chunks = extract_chunks()
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")  # or Ollama
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("pdf_index")

if __name__ == "__main__":
    index_pdfs()
