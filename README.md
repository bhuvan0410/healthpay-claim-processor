# 🏥 HealthPay Claim Processor (AI-Powered Backend Assignment)

This is a modular, real-world backend system built as part of the HealthPay Backend Developer assignment. It automates the classification and processing of medical insurance claim documents (bills, discharge summaries, etc.) using AI agents.

> 👨‍💻 Built by: **Bhuvan Pagilla**

---

## 🚀 About the Project

The goal was to build an agentic pipeline that accepts multiple medical claim PDFs, classifies them using LLMs, extracts structured data, validates it, and returns a final claim decision (approve/reject). I chose **FastAPI** for its async capability and clarity, and used **Gemini 2.0 Flash (via REST API)** for classification and extraction agents.

---

## 🧠 My Approach & Workflow

1. **Setup & Planning**
   - Skimmed the assignment brief
   - Broke it into atomic steps (upload → classify → extract → validate → decide)
   - Set up FastAPI with basic `/process-claim` route

2. **PDF Text Extraction**
   - Used `PyMuPDF` (`fitz`) for fast, accurate multi-page extraction
   - Saved each uploaded PDF to `/tmp/` and extracted all text content

3. **Document Classification with Gemini**
   - Built `classifier_agent.py` to call Gemini Flash via REST
   - Prompted it with both filename + snippet of text
   - Ensured it outputs only a single label (`bill`, `discharge_summary`, etc.)

4. **Agentic Field Extraction**
   - Created two agents:
     - `BillAgent`: extracts `hospital_name`, `total_amount`, `date_of_service`
     - `DischargeAgent`: extracts `patient_name`, `diagnosis`, `admission_date`, `discharge_date`
   - Tuned prompts to force **compact JSON output**
   - Handled Gemini’s markdown-wrapped outputs with clean parsing logic

5. **Validation + Decision**
   - Checked for required documents (`bill` + `discharge_summary`)
   - If any missing → claim is **rejected**
   - Else → claim is **approved**

6. **Debugging & Iteration**
   - Faced some markdown issues in Gemini output → solved using `.strip('```')`
   - Also switched to `json.loads()` for safe parsing instead of `eval()`
   - Integrated live logging for debug visibility during testing

---

## 🧠 AI Agents: How They Work

### 1. 🔍 `ClassifierAgent` Prompt
Classify the following medical document into one of:

bill

discharge_summary

id_card

other

Use the filename and text snippet.

Respond with one label only.

shell
Copy
Edit

### 2. 💸 `BillAgent` Prompt
Extract the following fields from this hospital bill:

hospital_name

total_amount (numeric INR only)

date_of_service (YYYY-MM-DD)

Respond only with valid JSON.

shell
Copy
Edit

### 3. 🏥 `DischargeAgent` Prompt
Extract the following from the discharge summary:

patient_name

diagnosis

admission_date

discharge_date

Respond only with valid JSON.

yaml
Copy
Edit

---

## 📦 Project Structure

app/
-├── main.py # Entry point
-├── routes/
-│ └── claim_routes.py # Handles /process-claim logic
-├── agents/
-│ ├── classifier_agent.py
-│ ├── bill_agent.py
-│ └── discharge_agent.py
-├── services/
-│ └── (optional: file_handler.py)
-├── config.py (if needed)
- .env # Contains GEMINI_API_KEY
- requirements.txt
- README.md

yaml
Copy
Edit

---

## 🧪 Sample Output

```json
{
  "documents": [
    {
      "filename": "25020602669-2_20250427_120745-yashodha.pdf",
      "type": "bill",
      "hospital_name": "YASHODA HEALTHCARE SERVICES PVT LTD",
      "total_amount": 604210,
      "date_of_service": "2025-02-07"
    }
  ],
  "validation": {
    "missing_documents": ["discharge_summary"],
    "discrepancies": []
  },
  "claim_decision": {
    "status": "rejected",
    "reason": "Missing required document types: discharge_summary"
  }
}
```
🛠️ How to Run the Project

1. Clone & Set Up

bash
Copy
Edit
git clone https://github.com/yourname/healthpay-claim-processor.git
cd healthpay-claim-processor
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2. Add .env

bash
Copy
Edit
GEMINI_API_KEY=your_google_api_key_here

3. Start the Server

bash
Copy
Edit
uvicorn app.main:app --reload

4. Test at

http://localhost:8000/docs

🐳 Bonus (Docker Support)
dockerfile
Copy
Edit
# Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
Build & Run:

bash
Copy
Edit
docker build -t healthpay-backend .
docker run -d -p 8000:8000 healthpay-backend


💡 Reflection

This assignment was a great experience in applying AI tools for real-world workflows. I learned to:

Prompt and parse Gemini effectively

Modularize logic into clean agents

Handle async file uploads and PDF parsing

Write robust, production-style validation logic


Thank you for the opportunity!
