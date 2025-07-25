# 📚 PDF RAG Inquery
This project enables document-based question answering using Retrieval-Augmented Generation (RAG). Users can upload multiple PDF files via a simple Streamlit interface. The application will extract text from the PDFs, split the content into manageable chunks, create semantic embeddings for fast vector search, and enable natural language querying of your documents using a local Large Language Model via Ollama

# 🛠️ Setup
1. Clone the repository: 
git clone https://github.com/ChinnapatRuji/pdf-rag-inquiry.git
cd pdf-rag-inquiry

2. Download and install Ollama from:
👉 https://ollama.com
After installation, pull a model of your choice, for example:
ollama pull gemma3n:e2b

3. Set up the Environment in .env
OLLAMA_MODEL=gemma3n:e2b
HF_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

4. Download Dependencies
Ensure you have Python 3.9+ installed.
All required Python packages are listed in 'requirements.txt'. To install them, run:
pip install -r requirements.txt

5. Run the streamlit app:
streamlit run app.py
The Streamlit interface will open in your browser. Upload PDFs, ask questions, and get document-based answers instantly.

