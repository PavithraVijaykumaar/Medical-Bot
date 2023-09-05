import streamlit as st
from PyPDF2 import PdfReader
import openai
import tempfile

# Set your OpenAI API key here
key = st.secrets['key']
openai.api_key = key

def extract_text_from_pdf(uploaded_file):
    pdf_text = ""
    with tempfile.NamedTemporaryFile(delete=False) as temp_pdf:
        temp_pdf.write(uploaded_file.read())
        temp_pdf.seek(0)
        pdf_reader = PdfReader(temp_pdf.name)
        for page_num in range(len(pdf_reader.pages)):
            pdf_text += pdf_reader.pages[page_num].extract_text()
    return pdf_text

def main():
    st.title("Prodoc's MedicoBot")

    # Create a file uploader widget
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if pdf_file is not None:
        st.write("File uploaded!")

        # Extract text from the PDF using PdfReader
        pdf_text = extract_text_from_pdf(pdf_file)

        # Shorten the prompt and use GPT-3.5-turbo to summarize the text
        # You may need to adjust the length of pdf_text to fit within token limits
        pdf_text_shortened = pdf_text[:4000]  # Adjust the length as needed
        prompt = (
            f"You are PRODOC's medical report summarizer who accepts only medical reports:\n"
            f"{pdf_text_shortened}\n"
            f"Note: Please make sure the uploaded document is a medical report. "
            f"If not, do not read the report.\n"
            f"After confirming it as a medical report, you will summarize the report "
            f"and you will put 'Inference' as a heading and infer the report based on the details in the report.\n"
            f"You will put 'Specialist to consult' as a heading and list down the specialists to consult this report with.\n"
            f"You do nothing but summarize medical reports and specialization to consult.\n"
            f"Finally, end the summarization by saying 'Thanks for using PRODOC's Chat Application' in a new line."
        )
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]

        summary = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )

        st.write("Summary:")
        st.write(summary['choices'][-1]['message']['content'])

if __name__ == "__main__":
    main()