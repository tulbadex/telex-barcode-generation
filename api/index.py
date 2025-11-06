"""
Vercel serverless function entry point for QR Barcode Agent
"""

import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.main import app

# Export the FastAPI app for Vercel
handler = app