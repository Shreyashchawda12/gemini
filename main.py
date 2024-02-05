import streamlit as st
import os
import fitz  # PyMuPDF
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai
from typing import Any
load_dotenv()

# Configure API KEY
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Function to extract data from PDF using Gemini Pro LLM


# Function to extract data from PDF using Gemini Pro LLM
def extract_data_from_pdf(pdf_path: str) -> Any:
    model = genai.GenerativeModel('gemini-pro-llm')
    input_prompt = "Extract data from the provided PDF document."
    response = model.generate_content([input_prompt, pdf_path])
    return response.text


# Function to process the uploaded PDF file
def process_pdf(uploaded_file) -> str:
    if uploaded_file is not None:
        pdf_data = uploaded_file.read()
        
        # Process the PDF data using PyMuPDF
        pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
        text_content = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text_content += page.get_text()

        # Extract data from the text content using Gemini Pro LLM
        extracted_data = extract_data_from_pdf(text_content)
        return extracted_data
    else:
        raise FileNotFoundError("Please upload a PDF file.")

# Function to save extracted data to Excel
def save_to_excel(data: str, output_path: str) -> None:
    df = pd.DataFrame(data, columns=["Name", "Age", "Gender"])
    df.to_excel(output_path, index=False)

def main():
    st.set_page_config(page_title="PDF Data Extractor")
    st.header("Gemini Pro PDF Data Extractor")

    uploaded_file = st.file_uploader("Select a PDF file", type=["pdf"])

    if uploaded_file is not None:
        st.subheader("PDF Preview")

        try:
            extracted_data = process_pdf(uploaded_file)

            # Save extracted data to Excel
            excel_output_path = "extracted_data.xlsx"
            save_to_excel(extracted_data, excel_output_path)

            st.success(f"Data extracted successfully. Excel file saved to {excel_output_path}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
