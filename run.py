#!/usr/bin/env python3
"""
QR & Barcode Generator Agent for Telex.im
Entry point for the application
"""

import os
import sys
from src.main import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    
    print(f"Starting QR & Barcode Generator Agent on port {port}")
    print(f"Endpoints:")
    print(f"   GET  http://localhost:{port}/")
    print(f"   GET  http://localhost:{port}/health") 
    print(f"   POST http://localhost:{port}/ (A2A endpoint)")
    print(f"Agent config: http://localhost:{port}/.well-known/agent.json")
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)