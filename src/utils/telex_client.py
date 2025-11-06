import requests
import asyncio
from typing import Optional, Dict, Any
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class TelexClient:
    """Client for communicating with Telex.im platform following A2A protocol"""
    
    def __init__(self):
        self.webhook_url = os.getenv("TELEX_WEBHOOK_URL", "https://api.telex.im/webhook")
        self.agent_name = os.getenv("AGENT_NAME", "QRBarcodeBot")
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": f"{self.agent_name}/1.0"
        })
    
    async def send_message(self, channel_id: str, message: str, image_data: Optional[str] = None) -> bool:
        """
        Send message to Telex channel
        
        Args:
            channel_id: Target channel ID
            message: Text message to send
            image_data: Optional base64 image data
            
        Returns:
            bool: Success status
        """
        try:
            payload = {
                "channel_id": channel_id,
                "agent_name": self.agent_name,
                "message": message,
                "timestamp": datetime.utcnow().isoformat(),
                "type": "text"
            }
            
            if image_data:
                payload["image"] = image_data
                payload["type"] = "image"
            
            response = self.session.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            
            logger.info(f"Message sent successfully to channel {channel_id}")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send message to Telex: {str(e)}")
            return False
    
    async def send_proactive_message(self, channel_id: str) -> bool:
        """
        Send daily proactive message with QR tips
        
        Args:
            channel_id: Target channel ID
            
        Returns:
            bool: Success status
        """
        tips = [
            "💡 QR Tip: Use QR codes for WiFi passwords - guests can connect instantly!",
            "💡 QR Tip: Create QR codes for your contact info - no more typing phone numbers!",
            "💡 QR Tip: Generate QR codes for event invitations with all details included!",
            "💡 QR Tip: Use QR codes for product information - link to manuals or specs!",
            "💡 QR Tip: Create QR codes for feedback forms - make surveys accessible!",
            "💡 QR Tip: Generate QR codes for social media profiles - instant follows!",
            "💡 QR Tip: Use QR codes for restaurant menus - contactless and updatable!"
        ]
        
        import random
        daily_tip = random.choice(tips)
        
        return await self.send_message(channel_id, daily_tip)
    
    def validate_a2a_response(self, response_data: Dict[str, Any]) -> bool:
        """
        Validate A2A response format
        
        Args:
            response_data: Response data to validate
            
        Returns:
            bool: Validation result
        """
        required_fields = ["text", "type"]
        return all(field in response_data for field in required_fields)
    
    async def register_agent(self, agent_config: Dict[str, Any]) -> bool:
        """
        Register agent with Telex platform
        
        Args:
            agent_config: Agent configuration
            
        Returns:
            bool: Registration success
        """
        try:
            registration_url = f"{self.webhook_url}/register"
            response = self.session.post(registration_url, json=agent_config, timeout=10)
            response.raise_for_status()
            
            logger.info("Agent registered successfully with Telex")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to register agent: {str(e)}")
            return False