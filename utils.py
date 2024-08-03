 from flask import Flask, request, jsonify
from transformers import pipeline
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from pypdf import PdfReader

app = Flask(_name_)

# Initialize the summarization model
summarizer_model = pipeline("summarization", model="facebook/bart-large-cnn")

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

@app.route('/summarize', methods=['POST'])
def summarize():
    pdf_file = request.files.get('file')
    if pdf_file:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""

        knowledge_base = process_text(text)
        query = "Summarize the content of the uploaded PDF file in approximately 3-5 sentences."
        docs = knowledge_base.similarity_search(query)
        
        # Generate summary
        summary = summarizer_model(docs[0].page_content)
        return jsonify({'summary': summary[0]['summary_text']})
    return jsonify({'error': 'No PDF file provided'}), 400

if __name__ == "__main__":
    app.run(debug=True)
