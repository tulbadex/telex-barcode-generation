import uuid
import logging
from typing import Dict, Any, Optional
from src.services.qr_service import QRCodeService
from src.services.barcode_service import BarcodeService
from src.utils.message_parser import MessageParser

logger = logging.getLogger(__name__)

class A2AHandler:
    """Handler for A2A protocol JSON-RPC requests"""
    
    def __init__(self):
        self.qr_service = QRCodeService()
        self.barcode_service = BarcodeService()
        self.message_parser = MessageParser()
    
    async def handle_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming A2A JSON-RPC request
        
        Args:
            request_data: JSON-RPC request object
            
        Returns:
            JSON-RPC response object
        """
        try:
            method = request_data.get("method")
            request_id = request_data.get("id")
            params = request_data.get("params", {})
            
            if method == "message/send":
                result = await self._handle_message_send(params)
            else:
                return self._create_error_response(request_id, -32601, "Method not found")
            
            return self._create_success_response(request_id, result)
            
        except Exception as e:
            logger.error(f"A2A request handling error: {str(e)}")
            return self._create_error_response(
                request_data.get("id"), 
                -32603, 
                "Internal error"
            )
    
    async def _handle_message_send(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle message/send method"""
        try:
            message = params.get("message", {})
            parts = message.get("parts", [])
            
            # Extract text from parts
            text_content = ""
            for part in parts:
                if part.get("kind") == "text" or part.get("type") == "text":
                    text_content = part.get("text", "")
                    break
            
            if not text_content:
                return self._create_help_message()
            
            # Parse the message
            parsed_request = self.message_parser.parse_message(text_content)
            
            if parsed_request["type"] == "qr":
                return await self._generate_qr_response(parsed_request)
            elif parsed_request["type"] == "barcode":
                return await self._generate_barcode_response(parsed_request)
            else:
                return self._create_help_message()
                
        except Exception as e:
            logger.error(f"Message send handling error: {str(e)}")
            raise
    
    async def _generate_qr_response(self, parsed_request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate QR code and return A2A message"""
        try:
            file_path, base64_img = self.qr_service.generate_qr_code(
                parsed_request["text"], 
                parsed_request.get("size", 10)
            )
            
            return {
                "role": "agent",
                "parts": [
                    {
                        "kind": "text",
                        "text": f"QR code generated for: {parsed_request['text'][:50]}..."
                    },
                    {
                        "kind": "data",
                        "data": f"data:image/png;base64,{base64_img}",
                        "contentType": "image/png"
                    }
                ],
                "kind": "message",
                "messageId": str(uuid.uuid4())
            }
        except Exception as e:
            return {
                "role": "agent",
                "parts": [
                    {
                        "kind": "text",
                        "text": f"Error generating QR code: {str(e)}"
                    }
                ],
                "kind": "message",
                "messageId": str(uuid.uuid4())
            }
    
    async def _generate_barcode_response(self, parsed_request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate barcode and return A2A message"""
        try:
            file_path, base64_img = self.barcode_service.generate_barcode(
                parsed_request["text"],
                parsed_request.get("format", "code128")
            )
            
            return {
                "role": "agent",
                "parts": [
                    {
                        "kind": "text",
                        "text": f"Barcode generated for: {parsed_request['text']}"
                    },
                    {
                        "kind": "data",
                        "data": f"data:image/png;base64,{base64_img}",
                        "contentType": "image/png"
                    }
                ],
                "kind": "message",
                "messageId": str(uuid.uuid4())
            }
        except Exception as e:
            return {
                "role": "agent",
                "parts": [
                    {
                        "kind": "text",
                        "text": f"Error generating barcode: {str(e)}"
                    }
                ],
                "kind": "message",
                "messageId": str(uuid.uuid4())
            }
    
    def _create_help_message(self) -> Dict[str, Any]:
        """Create help message response"""
        help_text = """🔧 QR & Barcode Generator Bot

Commands:
• qr [text] - Generate QR code
• barcode [text] - Generate barcode
• qr size:15 [text] - QR with custom size
• barcode format:ean13 [text] - Barcode with format

Examples:
• qr https://example.com
• barcode 1234567890
• qr size:20 Hello World
• barcode format:ean13 123456789012

Supported formats: code128, ean13, ean8, upc"""
        
        return {
            "role": "agent",
            "parts": [
                {
                    "kind": "text",
                    "text": help_text
                }
            ],
            "kind": "message",
            "messageId": str(uuid.uuid4())
        }
    
    def _create_success_response(self, request_id: Any, result: Dict[str, Any]) -> Dict[str, Any]:
        """Create JSON-RPC success response"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }
    
    def _create_error_response(self, request_id: Any, code: int, message: str) -> Dict[str, Any]:
        """Create JSON-RPC error response"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }