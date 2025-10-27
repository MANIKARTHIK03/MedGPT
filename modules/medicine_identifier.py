import pytesseract
from PIL import Image
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables (your API key)
load_dotenv()

# Explicitly tell pytesseract where tesseract.exe is located
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_image(img_file):
    """Extract visible text from a tablet/medicine image."""
    img = Image.open(img_file)
    text = pytesseract.image_to_string(img)
    return text.strip()

def analyze_medicine_info(text):
    """Use LLM to describe the medicine's purpose and usage."""
    if not text:
        return "⚠️ Could not detect any text from the image. Please try again with a clearer photo."

    prompt = f"""
    You are a healthcare assistant. Based on the detected text from a tablet or medicine image,
    identify the medicine name and explain:
    - What the medicine is used for
    - Typical dosage or form (if known)
    - Common side effects and precautions

    Detected text: {text}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {e}"
