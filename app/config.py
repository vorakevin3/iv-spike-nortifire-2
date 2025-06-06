"""
Configuration settings for IV Spike Notifier
"""
import os
from typing import List

# IV Spike Detection Settings
IV_SPIKE_THRESHOLD_PERCENT = float(os.getenv("IV_SPIKE_THRESHOLD", "10.0"))  # 10% spike threshold
SCAN_INTERVAL_SECONDS = int(os.getenv("SCAN_INTERVAL", "1"))  # Check every 1 second

# Symbols to monitor
SYMBOLS_TO_MONITOR: List[str] = [
    "NIFTY",
    "BANKNIFTY",
    "FINNIFTY",
    "SENSEX",
    "RELIANCE",
    "TCS",
    "HDFCBANK",
    "INFY"
]

# Strike ranges for each symbol (for simulation)
STRIKE_RANGES = {
    "NIFTY": list(range(19000, 22000, 50)),
    "BANKNIFTY": list(range(45000, 50000, 100)),
    "FINNIFTY": list(range(19000, 22000, 50)),
    "SENSEX": list(range(70000, 75000, 100)),
    "RELIANCE": list(range(2400, 2800, 50)),
    "TCS": list(range(3800, 4200, 50)),
    "HDFCBANK": list(range(1600, 1900, 25)),
    "INFY": list(range(1700, 2000, 25))
}

# Expiry dates (for simulation)
EXPIRY_DATES = [
    "2025-06-12",  # Weekly
    "2025-06-19",  # Weekly
    "2025-06-26",  # Monthly
    "2025-07-24",  # Next month
]

# Telegram Bot Settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID_HERE")

# Logging Settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# API Settings
FASTAPI_HOST = os.getenv("FASTAPI_HOST", "127.0.0.1")
FASTAPI_PORT = int(os.getenv("FASTAPI_PORT", "8000"))

# Data simulation settings
SIMULATION_IV_BASE_RANGE = (15.0, 35.0)  # Base IV range for options
SIMULATION_VOLATILITY_FACTOR = 0.15  # How much IV can change per update (15%)
