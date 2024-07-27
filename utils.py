import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from pypdf import PdfReader

def process_text(text):
    # Process the given text by splitting it into chunks and converting
    # these chunks into embeddings to form a knowledge base.

    # Initialize a text splitter to divide the text into manageable chunks
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,  # Size of each chunk
        chunk_overlap=200,  # Overlap between chunks
        length_function=len
    )

    # Split the text into chunks
    chunks = text_splitter.split_text(text)

    # Load a model for generating embeddings from Hugging Face
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    # Create a FAISS index from the text chunks using the embeddings
    knowledgebase = FAISS.from_texts(chunks, embeddings)

    return knowledgebase

def summarizer(pdf):
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""

        knowledge_base = process_text(text)

        query = "Summarize the content of the uploaded PDF file in approximately 3-5 sentences."
        if query:
            docs = knowledge_base.similarity_search(query)
            OpenAIModel = "gpt-3.5-turbo-16k"
            llm = ChatOpenAI(model=OpenAIModel, temperature=0.1)
            chain = load_qa_chain(llm, chain_type='stuff')
            
            response = chain.run(input_documents=docs, question=query)
               
            return response

def main():
    st.set_page_config(page_title="PDF Summarizer")

    st.title("PDF Summarizing App")
    st.write("Summarize your PDF files in just a few seconds.")
    st.divider()

    pdf = st.file_uploader("Upload your PDF Document", type='pdf')
    submit = st.button("Generate Summary")

    if submit and pdf is not None:
        summary = summarizer(pdf)
        st.write("Summary:")
        st.write(summary)

if __name__ == "_main_":
    main()