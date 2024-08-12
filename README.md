## Contributors

**[Contributor Name](https://github.com/amantiwaricse))**
Contribution: Assisted in deploying the Large Language Model (LLM) locally, providing valuable guidance and technical support to successfully implement the local deployment process.



# Local LLM Model Deployment with Flask

This project demonstrates how to deploy a local large language model (LLM) using Flask. The application processes PDF files, extracts text, and generates summaries using the BART model from Hugging Face.

## Requirements

- Python 3.7 or higher
- transformers
- langchain
- flask
- pypdf

You can install the required libraries using pip:

bash
pip install transformers langchain flask pypdf


## Setup

1. *Clone the Repository*

   bash
   git clone https://github.com/Shivamjh09/your-repo.git
   cd Shivamjh09
   

2. *Prepare Your Environment*

   Create a virtual environment and activate it:

   bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   

3. *Install Dependencies*

   Install the necessary Python packages:

   bash
   pip install -r requirements.txt
   

## Code Overview

- *app.py*: Contains the Flask application with endpoints for processing and summarizing PDF files.
- *summarize_text(text)*: Uses the BART model to generate a summary from the input text.
- *process_text(text)*: Splits text into chunks, creates embeddings, and stores them in a FAISS vector store.
- */summarize*: Endpoint to upload a PDF file and get a summary.

## Running the Application

To start the Flask application, run:

bash
python app.py


The server will start locally at http://127.0.0.1:5000.

## Usage

1. *Upload a PDF File*

   Send a POST request to http://127.0.0.1:5000/summarize with the PDF file:

   bash
   curl -X POST -F "file=@path/to/your/file.pdf" http://127.0.0.1:5000/summarize
   

2. *Receive the Summary*

   The response will contain a JSON object with the summary of the PDF file:

   json
   {
     "summary": "Your summary here."
   }
   



