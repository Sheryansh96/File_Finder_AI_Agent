# pdf_semantic_agent.py
import os
from concurrent.futures import ThreadPoolExecutor
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain.tools import tool
import PyPDF2
llm = ChatOllama(model="llama3.2:latest")

PDF_DIR = "/Users/shreyas/Desktop/Test"

# Load FAISS
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.load_local("pdf_index", embeddings, allow_dangerous_deserialization=True)

def is_relevant_with_llama(file_path: str, file_name: str, query: str) -> str:
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages[:3]:
                text += page.extract_text() or ""
        prompt = (
            f"User is looking for: '{query}'.\n\n"
            f"Does the following PDF content seem related to that?\n"
            f"---\n{text[:3000]}\n---\n"
            f"Reply only YES or NO."
        )
        result = llm.invoke(prompt)
        if "yes" in result.content.lower():
            return file_name
    except Exception as e:
        print(f"Error with {file_name}: {e}")
    return None

@tool
def hybrid_pdf_search(query: str) -> str:
    """
    Use this when asked to find out a file with a required content.
    """
    results = vectorstore.similarity_search(query, k=3)
    top_files = list(set([doc.metadata['source'] for doc in results]))

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(is_relevant_with_llama, os.path.join(PDF_DIR, f), f, query)
            for f in top_files
        ]
        confirmed = [f.result() for f in futures if f.result()]

    return "\n".join(confirmed) if confirmed else "No relevant PDFs found."
