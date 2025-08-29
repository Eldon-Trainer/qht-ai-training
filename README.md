# QHT AI Training — Streamlit Prototype

This repository contains a simple Streamlit prototype for an AI-driven hybrid (text + audio upload) trainer that asks questions, transcribes audio using OpenAI's speech-to-text, and scores answers using an LLM.

## Files
- `app.py` — main Streamlit app
- `requirements.txt` — Python dependencies
- `README.md` — this file

## Deployment (Streamlit Cloud)
1. Create a GitHub repository and push these files (or use the GitHub web UI to create them).
2. Go to https://share.streamlit.io/ and sign in with GitHub.
3. Click **New app** → select the repository and branch (usually `main`) → set the main file path to `app.py` → click **Deploy**.
4. In your Streamlit app page, go to **Settings → Secrets** and add:
   - `OPENAI_API_KEY = "your_api_key_here"`
5. Reload the app. The app will now be able to call OpenAI APIs for transcription and scoring.

## Notes
- The prototype accepts typed answers or an uploaded audio file (mp3/wav). For an in-browser microphone recorder, additional work (e.g., `streamlit-webrtc`) is needed.
- Keep your OpenAI API key secret — don’t commit it to GitHub. Use Streamlit Secrets or environment variables.
