from fastapi import APIRouter, UploadFile, File
from typing import List
import fitz  # PyMuPDF
from app.agents.classifier_agent import classify_document
from app.agents.bill_agent import extract_bill_fields
from app.agents.discharge_agent import extract_discharge_fields

router = APIRouter()

@router.post("/process-claim")
async def process_claim(files: List[UploadFile] = File(...)):
    documents = []
    types_present = set()

    for file in files:
        file_content = await file.read()

    
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(file_content)

        try:
            doc = fitz.open(temp_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
        except Exception as e:
            documents.append({
                "filename": file.filename,
                "type": "error",
                "error": f"PDF extraction error: {e}"
            })
            continue

        # Classify
        doc_type = classify_document(file.filename, text)
        types_present.add(doc_type)

        # Build base response
        doc_result = {
            "filename": file.filename,
            "type": doc_type
        }

        # Route to agents
        if doc_type == "bill":
            doc_result.update(extract_bill_fields(text))
        elif doc_type == "discharge_summary":
            doc_result.update(extract_discharge_fields(text))

        documents.append(doc_result)

    # Validation
    required_types = {"bill", "discharge_summary"}
    missing_documents = sorted(list(required_types - types_present))

    validation = {
        "missing_documents": missing_documents,
        "discrepancies": []  # Extend if needed
    }

    # Claim Decision
    if not missing_documents:
        claim_decision = {
            "status": "approved",
            "reason": "All required documents present and data is consistent"
        }
    else:
        claim_decision = {
            "status": "rejected",
            "reason": f"Missing required document types: {', '.join(missing_documents)}"
        }

    return {
        "documents": documents,
        "validation": validation,
        "claim_decision": claim_decision
    }
