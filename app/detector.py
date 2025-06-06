from typing import List, Dict, Any
import math
from dataclasses import dataclass
from app.iv_calculator import implied_volatility, option_delta

@dataclass
class IVSpikeAlert:
    symbol: str
    strike: int
    expiry: str
    option_type: str
    old_iv: float
    new_iv: float
    change_percent: float
    timestamp: str

    def __str__(self) -> str:
        direction = "📈" if self.change_percent > 0 else "📉"
        return (f"{direction} {self.symbol} {self.strike}{self.option_type} "
                f"(Exp: {self.expiry}): IV {self.old_iv:.1f}% → {self.new_iv:.1f}% "
                f"({self.change_percent:+.1f}%)")

# Example function to filter options by delta ~0.40
def filter_options_by_delta(options: List[Dict[str, Any]], S: float, T: float, r: float) -> List[Dict[str, Any]]:
    """
    Filter options to include only those with abs(delta) around 0.40
    options: list of dicts with keys 'strike', 'last_price', 'option_type'
    S: spot price
    T: time to expiry in years
    r: risk-free rate
    """
    filtered = []
    for opt in options:
        iv = implied_volatility(
            market_price=opt['last_price'],
            S=S,
            K=opt['strike'],
            T=T,
            r=r,
            option_type=opt['option_type']
        )
        if iv is not None:
            delta = option_delta(S, opt['strike'], T, r, iv, opt['option_type'])
            if 0.38 <= abs(delta) <= 0.42:
                filtered.append({**opt, 'iv': iv, 'delta': delta})
    return filtered

# Provide the functions expected by main.py for compatibility
def detect_spikes(options_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return filter_options_by_delta(options_data, S=0, T=0, r=0)  # Placeholder values, adjust as needed

def get_detector_stats() -> dict:
    return {}

def get_recent_spikes(limit: int = 10) -> List[Dict[str, Any]]:
    return []
