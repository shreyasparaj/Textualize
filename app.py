import os
import re
import streamlit as st
from google.cloud import vision
import requests
from docx import Document

# Set up Google Cloud Vision API credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vision_key.json'

# Load Gemini API Key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Ensure your API key is set

def detect_text(image_content):
    """Detects text from a single image using Google Vision API."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)
    response = client.text_detection(image=image)

    if response.error.message:
        raise Exception(f"API Error: {response.error.message}")

    text = response.text_annotations[0].description if response.text_annotations else ""
    return text.strip()

def extract_questions_answers(text):
    """Extracts questions and answers, formats them with better spacing and structure."""
    question_answer_pattern = r'(.?)(\d+)\s?(\([^()]+\))\s?(.?)\s+([a-d]\))'
    questions_answers = re.findall(question_answer_pattern, text, re.DOTALL)
    
    formatted_qna = ""
    for question_text, question_num, question_content, answer_text, answer_options in questions_answers:
        formatted_qna += f"{question_num}. {question_content.strip()}?\n"
        formatted_qna += f"{answer_options.strip()} \n\n"
    return formatted_qna

def format_text_with_gemini(text):
    """Formats the extracted text using the Gemini API with structured prompt."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}

    # Structured prompt for cleaner formatting
    prompt = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Please organize and format the following text for better readability:\n\n{text}"
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=prompt)
    
    if response.status_code == 200:
        formatted_response = response.json()
        output = formatted_response.get('contents', [{}])[0].get('parts', [{}])[0].get('text', "")
        return output.strip()
    else:
        raise Exception(f"Gemini API Error: {response.status_code} - {response.text}")

def save_to_word(formatted_text, output_file):
    """Saves the formatted text to a Word file."""
    doc = Document()
    doc.add_paragraph(formatted_text)
    doc.save(output_file)

def main():
    st.title("OCR with Structured Output and Word Download")
    st.write("Upload multiple images to extract and structure text, then download it as a Word file.")

    uploaded_files = st.file_uploader(
        "Choose images", accept_multiple_files=True, type=["jpg", "jpeg", "png"]
    )

    if uploaded_files:
        all_extracted_text = ""

        for uploaded_file in uploaded_files:
            image_content = uploaded_file.read()
            try:
                # Step 1: Extract text using Google Vision API
                extracted_text = detect_text(image_content)
                st.write(f"Extracted text from {uploaded_file.name}: {extracted_text}")

                # Step 2: Extract and structure questions and answers from the text
                questions_answers = extract_questions_answers(extracted_text)

                # Step 3: Format the extracted text using Gemini API
                final_text = format_text_with_gemini(questions_answers)
                st.text(final_text)

                # Append to the final output
                all_extracted_text += f"Formatted text from {uploaded_file.name}:\n{final_text}\n\n"
            except Exception as e:
                st.error(f"Failed to process {uploaded_file.name}: {e}")

        # Step 4: Save the final output to a Word file
        output_file_path = "formatted_output.docx"
        save_to_word(all_extracted_text, output_file_path)

        # Step 5: Provide a download button for the Word file
        with open(output_file_path, "rb") as f:
            st.download_button(
                label="Download Word File",
                data=f,
                file_name="formatted_output.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

if __name__ == "__main__":
    main()
