import streamlit as st
import openai
import pandas as pd
import os

# Load OpenAI API key from Streamlit Secrets
openai.api_key = os.getenv("OPENAI_API_KEY")

# Sample questions and ideal answers
QUESTIONS = [
    {
        "question": "What is QHT Clinic? And how many branches do you have?",
        "answer": "QHT Clinic is India's premier hair transplant leader with centres in Haridwar, Hyderabad, and New Delhi. 12+ years’ experience, 10,000+ surgeries, 99% success rate."
    },
    {
        "question": "What is QHT Technique? What is the success rate of your hair transplant?",
        "answer": "QHT is Quick Hair Transplant, an advanced FUE technique with simultaneous extraction and implantation. Graft survival is 98-99%, using 5X magnification, SAVA Implanters, and motorised punches."
    },
    {
        "question": "How many grafts do I need? Which area will it cover?",
        "answer": "Depends on baldness area, head size, and pattern. Approx. 4000–4500 grafts from occipital area + 1000–1500 from beard possible. Hairline drawn 6.5-7cm from glabella, age and face anatomy considered."
    },
    {
        "question": "Is my donor area sufficient for hair transplant?",
        "answer": "Doctor examines donor density. If good, up to 4000–4500 grafts from occipital and 1000–1500 from beard area possible."
    }
]

st.title("🎤 QHT AI Training & Scoring Demo")
st.write("This app asks questions and scores typed candidate answers using OpenAI.")

# Candidate Name
candidate_name = st.text_input("Enter Candidate/Doctor Name:")

# Select Question
question_index = st.number_input("Select Question Number", min_value=1, max_value=len(QUESTIONS), value=1)
q = QUESTIONS[question_index - 1]
st.subheader(f"Question {question_index}: {q['question']}")

# Candidate Answer (typed only)
user_answer = st.text_area("Type your answer here:")

# Evaluate Answer
if st.button("Evaluate My Answer") and user_answer.strip():
    with st.spinner("Scoring answer..."):
        prompt = f"""
        Question: {q['question']}
        Ideal Answer: {q['answer']}
        Candidate Answer: {user_answer}

        Score the candidate from 1-10 and give feedback in concise points.
        """
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a strict medical trainer."},
                    {"role": "user", "content": prompt}
                ]
            )
            feedback = response.choices[0].message.content
        except openai.error.RateLimitError:
            feedback = "API rate limit reached. Please try again later."
        except openai.error.AuthenticationError:
            feedback = "Authentication error. Check your API key."
        except Exception as e:
            feedback = f"An unexpected error occurred: {e}"

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


