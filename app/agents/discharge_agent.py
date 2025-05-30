import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def extract_discharge_fields(text: str) -> dict:
    prompt = f"""
You are a document extraction assistant.

From the discharge summary below, extract and return JSON with:

- patient_name
- diagnosis
- admission_date (format: YYYY-MM-DD)
- discharge_date (format: YYYY-MM-DD)

Only return valid JSON.

Text:
\"\"\"
{text[:3000]}
\"\"\"
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
        result = response.json()['candidates'][0]['content']['parts'][0]['text'].strip()

        if result.startswith("{") and "patient_name" in result:
            return eval(result)
        return {"error": "Unstructured response"}
    except Exception as e:
        return {"error": f"Gemini DischargeAgent error: {e}"}
