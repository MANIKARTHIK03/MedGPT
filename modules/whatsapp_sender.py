import requests
import os
from dotenv import load_dotenv

load_dotenv()

WHATSAPP_TOKEN = os.getenv("EAATK3NG23ZAEBP4ewRAnRaYLEIrIAZBaEUppC4HQMBTMy2OzgOBS7xniHdIM5ZAaCXw8mN4f1KPXlH2AJBZA7f0CZA6reum8DF8tJtmwjC9pQZBZC5vKB8jezdlAZByWqMZAoj878rFYPRdr96TRtUD8Wo3lk8wxj4fZBV7dAxEKYB8nVhRzdogS9kiE6onmiZAFS1sczGYlJD2522XhllcDo373iYjuKWqepgGTDZBkc5IxoK3fEe40TqeJ4zciQ2O4XgZDZD")
WHATSAPP_PHONE_ID = os.getenv("871813836010350")

def send_whatsapp_message(receiver_number, message):
    """
    Send WhatsApp message using Meta Cloud API.
    Works for both PC and mobile.
    """
    url = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": receiver_number.replace("+", ""),
        "type": "text",
        "text": {"body": message}
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("✅ WhatsApp message sent successfully!")
        return True
    else:
        print("❌ WhatsApp message failed:", response.text)
        return False
