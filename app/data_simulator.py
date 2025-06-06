"""
Market data simulator - Simulates NSE F&O option chain data
This will be replaced with real Arham Technologies API later
"""
import random
import logging
from typing import List, Dict, Any
from .config import (
    SYMBOLS_TO_MONITOR, 
    STRIKE_RANGES, 
    EXPIRY_DATES,
    SIMULATION_IV_BASE_RANGE,
    SIMULATION_VOLATILITY_FACTOR
)

logger = logging.getLogger(__name__)

class DataSimulator:
    def __init__(self):
        self.previous_ivs = {}  # Store previous IV values for continuity
        self.initialized = False
        
    def _generate_option_key(self, symbol: str, strike: int, expiry: str, option_type: str) -> str:
        """Generate unique key for option"""
        return f"{symbol}_{strike}_{expiry}_{option_type}"
    
    def _get_base_iv(self, symbol: str) -> float:
        """Get base IV for symbol (different symbols have different typical IV ranges)"""
        base_ivs = {
            "NIFTY": 20.0,
            "BANKNIFTY": 25.0,
            "FINNIFTY": 22.0,
            "SENSEX": 18.0,
            "RELIANCE": 28.0,
            "TCS": 24.0,
            "HDFCBANK": 26.0,
            "INFY": 30.0
        }
        return base_ivs.get(symbol, 25.0)
    
    def _simulate_iv_change(self, current_iv: float, symbol: str) -> float:
        """Simulate realistic IV changes"""
        # Most of the time, small changes
        if random.random() < 0.85:  # 85% chance of small change
            change_percent = random.uniform(-0.05, 0.05)  # ±5%
        else:  # 15% chance of larger change (potential spike)
            if random.random() < 0.7:  # 70% of large changes are positive (spikes)
                change_percent = random.uniform(0.05, 0.25)  # +5% to +25%
            else:
                change_percent = random.uniform(-0.15, -0.05)  # -15% to -5%
        
        new_iv = current_iv * (1 + change_percent)
        
        # Keep IV within reasonable bounds
        min_iv = self._get_base_iv(symbol) * 0.5
        max_iv = self._get_base_iv(symbol) * 2.5
        
        return max(min_iv, min(max_iv, new_iv))
    
    def fetch_option_data(self) -> List[Dict[str, Any]]:
        """
        Simulate fetching option chain data from API
        Returns list of option data dictionaries
        """
        try:
            options_data = []
            
            for symbol in SYMBOLS_TO_MONITOR:
                if symbol not in STRIKE_RANGES:
                    continue
                    
                # Get subset of strikes (simulate limited data)
                strikes = random.sample(STRIKE_RANGES[symbol], 
                                      min(10, len(STRIKE_RANGES[symbol])))
                
                for strike in strikes:
                    for expiry in EXPIRY_DATES[:2]:  # Use only first 2 expiries
                        for option_type in ['CE', 'PE']:
                            option_key = self._generate_option_key(symbol, strike, expiry, option_type)
                            
                            # Initialize IV if first time
                            if not self.initialized or option_key not in self.previous_ivs:
                                base_iv = self._get_base_iv(symbol)
                                # Add some randomness to base IV
                                iv = base_iv + random.uniform(-5.0, 5.0)
                                self.previous_ivs[option_key] = max(5.0, iv)
                            
                            # Simulate IV change
                            current_iv = self.previous_ivs[option_key]
                            new_iv = self._simulate_iv_change(current_iv, symbol)
                            self.previous_ivs[option_key] = new_iv
                            
                            # Create option data
                            last_price = round(random.uniform(10, 500), 2)
                            option_data = {
                                "symbol": symbol,
                                "strike": strike,
                                "expiry": expiry,
                                "option_type": option_type,
                                "iv": round(new_iv, 2),
                                "last_price": last_price,
                                "price": last_price,
                                "volume": random.randint(100, 10000),
                                "oi": random.randint(1000, 50000)
                            }
                            options_data.append(option_data)
            
            self.initialized = True
            logger.info(f"Simulated {len(options_data)} option data points")
            return options_data
            
        except Exception as e:
            logger.error(f"Error in data simulation: {e}")
            return []

# Global simulator instance
simulator = DataSimulator()

def fetch_option_data() -> List[Dict[str, Any]]:
    """Public interface to fetch option data"""
    return simulator.fetch_option_data()

def get_simulation_stats() -> Dict[str, Any]:
    """Get statistics about simulated data"""
    return {
        "total_options_tracked": len(simulator.previous_ivs),
        "symbols_monitored": SYMBOLS_TO_MONITOR,
        "initialized": simulator.initialized
    }
