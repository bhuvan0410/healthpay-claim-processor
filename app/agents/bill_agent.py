

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def extract_bill_fields(text: str) -> dict:
    prompt = f"""
Extract the following fields from this hospital bill:
- hospital_name
- total_amount (numeric INR only)
- date_of_service (YYYY-MM-DD)

⚠️ Respond ONLY with valid JSON. No explanation, no markdown, no headings.

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

        result_text = response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
        print("[DEBUG] Gemini Output:", result_text)

        
        if result_text.startswith("```"):
            result_text = result_text.strip("`").strip().replace("json", "", 1).strip()

        return json.loads(result_text)
    except Exception as e:
        return {"error": f"Gemini JSON parsing error: {e}"}
