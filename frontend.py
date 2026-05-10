import streamlit as st
import requests
import os

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Babu Chor Police Dakat",
    layout="wide"
)

API = "http://localhost:5000"

# =========================
# IMAGE PATHS
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

cards = {
    "BABU": os.path.join(BASE_DIR, "images", "babu.png"),
    "CHOR": os.path.join(BASE_DIR, "images", "chor.png"),
    "POLICE": os.path.join(BASE_DIR, "images", "police.png"),
    "DAKAT": os.path.join(BASE_DIR, "images", "dakat.png"),
    "BACK": os.path.join(BASE_DIR, "images", "back.png")
}

# =========================
# SESSION STATE
# =========================

if "started" not in st.session_state:
    st.session_state.started = False

if "roles" not in st.session_state:
    st.session_state.roles = {}

if "babu" not in st.session_state:
    st.session_state.babu = ""

if "police" not in st.session_state:
    st.session_state.police = ""

if "scores" not in st.session_state:
    st.session_state.scores = {}

if "history" not in st.session_state:
    st.session_state.history = []

if "game_over" not in st.session_state:
    st.session_state.game_over = False

# =========================
# CSS
# =========================

st.markdown("""
<style>

body {
    background-color: #050816;
}

.main {
    background: #050816;
    color: white;
}

h1,h2,h3,h4,h5,p {
    color:white;
}

.stButton>button {
    width:100%;
    border-radius:12px;
    height:55px;
    font-size:20px;
    font-weight:bold;
    background:#00cc88;
    color:white;
    border:none;
}

.stButton>button:hover {
    background:#00ffaa;
    color:black;
}

.stSelectbox label {
    color:white !important;
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================

st.markdown("""
<h1 style='text-align:center; color:#FFD700; font-size:65px; margin-bottom:30px;'>
🎮 BABU CHOR POLICE DAKAT
</h1>
""", unsafe_allow_html=True)

# =========================
# START ROUND
# =========================

if st.button("🎲 START ROUND"):

    try:

        res = requests.get(f"{API}/start-round").json()

        st.session_state.started = True
        st.session_state.roles = res["roles"]
        st.session_state.babu = res["babu"]
        st.session_state.police = res["police"]

    except:
        st.error("❌ Backend server not running!")

# =========================
# SHOW PLAYERS
# =========================

if st.session_state.started:

    st.markdown("""
    <h1 style='color:#00ffcc; text-align:center; margin-top:20px;'>
    🎯 CURRENT ROUND
    </h1>
    """, unsafe_allow_html=True)

    cols = st.columns(4)

    for i, (player, role) in enumerate(st.session_state.roles.items()):

        with cols[i]:

            st.markdown(f"""
            <h2 style='text-align:center;'>{player}</h2>
            """, unsafe_allow_html=True)

            if player == st.session_state.babu:
                st.image(cards["BABU"], use_container_width=True)
                st.success(f"{player} is BABU 👑")

            elif player == st.session_state.police:
                st.image(cards["POLICE"], use_container_width=True)
                st.info(f"{player} is POLICE 🚓")

            else:
                st.image(cards["BACK"], use_container_width=True)
                st.warning("Hidden Card")

# =========================
# GUESS SECTION
# =========================

if st.session_state.started:

    st.markdown("""
    <h2 style='color:#FFD700; margin-top:30px;'>
    🚓 Police Guess
    </h2>
    """, unsafe_allow_html=True)

    remaining_players = [
        p for p in st.session_state.roles
        if p != st.session_state.babu
        and p != st.session_state.police
    ]

    chor_guess = st.selectbox("Guess CHOR 🕵️", remaining_players)

    dakat_options = [p for p in remaining_players if p != chor_guess]

    dakat_guess = st.selectbox("Guess DAKAT 😈", dakat_options)

    # =========================
    # SUBMIT GUESS
    # =========================

    if st.button("✅ SUBMIT GUESS"):

        try:

            res = requests.post(
                f"{API}/guess",
                json={
                    "chor": chor_guess,
                    "dakat": dakat_guess
                }
            ).json()

            st.session_state.scores = res["scores"]
            st.session_state.history = res["history"]
            st.session_state.game_over = res["game_over"]

            # =========================
            # FINAL REVEAL
            # =========================

            st.markdown("""
            <h1 style='color:#FFD700; text-align:center; margin-top:30px;'>
            🃏 FINAL REVEAL
            </h1>
            """, unsafe_allow_html=True)

            cols = st.columns(4)

            for i, (player, role) in enumerate(st.session_state.roles.items()):

                with cols[i]:

                    st.markdown(f"""
                    <h2 style='text-align:center;'>{player}</h2>
                    """, unsafe_allow_html=True)

                    st.image(cards[role], use_container_width=True)

                    if role == "BABU":
                        st.success("👑 BABU")
                    elif role == "POLICE":
                        st.info("🚓 POLICE")
                    elif role == "CHOR":
                        st.warning("🕵️ CHOR")
                    elif role == "DAKAT":
                        st.error("😈 DAKAT")

            # =========================
            # RESULT
            # =========================

            if res["result"] == "correct":
                st.success("🚓 Police guessed correctly! +500 pts")
            else:
                st.error("❌ Wrong Guess! CHOR +400, DAKAT +600")

        except Exception as e:
            st.error(f"❌ Error submitting guess: {e}")

# =========================
# GRAND LEADERBOARD
# =========================

if st.session_state.scores:

    st.markdown("""
    <h1 style='text-align:center; color:#FFD700; font-size:55px; margin-top:40px;'>
    🏆 GRAND LEADERBOARD 🏆
    </h1>
    """, unsafe_allow_html=True)

    sorted_scores = sorted(
        st.session_state.scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    cols = st.columns(4)

    for i, (player, score) in enumerate(sorted_scores):

        if i == 0:
            bg = "linear-gradient(135deg, #FFD700, #FFB800)"
            text_color = "black"
        else:
            bg = "linear-gradient(135deg, #1f2937, #111827)"
            text_color = "white"

        cols[i].markdown(f"""
        <div style="background:{bg}; padding:30px; border-radius:30px; text-align:center; box-shadow:0 10px 30px rgba(0,0,0,0.5); border:3px solid rgba(255,255,255,0.1); min-height:320px;">
            <div style="background:#111827; width:80px; height:80px; border-radius:50%; margin:auto; display:flex; align-items:center; justify-content:center; font-size:40px; font-weight:bold; color:#FFD700; margin-bottom:20px;">
                #{i + 1}
            </div>
            <h1 style="color:{text_color}; font-size:38px; margin-bottom:20px;">{player}</h1>
            <div style="background:rgba(0,0,0,0.25); padding:25px; border-radius:20px;">
                <div style="font-size:65px; font-weight:bold; color:#00ff99;">{score}</div>
                <div style="font-size:22px; color:white; margin-top:10px;">TOTAL POINTS</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# =========================
# ROUND HISTORY
# =========================

if st.session_state.history:

    st.markdown("""
    <h1 style='color:#00ffcc; margin-top:50px; text-align:center;'>
    📜 ROUND HISTORY
    </h1>
    """, unsafe_allow_html=True)

    for h in st.session_state.history:

        result_color = "#00ff99" if h["result"] == "correct" else "#ff4b4b"

        st.markdown(f"""
        <div style="background:#111827; padding:25px; margin-bottom:20px; border-radius:20px; border:1px solid #333; color:white;">
            <h2 style="color:#FFD700;">ROUND {h['round']}</h2>
            <h3>👑 BABU : {h['babu']}</h3>
            <h3>🚓 POLICE : {h['police']}</h3>
            <h3>🕵️ CHOR : {h['chor']}</h3>
            <h3>😈 DAKAT : {h['dakat']}</h3>
            <h2 style="color:{result_color};">RESULT : {h['result'].upper()}</h2>
        </div>
        """, unsafe_allow_html=True)

# =========================
# GAME OVER
# =========================

if st.session_state.game_over:

    winner = max(
        st.session_state.scores,
        key=st.session_state.scores.get
    )

    st.balloons()

    st.markdown(f"""
    <div style="background:linear-gradient(135deg, #FFD700, #FFB800); color:black; padding:50px; border-radius:30px; text-align:center; font-size:50px; font-weight:bold; margin-top:40px; box-shadow:0 10px 30px rgba(255,215,0,0.4);">
        🏆 WINNER : {winner}
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 RESET GAME"):

        requests.post(f"{API}/reset")

        st.session_state.started = False
        st.session_state.roles = {}
        st.session_state.babu = ""
        st.session_state.police = ""
        st.session_state.scores = {}
        st.session_state.history = []
        st.session_state.game_over = False

        st.rerun()