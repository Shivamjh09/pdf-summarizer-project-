 from flask import Flask, request, jsonify
from transformers import BartForConditionalGeneration, BartTokenizer
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from pypdf import PdfReader

app = Flask(_name_)

# Initialize the tokenizer and model  locally
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

def summarize_text(text):
    inputs = tokenizer.encode(text, return_tensors='pt', max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

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
        summary = summarize_text(docs[0].page_content)
        return jsonify({'summary': summary})
    return jsonify({'error': 'No PDF file provided'}), 400

if _name_ == "_main_":
    app.run(debug=True)
