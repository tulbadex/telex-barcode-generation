from barcode import Code128, EAN13, EAN8, UPCA
from barcode.writer import ImageWriter
import io
import base64
import uuid
import os
from typing import Optional
from src.models.request_models import BarcodeFormat

class BarcodeService:
    """Service class for barcode generation following Single Responsibility Principle"""
    
    def __init__(self, output_dir: str = "static/images"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Barcode format mapping
        self.format_map = {
            BarcodeFormat.CODE128: Code128,
            BarcodeFormat.EAN13: EAN13,
            BarcodeFormat.EAN8: EAN8,
            BarcodeFormat.UPC: UPCA
        }
    
    def generate_barcode(self, text: str, format_type: BarcodeFormat = BarcodeFormat.CODE128) -> tuple[str, str]:
        """
        Generate barcode and return file path and base64 string
        
        Args:
            text: Text to encode
            format_type: Barcode format
            
        Returns:
            tuple: (file_path, base64_string)
        """
        try:
            # Get barcode class
            barcode_class = self.format_map.get(format_type, Code128)
            
            # Validate text for specific formats
            validated_text = self._validate_text_for_format(text, format_type)
            
            # Create barcode
            barcode = barcode_class(validated_text, writer=ImageWriter())
            
            # Generate unique filename
            filename = f"barcode_{uuid.uuid4().hex[:8]}"
            file_path = os.path.join(self.output_dir, filename)
            
            # Save barcode
            barcode.save(file_path)
            full_path = f"{file_path}.png"
            
            # Convert to base64
            with open(full_path, 'rb') as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode()
            
            return full_path, img_base64
            
        except Exception as e:
            raise Exception(f"Barcode generation failed: {str(e)}")
    
    def _validate_text_for_format(self, text: str, format_type: BarcodeFormat) -> str:
        """Validate and format text based on barcode type"""
        if format_type == BarcodeFormat.EAN13:
            # EAN13 needs 12 digits (13th is checksum)
            digits = ''.join(filter(str.isdigit, text))
            if len(digits) < 12:
                digits = digits.ljust(12, '0')
            return digits[:12]
        
        elif format_type == BarcodeFormat.EAN8:
            # EAN8 needs 7 digits (8th is checksum)
            digits = ''.join(filter(str.isdigit, text))
            if len(digits) < 7:
                digits = digits.ljust(7, '0')
            return digits[:7]
        
        elif format_type == BarcodeFormat.UPC:
            # UPC needs 11 digits (12th is checksum)
            digits = ''.join(filter(str.isdigit, text))
            if len(digits) < 11:
                digits = digits.ljust(11, '0')
            return digits[:11]
        
        # CODE128 can handle any text
        return text
    
    def cleanup_old_files(self, max_files: int = 100):
        """Clean up old barcode files to prevent storage overflow"""
        try:
            files = [f for f in os.listdir(self.output_dir) if f.startswith('barcode_')]
            if len(files) > max_files:
                files.sort(key=lambda x: os.path.getctime(os.path.join(self.output_dir, x)))
                for file in files[:-max_files]:
                    os.remove(os.path.join(self.output_dir, file))
        except Exception:
            pass  # Silent cleanup failure