import streamlit as st
import os
from utils import *

def main():
    # Set page configurations
    st.set_page_config(page_title="PDF Summarizer")

    st.title("PDF Summarizing App")  # Setting the title of the app
    st.write("Summarize your PDF files in just a few seconds.")  # Displaying a description
    st.divider()  # Inserting a divider for better layout

    # Creating a file uploader widget to upload PDF files
    pdf = st.file_uploader("Upload your PDF Document", type='pdf')

    # Creating a button for users to submit their PDF for summarization
    submit = st.button("Generate Summary")

    # Logic to handle file upload and summarization
    if submit and pdf is not None:
        st.write("File uploaded successfully!")  # Example success message
        response = summarizer(pdf)
        
        st.subheader('Summary of File:')
        st.write(response)

if __name__ == "__main__":
    main()  # Calling the main function to start the Streamlit app
