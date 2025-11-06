from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
import os
import uuid
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv

from src.controllers.agent_controller import AgentController
from src.utils.telex_client import TelexClient
from src.services.a2a_handler import A2AHandler

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Disable scheduler for serverless deployment
# scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager - simplified for serverless"""
    # Startup
    logger.info("Starting QR & Barcode Generator Agent")
    
    # Skip scheduler for serverless deployment
    # Vercel functions are stateless
    
    yield
    
    # Shutdown
    logger.info("QR & Barcode Generator Agent stopped")

# Create FastAPI app
app = FastAPI(
    title="QR & Barcode Generator Agent",
    description="AI Agent for generating QR codes and barcodes via Telex.im",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize controller and A2A handler
controller = AgentController()
a2a_handler = A2AHandler()
app.include_router(controller.router, prefix="/api/v1")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with agent information"""
    return {
        "agent": "QR & Barcode Generator",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "qr_generation": "/api/v1/qr",
            "barcode_generation": "/api/v1/barcode",
            "telex_webhook": "/api/v1/a2a/agent/qrBarcodeAgent",
            "health": "/api/v1/health"
        },
        "description": "Generate QR codes and barcodes for any text or data"
    }

# A2A Protocol endpoints
@app.get("/.well-known/agent.json")
async def get_agent_card():
    """Return agent card for A2A discovery"""
    import json
    with open(".well-known/agent.json", "r") as f:
        return json.load(f)

@app.post("/")
async def handle_a2a_request(request: Request):
    """Main A2A JSON-RPC endpoint"""
    try:
        body = await request.json()
        response = await a2a_handler.handle_request(body)
        return JSONResponse(content=response)
    except Exception as e:
        logger.error(f"A2A request error: {str(e)}")
        return JSONResponse(
            content={
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": "Parse error"
                }
            },
            status_code=400
        )

if __name__ == "__main__":
    port = int(os.getenv("AGENT_PORT", 8000))
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=port,
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )