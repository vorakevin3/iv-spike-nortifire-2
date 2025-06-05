import unittest
from iv_spike_notifier.app.iv_calculator import option_delta

class TestOptionDelta(unittest.TestCase):

    def test_option_delta_call(self):
        delta = option_delta(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type='call')
        self.assertAlmostEqual(delta, 0.6368, places=4)

    def test_option_delta_put(self):
        delta = option_delta(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type='put')
        self.assertAlmostEqual(delta, -0.3632, places=4)

if __name__ == '__main__':
    unittest.main()
