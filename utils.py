from transformers import pipeline
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from pypdf import PdfReader

def process_text(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
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
            
            # Use a local summarization model
            summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            summary = summarizer(docs[0].page_content)  # Summarize the content
            
            return summary[0]['summary_text']

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

if __name__ == "__main__":
    main()
