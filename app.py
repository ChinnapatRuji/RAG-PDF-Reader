import streamlit as st
import app_functions as af

def main():
    st.set_page_config(
        page_title = "PDF Robot Assistance",
        page_icon = ":robot:"
    )
    st.header("RAG: Get answers from multiple PDFs :books:")
    query = st.text_input("Ask a question about your documents")

    with st.sidebar:
        st.subheader("Upload your PDFs")
        pdf_docs = st.file_uploader("Upload your PDFs here", accept_multiple_files=True)
        if st.button("Process"):
            if "vector_db" in st.session_state:
                del st.session_state["vector_db"]
            try:
                with st.spinner("Processing"):
                    text = af.load_pdf(pdf_docs)
                    chunks = af.text_splitter(text)
                    st.session_state.vector_db = af.get_vector(chunks)
                    st.success("Processing Complete")
            except:
                st.write("Please upload a valid PDF")

    if st.button("enter"):
        try:
            with st.spinner("Searching..."):
                vector_db = st.session_state.get("vector_db")
                context = af.get_context(vector_db, query)
                st.subheader("Answer from LLM:")
                answer = af.ask_ollama(context, query)
                st.text(answer)
        except:
            st.error("Input and Process a valid PDF")

if __name__ == "__main__":
    main()