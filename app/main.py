from fastapi import FastAPI
from app.routes.claim_routes import router as claim_router

app = FastAPI(title="HealthPay Claim Processor")

app.include_router(claim_router, prefix="/api")
