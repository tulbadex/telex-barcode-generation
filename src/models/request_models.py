from pydantic import BaseModel, Field
from typing import Optional, Literal
from enum import Enum

class BarcodeFormat(str, Enum):
    CODE128 = "code128"
    EAN13 = "ean13"
    EAN8 = "ean8"
    UPC = "upc"

class QRRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000, description="Text to encode in QR code")
    size: Optional[int] = Field(default=10, ge=1, le=40, description="QR code size")

class BarcodeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=100, description="Text to encode in barcode")
    format: BarcodeFormat = Field(default=BarcodeFormat.CODE128, description="Barcode format")

class TelexMessage(BaseModel):
    message: str = Field(..., description="User message from Telex")
    user_id: Optional[str] = Field(default=None, description="User ID from Telex")
    channel_id: Optional[str] = Field(default=None, description="Channel ID from Telex")

class AgentResponse(BaseModel):
    success: bool
    message: str
    image_url: Optional[str] = None
    error: Optional[str] = None