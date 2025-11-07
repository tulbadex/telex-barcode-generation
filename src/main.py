from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import qrcode
import barcode
from barcode.writer import ImageWriter
import io
import base64
import os
import json
from typing import Optional, Dict, Any
from datetime import datetime

app = FastAPI(
    title="QR & Barcode Generator Agent for Telex.im",
    description="An AI agent that generates QR codes and barcodes for any text, URLs, or data",
    version="1.0.0"
)

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

class MessageRequest(BaseModel):
    text: Optional[str] = None
    message: Optional[str] = None

class QRRequest(BaseModel):
    text: str
    size: Optional[int] = 10

class BarcodeRequest(BaseModel):
    text: str
    format: Optional[str] = "code128"

@app.get("/")
async def root():
    """Home page with detailed agent information"""
    return {
        "name": "QR & Barcode Generator Agent",
        "description": "An AI agent that generates QR codes and barcodes for any text, URLs, or data",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "GET /": "Agent information and documentation",
            "GET /health": "Health check endpoint",
            "GET /.well-known/agent.json": "Agent configuration for Telex.im",
            "POST /": "A2A protocol endpoint for QR/barcode generation",
            "POST /api/v1/qr": "Direct QR code generation",
            "POST /api/v1/barcode": "Direct barcode generation"
        },
        "commands": {
            "qr [text]": "Generate QR code for any text or URL",
            "qr size:X [text]": "Generate QR code with custom size (1-40)",
            "barcode [text]": "Generate barcode with default format (CODE128)",
            "barcode format:X [text]": "Generate barcode with specific format"
        },
        "supported_formats": {
            "qr": ["Standard QR with customizable size (1-40)"],
            "barcode": ["CODE128", "EAN13", "EAN8", "UPC"]
        },
        "examples": [
            "qr Hello World",
            "qr https://example.com",
            "qr size:20 Contact: John Doe",
            "barcode 1234567890",
            "barcode format:ean13 123456789012"
        ],
        "integration": {
            "platform": "Telex.im",
            "protocol": "A2A",
            "repository": "https://github.com/tulbadex/telex-barcode-generation",
            "documentation": "https://telex-barcode-generation.vercel.app"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0",
        "uptime": "running"
    }

@app.get("/.well-known/agent.json")
async def agent_config():
    """Serve agent configuration for Telex.im"""
    try:
        with open(".well-known/agent.json", "r") as f:
            agent_data = json.load(f)
        return agent_data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Agent configuration not found")

@app.post("/")
async def a2a_endpoint(request: MessageRequest):
    """A2A protocol endpoint for Telex.im integration"""
    message = request.text or request.message or ""
    
    print(f"[A2A] Received: {message}")
    
    # Parse QR command
    if message.lower().startswith("qr "):
        return await handle_qr_command(message)
    
    # Parse barcode command
    elif message.lower().startswith("barcode "):
        return await handle_barcode_command(message)
    
    # Help command
    elif message.lower() in ["help", "commands"]:
        return {
            "text": "QR & Barcode Generator Agent\\n\\nCommands:\\n• qr [text] - Generate QR code\\n• qr size:X [text] - QR with custom size\\n• barcode [text] - Generate barcode\\n• barcode format:X [text] - Barcode with format\\n\\nExamples:\\n• qr Hello World\\n• qr size:20 https://example.com\\n• barcode 1234567890\\n• barcode format:ean13 123456789012",
            "type": "text"
        }
    
    # Default response
    return {
        "text": "QR & Barcode Generator Agent\\n\\nCommands:\\n• qr [text] - Generate QR code\\n• barcode [text] - Generate barcode\\n\\nType 'help' for more commands",
        "type": "text"
    }

async def handle_qr_command(message: str) -> Dict[str, Any]:
    """Handle QR code generation command"""
    # Parse command: "qr size:15 Hello World" or "qr Hello World"
    parts = message[3:].strip().split(" ", 1)
    
    size = 10  # default size
    text = ""
    
    if len(parts) == 1:
        text = parts[0]
    elif len(parts) == 2:
        if parts[0].startswith("size:"):
            try:
                size = int(parts[0].split(":")[1])
                size = max(1, min(40, size))  # Clamp between 1-40
                text = parts[1]
            except (ValueError, IndexError):
                text = " ".join(parts)
        else:
            text = " ".join(parts)
    
    if not text:
        return {
            "text": "Please provide text to generate QR code.\\nExample: qr Hello World\\nWith size: qr size:20 Hello World",
            "type": "text"
        }
    
    try:
        # Generate QR code
        qr = qrcode.QRCode(version=size, box_size=10, border=5)
        qr.add_data(text)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        print(f"[QR] Generated for: {text} (size: {size})")
        
        return {
            "text": f"QR code generated for: {text}",
            "type": "image",
            "image": f"data:image/png;base64,{img_str}"
        }
        
    except Exception as e:
        print(f"[QR] Error: {str(e)}")
        return {
            "text": f"QR generation failed: {str(e)}",
            "type": "text"
        }

async def handle_barcode_command(message: str) -> Dict[str, Any]:
    """Handle barcode generation command"""
    # Parse command: "barcode format:ean13 123456789012" or "barcode 1234567890"
    parts = message[8:].strip().split(" ", 1)
    
    format_type = "code128"  # default format
    text = ""
    
    if len(parts) == 1:
        text = parts[0]
    elif len(parts) == 2:
        if parts[0].startswith("format:"):
            format_type = parts[0].split(":")[1].lower()
            text = parts[1]
        else:
            text = " ".join(parts)
    
    if not text:
        return {
            "text": "Please provide text to generate barcode.\\nExample: barcode 1234567890\\nWith format: barcode format:ean13 123456789012",
            "type": "text"
        }
    
    try:
        # Validate format
        supported_formats = ["code128", "ean13", "ean8", "upc"]
        if format_type not in supported_formats:
            return {
                "text": f"Unsupported format: {format_type}\\nSupported formats: {', '.join(supported_formats)}",
                "type": "text"
            }
        
        # Format-specific validation
        if format_type == "ean13" and len(text) != 12:
            return {
                "text": "EAN13 requires exactly 12 digits.\\nExample: barcode format:ean13 123456789012",
                "type": "text"
            }
        
        if format_type == "ean8" and len(text) != 7:
            return {
                "text": "EAN8 requires exactly 7 digits.\\nExample: barcode format:ean8 1234567",
                "type": "text"
            }
        
        # Generate barcode
        barcode_class = barcode.get_barcode_class(format_type)
        code = barcode_class(text, writer=ImageWriter())
        
        # Convert to base64
        buffer = io.BytesIO()
        code.write(buffer)
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        print(f"[Barcode] Generated {format_type.upper()} for: {text}")
        
        return {
            "text": f"{format_type.upper()} barcode generated for: {text}",
            "type": "image",
            "image": f"data:image/png;base64,{img_str}"
        }
        
    except Exception as e:
        print(f"[Barcode] Error: {str(e)}")
        return {
            "text": f"Barcode generation failed: {str(e)}",
            "type": "text"
        }

@app.post("/api/v1/qr")
async def generate_qr(request: QRRequest):
    """Direct QR code generation endpoint"""
    try:
        qr = qrcode.QRCode(version=request.size, box_size=10, border=5)
        qr.add_data(request.text)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return {
            "success": True,
            "text": request.text,
            "size": request.size,
            "image": f"data:image/png;base64,{img_str}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/barcode")
async def generate_barcode(request: BarcodeRequest):
    """Direct barcode generation endpoint"""
    try:
        barcode_class = barcode.get_barcode_class(request.format)
        code = barcode_class(request.text, writer=ImageWriter())
        
        buffer = io.BytesIO()
        code.write(buffer)
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return {
            "success": True,
            "text": request.text,
            "format": request.format,
            "image": f"data:image/png;base64,{img_str}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)