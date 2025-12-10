"""
Telegram Bot Notification Service
FREE alternative to Twilio WhatsApp - full customization supported
"""
import os
import logging
import httpx
from typing import Optional

logger = logging.getLogger(__name__)


class TelegramService:
    """Service for sending Telegram notifications via Bot API."""
    
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.api_base = f"https://api.telegram.org/bot{self.bot_token}" if self.bot_token else None
        
        self._configured = bool(self.bot_token and self.chat_id)
        
        if self._configured:
            logger.info("Telegram service initialized successfully")
        else:
            logger.warning("Telegram service not configured - set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID")
    
    @property
    def is_configured(self) -> bool:
        """Check if the service is properly configured."""
        return self._configured
    
    async def send_message(self, message: str, parse_mode: str = "Markdown") -> dict:
        """
        Send a Telegram message.
        
        Args:
            message: The message text to send (supports Markdown/HTML)
            parse_mode: "Markdown" or "HTML"
            
        Returns:
            dict with status and message_id or error
        """
        if not self._configured:
            return {
                "success": False,
                "error": "Telegram service not configured. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID"
            }
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    f"{self.api_base}/sendMessage",
                    json={
                        "chat_id": self.chat_id,
                        "text": message,
                        "parse_mode": parse_mode,
                        "disable_web_page_preview": True
                    }
                )
                
                data = response.json()
                
                if data.get("ok"):
                    logger.info(f"Telegram message sent: {data['result']['message_id']}")
                    return {
                        "success": True,
                        "message_id": data["result"]["message_id"]
                    }
                else:
                    error = data.get("description", "Unknown error")
                    logger.error(f"Telegram API error: {error}")
                    return {
                        "success": False,
                        "error": error
                    }
                    
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def send_spike_alert(
        self,
        metric_name: str,
        network: str,
        current_value: float,
        previous_value: float,
        change_percent: float,
        direction: str  # "up" or "down"
    ) -> dict:
        """
        Send a formatted spike alert message.
        
        Args:
            metric_name: Name of the metric (e.g., "Leads", "Revenue")
            network: Network name (e.g., "Kelkoo", "Admedia", "MaxBounty")
            current_value: Current metric value
            previous_value: Previous metric value
            change_percent: Percentage change
            direction: "up" for increase, "down" for decrease
            
        Returns:
            dict with status
        """
        trend = "INCREASED" if direction == "up" else "DECREASED"
        alert_type = "[SPIKE UP]" if direction == "up" else "[SPIKE DOWN]"
        dashboard_url = os.getenv('FRONTEND_URL', 'https://googleadsdashboard-beta.vercel.app')
        
        message = f"""
*SPIKE ALERT* {alert_type}
━━━━━━━━━━━━━━━━━━━━━━━━

*Network:* {network}
*Metric:* {metric_name}
*Change:* {trend} by *{abs(change_percent):.1f}%*

*Previous:* {previous_value:,.2f}
*Current:* {current_value:,.2f}

━━━━━━━━━━━━━━━━━━━━━━━━
[View Dashboard]({dashboard_url}/dashboard/alerts)
"""
        return await self.send_message(message.strip())
    
    async def send_test_message(self) -> dict:
        """Send a test message to verify configuration."""
        threshold = os.getenv('SPIKE_THRESHOLD_PERCENT', '20')
        dashboard_url = os.getenv('FRONTEND_URL', 'https://googleadsdashboard-beta.vercel.app')
        
        message = f"""
*TellSpike Alert System*
━━━━━━━━━━━━━━━━━━━━━━━━

Status: CONNECTED

Telegram notifications are working.

*Alert Triggers:*
  - Kelkoo metrics change >{threshold}%
  - Admedia metrics change >{threshold}%
  - MaxBounty metrics change >{threshold}%

━━━━━━━━━━━━━━━━━━━━━━━━
[Open Dashboard]({dashboard_url}/dashboard)
"""
        return await self.send_message(message.strip())


# Singleton instance
_telegram_service: Optional[TelegramService] = None


async def get_telegram_service() -> TelegramService:
    """Get the singleton Telegram service instance."""
    global _telegram_service
    if _telegram_service is None:
        _telegram_service = TelegramService()
    return _telegram_service
