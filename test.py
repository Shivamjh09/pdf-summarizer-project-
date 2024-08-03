import streamlit as st
import requests
import io

def main():
    st.title("PDF Summarizer")

    # File uploader widget to upload PDF files
    pdf_file = st.file_uploader("Upload your PDF Document", type="pdf")

    if pdf_file:
        # Display a success message
        st.write("File uploaded successfully!")
        
        # Prepare the file for sending to Flask
        files = {"file": ("uploaded.pdf", pdf_file, "application/pdf")}
        
        # Send the file to the Flask backend
        response = requests.post("http://localhost:5000/summarize", files=files)
        
        if response.status_code == 200:
            summary = response.json().get("summary", "No summary returned.")
            st.subheader("Summary of File:")
            st.write(summary)
        else:
            st.error("Error: " + response.json().get("error", "Unknown error"))

if __name__ == "__main__":
    main()
