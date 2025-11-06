from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "QR & Barcode Generator Agent", "status": "active"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/.well-known/agent.json")
async def get_agent_card():
    return {
        "name": "QR & Barcode Generator",
        "version": "1.0.0",
        "description": "Generate QR codes and barcodes",
        "skills": [
            {"name": "generate_qr", "description": "Generate QR codes"},
            {"name": "generate_barcode", "description": "Generate barcodes"}
        ]
    }

handler = app