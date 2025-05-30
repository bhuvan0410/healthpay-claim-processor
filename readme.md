# HealthPay Claim Processor 🏥🤖

An AI-powered backend pipeline built with FastAPI that processes medical insurance claim documents (PDFs) using Gemini AI to classify, extract, validate, and make claim decisions.

---

## 🔧 Tech Stack

- **FastAPI** (Python 3.10)
- **Google Gemini Flash (REST API)**
- **PyMuPDF** for PDF text extraction
- **Requests** for AI HTTP calls
- **Dotenv** for API key management

---

## 📂 Architecture

/app
├── main.py
├── routes/
│ └── claim_routes.py
├── agents/
│ ├── classifier_agent.py
│ ├── bill_agent.py
│ └── discharge_agent.py
└── .env

yaml
Copy
Edit

---

## 🧠 AI Agent Flow

1. **Upload PDFs** to `/api/process-claim`
2. **Extract Text** from each PDF using PyMuPDF
3. **Classify Document** as `bill`, `discharge_summary`, `id_card`, or `other` using Gemini
4. **Route to Agent**:
   - `BillAgent`: extracts hospital_name, total_amount, date_of_service
   - `DischargeAgent`: extracts patient_name, diagnosis, admission_date, discharge_date
5. **Validate** if all required document types are present
6. **Decide** claim approval or rejection

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
🤖 Prompts Used
1. Classification Prompt

text
Copy
Edit
Classify the following medical document into one of:
- bill
- discharge_summary
- id_card
- other

Use the filename and text snippet.

Respond with one label only.
2. BillAgent Prompt

text
Copy
Edit
Extract the following fields from this hospital bill:
- hospital_name
- total_amount (numeric INR only)
- date_of_service (YYYY-MM-DD)

Respond only with valid JSON.