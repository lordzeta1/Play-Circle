import streamlit as st
import random

st.set_page_config(
    page_title="PlayCircle | Game Zone",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- GAMING DESIGN ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #080b1a, #11152b, #170d2b);
    color: #f5f7ff;
}

.block-container {
    padding-top: 2rem;
    max-width: 1100px;
}

h1, h2, h3, p, label {
    color: #f5f7ff !important;
}

.pc-hero {
    padding: 30px 22px;
    border-radius: 24px;
    background: linear-gradient(120deg, #18285a, #35145e);
    border: 1px solid #536bff;
    margin-bottom: 24px;
}

.pc-hero h1 {
    font-size: 42px;
    margin-bottom: 8px;
}

.pc-hero p {
    color: #c9d3ff !important;
    font-size: 17px;
}

div.stButton > button {
    width: 100%;
    min-height: 52px;
    border-radius: 13px;
    border: 1px solid #6677ff;
    background: linear-gradient(100deg, #235dff, #803cff);
    color: white;
    font-weight: 700;
    transition: 0.2s;
}

div.stButton > button:hover {
    border-color: #54f5ff;
    color: white;
    box-shadow: 0 0 14px #514bff;
}

.game-card {
    background: linear-gradient(145deg, #171f3b, #211538);
    border: 1px solid #414a86;
    border-radius: 18px;
    padding: 22px;
    min-height: 155px;
    margin-bottom: 12px;
}

.game-icon {
    font-size: 34px;
}

.game-card h3 {
    color: #72eaff !important;
}

.pc-small {
    color: #b7c2e8 !important;
    font-size: 14px;
}

div[data-testid="stMetric"] {
    background: #171f3b;
    border: 1px solid #414a86;
    padding: 15px;
    border-radius: 15px;
}

div[data-testid="stMetricValue"] {
    color: #58f5ff;
}

.stProgress > div > div > div > div {
    background-color: #8b5cff;
}

hr {
    border-color: #343d65;
}
</style>
""", unsafe_allow_html=True)


# ---------- SESSION DATA ----------
if "username" not in st.session_state:
    st.session_state.username = ""

if "score" not in st.session_state:
    st.session_state.score = 0

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "feedback" not in st.session_state:
    st.session_state.feedback = None


# ---------- QUIZ QUESTIONS ----------
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
        "question": "Which language is used to structure web pages?",
        "options": ["HTML", "Python", "C++", "Java"],
        "answer": "HTML"
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
        "answer": "Pacific"
    },
    {
        "question": "How many days are in a leap year?",
        "options": ["364", "365", "366", "367"],
        "answer": "366"
    },
    {
        "question": "Which device is used to type text?",
        "options": ["Monitor", "Keyboard", "Speaker", "Printer"],
        "answer": "Keyboard"
    },
    {
        "question": "What is 9 x 7?",
        "options": ["56", "63", "72", "49"],
        "answer": "63"
    },
    {
        "question": "Which animal is known as the king of the jungle?",
        "options": ["Tiger", "Elephant", "Lion", "Leopard"],
        "answer": "Lion"
    }
]


# ---------- NAVIGATION ----------
def go_to(page):
    st.session_state.page = page
    st.rerun()


with st.sidebar:
    st.title("🎮 PlayCircle")
    st.caption("YOUR GAMING ZONE")

    if st.button("🏠 Home"):
        go_to("Home")

    if st.button("🧠 Brain Battle"):
        go_to("Brain Battle")

    if st.button("🏆 Leaderboard"):
        go_to("Leaderboard")

    if st.button("👤 My Profile"):
        go_to("My Profile")


# ---------- HEADER ----------
st.markdown("""
<div class="pc-hero">
    <h1>🎮 PlayCircle</h1>
    <p>PLAY TOGETHER. CHALLENGE YOURSELF. OWN THE GAME.</p>
</div>
""", unsafe_allow_html=True)


# ---------- HOME DASHBOARD ----------
if st.session_state.page == "Home":

    if st.session_state.username:
        st.subheader(f"Welcome back, {st.session_state.username}! 👋")
    else:
        st.subheader("Welcome, Player! 👋")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="game-card">
            <div class="game-icon">🧠</div>
            <h3>Brain Battle</h3>
            <p>Test your knowledge and earn points!</p>
            <p class="pc-small">QUIZ • THINK FAST • SCORE BIG</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🎮 PLAY BRAIN BATTLE", key="play_brain"):
            go_to("Brain Battle")

    with col2:
        st.markdown("""
        <div class="game-card">
            <div class="game-icon">🏆</div>
            <h3>Leaderboard</h3>
            <p>Check your current score and ranking.</p>
            <p class="pc-small">COMPETE • IMPROVE • ACHIEVE</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🏆 VIEW LEADERBOARD", key="view_board"):
            go_to("Leaderboard")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("""
        <div class="game-card">
            <div class="game-icon">👤</div>
            <h3>Player Profile</h3>
            <p>See your player name and gaming progress.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("👤 MY PROFILE", key="view_profile"):
            go_to("My Profile")

    with col4:
        st.markdown("""
        <div class="game-card">
            <div class="game-icon">🎯</div>
            <h3>More Games Coming</h3>
            <p>New challenges will join the arena soon.</p>
            <p class="pc-small">YOUR NEXT CHALLENGE AWAITS</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.subheader("⚡ Your Gaming Stats")

    m1, m2 = st.columns(2)

    with m1:
        st.metric("YOUR POINTS", st.session_state.score)

    with m2:
        st.metric(
            "QUESTIONS ANSWERED",
            st.session_state.question_index
        )

    st.divider()
    st.subheader("🪪 Join the Game")

    with st.form("player_name_form"):
        player_name = st.text_input(
            "Choose your player name",
            value=st.session_state.username,
            max_chars=20
        )

        save_name = st.form_submit_button("SAVE PLAYER NAME")

        if save_name:
            if player_name.strip():
                st.session_state.username = player_name.strip()
                st.success(f"Welcome to the arena, {player_name.strip()}!")
                st.rerun()
            else:
                st.warning("Enter a player name first.")


# ---------- BRAIN BATTLE ----------
elif st.session_state.page == "Brain Battle":

    st.subheader("🧠 BRAIN BATTLE")
    st.caption("EIGHT QUESTIONS. TEN POINTS PER CORRECT ANSWER.")

    if not st.session_state.username:
        st.warning("Choose your player name on the Home dashboard first.")

        if st.button("🏠 GO TO HOME"):
            go_to("Home")

    elif st.session_state.question_index < len(questions):

        index = st.session_state.question_index
        question = questions[index]

        st.progress(index / len(questions))
        st.write(f"**QUESTION {index + 1} OF {len(questions)}**")
        st.markdown(f"### {question['question']}")

        selected_answer = st.radio(
            "Choose your answer:",
            question["options"],
            key=f"question_{index}"
        )

        if st.button("⚡ LOCK IN ANSWER", key=f"submit_{index}"):

            if selected_answer == question["answer"]:
                st.session_state.score += 10
                st.session_state.feedback = ("correct", "Correct! +10 points 🎉")
            else:
                st.session_state.feedback = (
                    "wrong",
                    f"The correct answer is {question['answer']}."
                )

            st.session_state.question_index += 1
            st.rerun()

    else:
        st.success("🏆 CHALLENGE COMPLETED!")

        st.metric("FINAL SCORE", st.session_state.score)

        st.write("Great effort! Ready for another round?")

        if st.button("🔄 PLAY AGAIN"):
            st.session_state.score = 0
            st.session_state.question_index = 0
            st.session_state.feedback = None
            go_to("Brain Battle")

        if st.button("🏠 BACK TO DASHBOARD"):
            go_to("Home")

    if st.session_state.feedback:
        kind, message = st.session_state.feedback

        if kind == "correct":
            st.success(message)
        else:
            st.error(message)

    if st.button("🏠 DASHBOARD", key="brain_home"):
        go_to("Home")


# ---------- LEADERBOARD ----------
elif st.session_state.page == "Leaderboard":

    st.subheader("🏆 PLAYER LEADERBOARD")
    st.write("Your current session results.")

    if st.session_state.username:
        st.markdown(
            f"### 🥇 {st.session_state.username}"
        )
        st.metric("YOUR POINTS", st.session_state.score)
        st.caption(
            "This is your current session score, not a shared global ranking yet."
        )
    else:
        st.info("Choose a player name on the Home dashboard to get started.")

    if st.button("🧠 PLAY BRAIN BATTLE"):
        go_to("Brain Battle")

    if st.button("🏠 BACK TO DASHBOARD"):
        go_to("Home")


# ---------- PROFILE ----------
elif st.session_state.page == "My Profile":

    st.subheader("👤 PLAYER PROFILE")

    if st.session_state.username:
        st.markdown(f"### 🎮 {st.session_state.username}")
        st.metric("TOTAL SESSION POINTS", st.session_state.score)
        st.metric("QUESTIONS ANSWERED", st.session_state.question_index)
    else:
        st.info("Choose a player name on the Home dashboard.")

    if st.button("🧠 PLAY BRAIN BATTLE"):
        go_to("Brain Battle")

    if st.button("🏠 BACK TO DASHBOARD"):
        go_to("Home")


st.divider()
st.caption("🎮 PLAYCIRCLE • ENTER THE ARENA • PLAY FAIR • HAVE FUN")
