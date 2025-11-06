#!/usr/bin/env python3
"""
QR & Barcode Generator Agent - A2A Protocol Implementation
Run without Docker for development and testing
"""

import os
import sys
import subprocess
import uvicorn
from dotenv import load_dotenv

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Dependencies installed")

def setup_environment():
    """Setup environment variables"""
    load_dotenv()
    
    # Create static directory if it doesn't exist
    os.makedirs("static/images", exist_ok=True)
    print("Static directories created")

def run_agent():
    """Run the QR Barcode Agent"""
    port = int(os.getenv("AGENT_PORT", 8000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    print(f"Starting QR & Barcode Generator Agent on port {port}")
    print(f"Debug mode: {debug}")
    print(f"A2A Endpoint: http://localhost:{port}/")
    print(f"Agent Card: http://localhost:{port}/.well-known/agent.json")
    print(f"Health Check: http://localhost:{port}/api/v1/health")
    
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=port,
        reload=debug,
        log_level="info" if debug else "warning"
    )

if __name__ == "__main__":
    try:
        # Check if dependencies are installed
        try:
            import fastapi
            import qrcode
            import barcode
        except ImportError:
            install_dependencies()
        
        setup_environment()
        run_agent()
        
    except KeyboardInterrupt:
        print("\nAgent stopped by user")
    except Exception as e:
        print(f"Error starting agent: {str(e)}")
        sys.exit(1)