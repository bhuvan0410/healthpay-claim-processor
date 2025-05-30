import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def classify_document(file_name: str, content_excerpt: str) -> str:
    prompt = f"""
Classify the following medical document into one of the following types:
- bill
- discharge_summary
- id_card
- other

Use both the filename and the content snippet below.

Filename: {file_name}
Content:
\"\"\"
{content_excerpt[:2000]}
\"\"\"

Respond with only one label.
"""

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_URL, json=data)
        response.raise_for_status()
        output = response.json()
        result = output['candidates'][0]['content']['parts'][0]['text'].strip().lower()

        if result in ["bill", "discharge_summary", "id_card"]:
            return result
        return "other"
    except Exception as e:
        print(f"[Gemini REST Error] {e}")
        return "other"
