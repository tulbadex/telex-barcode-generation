from fastapi import APIRouter, HTTPException, BackgroundTasks
from src.models.request_models import QRRequest, BarcodeRequest, TelexMessage, AgentResponse
from src.services.qr_service import QRCodeService
from src.services.barcode_service import BarcodeService
from src.utils.message_parser import MessageParser
from src.utils.telex_client import TelexClient
import logging

logger = logging.getLogger(__name__)

class AgentController:
    """Controller class handling agent endpoints following MVC pattern"""
    
    def __init__(self):
        self.router = APIRouter()
        self.qr_service = QRCodeService()
        self.barcode_service = BarcodeService()
        self.message_parser = MessageParser()
        self.telex_client = TelexClient()
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup API routes"""
        self.router.post("/qr", response_model=AgentResponse)(self.generate_qr)
        self.router.post("/barcode", response_model=AgentResponse)(self.generate_barcode)
        self.router.post("/a2a/agent/qrBarcodeAgent", response_model=dict)(self.handle_telex_message)
        self.router.get("/health")(self.health_check)
    
    async def generate_qr(self, request: QRRequest, background_tasks: BackgroundTasks) -> AgentResponse:
        """Generate QR code endpoint"""
        try:
            file_path, base64_img = self.qr_service.generate_qr_code(request.text, request.size)
            
            # Schedule cleanup
            background_tasks.add_task(self.qr_service.cleanup_old_files)
            
            return AgentResponse(
                success=True,
                message=f"QR code generated successfully for: {request.text[:50]}...",
                image_url=f"/static/images/{file_path.split('/')[-1]}"
            )
        except Exception as e:
            logger.error(f"QR generation error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def generate_barcode(self, request: BarcodeRequest, background_tasks: BackgroundTasks) -> AgentResponse:
        """Generate barcode endpoint"""
        try:
            file_path, base64_img = self.barcode_service.generate_barcode(request.text, request.format)
            
            # Schedule cleanup
            background_tasks.add_task(self.barcode_service.cleanup_old_files)
            
            return AgentResponse(
                success=True,
                message=f"Barcode generated successfully for: {request.text}",
                image_url=f"/static/images/{file_path.split('/')[-1]}"
            )
        except Exception as e:
            logger.error(f"Barcode generation error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def handle_telex_message(self, message_data: dict) -> dict:
        """Handle incoming Telex messages via A2A protocol"""
        try:
            # Parse message
            parsed_request = self.message_parser.parse_message(message_data.get("message", ""))
            
            if parsed_request["type"] == "qr":
                file_path, base64_img = self.qr_service.generate_qr_code(
                    parsed_request["text"], 
                    parsed_request.get("size", 10)
                )
                response_text = f"QR code generated for: {parsed_request['text'][:50]}..."
                
            elif parsed_request["type"] == "barcode":
                file_path, base64_img = self.barcode_service.generate_barcode(
                    parsed_request["text"],
                    parsed_request.get("format", "code128")
                )
                response_text = f"Barcode generated for: {parsed_request['text']}"
                
            else:
                response_text = self._get_help_message()
                base64_img = None
            
            # Return A2A response format
            response = {
                "text": response_text,
                "type": "text"
            }
            
            if base64_img:
                response["image"] = f"data:image/png;base64,{base64_img}"
                response["type"] = "image"
            
            return response
            
        except Exception as e:
            logger.error(f"Telex message handling error: {str(e)}")
            return {
                "text": f"Error processing request: {str(e)}",
                "type": "text"
            }
    
    async def health_check(self) -> dict:
        """Health check endpoint"""
        return {"status": "healthy", "agent": "QRBarcodeBot"}
    
    def _get_help_message(self) -> str:
        """Return help message for users"""
        return """
🔧 QR & Barcode Generator Bot

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

Supported formats: code128, ean13, ean8, upc
        """.strip()