import unittest
from iv_spike_notifier.app.iv_calculator import black_scholes_price, implied_volatility

class TestIVCalculator(unittest.TestCase):

    def test_black_scholes_price_call(self):
        price = black_scholes_price(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type='call')
        self.assertAlmostEqual(price, 10.4506, places=4)

    def test_black_scholes_price_put(self):
        price = black_scholes_price(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type='put')
        self.assertAlmostEqual(price, 5.5735, places=4)

    def test_implied_volatility_call(self):
        market_price = 10.4506
        iv = implied_volatility(market_price, S=100, K=100, T=1, r=0.05, option_type='call')
        self.assertAlmostEqual(iv, 0.2, places=2)

    def test_implied_volatility_put(self):
        market_price = 5.5735
        iv = implied_volatility(market_price, S=100, K=100, T=1, r=0.05, option_type='put')
        self.assertAlmostEqual(iv, 0.2, places=2)

    def test_implied_volatility_invalid(self):
        iv = implied_volatility(-1, S=100, K=100, T=1, r=0.05, option_type='call')
        self.assertIsNone(iv)

if __name__ == '__main__':
    unittest.main()
