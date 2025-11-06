from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Create a simplified FastAPI app for Vercel
app = FastAPI(
    title="QR & Barcode Generator Agent",
    description="AI Agent for generating QR codes and barcodes via Telex.im",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import services
try:
    from services.a2a_handler import A2AHandler
    a2a_handler = A2AHandler()
except ImportError:
    a2a_handler = None

@app.get("/")
async def root():
    return {
        "agent": "QR & Barcode Generator",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/.well-known/agent.json")
async def get_agent_card():
    try:
        agent_path = os.path.join(os.path.dirname(__file__), '..', '.well-known', 'agent.json')
        with open(agent_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "name": "QR & Barcode Generator",
            "version": "1.0.0",
            "skills": [
                {
                    "name": "generate_qr",
                    "description": "Generate QR codes"
                },
                {
                    "name": "generate_barcode", 
                    "description": "Generate barcodes"
                }
            ]
        }

@app.post("/")
async def handle_a2a_request(request: Request):
    try:
        body = await request.json()
        if a2a_handler:
            response = await a2a_handler.handle_request(body)
            return JSONResponse(content=response)
        else:
            return JSONResponse(
                content={
                    "jsonrpc": "2.0",
                    "id": body.get("id"),
                    "error": {
                        "code": -32601,
                        "message": "Method not found"
                    }
                },
                status_code=404
            )
    except Exception as e:
        return JSONResponse(
            content={
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": f"Parse error: {str(e)}"
                }
            },
            status_code=400
        )

# Export for Vercel
handler = app