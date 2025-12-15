# streamlit_app.py - AFYA-MIND FINAL WINNER (ERIC JEREMIAH)
# Full end-to-end app with login, screening, journal, fun questions, and final messages

import os
os.environ['PIL_AVIF_IGNORE'] = '1'
import streamlit as st

# === REAL QUESTIONS ===
PHQ9 = [
    "Little interest or pleasure in doing things?",
    "Feeling down, depressed, or hopeless?",
    "Trouble falling or staying asleep, or sleeping too much?",
    "Feeling tired or having little energy?",
    "Poor appetite or overeating?",
    "Feeling bad about yourself — or that you are a failure?",
    "Trouble concentrating on things?",
    "Moving or speaking so slowly? Or very fidgety/restless?",
    "Thoughts that you would be better off dead or hurting yourself?"
]

GAD7 = [
    "Feeling nervous, anxious or on edge?",
    "Not being able to stop or control worrying?",
    "Worrying too much about different things?",
    "Trouble relaxing?",
    "Being so restless that it is hard to sit still?",
    "Becoming easily annoyed or irritable?",
    "Feeling afraid as if something awful might happen?"
]

WERCAP = [
    "I hear sounds or voices that other people think aren't there.",
    "I feel that other people can read my thoughts or that I can read others' thoughts.",
    "I have visions or see things that others cannot see.",
    "I feel that I have special or supernatural powers.",
    "My thoughts are sometimes so strong that I can almost hear them.",
    "I have had experiences with the supernatural or spiritual world.",
    "I feel that parts of my body have changed into something else.",
    "People sometimes stare at me because of the way I look or behave.",
    "I feel like I am being followed or watched.",
    "I feel that I am not in control of my own ideas or thoughts.",
    "I have seen things that other people can't see or don't see.",
    "I have seen or heard things when dreaming/half-asleep that others say aren't real.",
    "I feel like electrical appliances or machines affect my thoughts.",
    "I feel that my thoughts are being taken away from me.",
    "I have had the experience of feeling that I am someone else.",
    "I have felt that I am not in control of my body.",
    "I have felt that my body has changed in some strange way.",
    "I have felt that I do not exist or that I have died.",
    "I have felt that I am being controlled by someone or something else.",
    "I have felt that my thoughts are being broadcast out loud.",
    "I have felt that thoughts were put into my head that were not my own.",
    "I have felt that I have no thoughts or an empty mind."
]

# === SCORING FUNCTION ===
def calculate_score(tool, answers):
    score = sum(answers)
    if tool == "PHQ-9":
        level = "Minimal" if score <= 4 else "Mild" if score <= 9 else "Moderate" if score <= 14 else "Moderately Severe" if score <= 19 else "Severe"
    elif tool == "GAD-7":
        level = "Minimal" if score <= 4 else "Mild" if score <= 9 else "Moderate" if score <= 14 else "Severe Anxiety"
    else:
        level = "Low Risk" if score <= 20 else "Moderate Risk" if score <= 40 else "High Risk"
    return score, level

# === APP CONFIG ===
st.set_page_config(page_title="AFYA-MIND", page_icon="🧠", layout="centered")

# === LOGIN PAGE WITH SAFE RERUN ===
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_submitted" not in st.session_state:
    st.session_state.login_submitted = False

if not st.session_state.logged_in:
    st.title("🌟 Welcome to AFYA-MIND 🌟")
    st.markdown("""
**Happiness starts here!**  
Hi there! I’m **MentaBot**, your AI friend. 😊  
We’re going to explore how you feel today — your joys, worries, and little wins.  
Take a deep breath. You are safe, you are heard, and we are friends.  
Let’s start your journey to feeling a bit lighter today.
""")
    st.markdown("Please enter your name to begin your healing journey")
   
    name = st.text_input("Your Name", placeholder="e.g., Eric, Amina, John...")

    if st.button("Start My Journey", type="primary"):
        if name.strip():
            st.session_state.logged_in = True
            st.session_state.user_name = name.strip()
            st.session_state.login_submitted = True
        else:
            st.error("Please enter your name")

# Safe rerun after login submission
if st.session_state.get("login_submitted"):
    st.session_state.login_submitted = False
    st.experimental_rerun()

# === MAIN APP ===
if st.session_state.get("logged_in"):
    st.title(f"Welcome back, {st.session_state.user_name} ")
    st.markdown("**You are safe here. Let's begin.**")

    # Choose Screening Tool
    tool = st.selectbox("Choose Screening Tool", ["PHQ-9 (Depression)", "GAD-7 (Anxiety)", "WERCAP (Psychosis Risk)"])
    questions = PHQ9 if "PHQ-9" in tool else GAD7 if "GAD-7" in tool else WERCAP

    st.markdown("### Over the last 2 weeks, how often have you been bothered by:")
    answers = []
    for i, q in enumerate(questions):
        val = st.radio(q, ["Not at all", "Several days", "More than half the days", "Nearly every day"],
                       index=0, horizontal=True, key=f"q{i}")
        answers.append(["Not at all", "Several days", "More than half the days", "Nearly every day"].index(val))

    journal = st.text_area("How are you really feeling today?", placeholder="e.g., Work stress, family pressure...")

    if st.button("Submit & Talk to MentaBot", type="primary"):
        score, level = calculate_score(tool.split()[0], answers)

        # Trigger detection
        text = journal.lower()
        trigger = "stress"
        if any(w in text for w in ["work","job","boss"]): trigger = "work stress"
        elif any(w in text for w in ["family","parent","child"]): trigger = "family"
        elif any(w in text for w in ["money","bill"]): trigger = "finances"
        elif any(w in text for w in ["exam","study"]): trigger = "academic pressure"
        elif journal.strip(): trigger = journal.strip().split()[0] + " concern"

        st.balloons()  # BUBBLES 1
        st.success(f"Score: {score} → {level}")
        st.info(f"Detected trigger: **{trigger.capitalize()}**")

        st.subheader("MentaBot is here for you")
        st.write(f"""
**Pole sana {st.session_state.user_name}** — I see you're carrying **{trigger}** today.
**Breathing exercise**: Inhale 4 → Hold 4 → Exhale 4 → Repeat 5 times.
**Now tell me —**
        """)

# === USER HAPPY ACTION + FUN QUESTIONS PERSISTENT ===
if "user_happy" not in st.session_state:
    st.session_state.user_happy = ""

st.session_state.user_happy = st.text_input(
    "What is one small thing I can do today to feel 1% better?",
    placeholder="Type anything and press Enter...",
    value=st.session_state.user_happy,
    key="hope_answer"
)

if st.session_state.user_happy.strip():
    st.balloons()  # BUBBLES 2

    if "PHQ-9" in tool:
        recovery = f"Doing **{st.session_state.user_happy}** is a beautiful step. Small actions like this lift mood and reduce depression."
    elif "GAD-7" in tool:
        recovery = f"Choosing **{st.session_state.user_happy}** calms your nervous system and lowers anxiety naturally."
    else:
        recovery = f"Engaging in **{st.session_state.user_happy}** grounds you and reduces psychosis risk."

    st.success("**Uko sawa, utapita hii.**")
    st.markdown(f"**{recovery}**")

    # 3 FUNNY QUESTIONS
    st.markdown("### Just for fun — answer these 3 quick questions:")
    funny_questions = [
        f"If **{st.session_state.user_happy}** was a Kenyan celebrity, who would it be?",
        f"How many chapatis would **{st.session_state.user_happy}** eat in one sitting?",
        f"If **{st.session_state.user_happy}** had a superpower, what would it be?"
    ]

    for i, q in enumerate(funny_questions):
        key_fun = f"fun{i}"
        if key_fun not in st.session_state:
            st.session_state[key_fun] = ""
        ans = st.text_input(q, placeholder="Your funny answer...", value=st.session_state[key_fun], key=key_fun)
        if ans.strip():
            st.balloons()
            st.markdown(f"😂 {ans} — I love it!")

    # FINAL MESSAGE
    st.success("**Uko sawa, utapita hii.**")
    st.markdown("**You are stronger than you know. I'm here to help you.**")
    st.markdown("— MentaBot")
    st.info("Click below to start a new session:")

    # Reset session button
    if st.button("Start New Session"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

st.markdown("---")
st.caption("Real PHQ-9 • GAD-7 • WERCAP | Bubbles | Personalized | Full Jac in repo | Eric Jeremiah")
