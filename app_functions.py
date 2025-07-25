import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import re
import ollama
import os
from dotenv import load_dotenv

load_dotenv()
CHROMA_PATH = "chroma"
embedding_model_name = os.getenv("HF_EMBEDDING_MODEL")
embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_name)
ollama_model = os.getenv("OLLAMA_MODEL")

def load_pdf(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf.seek(0)  # Important: reset file pointer
        doc = fitz.open(stream=pdf.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()
        doc.close()
    return text

def text_splitter(doc):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        length_function=len,
        is_separator_regex=False,
    )
    return splitter.split_text(doc)

def get_vector(chunks):
    db = Chroma.from_texts(
        texts=chunks,
        embedding=embedding_model,
        collection_name="my_collection"
    )
    return db

def clean_text(text):
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def get_context(vector_db, query):
    docs = vector_db.similarity_search(query, k=3)
    context = "\n\n".join([clean_text(doc.page_content) for doc in docs])
    return context

def ask_ollama(context, query):
    prompt = (
        f"You are an assistant that answers questions STRICTLY based on the provided document content. "
        f"If there is no mention in the content, respond with 'No relevant information found in the document.'\n\n"
        f"Content:\n{context}\n\n"
        f"Question:\n{query}"
    )
    response = ollama.chat(
        model= ollama_model,
        messages=[
            {"role": "system", "content": "You are an assistant that answers questions STRICTLY based on ONLY provided document content."},
            {"role": "user", "content": prompt}
        ],
        stream=False
    )
    return response['message']['content'] if 'message' in response and 'content' in response['message'] else str(response)