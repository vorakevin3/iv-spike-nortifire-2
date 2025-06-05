"""
Notification system for IV spike alerts
Supports Telegram (and easily extendable to other platforms)
"""
import requests
import logging
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from .config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from .detector import IVSpikeAlert

logger = logging.getLogger(__name__)

class NotificationChannel(ABC):
    """Abstract base class for notification channels"""
    
    @abstractmethod
    def send_message(self, message: str) -> bool:
        """Send a message through this channel"""
        pass
    
    @abstractmethod
    def is_configured(self) -> bool:
        """Check if this channel is properly configured"""
        pass

class TelegramNotifier(NotificationChannel):
    """Telegram notification channel"""
    
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        
    def is_configured(self) -> bool:
        """Check if Telegram is properly configured"""
        return (self.bot_token != "YOUR_BOT_TOKEN_HERE" and 
                self.chat_id != "YOUR_CHAT_ID_HERE" and
                self.bot_token and self.chat_id)
    
    def send_message(self, message: str) -> bool:
        """Send message via Telegram"""
        if not self.is_configured():
            logger.warning("Telegram not configured - message not sent")
            return False
            
        try:
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(self.api_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                logger.info("Telegram message sent successfully")
                return True
            else:
                logger.error(f"Telegram API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False

class EmailNotifier(NotificationChannel):
    """Email notification channel (placeholder for future implementation)"""
    
    def __init__(self, smtp_server: str = "", email: str = "", password: str = ""):
        self.smtp_server = smtp_server
        self.email = email
        self.password = password
    
    def is_configured(self) -> bool:
        return False  # Not implemented yet
    
    def send_message(self, message: str) -> bool:
        logger.info("Email notifications not implemented yet")
        return False

class ConsoleNotifier(NotificationChannel):
    """Console/logging notification channel (for testing)"""
    
    def is_configured(self) -> bool:
        return True
    
    def send_message(self, message: str) -> bool:
        logger.info(f"CONSOLE NOTIFICATION: {message}")
        print(f"🔔 NOTIFICATION: {message}")
        return True

class NotificationManager:
    """Manages multiple notification channels"""
    
    def __init__(self):
        self.channels: List[NotificationChannel] = []
        self.sent_count = 0
        self.failed_count = 0
        
        # Initialize default channels
        self.telegram = TelegramNotifier(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
        self.console = ConsoleNotifier()
        self.email = EmailNotifier()  # Not implemented yet
        
        # Add configured channels
        if self.telegram.is_configured():
            self.channels.append(self.telegram)
            logger.info("Telegram notifications enabled")
        else:
            logger.warning("Telegram not configured - add your bot token and chat ID to config.py")
        
        # Always add console for testing
        self.channels.append(self.console)
    
    def add_channel(self, channel: NotificationChannel):
        """Add a new notification channel"""
        if channel.is_configured():
            self.channels.append(channel)
            logger.info(f"Added notification channel: {type(channel).__name__}")
    
    def send_notification(self, message: str) -> bool:
        """Send notification through all configured channels"""
        if not self.channels:
            logger.error("No notification channels configured")
            return False
        
        success = False
        for channel in self.channels:
            try:
                if channel.send_message(message):
                    success = True
                    self.sent_count += 1
                else:
                    self.failed_count += 1
            except Exception as e:
                logger.error(f"Error with notification channel {type(channel).__name__}: {e}")
                self.failed_count += 1
        
        return success
    
    def send_spike_alert(self, spike: IVSpikeAlert) -> bool:
        """Send formatted spike alert"""
        message = self._format_spike_message(spike)
        return self.send_notification(message)
    
    def send_multiple_spike_alerts(self, spikes: List[IVSpikeAlert]) -> bool:
        """Send multiple spike alerts (batched or individual)"""
        if not spikes:
            return True
            
        if len(spikes) == 1:
            return self.send_spike_alert(spikes[0])
        
        # For multiple spikes, send a summary
        message = self._format_multiple_spikes_message(spikes)
        return self.send_notification(message)
    
    def _format_spike_message(self, spike: IVSpikeAlert) -> str:
        """Format single spike alert message"""
        direction_emoji = "🚀" if spike.change_percent > 0 else "📉"
        urgency_emoji = "🔥" if abs(spike.change_percent) > 20 else "⚡"
        
        message = (
            f"{urgency_emoji} <b>IV SPIKE ALERT</b> {direction_emoji}\n\n"
            f"<b>Symbol:</b> {spike.symbol}\n"
            f"<b>Strike:</b> {spike.strike} {spike.option_type}\n"
            f"<b>Expiry:</b> {spike.expiry}\n"
            f"<b>IV Change:</b> {spike.old_iv:.1f}% → {spike.new_iv:.1f}%\n"
            f"<b>Change:</b> {spike.change_percent:+.1f}%\n"
            f"<b>Time:</b> {spike.timestamp.split('T')[1][:8]}"
        )
        
        return message
    
    def _format_multiple_spikes_message(self, spikes: List[IVSpikeAlert]) -> str:
        """Format multiple spikes summary message"""
        message = f"🔥 <b>MULTIPLE IV SPIKES DETECTED</b> ({len(spikes)} alerts)\n\n"
        
        for i, spike in enumerate(spikes[:10], 1):  # Limit to first 10
            message += (
                f"{i}. {spike.symbol} {spike.strike}{spike.option_type} "
                f"{spike.change_percent:+.1f}%\n"
            )
        
        if len(spikes) > 10:
            message += f"\n... and {len(spikes) - 10} more spikes"
        
        return message
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get notification statistics"""
        return {
            "channels_configured": len(self.channels),
            "messages_sent": self.sent_count,
            "messages_failed": self.failed_count,
            "success_rate": (self.sent_count / max(1, self.sent_count + self.failed_count)) * 100,
            "telegram_configured": self.telegram.is_configured(),
            "email_configured": self.email.is_configured()
        }
    
    def test_notifications(self) -> bool:
        """Send test notification to verify setup"""
        test_message = "🧪 <b>Test Notification</b>\n\nIV Spike Notifier is working correctly!"
        return self.send_notification(test_message)

# Global notification manager
notification_manager = NotificationManager()

# Public interface functions
def send_spike_alert(spike: IVSpikeAlert) -> bool:
    """Send single spike alert"""
    return notification_manager.send_spike_alert(spike)

def send_multiple_spike_alerts(spikes: List[IVSpikeAlert]) -> bool:
    """Send multiple spike alerts"""
    return notification_manager.send_multiple_spike_alerts(spikes)

def send_notification(message: str) -> bool:
    """Send custom notification message"""
    return notification_manager.send_notification(message)

def test_notifications() -> bool:
    """Test notification system"""
    return notification_manager.test_notifications()

def get_notification_stats() -> Dict[str, Any]:
    """Get notification statistics"""
    return notification_manager.get_statistics()
