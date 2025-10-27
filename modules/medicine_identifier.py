import os
import io
from PIL import Image
import easyocr
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_image(img_file):
    """
    Extract visible text from a tablet or medicine image using EasyOCR.
    Works on both local and Streamlit Cloud environments.
    """
    try:
        # Read image and convert to bytes
        image = Image.open(img_file).convert("RGB")
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes = image_bytes.getvalue()

        # Initialize EasyOCR reader
        reader = easyocr.Reader(['en'], gpu=False)
        results = reader.readtext(image_bytes, detail=0)
        text = " ".join(results)

        if not text.strip():
            return "⚠️ No text detected. Please upload a clearer image."

        return text.strip()

    except Exception as e:
        return f"⚠️ Error reading image: {e}"


def analyze_medicine_info(text):
    """
    Use LLM to describe the medicine's purpose and usage.
    """
    if not text or text.startswith("⚠️"):
        return "⚠️ Could not detect valid text from the image. Please try again with a better photo."

    prompt = f"""
    You are a helpful AI healthcare assistant. Based on the detected text from a medicine image,
    identify the medicine name and explain clearly:
    - What the medicine is used for
    - Its typical dosage or form (if known)
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
        return f"⚠️ Error during LLM analysis: {e}"
