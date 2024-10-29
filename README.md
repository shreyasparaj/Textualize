# Textualize Version 1

**Textualize** is a robust application designed for extracting and organizing text from images through Optical Character Recognition (OCR) technology. By leveraging the Google Cloud Vision API for text detection and the Gemini API(gemini-1.5-flash) for advanced text formatting, this tool is perfect for educators, students, and professionals looking to efficiently structure and download text content.

## Features

- **Multi-Image Upload:** Supports uploading multiple images in JPG, JPEG, or PNG formats for text extraction.
- **OCR Text Detection:** Accurately detects and extracts text from images using the Google Cloud Vision API.
- **Structured Output:** Extracts and organizes questions and answers from the detected text for enhanced readability.
- **Gemini API Integration:** Utilizes the Gemini API to format the extracted text for improved presentation.
- **Word Document Export:** Exports the structured text to a Word document for convenient downloading and sharing.

## Installation

### Prerequisites

- Python 3.7 or higher
- Streamlit
- Google Cloud Vision library
- Requests library
- python-docx library

### Setup Instructions

1. **Set up your Google Cloud Vision API credentials:**

   - Create a Google Cloud project and enable the Vision API.
   - Download the service account key JSON file and rename it to `vision_key.json`.

2. **Clone the repository:**

   ```bash
   git clone https://github.com/shreyasparaj/Textualize.git
   cd Textualize

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt

4. **Run the Streamlit app:**

   ```bash
   streamlit run app.py


## Contact

For any inquiries or feedback, feel free to reach out:

**Email:** [shreyasparaj1@gmail.com](mailto:shreyasparaj1@gmail.com)
