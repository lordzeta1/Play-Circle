import streamlit as st
import random
import html
import base64
import io
import math
import struct
import wave
from datetime import datetime

# ------------------------------------------------------------
# PLAYCIRCLE — Neon arcade gaming hub
# ------------------------------------------------------------
st.set_page_config(
    page_title="PlayCircle | Arcade",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Session state
defaults = {
    "page": "Home",
    "username": "PlayerOne",
    "points": 0,
    "correct_answers": 0,
    "games_played": 0,
    "quiz_questions": [],
    "quiz_index": 0,
    "quiz_score": 0,
    "quiz_finished": False,
    "quiz_feedback": "",
    "quiz_selected": None,
    "quiz_count": 5,
    "number_secret": None,
    "number_attempts": 0,
    "number_message": "",
    "rps_rounds": 0,
    "rps_wins": 0,
    "rps_message": "",
    "sound_enabled": True,
    "music_enabled": False,
    "last_sound": "",
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def go_to(page):
    st.session_state.page = page


# Small, self-generated sound effects/music. No external audio files required.
def make_wav(freq=440, duration=0.18, volume=0.12, sample_rate=22050, melody=None):
    """Create a short synthesized WAV in memory."""
    samples = []
    if melody:
        beat_duration = duration / len(melody)
        for note in melody:
            count = int(sample_rate * beat_duration)
            for i in range(count):
                t = i / sample_rate
                envelope = min(1.0, i / max(1, int(sample_rate * 0.012)))
                envelope *= min(1.0, (count - i) / max(1, int(sample_rate * 0.035)))
                samples.append(int(32767 * volume * envelope * math.sin(2 * math.pi * note * t)))
    else:
        count = int(sample_rate * duration)
        for i in range(count):
            t = i / sample_rate
            envelope = min(1.0, i / max(1, int(sample_rate * 0.01)))
            envelope *= max(0.0, 1 - i / count)
            samples.append(int(32767 * volume * envelope * math.sin(2 * math.pi * freq * t)))
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(b"".join(struct.pack("<h", max(-32768, min(32767, s))) for s in samples))
    return buffer.getvalue()


def audio_data_uri(wav_bytes):
    return "data:audio/wav;base64," + base64.b64encode(wav_bytes).decode("ascii")


def play_sound(kind):
    if not st.session_state.sound_enabled:
        return
    sounds = {
        "click": (520, 0.07, 0.08),
        "correct": (880, 0.22, 0.13),
        "wrong": (180, 0.24, 0.11),
        "win": (440, 0.55, 0.12),
    }
    if kind == "win":
        uri = audio_data_uri(make_wav(duration=0.55, volume=0.12, melody=[523, 659, 784, 1046]))
    else:
        freq, duration, volume = sounds.get(kind, sounds["click"])
        uri = audio_data_uri(make_wav(freq, duration, volume))
    st.markdown(
        f'<audio autoplay="autoplay"><source src="{uri}" type="audio/wav"></audio>',
        unsafe_allow_html=True,
    )


def music_player():
    if st.session_state.music_enabled:
        # A short original chiptune-style loop generated in memory.
        melody = [262, 330, 392, 523, 392, 330, 294, 349, 440, 587, 440, 349]
        music_uri = audio_data_uri(make_wav(duration=8.0, volume=0.055, melody=melody))
        st.markdown(
            f"""
            <audio autoplay loop controls style="width:100%;height:34px">
              <source src="{music_uri}" type="audio/wav">
            </audio>
            <small style="color:#a9b4d0">If music does not start automatically, press play above. Your browser may block autoplay.</small>
            """,
            unsafe_allow_html=True,
        )


# Styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
    :root { --bg:#080b18; --panel:#11182b; --cyan:#00f5ff; --pink:#ff38d1; --purple:#8b5cf6; --text:#f5f7ff; }
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background: radial-gradient(ellipse at top left, #17204a 0%, #080b18 46%, #050711 100%); color:var(--text); }
    [data-testid="stHeader"] { background:rgba(8,11,24,.82); }
    [data-testid="stSidebar"] { background:linear-gradient(180deg,#11182b,#090c19); border-right:1px solid #26365a; }
    [data-testid="stSidebar"] * { color:#f5f7ff !important; }
    h1,h2,h3,.arcade-title { font-family:'Orbitron',sans-serif !important; letter-spacing:1px; }
    h1 { color:#fff; text-shadow:0 0 18px #00d9ff77; }
    h2,h3 { color:#eafaff; }
    p, label, li, .stMarkdown { color:#e6eaff; }
    .hero { padding:26px 24px; border:1px solid #00f5ff66; border-radius:20px; background:linear-gradient(120deg,#14254aee,#24143fee); box-shadow:0 0 28px #00d9ff18,inset 0 0 24px #ff38d10a; margin-bottom:18px; }
    .hero h1 { margin:0 0 8px 0; font-size:clamp(28px,4vw,46px); }
    .hero p { margin:0; color:#c8d5f5; font-size:16px; }
    .game-card { min-height:185px; padding:20px; border-radius:18px; border:1px solid #33466e; background:linear-gradient(145deg,#141d34,#101326); box-shadow:0 8px 25px #0005; margin-bottom:12px; }
    .game-icon { font-size:36px; margin-bottom:8px; }
    .game-card h3 { font-size:17px; margin:4px 0 10px; color:#00f5ff; }
    .game-card p { font-size:14px; color:#d3dbf4; }
    .metric-card { padding:16px; border-radius:14px; background:#121a30; border:1px solid #34466d; text-align:center; }
    .metric-value { font-family:'Orbitron',sans-serif; font-size:28px; color:#00f5ff; }
    .metric-label { color:#b8c5e7; font-size:12px; text-transform:uppercase; letter-spacing:1px; }
    .notice { padding:13px 16px; border-radius:12px; background:#111b33; border:1px solid #34466d; color:#eafaff; }
    .stButton > button { width:100%; border-radius:10px; border:1px solid #00d9ff; background:linear-gradient(100deg,#0a6f89,#542d93); color:white; font-weight:700; min-height:44px; transition:all .18s ease; }
    .stButton > button:hover { border-color:#ff38d1; color:white; box-shadow:0 0 18px #ff38d155; transform:translateY(-1px); }
    div[data-testid="stRadio"] label { color:#f5f7ff !important; }
    .small-muted { color:#b8c5e7; font-size:13px; }
    [data-testid="stMetricValue"] { color:#00f5ff; }
    hr { border-color:#283757; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar navigation and settings
with st.sidebar:
    st.markdown('<div class="arcade-title" style="font-size:24px;color:#00f5ff">🎮 PLAYCIRCLE</div>', unsafe_allow_html=True)
    st.caption("YOUR NEON ARCADE")
    st.markdown("---")
    pages = ["Home", "Brain Battle", "Guess the Number", "Rock Paper Scissors", "Leaderboard", "My Profile"]
    for page in pages:
        icon = {
            "Home": "🏠", "Brain Battle": "🧠", "Guess the Number": "🔢",
            "Rock Paper Scissors": "✊", "Leaderboard": "🏆", "My Profile": "👤"
        }[page]
        if st.button(f"{icon}  {page}", key=f"nav_{page}", type="primary" if st.session_state.page == page else "secondary"):
            go_to(page)
            st.rerun()
    st.markdown("---")
    st.markdown("### 🔊 Audio settings")
    st.session_state.sound_enabled = st.toggle("Game sound effects", value=st.session_state.sound_enabled)
    st.session_state.music_enabled = st.toggle("Background music", value=st.session_state.music_enabled)
    st.caption("Music can be turned on or off anytime.")
    st.markdown("---")
    st.caption("Play fair. Have fun. Level up.")

music_player()

# Question bank: 100 questions
QUESTION_BANK = [
("Which device is used to point and click on a computer?", ["Scanner", "Mouse", "Speaker", "Router"], "Mouse", "Computer Basics"),
("What does CPU stand for?", ["Central Processing Unit", "Computer Power Utility", "Central Program User", "Core Processing Unit"], "Central Processing Unit", "Computer Basics"),
("Which of these is an input device?", ["Monitor", "Printer", "Keyboard", "Speaker"], "Keyboard", "Computer Basics"),
("Which device displays computer output?", ["Monitor", "Mouse", "Microphone", "Joystick"], "Monitor", "Computer Basics"),
("Which key creates a space between words?", ["Shift", "Spacebar", "Escape", "Tab"], "Spacebar", "Computer Basics"),
("Which of these is an operating system?", ["Windows", "Google Chrome", "Microsoft Word", "YouTube"], "Windows", "Computer Basics"),
("What is the main function of RAM?", ["Long-term storage", "Temporary working memory", "Printing pages", "Connecting speakers"], "Temporary working memory", "Computer Basics"),
("Which device is used to print documents?", ["Scanner", "Printer", "Webcam", "Projector"], "Printer", "Computer Basics"),
("What does URL refer to?", ["A web address", "A computer battery", "A file type", "A keyboard layout"], "A web address", "Internet"),
("Which program is commonly used to create documents?", ["Microsoft Word", "Paint only", "Calculator", "Camera"], "Microsoft Word", "Software"),
("Which symbol is often used in an email address?", ["#", "@", "&", "%"], "@", "Internet"),
("Which of these is a web browser?", ["Chrome", "Excel", "PowerPoint", "Notepad"], "Chrome", "Internet"),
("What should you do with a strong password?", ["Share it publicly", "Reuse it everywhere", "Keep it private", "Post it online"], "Keep it private", "Cyber Safety"),
("Which is a safe online habit?", ["Click every pop-up", "Use unique passwords", "Share bank PINs", "Download unknown files"], "Use unique passwords", "Cyber Safety"),
("What does Wi-Fi help devices do?", ["Connect wirelessly to a network", "Print without ink", "Charge instantly", "Increase screen size"], "Connect wirelessly to a network", "Networking"),
("Which is a spreadsheet program?", ["Excel", "PowerPoint", "Paint", "VLC"], "Excel", "Software"),
("Which app is mainly used for slide presentations?", ["PowerPoint", "WordPad", "Calculator", "File Explorer"], "PowerPoint", "Software"),
("What does HTML help create?", ["Web page structure", "Computer hardware", "Wi-Fi signals", "Printed ink"], "Web page structure", "Web Development"),
("Which language is commonly used to style web pages?", ["CSS", "SQL", "Bash only", "C"], "CSS", "Web Development"),
("What does AI stand for?", ["Artificial Intelligence", "Automatic Internet", "Advanced Input", "Applied Icons"], "Artificial Intelligence", "Technology"),
("Which is a programming language?", ["Python", "Wi-Fi", "Bluetooth", "USB"], "Python", "Programming"),
("Which data type usually stores true or false?", ["Boolean", "String", "Image", "Folder"], "Boolean", "Programming"),
("What is a bug in software?", ["An error or flaw", "A computer mouse", "A security badge", "A monitor stand"], "An error or flaw", "Programming"),
("What does a loop do in programming?", ["Repeats instructions", "Deletes the keyboard", "Turns off the screen", "Prints only photos"], "Repeats instructions", "Programming"),
("Which is an example of cloud storage?", ["Google Drive", "A paper folder", "A desk drawer", "A USB cable"], "Google Drive", "Cloud Computing"),
("What is a database used for?", ["Organizing and storing data", "Cooling a laptop", "Drawing only", "Playing sound only"], "Organizing and storing data", "Databases"),
("What does USB commonly connect?", ["Devices and accessories", "Only buildings", "Only websites", "Only power stations"], "Devices and accessories", "Hardware"),
("Which component performs most computer calculations?", ["CPU", "Monitor", "Keyboard", "Mouse pad"], "CPU", "Hardware"),
("Which device captures live video?", ["Webcam", "Printer", "Speaker", "UPS"], "Webcam", "Hardware"),
("What does a backup help protect against?", ["Data loss", "Bright screens", "Slow typing only", "Low speaker volume"], "Data loss", "Cyber Safety"),
("Which file extension is commonly used for Python code?", [".py", ".jpg", ".mp3", ".pptx"], ".py", "Programming"),
("Which is a common image file format?", [".png", ".exe", ".sql", ".py"], ".png", "Computing"),
("What does Ctrl+C usually do?", ["Copy", "Paste", "Undo", "Save"], "Copy", "Computer Basics"),
("What does Ctrl+V usually do?", ["Paste", "Copy", "Print", "Close"], "Paste", "Computer Basics"),
("What does Ctrl+Z usually do?", ["Undo", "Zoom", "Save", "Select all"], "Undo", "Computer Basics"),
("Which is an output device?", ["Speaker", "Keyboard", "Mouse", "Scanner"], "Speaker", "Hardware"),
("What does a router commonly do?", ["Directs network traffic", "Types documents", "Scans photos", "Displays video"], "Directs network traffic", "Networking"),
("What is phishing?", ["A deceptive attempt to steal information", "A video format", "A safe backup", "A coding loop"], "A deceptive attempt to steal information", "Cyber Safety"),
("Why should software be updated?", ["To improve security and fix issues", "To reveal passwords", "To delete all files", "To stop backups"], "To improve security and fix issues", "Cyber Safety"),
("What is two-factor authentication?", ["An extra identity check", "Two usernames on paper", "A larger monitor", "A type of keyboard"], "An extra identity check", "Cyber Safety"),
("What does a search engine help you do?", ["Find information online", "Charge a phone", "Create electricity", "Print without a printer"], "Find information online", "Internet"),
("Which is an example of video conferencing?", ["A live online meeting", "A spreadsheet formula", "A file extension", "A keyboard shortcut"], "A live online meeting", "Internet"),
("What does LAN stand for?", ["Local Area Network", "Large Access Number", "Linked App Name", "Long Analog Node"], "Local Area Network", "Networking"),
("Which unit is commonly larger?", ["Gigabyte", "Kilobyte", "Byte", "Bit"], "Gigabyte", "Computing"),
("What is an algorithm?", ["A sequence of steps to solve a problem", "A computer screen", "A type of cable", "A photo filter"], "A sequence of steps to solve a problem", "Programming"),
("What is source code?", ["Instructions written by a programmer", "A monitor brand", "A network cable", "A printer tray"], "Instructions written by a programmer", "Programming"),
("What does Git help developers do?", ["Track changes to files", "Increase screen brightness", "Clean a keyboard", "Create Wi-Fi signals"], "Track changes to files", "Development"),
("What is GitHub commonly used for?", ["Hosting and collaborating on code", "Making phone calls", "Printing receipts", "Editing audio only"], "Hosting and collaborating on code", "Development"),
("What is a variable in programming?", ["A named place to store a value", "A physical cable", "A web browser", "A printer setting"], "A named place to store a value", "Programming"),
("Which SQL command retrieves data?", ["SELECT", "PAINT", "LAUNCH", "SPEAK"], "SELECT", "Databases"),
("What does HTTP help define?", ["Communication for web pages", "A computer battery", "An image size", "A typing speed"], "Communication for web pages", "Internet"),
("What is a firewall designed to do?", ["Filter network traffic", "Cool a computer", "Increase font size", "Store photos only"], "Filter network traffic", "Cyber Safety"),
("What is malware?", ["Harmful software", "A spreadsheet chart", "A safe password", "A display cable"], "Harmful software", "Cyber Safety"),
("What does encryption do?", ["Makes data unreadable without the right key", "Prints a file", "Speeds up typing", "Deletes a browser"], "Makes data unreadable without the right key", "Cyber Safety"),
("What is digital citizenship?", ["Responsible technology use", "Owning many devices", "A computer brand", "A game score"], "Responsible technology use", "Digital Citizenship"),
("Which is personal information?", ["Home address", "Public weather report", "A math formula", "A generic slogan"], "Home address", "Digital Citizenship"),
("What should you do before sharing someone else's photo?", ["Ask for permission", "Post it immediately", "Add their password", "Send it to strangers"], "Ask for permission", "Digital Citizenship"),
("What is cyberbullying?", ["Bullying using digital technology", "A computer upgrade", "A safe search", "A backup method"], "Bullying using digital technology", "Digital Citizenship"),
("Which is a good way to evaluate online information?", ["Check reliable sources", "Believe every headline", "Ignore dates", "Trust every anonymous post"], "Check reliable sources", "Digital Citizenship"),
("What is a spreadsheet cell?", ["Intersection of a row and column", "A browser tab", "A printer button", "A Wi-Fi password"], "Intersection of a row and column", "Software"),
("In Excel, what does SUM do?", ["Adds numbers", "Changes font only", "Opens a browser", "Deletes a sheet"], "Adds numbers", "Software"),
("Which chart is useful for showing parts of a whole?", ["Pie chart", "Keyboard chart", "Folder chart", "Cable chart"], "Pie chart", "Data"),
("What does a presentation slide contain?", ["Content for an audience", "Only computer parts", "A network password", "A database server"], "Content for an audience", "Software"),
("What is a PDF commonly used for?", ["Sharing documents with consistent layout", "Running a computer fan", "Connecting to Wi-Fi", "Programming a CPU"], "Sharing documents with consistent layout", "Files"),
("Which is an example of an open-source operating system?", ["Linux", "Microsoft Word", "PowerPoint", "Photoshop"], "Linux", "Software"),
("What does responsive web design aim to do?", ["Adapt layouts to different screen sizes", "Make every page audio-only", "Require one exact screen", "Disable mobile devices"], "Adapt layouts to different screen sizes", "Web Development"),
("What is a website homepage?", ["The main entry page of a site", "A computer's power button", "A spreadsheet row", "A keyboard key"], "The main entry page of a site", "Web Development"),
("What is a domain name?", ["A readable name for an internet address", "A computer fan", "A programming error", "A type of RAM"], "A readable name for an internet address", "Internet"),
("What is an API?", ["A way for software systems to communicate", "A keyboard layout", "A type of monitor", "A photo album"], "A way for software systems to communicate", "Development"),
("What does debugging mean?", ["Finding and fixing code errors", "Designing a logo only", "Replacing a mouse", "Uploading music"], "Finding and fixing code errors", "Programming"),
("What is a function in programming?", ["Reusable block of instructions", "A computer chair", "A network signal", "A monitor setting"], "Reusable block of instructions", "Programming"),
("What does an if statement do?", ["Chooses actions based on a condition", "Always repeats forever", "Prints every file", "Changes a cable"], "Chooses actions based on a condition", "Programming"),
("What is a list in Python?", ["A collection of items", "A web address", "A computer screen", "A type of printer"], "A collection of items", "Programming"),
("What is a string in programming?", ["Text data", "A network router", "A graphics card", "A battery"], "Text data", "Programming"),
("What is a server?", ["A computer or program providing services", "A mouse button", "A font style", "A game controller only"], "A computer or program providing services", "Networking"),
("What does bandwidth describe?", ["Data-carrying capacity of a connection", "Screen height", "Keyboard weight", "Battery colour"], "Data-carrying capacity of a connection", "Networking"),
("What is latency?", ["Delay before data transfer responds", "The size of a keyboard", "A file name", "A monitor colour"], "Delay before data transfer responds", "Networking"),
("What does Bluetooth usually provide?", ["Short-range wireless connections", "Long-term file printing", "A web domain", "A spreadsheet formula"], "Short-range wireless connections", "Networking"),
("What is an IP address used for?", ["Identifying a device on a network", "Naming a Word document", "Cleaning a screen", "Charging a laptop"], "Identifying a device on a network", "Networking"),
("What is a QR code?", ["A scannable code that stores information", "A computer fan", "A type of keyboard", "A programming loop"], "A scannable code that stores information", "Technology"),
("What is machine learning?", ["AI methods that learn patterns from data", "A manual typewriter", "A printer cable", "A file folder"], "AI methods that learn patterns from data", "AI"),
("Why should AI outputs be checked?", ["They can contain mistakes", "They are always perfect", "They never use data", "They cannot produce text"], "They can contain mistakes", "AI"),
("What is a prompt in generative AI?", ["Instructions or input given to the AI", "A computer's power cord", "A file extension", "A screen protector"], "Instructions or input given to the AI", "AI"),
("What is a sensor?", ["A component that detects a condition", "A web browser", "A text document", "A programming language"], "A component that detects a condition", "Technology"),
("What does GPS help determine?", ["Location", "Typing speed", "Screen brightness", "File size"], "Location", "Technology"),
("What is a digital footprint?", ["Traces of activity left online", "A shoe size stored in RAM", "A computer mouse pad", "A type of monitor"], "Traces of activity left online", "Digital Citizenship"),
("What should you do if a message asks for your password unexpectedly?", ["Verify it through an official channel", "Reply with the password", "Forward it to everyone", "Ignore all security advice"], "Verify it through an official channel", "Cyber Safety"),
("What is a passphrase?", ["A longer sequence of words used as a secret", "A public username", "A computer port", "A display setting"], "A longer sequence of words used as a secret", "Cyber Safety"),
("What does a UPS help provide?", ["Temporary backup power", "Internet search results", "Extra storage space", "A new operating system"], "Temporary backup power", "Hardware"),
("What is a GPU especially designed to handle?", ["Graphics and parallel processing", "Typing letters", "Printing paper", "Managing passwords only"], "Graphics and parallel processing", "Hardware"),
("What does SSD stand for?", ["Solid State Drive", "Secure Screen Display", "System Software Data", "Simple Storage Directory"], "Solid State Drive", "Hardware"),
("What is virtualization?", ["Running virtual computer environments on hardware", "Drawing a paper map", "Making a keyboard wireless", "Scanning a photo"], "Running virtual computer environments on hardware", "Cloud Computing"),
("What is SaaS?", ["Software delivered as an online service", "A computer's sound card", "A type of cable", "A file compression key"], "Software delivered as an online service", "Cloud Computing"),
("What is a data visualization?", ["A visual representation of data", "A password manager", "A computer chip", "A type of mouse"], "A visual representation of data", "Data"),
("What is a primary key in a database?", ["A field that uniquely identifies a record", "The first key on a keyboard", "A Wi-Fi code", "A backup cable"], "A field that uniquely identifies a record", "Databases"),
("What is a foreign key used for?", ["Linking related records between tables", "Opening a browser", "Changing a password", "Printing a document"], "Linking related records between tables", "Databases"),
("What does normalization help reduce in databases?", ["Unnecessary data duplication", "Screen glare", "Keyboard noise", "Internet speed"], "Unnecessary data duplication", "Databases"),
("What is a cache?", ["Temporary storage for faster access", "A permanent paper archive", "A display cable", "A programming error"], "Temporary storage for faster access", "Computing"),
("What does open-source software mean?", ["Its source code is available under a licence", "It has no source code", "It can never be changed", "It only works offline"], "Its source code is available under a licence", "Software"),
("What is a user interface?", ["The parts of a system a user interacts with", "A computer battery", "A server room", "A file backup"], "The parts of a system a user interacts with", "Design"),
("What is accessibility in digital design?", ["Making products usable by people with different needs", "Using only tiny fonts", "Removing all labels", "Using colour as the only signal"], "Making products usable by people with different needs", "Design"),
("What does a licence explain for software?", ["Terms for using and sharing it", "The screen resolution", "The CPU temperature", "The Wi-Fi signal strength"], "Terms for using and sharing it", "Software"),
("What is a local file?", ["A file stored on your device or local storage", "A file that exists only in the sky", "A web search result", "A public password"], "A file stored on your device or local storage", "Files"),
("What is a computer network?", ["Connected devices that exchange data", "A single paper notebook", "A slide animation", "A font family"], "Connected devices that exchange data", "Networking"),
("What is an e-learning platform?", ["A digital environment for learning", "A computer cooling fan", "A game score counter", "A printer cartridge"], "A digital environment for learning", "Education Technology"),
]

# Make sure the question bank has 100 items even if edited later.
QUESTION_BANK = QUESTION_BANK[:100]

def reset_quiz():
    st.session_state.quiz_questions = random.sample(QUESTION_BANK, min(st.session_state.quiz_count, len(QUESTION_BANK)))
    st.session_state.quiz_index = 0
    st.session_state.quiz_score = 0
    st.session_state.quiz_finished = False
    st.session_state.quiz_feedback = ""
    st.session_state.quiz_selected = None


def metric_card(value, label):
    st.markdown(
        f'<div class="metric-card"><div class="metric-value">{html.escape(str(value))}</div><div class="metric-label">{html.escape(label)}</div></div>',
        unsafe_allow_html=True,
    )


# HOME
if st.session_state.page == "Home":
    st.markdown(
        """
        <div class="hero">
          <h1>WELCOME TO PLAYCIRCLE ⚡</h1>
          <p>Your neon arcade for quick games, brain challenges, and friendly competition.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    a, b, c = st.columns(3)
    with a:
        metric_card(st.session_state.points, "Total points")
    with b:
        metric_card(st.session_state.games_played, "Games played")
    with c:
        metric_card(st.session_state.correct_answers, "Quiz answers correct")
    st.markdown("## 🕹️ Choose your game")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="game-card">
          <div class="game-icon">🧠</div>
          <h3>BRAIN BATTLE</h3>
          <p>Test your knowledge with a random quiz from a 100-question bank.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🧠 PLAY BRAIN BATTLE", key="home_brain"):
            go_to("Brain Battle")
            st.rerun()
    with col2:
        st.markdown("""
        <div class="game-card">
          <div class="game-icon">🔢</div>
          <h3>GUESS THE NUMBER</h3>
          <p>Can you guess the secret number in as few attempts as possible?</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔢 PLAY GUESS THE NUMBER", key="home_number"):
            go_to("Guess the Number")
            st.rerun()
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
            st.rerun()
    with col4:
        st.markdown("""
        <div class="game-card">
          <div class="game-icon">🏆</div>
          <h3>LEADERBOARD</h3>
          <p>View your points and progress in this session.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🏆 VIEW LEADERBOARD", key="home_leaderboard"):
            go_to("Leaderboard")
            st.rerun()
    st.info("Tip: Turn on Background music in the sidebar when you want an arcade soundtrack.")

# BRAIN BATTLE
elif st.session_state.page == "Brain Battle":
    st.markdown('<div class="hero"><h1>🧠 BRAIN BATTLE</h1><p>Think fast. Choose wisely. Earn points.</p></div>', unsafe_allow_html=True)
    if not st.session_state.quiz_questions or st.session_state.quiz_finished:
        st.markdown("### Choose your challenge")
        st.session_state.quiz_count = st.select_slider(
            "Number of questions",
            options=[5, 10, 15, 20, 25, 50, 100],
            value=st.session_state.quiz_count,
        )
        st.write(f"Your quiz will randomly select **{st.session_state.quiz_count}** questions.")
        if st.button("⚡ START NEW BATTLE", key="start_quiz"):
            reset_quiz()
            st.session_state.games_played += 1
            st.rerun()
        if st.session_state.quiz_finished:
            st.success(f"Battle complete! You scored {st.session_state.quiz_score} out of {len(st.session_state.quiz_questions)}.")
            st.metric("Points earned", st.session_state.quiz_score * 10)
            if st.button("🔁 PLAY AGAIN", key="quiz_again"):
                reset_quiz()
                st.session_state.games_played += 1
                st.rerun()
    else:
        total = len(st.session_state.quiz_questions)
        idx = st.session_state.quiz_index
        if idx >= total:
            st.session_state.quiz_finished = True
            st.rerun()
        q, options, answer, topic = st.session_state.quiz_questions[idx]
        st.progress(idx / total, text=f"Question {idx + 1} of {total}  •  {topic}")
        st.markdown(f"### {html.escape(q)}")
        choice = st.radio("Choose one answer:", options, key=f"quiz_choice_{idx}", index=None)
        if st.button("SUBMIT ANSWER", key=f"submit_{idx}", disabled=(choice is None)):
            if choice == answer:
                st.session_state.quiz_score += 1
                st.session_state.correct_answers += 1
                st.session_state.points += 10
                st.session_state.quiz_feedback = "correct"
                play_sound("correct")
                st.success("Correct! +10 points ⚡")
                st.balloons()
            else:
                st.session_state.quiz_feedback = "wrong"
                play_sound("wrong")
                st.error(f"Not quite! The correct answer is: {answer}")
            st.session_state.quiz_selected = choice
            st.session_state.quiz_index += 1
            if st.session_state.quiz_index >= total:
                st.session_state.quiz_finished = True
            st.rerun()
        st.caption("Correct answer: +10 points. Each battle uses a random selection from the question bank.")
        if st.button("Exit to Home", key="exit_quiz"):
            go_to("Home")
            st.rerun()

# GUESS THE NUMBER
elif st.session_state.page == "Guess the Number":
    st.markdown('<div class="hero"><h1>🔢 GUESS THE NUMBER</h1><p>The computer picked a number from 1 to 100.</p></div>', unsafe_allow_html=True)
    if st.session_state.number_secret is None:
        if st.button("🎲 START ROUND", key="start_number"):
            st.session_state.number_secret = random.randint(1, 100)
            st.session_state.number_attempts = 0
            st.session_state.number_message = "A secret number is ready. Make your first guess!"
            st.session_state.games_played += 1
            st.rerun()
    else:
        st.markdown(f'<div class="notice">{html.escape(st.session_state.number_message or "Make a guess!")}</div>', unsafe_allow_html=True)
        guess = st.number_input("Your guess (1–100)", min_value=1, max_value=100, value=50, step=1, key="number_guess")
        if st.button("CHECK GUESS", key="check_guess"):
            st.session_state.number_attempts += 1
            secret = st.session_state.number_secret
            if guess == secret:
                points = max(10, 100 - (st.session_state.number_attempts - 1) * 10)
                st.session_state.points += points
                st.session_state.number_message = f"🎉 Correct! You found {secret} in {st.session_state.number_attempts} attempts and earned {points} points."
                play_sound("win")
                st.success(st.session_state.number_message)
                st.session_state.number_secret = None
            elif guess < secret:
                st.session_state.number_message = "Too low! Try a higher number."
                play_sound("wrong")
                st.warning(st.session_state.number_message)
            else:
                st.session_state.number_message = "Too high! Try a lower number."
                play_sound("wrong")
                st.warning(st.session_state.number_message)
            st.rerun()
        st.caption(f"Attempts this round: {st.session_state.number_attempts}")
        if st.button("🆕 NEW NUMBER / RESET", key="reset_number"):
            st.session_state.number_secret = None
            st.session_state.number_attempts = 0
            st.session_state.number_message = ""
            st.rerun()

# ROCK PAPER SCISSORS
elif st.session_state.page == "Rock Paper Scissors":
    st.markdown('<div class="hero"><h1>✊ ROCK PAPER SCISSORS</h1><p>Pick your move and challenge the computer.</p></div>', unsafe_allow_html=True)
    player = st.radio("Choose your move:", ["✊ Rock", "✋ Paper", "✌️ Scissors"], horizontal=True, key="rps_choice")
    if st.button("⚔️ PLAY ROUND", key="play_rps"):
        computer = random.choice(["Rock", "Paper", "Scissors"])
        p = player.split(" ", 1)[1]
        st.session_state.rps_rounds += 1
        st.session_state.games_played += 1
        if p == computer:
            result = f"It's a draw! You both chose {computer}."
        elif (p == "Rock" and computer == "Scissors") or (p == "Paper" and computer == "Rock") or (p == "Scissors" and computer == "Paper"):
            result = f"You win! You chose {p}; computer chose {computer}. +10 points!"
            st.session_state.rps_wins += 1
            st.session_state.points += 10
            play_sound("win")
        else:
            result = f"Computer wins this round. You chose {p}; computer chose {computer}."
            play_sound("wrong")
        st.session_state.rps_message = result
    if st.session_state.rps_message:
        st.markdown(f'<div class="notice">{html.escape(st.session_state.rps_message)}</div>', unsafe_allow_html=True)
    x, y = st.columns(2)
    with x:
        metric_card(st.session_state.rps_rounds, "Rounds played")
    with y:
        metric_card(st.session_state.rps_wins, "Rounds won")

# LEADERBOARD
elif st.session_state.page == "Leaderboard":
    st.markdown('<div class="hero"><h1>🏆 LEADERBOARD</h1><p>Your current-session arcade stats.</p></div>', unsafe_allow_html=True)
    st.info("This prototype stores scores only for the current session. A shared leaderboard will need a database and player accounts.")
    st.markdown("### Current player")
    st.markdown(f'<div class="metric-card"><div class="metric-value">{html.escape(st.session_state.username)}</div><div class="metric-label">Player</div><div style="margin-top:12px;color:#f5f7ff">Total points: <b>{st.session_state.points}</b></div></div>', unsafe_allow_html=True)
    st.markdown("### Stats")
    a, b, c = st.columns(3)
    with a:
        metric_card(st.session_state.points, "Points")
    with b:
        metric_card(st.session_state.games_played, "Games played")
    with c:
        metric_card(st.session_state.correct_answers, "Correct quiz answers")
    if st.button("↻ RESET SESSION SCORES", key="reset_scores"):
        st.session_state.points = 0
        st.session_state.correct_answers = 0
        st.session_state.games_played = 0
        st.session_state.rps_rounds = 0
        st.session_state.rps_wins = 0
        st.success("Session scores reset.")
        st.rerun()

# PROFILE
elif st.session_state.page == "My Profile":
    st.markdown('<div class="hero"><h1>👤 MY PROFILE</h1><p>Make your player identity your own.</p></div>', unsafe_allow_html=True)
    st.session_state.username = st.text_input("Player name", value=st.session_state.username, max_chars=24)
    st.markdown("### Your arcade card")
    st.markdown(f'<div class="game-card"><div class="game-icon">🕹️</div><h3>{html.escape(st.session_state.username or "Player")}</h3><p>PlayCircle arcade player</p><p>⚡ Points: {st.session_state.points}</p><p>🎮 Games played: {st.session_state.games_played}</p></div>', unsafe_allow_html=True)
    st.caption("This profile is saved only in the active session for now.")

st.markdown("---")
st.markdown(
    '<div style="text-align:center;color:#98a8d0;font-size:12px;padding:8px">PLAYCIRCLE • NEON ARCADE • Keep playing, keep improving ⚡</div>',
    unsafe_allow_html=True,
)
