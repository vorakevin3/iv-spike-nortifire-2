import math
from scipy.stats import norm
from scipy.optimize import brentq

def black_scholes_price(S, K, T, r, sigma, option_type='call'):
    """Calculate Black-Scholes option price"""
    if T <= 0:
        return max(0, S - K) if option_type == 'call' else max(0, K - S)

    d1 = (math.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    if option_type == 'call':
        return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    else:
        return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

def implied_volatility(market_price, S, K, T, r, option_type='call'):
    """Numerically solve for implied volatility given market price"""
    try:
        # Define function whose root gives the IV
        def objective(sigma):
            return black_scholes_price(S, K, T, r, sigma, option_type) - market_price

        # Solve for IV
        return brentq(objective, 0.0001, 5.0, maxiter=1000)
    except Exception as e:
        return None

def option_delta(S, K, T, r, sigma, option_type='call'):
    """Calculate Delta of an option using Black-Scholes"""
    d1 = (math.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * math.sqrt(T))
    if option_type == 'call':
        return norm.cdf(d1)
    else:
        return -norm.cdf(-d1)

if __name__ == "__main__":
    S = 22000         # Current index price (e.g., NIFTY)
    r = 0.06          # Risk-free interest rate
    T = 7 / 365       # Days to expiry (e.g., 7 days)
    
    options = [
        {"K": 22200, "price": 130.0, "type": "call"},
        {"K": 21800, "price": 140.0, "type": "put"},
        {"K": 22100, "price": 145.0, "type": "call"},
        {"K": 21900, "price": 120.0, "type": "put"},
    ]
    
    for opt in options:
        iv = implied_volatility(
            market_price=opt["price"],
            S=S,
            K=opt["K"],
            T=T,
            r=r,
            option_type=opt["type"]
        )

        if iv is not None:
            delta = option_delta(S, opt["K"], T, r, iv, opt["type"])
            if 0.38 <= abs(delta) <= 0.42:
                print(f"{opt['type'].upper()} {opt['K']}: IV={iv:.2%}, \u0394={delta:.2f}")
