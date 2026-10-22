import streamlit as st
import random

st.set_page_config(
    page_title="PlayCircle",
    page_icon="🎮",
    layout="wide"
)

# Page styling
st.markdown("""
<style>
.stApp {
    background-color: #f5f7ff;
}
h1, h2, h3 {
    color: #243b80;
}
.game-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #e1e7f5;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# Session state
if "username" not in st.session_state:
    st.session_state.username = ""

if "score" not in st.session_state:
    st.session_state.score = 0

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

# Questions
questions = [
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Venus"],
        "answer": "Mars"
    },
    {
        "question": "How many sides does a triangle have?",
        "options": ["Two", "Three", "Four", "Five"],
        "answer": "Three"
    },
    {
        "question": "Which language is commonly used to create web pages?",
        "options": ["HTML", "Python", "C++", "Java"],
        "answer": "HTML"
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
        "answer": "Pacific"
    },
    {
        "question": "How many days are there in a leap year?",
        "options": ["364", "365", "366", "367"],
        "answer": "366"
    }
]

# Sidebar
st.sidebar.title("🎮 PlayCircle")
page = st.sidebar.radio(
    "Navigate",
    ["Home", "Brain Battle", "My Profile", "Leaderboard"]
)

# Home page
if page == "Home":
    st.title("🎮 Welcome to PlayCircle!")
    st.subheader("Play together. Challenge yourself. Have fun.")

    st.markdown("""
    <div class="game-card">
        <h3>Your next favourite game starts here!</h3>
        <p>Play fun mini-games, test your knowledge, and aim for the top.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("### 🕹️ Explore PlayCircle")

    col1, col2 = st.columns(2)

    with col1:
        st.info("🧠 **Brain Battle**\n\nAnswer quiz questions and earn points.")

    with col2:
        st.info("🏆 **Leaderboard**\n\nTrack your score during your session.")

    st.write("### 👋 Join the community")
    name = st.text_input(
        "Choose your player name",
        value=st.session_state.username,
        max_chars=20
    )

    if st.button("Save Player Name"):
        if name.strip():
            st.session_state.username = name.strip()
            st.success(f"Welcome to PlayCircle, {name.strip()}!")
        else:
            st.warning("Please enter a player name.")

# Brain Battle
elif page == "Brain Battle":
    st.title("🧠 Brain Battle")
    st.write("Answer correctly to earn 10 points!")

    if st.session_state.username == "":
        st.warning("Go to Home and choose a player name first.")
    else:
        if st.session_state.question_index < len(questions):
            q = questions[st.session_state.question_index]

            st.progress(
                st.session_state.question_index / len(questions)
            )

            st.subheader(
                f"Question {st.session_state.question_index + 1} "
                f"of {len(questions)}"
            )
            st.write(q["question"])

            answer = st.radio(
                "Choose your answer:",
                q["options"],
                key=f"answer_{st.session_state.question_index}"
            )

            if st.button("Submit Answer"):
                if answer == q["answer"]:
                    st.session_state.score += 10
                    st.success("Correct! +10 points 🎉")
                else:
                    st.error(f"Not quite! The correct answer is {q['answer']}.")

                st.session_state.question_index += 1
                st.rerun()

        else:
            st.success("Quiz completed! 🎉")
            st.metric("Your Final Score", st.session_state.score)

            if st.button("Play Again"):
                st.session_state.score = 0
                st.session_state.question_index = 0
                st.rerun()

# Profile
elif page == "My Profile":
    st.title("👤 My Profile")

    if st.session_state.username:
        st.subheader(f"Welcome, {st.session_state.username}!")
        st.metric("Current Score", st.session_state.score)
        st.write("Keep playing to improve your score!")
    else:
        st.info("Visit Home to choose your player name.")

# Leaderboard
elif page == "Leaderboard":
    st.title("🏆 Leaderboard")
    st.write("Your current session results:")

    if st.session_state.username:
        st.table({
            "Player": [st.session_state.username],
            "Points": [st.session_state.score]
        })
    else:
        st.info("Choose a player name on the Home page to get started.")

st.divider()
st.caption("PlayCircle • Play together. Compete fairly. Have fun.")
