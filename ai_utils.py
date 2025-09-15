import os
import requests
import time

API_KEY = os.getenv("gemini_flask_api")
if not API_KEY:
    raise EnvironmentError("Error: GEMINI API key not found in environment variable 'gemini_flask_api'")

API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def get_best_response(history, user_input, retries=3):
    """
    Send a request to Gemini API with proper format.
    """
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": " ".join([h['parts'][0]['text'] for h in history]) + " " + user_input}]}
        ]
    }

    for attempt in range(retries):
        try:
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
                continue
            raise ConnectionError(f"Error: Could not connect to the API after retries. Last error: {e}")
