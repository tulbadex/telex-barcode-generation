import re
from typing import Dict, Any
from src.models.request_models import BarcodeFormat

class MessageParser:
    """Utility class for parsing Telex messages following Single Responsibility Principle"""
    
    def __init__(self):
        self.qr_pattern = re.compile(r'^qr\s+(?:size:(\d+)\s+)?(.+)', re.IGNORECASE)
        self.barcode_pattern = re.compile(r'^barcode\s+(?:format:(\w+)\s+)?(.+)', re.IGNORECASE)
    
    def parse_message(self, message: str) -> Dict[str, Any]:
        """
        Parse incoming message and extract command, parameters, and text
        
        Args:
            message: Raw message from Telex
            
        Returns:
            Dict containing parsed command information
        """
        message = message.strip()
        
        # Check for QR command
        qr_match = self.qr_pattern.match(message)
        if qr_match:
            size = int(qr_match.group(1)) if qr_match.group(1) else 10
            text = qr_match.group(2).strip()
            return {
                "type": "qr",
                "text": text,
                "size": min(max(size, 1), 40)  # Clamp between 1-40
            }
        
        # Check for barcode command
        barcode_match = self.barcode_pattern.match(message)
        if barcode_match:
            format_str = barcode_match.group(1) if barcode_match.group(1) else "code128"
            text = barcode_match.group(2).strip()
            
            # Validate format
            try:
                barcode_format = BarcodeFormat(format_str.lower())
            except ValueError:
                barcode_format = BarcodeFormat.CODE128
            
            return {
                "type": "barcode",
                "text": text,
                "format": barcode_format
            }
        
        # Check for help commands
        if message.lower() in ['help', 'commands', '?']:
            return {"type": "help"}
        
        # Default: treat as QR code text
        if len(message) > 0:
            return {
                "type": "qr",
                "text": message,
                "size": 10
            }
        
        return {"type": "help"}
    
    def extract_url_from_text(self, text: str) -> str:
        """Extract URL from text if present"""
        url_pattern = re.compile(r'https?://[^\s]+')
        match = url_pattern.search(text)
        return match.group(0) if match else text
    
    def validate_barcode_text(self, text: str, format_type: BarcodeFormat) -> bool:
        """Validate if text is suitable for specific barcode format"""
        if format_type in [BarcodeFormat.EAN13, BarcodeFormat.EAN8, BarcodeFormat.UPC]:
            # These formats need numeric data
            return bool(re.search(r'\d', text))
        return True  # CODE128 accepts any text