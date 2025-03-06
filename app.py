import streamlit as st
import cv2
import pytesseract
from gtts import gTTS
from googletrans import Translator
from docx import Document
import pdfplumber
import numpy as np
from io import BytesIO

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
# Function to extract text from image
def extract_text_from_image(image_bytes):
    # Convert image bytes to OpenCV format
    image_np = np.frombuffer(image_bytes.read(), np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Perform OCR
    text = pytesseract.image_to_string(gray)
    
    return text.strip()

# Function to extract text from PDF
def extract_text_from_pdf(pdf_bytes):
    text = ""
    with pdfplumber.open(BytesIO(pdf_bytes.read())) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
    return text.strip()

# Function to extract text from Word Document
def extract_text_from_word(docx_bytes):
    doc = Document(BytesIO(docx_bytes.read()))
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()

# Function to translate text
def translate_text(text, target_language='ta'):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language).text
    return translated_text.strip()

# Function to convert text to speech
def text_to_speech(text, language='en'):
    tts = gTTS(text=text, lang=language, slow=False)
    audio_file = "output.mp3"
    tts.save(audio_file)
    return audio_file

# Streamlit UI
st.title("VisionVoice")

# File upload section
file = st.file_uploader("Upload an Image, PDF, or Word Document", type=["jpg", "png", "pdf", "docx"])

if file:
    text = ""
    file_name = file.name.lower()

    # Process files based on extension
    if file_name.endswith(("jpg", "png")):
        text = extract_text_from_image(file)
    elif file_name.endswith("pdf"):
        text = extract_text_from_pdf(file)
    elif file_name.endswith("docx"):
        text = extract_text_from_word(file)

    # Display extracted text
    st.subheader("Extracted Text")
    st.text_area("Extracted Text", text, height=200)

    # Language selection for translation
    languages = {
        'English': 'en', 'Tamil': 'ta', 'Telugu': 'te', 'Kannada': 'kn',
        'Malayalam': 'ml', 'Hindi': 'hi', 'Bengali': 'bn', 'Gujarati': 'gu', 'Punjabi': 'pa'
    }
    selected_language = st.selectbox("Select Language for Translation & Speech", list(languages.keys()))

    # Translation
    translated_text = text
    if selected_language != 'English':
        translated_text = translate_text(text, target_language=languages[selected_language])
        st.subheader(f"Translated Text ({selected_language})")
        st.text_area(f"Translated Text ({selected_language})", translated_text, height=200)

    # Generate Speech
    if st.button("Generate Speech"):
        audio_file = text_to_speech(translated_text, language=languages[selected_language])
        st.audio(audio_file, format="audio/mp3")