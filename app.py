import streamlit as st
import openai
import pandas as pd
import os

# Load API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Sample questions & answers
QUESTIONS = [
    {
        "question": "What is QHT Clinic? And how many branches do you have?",
        "answer": "QHT Clinic is India's premier hair transplant leader with centres in Haridwar, Hyderabad, and New Delhi. It has 12+ years’ experience, 10,000+ surgeries, and 99% success rate."
    },
    {
        "question": "What is QHT Technique? What is the success rate of your hair transplant?",
        "answer": "QHT means Quick Hair Transplant, an advanced version of FUE with simultaneous extraction and implantation. Grafts survival is 98-99%. Uses 5X magnification, SAVA Implanters, and motorised punches of 0.6-0.75mm."
    },
    {
        "question": "How many grafts do I need? Which area will it cover?",
        "answer": "Depends on baldness area, head size, and pattern. Around 4000–4500 grafts from occipital area + 1000–1500 from beard possible. Hairline drawn 6.5-7cm from glabella, age and face anatomy considered."
    },
    {
        "question": "Is my donor area sufficient for hair transplant?",
        "answer": "Doctor examines donor density. If good, up to 4000–4500 grafts from occipital and 1000–1500 from beard area possible."
    }
]

# Title
st.title("🎤 QHT AI Training & Scoring Demo")
st.write("This app asks questions, records candidate responses, and scores them against the ideal answers.")

# Candidate Name
candidate_name = st.text_input("Enter Candidate/Doctor Name:")

# Select Question
question_index = st.number_input("Select Question Number", min_value=1, max_value=len(QUESTIONS), value=1)
q = QUESTIONS[question_index - 1]
st.subheader(f"Question {question_index}: {q['question']}")

# Candidate Answer
answer_mode = st.radio("Answer Mode", ["Type", "Upload Audio"])

user_answer = ""
if answer_mode == "Type":
    user_answer = st.text_area("Type your answer here")
elif answer_mode == "Upload Audio":
    uploaded_file = st.file_uploader("Upload audio (mp3/wav)", type=["mp3","wav"])
    if uploaded_file:
        transcript = openai.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=uploaded_file
        )
        user_answer = transcript.text
        st.success("Transcribed successfully!")

# Evaluate Answer
if st.button("Evaluate My Answer") and user_answer.strip():
    with st.spinner("Scoring answer..."):
        prompt = f"Question: {q['question']}\nIdeal Answer: {q['answer']}\nCandidate Answer: {user_answer}\n\nScore the candidate from 1-10 and give feedback."
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a strict medical trainer."},
                     {"role": "user", "content": prompt}]
        )
        feedback = response.choices[0].message.content

        st.markdown("### 📝 Feedback")
        st.write(feedback)

        # Save results
        history_file = "results_history.csv"
        new_result = pd.DataFrame({
            "Name": [candidate_name],
            "Question": [q['question']],
            "Answer": [user_answer],
            "Feedback": [feedback]
        })
        if os.path.exists(history_file):
            old = pd.read_csv(history_file)
            all_results = pd.concat([old, new_result], ignore_index=True)
        else:
            all_results = new_result
        all_results.to_csv(history_file, index=False)
        st.success("Result saved!")

# Show History
if st.checkbox("Show Previous Attempts"):
    if os.path.exists("results_history.csv"):
        df = pd.read_csv("results_history.csv")
        st.dataframe(df)
    else:
        st.info("No previous attempts yet.")

---

# requirements.txt

```
streamlit
openai
pandas
python-dotenv
```

---

# README.md (copy this into README.md in your repo)

```
# QHT AI Training — Streamlit Prototype


## Files
- `app.py` — main Streamlit app (paste into GitHub as the app file)
- `requirements.txt` — Python dependencies to install
- `README.md` — this file

## Deployment (Streamlit Cloud)
1. Create a GitHub repository and push these files (or use the GitHub web UI to create them).
2. Go to https://share.streamlit.io/ and sign in with GitHub.
3. Click **New app** → select the repository and branch (usually `main`) → set the main file path to `app.py` → click **Deploy**.
4. In your Streamlit app page, go to **Settings → Secrets** and add:
   - `OPENAI_API_KEY` = `sk-...` (your OpenAI API key)
5. Reload the app. The app will now be able to call OpenAI APIs for transcription and scoring.

## Notes
- The prototype accepts typed answers or an uploaded audio file (mp3/wav). For an in-browser microphone recorder, additional work (e.g., `streamlit-webrtc`) is needed.
- Keep your OpenAI API key secret — don’t commit it to GitHub. Use Streamlit Secrets or environment variables.

```

