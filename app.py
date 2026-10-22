import streamlit as st
import random
import time

st.set_page_config(
    page_title="PlayCircle Arcade",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# PLAYCIRCLE ARCADE - GAMING DESIGN
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Inter:wght@400;600;700;800&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at top left, #172554 0%, transparent 45%),
        radial-gradient(ellipse at bottom right, #3b0764 0%, transparent 45%),
        #080b18;
    color: #ffffff;
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1100px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4 {
    color: #ffffff !important;
    font-family: 'Orbitron', 'Inter', sans-serif !important;
    font-weight: 800 !important;
}

p, label, li, span {
    color: #f1f5ff;
}

.stCaption, small {
    color: #d1d5ff !important;
}

.pc-hero {
    background: linear-gradient(120deg, #101c46, #35105b);
    border: 2px solid #5b7cfa;
    border-radius: 24px;
    padding: 30px 22px;
    margin-bottom: 25px;
    box-shadow: 0 0 24px rgba(67, 97, 238, 0.25);
}

.pc-hero h1 {
    font-size: clamp(30px, 6vw, 48px) !important;
    line-height: 1.3;
    color: #ffffff !important;
    text-shadow: 0 0 15px #427bff;
}

.pc-hero p {
    font-size: 16px;
    font-weight: 700;
    color: #bdeaff !important;
}

.game-card {
    background: linear-gradient(145deg, #151f3e, #211536);
    border: 1px solid #5968a9;
    border-radius: 20px;
    padding: 22px;
    min-height: 165px;
    margin-bottom: 12px;
    box-shadow: 0 5px 18px rgba(0,0,0,0.25);
}

.game-icon {
    font-size: 38px;
}

.game-card h3 {
    color: #70f0ff !important;
    font-size: 21px !important;
}

.game-card p {
    font-size: 15px;
    line-height: 1.6;
    color: #f1f5ff !important;
}

div.stButton > button,
div.stFormSubmitButton > button {
    width: 100%;
    min-height: 48px;
    border-radius: 13px;
    border: 2px solid #637bff;
    background: linear-gradient(100deg, #245bff, #7c3aed);
    color: #ffffff !important;
    font-size: 15px !important;
    font-weight: 800 !important;
    transition: all 0.2s ease;
}

div.stButton > button:hover,
div.stFormSubmitButton > button:hover {
    border-color: #67f7ff;
    box-shadow: 0 0 18px rgba(67, 230, 255, 0.55);
    transform: translateY(-2px);
}

div[data-testid="stMetric"] {
    background: #141d38;
    border: 1px solid #5365a0;
    border-radius: 15px;
    padding: 16px;
}

div[data-testid="stMetricLabel"] {
    color: #dbeafe !important;
    font-weight: 700 !important;
}

div[data-testid="stMetricValue"] {
    color: #62f4ff !important;
    font-weight: 900 !important;
}

div[data-testid="stRadio"] label {
    background: #141d38;
    border: 1px solid #5365a0;
    border-radius: 10px;
    padding: 9px 12px;
    margin-bottom: 6px;
    color: #ffffff !important;
}

input, textarea {
    color: #ffffff !important;
}

div[data-baseweb="select"] > div {
    background-color: #141d38 !important;
    color: #ffffff !important;
    border-color: #7184cf !important;
}

div[data-baseweb="select"] * {
    color: #ffffff !important;
}

div[data-testid="stSidebar"] {
    background: #0c1227;
    border-right: 1px solid #5268be;
}

div[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #22d3ee, #a855f7);
}

.pc-correct {
    padding: 22px;
    border-radius: 16px;
    text-align: center;
    color: #ffffff;
    font-size: 22px;
    font-weight: 900;
    background: #064e3b;
    border: 2px solid #34d399;
    box-shadow: 0 0 22px #10b981;
    animation: pulse 0.7s ease-in-out 2;
}

.pc-wrong {
    padding: 22px;
    border-radius: 16px;
    text-align: center;
    color: #ffffff;
    font-size: 21px;
    font-weight: 900;
    background: #7f1d1d;
    border: 2px solid #fb7185;
    box-shadow: 0 0 18px #ef4444;
    animation: shake 0.4s ease-in-out;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.035); }
}

@keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-5px); }
    75% { transform: translateX(5px); }
}

.pc-neon {
    color: #67e8f9 !important;
    text-shadow: 0 0 12px #0891b2;
}

hr {
    border-color: #3b4775;
}

@media (max-width: 600px) {
    .pc-hero {
        padding: 22px 16px;
    }

    .game-card {
        padding: 16px;
    }

    h2 {
        font-size: 23px !important;
    }
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# 100-QUESTION QUIZ BANK
# =====================================================

questions = [
    ("Which planet is called the Red Planet?", ["Mars", "Venus", "Earth", "Jupiter"], "Mars"),
    ("How many sides does a triangle have?", ["Two", "Three", "Four", "Five"], "Three"),
    ("Which language structures web pages?", ["HTML", "Python", "C++", "SQL"], "HTML"),
    ("What is the largest ocean?", ["Atlantic", "Indian", "Arctic", "Pacific"], "Pacific"),
    ("How many days are in a leap year?", ["364", "365", "366", "367"], "366"),
    ("Which device is used for typing?", ["Monitor", "Keyboard", "Speaker", "Printer"], "Keyboard"),
    ("What is 9 × 7?", ["56", "63", "72", "49"], "63"),
    ("Which animal is known as the king of the jungle?", ["Tiger", "Elephant", "Lion", "Leopard"], "Lion"),
    ("What is the capital of France?", ["Rome", "Paris", "Madrid", "Berlin"], "Paris"),
    ("How many continents are there?", ["Five", "Six", "Seven", "Eight"], "Seven"),
    ("Which gas do humans need to breathe?", ["Oxygen", "Helium", "Hydrogen", "Neon"], "Oxygen"),
    ("What is H2O commonly called?", ["Salt", "Water", "Oxygen", "Sugar"], "Water"),
    ("Which star is closest to Earth?", ["Sirius", "The Sun", "Polaris", "Vega"], "The Sun"),
    ("How many hours are in a day?", ["12", "18", "24", "36"], "24"),
    ("Which organ pumps blood around the body?", ["Lungs", "Brain", "Heart", "Liver"], "Heart"),
    ("What is 12 × 12?", ["124", "144", "132", "154"], "144"),
    ("Which is the smallest prime number?", ["0", "1", "2", "3"], "2"),
    ("What is the opposite of ancient?", ["Old", "Modern", "Historic", "Former"], "Modern"),
    ("Which planet is famous for its rings?", ["Mercury", "Saturn", "Mars", "Earth"], "Saturn"),
    ("How many letters are in the English alphabet?", ["24", "25", "26", "27"], "26"),
    ("Which computer component performs calculations?", ["CPU", "Mouse", "Monitor", "Speaker"], "CPU"),
    ("What does URL identify?", ["A web address", "A keyboard", "A processor", "A printer"], "A web address"),
    ("Which device displays computer output?", ["Monitor", "Mouse", "Microphone", "Scanner"], "Monitor"),
    ("What does Wi-Fi provide?", ["Wireless networking", "Printing paper", "Electricity", "Storage only"], "Wireless networking"),
    ("Which of these is an operating system?", ["Windows", "Google Search", "HTML", "Wi-Fi"], "Windows"),
    ("Which symbol commonly begins a Python comment?", ["#", "//", "<!--", "$$"], "#"),
    ("What is the binary representation of decimal 1?", ["0", "1", "10", "11"], "1"),
    ("Which device moves a pointer on a computer?", ["Mouse", "Printer", "Speaker", "Router"], "Mouse"),
    ("What does CPU stand for?", ["Central Processing Unit", "Computer Power Utility", "Central Program Upload", "Control Printing Unit"], "Central Processing Unit"),
    ("Which is used to store files permanently?", ["SSD", "CPU register", "Cache only", "ALU"], "SSD"),
    ("Which country has the city of Tokyo?", ["China", "Japan", "Thailand", "India"], "Japan"),
    ("What is the capital of Nigeria?", ["Lagos", "Kano", "Abuja", "Enugu"], "Abuja"),
    ("Which continent is Nigeria in?", ["Asia", "Africa", "Europe", "South America"], "Africa"),
    ("What is the largest land animal?", ["Lion", "Giraffe", "African elephant", "Rhinoceros"], "African elephant"),
    ("Which animal is a mammal?", ["Crocodile", "Dolphin", "Eagle", "Frog"], "Dolphin"),
    ("How many legs does a spider have?", ["Six", "Eight", "Ten", "Twelve"], "Eight"),
    ("What do bees collect from flowers?", ["Sand", "Nectar", "Leaves", "Bark"], "Nectar"),
    ("What is a baby dog called?", ["Kitten", "Calf", "Puppy", "Cub"], "Puppy"),
    ("Which bird is known for mimicking human speech?", ["Parrot", "Penguin", "Ostrich", "Swan"], "Parrot"),
    ("What is the fastest land animal?", ["Horse", "Cheetah", "Lion", "Wolf"], "Cheetah"),
    ("At what temperature does water freeze in Celsius?", ["0", "10", "32", "100"], "0"),
    ("What force pulls objects toward Earth?", ["Friction", "Gravity", "Magnetism", "Pressure"], "Gravity"),
    ("Which part of a plant absorbs most water?", ["Flower", "Roots", "Fruit", "Petals"], "Roots"),
    ("What do plants absorb from the atmosphere for photosynthesis?", ["Oxygen", "Carbon dioxide", "Helium", "Hydrogen"], "Carbon dioxide"),
    ("Which vitamin can the body produce with sunlight exposure?", ["Vitamin A", "Vitamin B12", "Vitamin C", "Vitamin D"], "Vitamin D"),
    ("What is the boiling point of water at sea level in Celsius?", ["50", "75", "100", "150"], "100"),
    ("Which part of the cell contains most genetic material?", ["Nucleus", "Cell wall", "Ribosome", "Membrane"], "Nucleus"),
    ("Which blood cells help fight infection?", ["White blood cells", "Red blood cells", "Platelets only", "Plasma only"], "White blood cells"),
    ("What is Earth's natural satellite?", ["The Sun", "The Moon", "Mars", "Venus"], "The Moon"),
    ("Which energy source comes directly from sunlight?", ["Solar energy", "Coal", "Petrol", "Natural gas"], "Solar energy"),
    ("What is 100 divided by 4?", ["20", "25", "40", "50"], "25"),
    ("What is the square root of 81?", ["7", "8", "9", "10"], "9"),
    ("How many degrees are in a right angle?", ["45", "90", "180", "360"], "90"),
    ("What is 15 + 27?", ["32", "42", "43", "52"], "42"),
    ("What is 50% of 80?", ["20", "30", "40", "50"], "40"),
    ("Which shape has four equal sides and four right angles?", ["Rectangle", "Square", "Triangle", "Trapezoid"], "Square"),
    ("What is the next number: 2, 4, 6, 8, ...?", ["9", "10", "11", "12"], "10"),
    ("How many minutes are in two hours?", ["60", "90", "120", "180"], "120"),
    ("What is 7 cubed?", ["49", "147", "343", "512"], "343"),
    ("Which fraction equals one half?", ["2/3", "2/4", "3/4", "1/3"], "2/4"),
    ("What is the perimeter of a square with sides of 5 cm?", ["10 cm", "15 cm", "20 cm", "25 cm"], "20 cm"),
    ("Which word is a noun?", ["Quickly", "Happiness", "Run", "Blue"], "Happiness"),
    ("What is the plural of child?", ["Childs", "Children", "Childes", "Childrens"], "Children"),
    ("Which punctuation mark ends a direct question?", ["Comma", "Full stop", "Question mark", "Colon"], "Question mark"),
    ("Which word is an adjective?", ["Beautiful", "Run", "Quickly", "Under"], "Beautiful"),
    ("What is the past tense of go?", ["Goed", "Gone", "Went", "Going"], "Went"),
    ("Which is a synonym for happy?", ["Joyful", "Angry", "Tired", "Afraid"], "Joyful"),
    ("Which is an antonym of expand?", ["Grow", "Increase", "Contract", "Stretch"], "Contract"),
    ("What is the main language spoken in Brazil?", ["Spanish", "Portuguese", "French", "English"], "Portuguese"),
    ("How many vowels are in the English alphabet?", ["4", "5", "6", "7"], "5"),
    ("Which instrument has black and white keys?", ["Piano", "Flute", "Drum", "Trumpet"], "Piano"),
    ("Who paints pictures as an occupation?", ["Painter", "Carpenter", "Pilot", "Baker"], "Painter"),
    ("Which instrument typically has six strings?", ["Guitar", "Flute", "Tuba", "Drum"], "Guitar"),
    ("What is the art of making moving images called?", ["Cinema", "Sculpture", "Pottery", "Weaving"], "Cinema"),
    ("Which sport uses a racket and a shuttlecock?", ["Tennis", "Badminton", "Football", "Rugby"], "Badminton"),
    ("How many players from one team are on a football field during normal play?", ["9", "10", "11", "12"], "11"),
    ("Which sport uses a hoop and a bouncing ball?", ["Basketball", "Swimming", "Boxing", "Cycling"], "Basketball"),
    ("How many rings appear on the Olympic flag?", ["Four", "Five", "Six", "Seven"], "Five"),
    ("In chess, which piece moves in an L shape?", ["Bishop", "Knight", "Rook", "Queen"], "Knight"),
    ("Which sport is played at Wimbledon?", ["Tennis", "Golf", "Cricket", "Rugby"], "Tennis"),
    ("What is the currency of Japan?", ["Yuan", "Yen", "Won", "Rupee"], "Yen"),
    ("Which ocean lies between Africa and Australia?", ["Atlantic", "Indian", "Arctic", "Southern"], "Indian"),
    ("Which planet is closest to the Sun?", ["Mercury", "Venus", "Earth", "Mars"], "Mercury"),
    ("Which country is famous for the pyramids at Giza?", ["Egypt", "Greece", "Mexico", "Peru"], "Egypt"),
    ("What is the capital of Ghana?", ["Kumasi", "Accra", "Tamale", "Lagos"], "Accra"),
    ("Which is the largest continent by area?", ["Africa", "Asia", "Europe", "Antarctica"], "Asia"),
    ("What is the capital of Italy?", ["Athens", "Rome", "Lisbon", "Vienna"], "Rome"),
    ("Which ocean is on the east coast of the United States?", ["Pacific", "Atlantic", "Indian", "Arctic"], "Atlantic"),
    ("Which country is associated with the maple leaf symbol?", ["Canada", "Australia", "Brazil", "Kenya"], "Canada"),
    ("What is the currency used in the United States?", ["Euro", "Dollar", "Pound", "Yen"], "Dollar"),
    ("Which of these is a web browser?", ["Firefox", "Excel", "PowerPoint", "Notepad"], "Firefox"),
    ("What does HTTPS help provide for a website connection?", ["Encrypted communication", "Faster typing", "More battery", "Larger screens"], "Encrypted communication"),
    ("Which is a strong password practice?", ["Reuse one password", "Share passwords", "Use unique long passwords", "Use your name only"], "Use unique long passwords"),
    ("What is phishing?", ["A scam to trick people", "A computer monitor", "A file format", "A programming loop"], "A scam to trick people"),
    ("Which file extension is commonly used for Python programs?", [".py", ".jpg", ".mp3", ".docx"], ".py"),
    ("What does RAM primarily provide?", ["Temporary working memory", "Permanent paper storage", "Internet access", "Sound output"], "Temporary working memory"),
    ("Which device directs traffic between networks?", ["Router", "Keyboard", "Webcam", "Projector"], "Router"),
    ("Which number system uses only 0 and 1?", ["Decimal", "Binary", "Roman", "Hexadecimal only"], "Binary"),
    ("What does AI stand for?", ["Artificial Intelligence", "Automatic Internet", "Applied Interface", "Advanced Input"], "Artificial Intelligence"),
    ("Which action helps protect personal information online?", ["Share passwords publicly", "Use privacy settings", "Click every link", "Post account details"], "Use privacy settings"),
    ("Which is an example of cloud storage?", ["Google Drive", "A paper notebook", "A keyboard", "A power cable"], "Google Drive"),
    ("Which programming structure repeats instructions?", ["Loop", "Monitor", "Folder", "Pixel"], "Loop"),
    ("What is a database used for?", ["Organizing stored information", "Displaying only videos", "Charging devices", "Printing photographs only"], "Organizing stored information"),
]


# =====================================================
# SESSION STATE
# =====================================================

defaults = {
    "username": "",
    "page": "Home",
    "score": 0,
    "questions_answered": 0,
    "quiz_questions": [],
    "quiz_index": 0,
    "quiz_active": False,
    "quiz_finished": False,
    "quiz_size": 5,
    "quiz_feedback": None,
    "quiz_round_score": 0,
    "number_secret": None,
    "number_attempts": 0,
    "number_wins": 0,
    "rps_wins": 0,
    "rps_losses": 0,
    "rps_draws": 0,
    "last_rps": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================================
# HELPERS
# =====================================================

def go_to(page):
    st.session_state.page = page
    st.rerun()


def start_quiz(size):
    st.session_state.quiz_size = size
    selected = random.sample(questions, size)

    # Randomize answer positions independently for every question.
    prepared = []
    for question, options, answer in selected:
        shuffled_options = options.copy()
        random.shuffle(shuffled_options)
        prepared.append({
            "question": question,
            "options": shuffled_options,
            "answer": answer
        })

    st.session_state.quiz_questions = prepared
    st.session_state.quiz_index = 0
    st.session_state.quiz_round_score = 0
    st.session_state.quiz_feedback = None
    st.session_state.quiz_active = True
    st.session_state.quiz_finished = False
    go_to("Brain Battle")


# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

with st.sidebar:
    st.markdown("## 🎮 PLAYCIRCLE")
    st.caption("YOUR NEON ARCADE")

    if st.button("🏠 HOME", key="nav_home"):
        go_to("Home")

    if st.button("🧠 BRAIN BATTLE", key="nav_quiz"):
        go_to("Brain Battle")

    if st.button("🎯 GUESS THE NUMBER", key="nav_number"):
        go_to("Guess the Number")

    if st.button("✊ ROCK PAPER SCISSORS", key="nav_rps"):
        go_to("Rock Paper Scissors")

    if st.button("🏆 LEADERBOARD", key="nav_board"):
        go_to("Leaderboard")

    if st.button("👤 MY PROFILE", key="nav_profile"):
        go_to("My Profile")

    st.divider()
    st.caption("PLAY FAIR. THINK FAST. HAVE FUN.")


# =====================================================
# APP HEADER
# =====================================================

st.markdown("""
<div class="pc-hero">
    <h1>🎮 PLAYCIRCLE ARCADE</h1>
    <p>ENTER THE ARENA. CHALLENGE YOURSELF. OWN THE GAME.</p>
</div>
""", unsafe_allow_html=True)


# =====================================================
# HOME DASHBOARD
# =====================================================

if st.session_state.page == "Home":

    name = st.session_state.username or "Player"
    st.markdown(
        f"<h2 class='pc-neon'>WELCOME, {name.upper()}! 👾</h2>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="game-card">
            <div class="game-icon">🧠</div>
            <h3>BRAIN BATTLE</h3>
            <p>100 questions. Random challenges. Earn 10 points per correct answer.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("⚡ PLAY BRAIN BATTLE", key="home_quiz"):
            go_to("Brain Battle")

    with col2:
        st.markdown("""
        <div class="game-card">
            <div class="game-icon">🎯</div>
            <h3>GUESS THE NUMBER</h3>
            <p>Find the secret number with higher-or-lower hints.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🎯 PLAY GUESS THE NUMBER", key="home_number"):
            go_to("Guess the Number")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("""
        <div class="game-card">
            <div class="game-icon">✊</div>
            <h3>ROCK PAPER SCISSORS</h3>
            <p>Challenge the computer and track your results.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("✊ PLAY ROCK PAPER SCISSORS", key="home_rps"):
            go_to("Rock Paper Scissors")
            
            with col4:
        st.markdown("""
        <div class="game-card">
            <div class="game-icon">🏆</div>
            <h3>LEADERBOARD</h3>
            <p>View your current session points and progress.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🏆 VIEW LEADERBOARD", key="home_leaderboard"):
            go_to("Leaderboard")
