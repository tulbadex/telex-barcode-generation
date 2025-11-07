#!/usr/bin/env python3
"""
Start the QR & Barcode Generator Agent server
"""

import os
import sys
import subprocess
import time

def start_server():
    """Start the FastAPI server"""
    port = int(os.environ.get("PORT", 8000))
    
    print(f"Starting QR & Barcode Generator Agent on port {port}")
    print(f"Endpoints:")
    print(f"   GET  http://localhost:{port}/")
    print(f"   GET  http://localhost:{port}/health") 
    print(f"   POST http://localhost:{port}/ (A2A endpoint)")
    print(f"   GET  http://localhost:{port}/.well-known/agent.json")
    print(f"Press Ctrl+C to stop the server\n")
    
    try:
        # Start uvicorn server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "src.main:app", 
            "--host", "0.0.0.0", 
            "--port", str(port),
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\nServer stopped")

if __name__ == "__main__":
    start_server()