import os
import PyPDF2
from langchain.tools import tool
from langchain_core.language_models import BaseLLM
from concurrent.futures import ThreadPoolExecutor
from typing import Optional
from llama_llm import llm

PDF_DIR = "/Users/shreyas/Desktop/Test" 

def judge_pdf(file_path: str, file_name: str, query: str) -> str:
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages[:3]:
                page_text = page.extract_text()
                if page_text:
                    text += page_text.strip() + "\n"

        prompt = (
            f"User is looking for: '{query}'.\n\n"
            f"Does the following PDF content seem related to that?\n"
            f"---\n{text[:1000]}\n---\n"
            f"Reply with only YES or NO."
        )

        result = llm.invoke(prompt)
        if "YES" in result.content.upper():
            return file_name
    except Exception as e:
        print(f"❌ Error reading {file_name}: {e}")
    return None

@tool
def search_pdfs_semantic(query: str) -> str:
    """
    Use LLM to semantically judge if any PDF contains content related to the query.
    Returns matching PDF filenames.
    """

    pdf_files = [
        f for f in os.listdir(PDF_DIR)
        if f.lower().endswith(".pdf")
    ]

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(judge_pdf, os.path.join(PDF_DIR, f), f, query)
            for f in pdf_files
        ]
        results = [f.result() for f in futures if f.result()]

    return "\n".join(results) if results else "No matching PDFs found."


    # if llm is None:
    #     return "LLM is required for semantic search."

    # matching_files = []

    # for file in os.listdir(PDF_DIR):
    #     if not file.lower().endswith(".pdf"):
    #         continue

    #     file_path = os.path.join(PDF_DIR, file)

    #     try:
    #         with open(file_path, 'rb') as f:
    #             reader = PyPDF2.PdfReader(f)
    #             text = ""
    #             for page in reader.pages[:3]:  # limit to 3 pages
    #                 page_text = page.extract_text()
    #                 if page_text:
    #                     text += page_text.strip() + "\n"
    #             prompt = (
    #                 f"User is looking for: '{query}'.\n\n"
    #                 f"Does the following PDF content seem related to that?\n"
    #                 f"---\n{text[:3000]}\n---\n"
    #                 f"Reply with only YES or NO."
    #             )
    #             result = llm.invoke(prompt)
    #             if "YES" in result.content:
    #                 matching_files.append(file)

    #     except Exception as e:
    #         print(f"Error reading {file}: {e}")

    # return "\n".join(matching_files) if matching_files else "No matching PDFs found."