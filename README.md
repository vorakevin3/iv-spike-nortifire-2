# IV Spike Notifier

## Overview
This project monitors implied volatility (IV) spikes in options data and sends notifications when significant changes are detected.

## How to Run
1. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Mac/Linux
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

## How to Share the Software
To share this software with someone else, you can:

1. **Package the Project Folder:**
   - Compress the entire `iv_spike_notifier` directory into a zip file.
   - Share the zip file via email, cloud storage (Google Drive, Dropbox), or any file transfer method.

2. **Use Git:**
   - Initialize a Git repository in the project folder (if not already done).
   - Push the code to a remote repository (GitHub, GitLab, Bitbucket).
   - Share the repository URL with the recipient.

3. **Provide Setup Instructions:**
   - Include this README file.
   - Ensure `requirements.txt` is included for dependency installation.
   - Instruct the recipient to create and activate a virtual environment, install dependencies, and run the app as above.

## Additional Notes
- The recipient needs Python 3.7+ installed.
- The app runs a FastAPI server with scheduled IV spike monitoring.
- Notifications are currently logged to console; you can extend to other notification methods.
