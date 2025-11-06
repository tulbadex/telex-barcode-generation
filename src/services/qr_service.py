import qrcode
from PIL import Image
import io
import base64
from typing import Optional
import uuid
import os

class QRCodeService:
    """Service class for QR code generation following Single Responsibility Principle"""
    
    def __init__(self, output_dir: str = "static/images"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_qr_code(self, text: str, size: int = 10) -> tuple[str, str]:
        """
        Generate QR code and return file path and base64 string
        
        Args:
            text: Text to encode
            size: QR code box size
            
        Returns:
            tuple: (file_path, base64_string)
        """
        try:
            # Create QR code instance
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=size,
                border=4,
            )
            
            qr.add_data(text)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Generate unique filename
            filename = f"qr_{uuid.uuid4().hex[:8]}.png"
            file_path = os.path.join(self.output_dir, filename)
            
            # Save image
            img.save(file_path)
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            return file_path, img_base64
            
        except Exception as e:
            raise Exception(f"QR code generation failed: {str(e)}")
    
    def cleanup_old_files(self, max_files: int = 100):
        """Clean up old QR code files to prevent storage overflow"""
        try:
            files = [f for f in os.listdir(self.output_dir) if f.startswith('qr_')]
            if len(files) > max_files:
                files.sort(key=lambda x: os.path.getctime(os.path.join(self.output_dir, x)))
                for file in files[:-max_files]:
                    os.remove(os.path.join(self.output_dir, file))
        except Exception:
            pass  # Silent cleanup failure