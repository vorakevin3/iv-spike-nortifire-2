import unittest
import subprocess
import time

class TestIntegration(unittest.TestCase):

    def test_app_run(self):
        # Run the main.py module as a subprocess and check it starts without error
        try:
            proc = subprocess.Popen(['python', '-m', 'iv_spike_notifier.app.main'])
            time.sleep(5)
            proc.terminate()
            proc.wait(timeout=5)
        except Exception as e:
            self.fail(f"App run failed with exception: {e}")

if __name__ == '__main__':
    unittest.main()
