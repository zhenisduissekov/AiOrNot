import streamlit as st
import random

# --- Mock AI Detector Function ---
def mock_ai_detector(text):
    """Mock function to simulate AI detection. Replace with real API call if available."""
    # For demo: random probability based on text length and some keywords
    ai_keywords = ['GPT', 'AI', 'neural', 'language model', 'generated']
    score = 0.2 * sum(kw.lower() in text.lower() for kw in ai_keywords)
    score += min(len(text) / 500, 1) * 0.5  # longer texts more likely AI
    score += random.uniform(0, 0.3)
    return min(int(score * 100), 100)

# --- Predefined Texts for Guessing Game ---
GAME_TEXTS = [
    {"text": "The mitochondria is the powerhouse of the cell.", "label": "human"},
    {"text": "In a world where technology evolves rapidly, artificial intelligence shapes our future.", "label": "ai"},
    {"text": "I went to the store yesterday and bought some apples.", "label": "human"},
    {"text": "The quick brown fox jumps over the lazy dog.", "label": "human"},
    {"text": "As an AI language model, I can assist you with a variety of tasks.", "label": "ai"},
    {"text": "Quantum computing leverages quantum bits to perform complex calculations.", "label": "ai"},
]

# --- Sidebar Navigation ---
st.sidebar.title("AI or Not?")
mode = st.sidebar.radio("Choose a mode:", ["AI vs Human Text Detection", "AI vs Human Text Guessing Game"])

# --- AI vs Human Text Detection ---
if mode == "AI vs Human Text Detection":
    st.header("AI vs Human Text Detection")
    st.write("Paste a block of text below and find out the probability that it was written by AI.")

    user_text = st.text_area("Paste your text here:", height=150)
    if st.button("Detect AI Probability"):
        if user_text.strip():
            probability = mock_ai_detector(user_text)
            st.success(f"AI Probability: {probability}%")
            st.progress(probability)
        else:
            st.warning("Please paste some text to analyze.")

# --- AI vs Human Text Guessing Game ---
else:
    st.header("AI vs Human Text Guessing Game")
    st.write("Guess whether each text was written by a human or AI. 3 rounds per game.")

    # Session state for game progress
    if "game_round" not in st.session_state:
        st.session_state.game_round = 0
        st.session_state.score = 0
        st.session_state.indices = random.sample(range(len(GAME_TEXTS)), 3)
        st.session_state.guesses = []

    round_num = st.session_state.game_round

    if round_num < 3:
        idx = st.session_state.indices[round_num]
        current_text = GAME_TEXTS[idx]["text"]
        correct_label = GAME_TEXTS[idx]["label"]

        st.markdown(f"**Round {round_num + 1} of 3**")
        st.write(current_text)
        guess = st.radio("Your guess:", ["human", "ai"], key=f"guess_{round_num}")

        if st.button("Submit Guess", key=f"submit_{round_num}"):
            st.session_state.guesses.append(guess)
            if guess == correct_label:
                st.session_state.score += 1
                st.success("Correct!")
            else:
                st.error(f"Incorrect! It was written by **{correct_label}**.")
            st.session_state.game_round += 1
            st.rerun()
    else:
        st.markdown(f"### Game Over! Your score: **{st.session_state.score} / 3**")
        st.write("Your guesses:")
        for i in range(3):
            idx = st.session_state.indices[i]
            label = GAME_TEXTS[idx]["label"]
            guess = st.session_state.guesses[i]
            st.write(f"Round {i+1}: You guessed **{guess}**. Correct answer: **{label}**.")

        if st.button("Play Again"):
            st.session_state.game_round = 0
            st.session_state.score = 0
            st.session_state.indices = random.sample(range(len(GAME_TEXTS)), 3)
            st.session_state.guesses = []
            # st.experimental_rerun()
            st.rerun()
