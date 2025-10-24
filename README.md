# hand_ai_project

Quickstart (Windows):

1. Open Command Prompt in this folder.
2. Create venv and activate:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install deps:
   ```
   pip install -r requirements.txt
   ```
4. Run realtime demo:
   ```
   python main_realtime.py
   ```
Controls:
- Q : quit
- C : clear drawing trace

This project shows MediaPipe hand landmarks, draws a trail from the index fingertip,
and performs simple rule-based gesture detection for "thumbs-up" and "ok".
