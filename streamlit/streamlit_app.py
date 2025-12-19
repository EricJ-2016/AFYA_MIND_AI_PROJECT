# streamlit_app.py — AFYA-MIND FINAL STABLE BUILD
# Author: Eric Jeremiah

import os
os.environ['PIL_AVIF_IGNORE'] = '1'

import streamlit as st
import pickle
import datetime
import networkx as nx
import matplotlib.pyplot as plt


# REAL SCREENING QUESTIONS

PHQ9 = [
    "Little interest or pleasure in doing things?",
    "Feeling down, depressed, or hopeless?",
    "Trouble falling or staying asleep, or sleeping too much?",
    "Feeling tired or having little energy?",
    "Poor appetite or overeating?",
    "Feeling bad about yourself — or that you are a failure?",
    "Trouble concentrating on things?",
    "Moving or speaking slowly, or being very restless?",
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
    "I hear sounds or voices others do not.",
    "I feel others can read my thoughts.",
    "I see things others cannot.",
    "I feel I have special powers.",
    "My thoughts feel unusually strong.",
    "I have spiritual or supernatural experiences.",
    "My body feels changed.",
    "People stare at me unusually.",
    "I feel followed or watched.",
    "I feel out of control of my thoughts.",
    "I experience unreal perceptions.",
    "Dream-like hallucinations.",
    "Machines affect my thoughts.",
    "Thoughts taken from my mind.",
    "Feeling like another person.",
    "Loss of body control.",
    "Strange body changes.",
    "Feeling unreal or dead.",
    "Being controlled by others.",
    "Thought broadcasting.",
    "Thought insertion.",
    "Empty mind feeling."
]


# SCORING FUNCTION

def calculate_score(tool, answers):
    score = sum(answers)
    if tool == "PHQ-9":
        level = "Minimal" if score <= 4 else "Mild" if score <= 9 else "Moderate" if score <= 14 else "Severe"
    elif tool == "GAD-7":
        level = "Minimal" if score <= 4 else "Mild" if score <= 9 else "Moderate" if score <= 14 else "Severe Anxiety"
    else:
        level = "Low Risk" if score <= 20 else "Moderate Risk" if score <= 40 else "High Risk"
    return score, level


# APP CONFIG

st.set_page_config(
    page_title="AFYA-MIND",
    page_icon="🧠",
    layout="centered"
)


# SESSION INITIALIZATION

defaults = {
    "logged_in": False,
    "user_name": "",
    "emotion_graph": nx.DiGraph(),
    "submissions": [],
    "user_happy": "",
    "latest": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

GRAPH_FILE = "graph.pkl"

# Load saved graph
try:
    with open(GRAPH_FILE, "rb") as f:
        st.session_state.emotion_graph = pickle.load(f)
except:
    pass


# WELCOME PAGE

if not st.session_state.logged_in:
    st.title("🌟 Welcome to AFYA-MIND 🌟")
    st.markdown("""
    **You are not alone. You are valued. You matter.**  
    AFYA-MIND is your safe space for reflection, growth, and healing.  
    Breathe. Smile. Hope lives here — and so do you. 💙
    """)

    name = st.text_input("Your Name", placeholder="e.g., Eric, Amina, John")

    if st.button("Start My Journey", type="primary"):
        if name.strip():
            st.session_state.user_name = name.strip()
            st.session_state.logged_in = True
        else:
            st.error("Please enter your name to continue.")

    st.stop()


# MAIN APP

st.title(f"Welcome back, {st.session_state.user_name} 😊")
st.markdown("**You are safe here. Let’s walk together.**")

tool = st.selectbox(
    "Choose Screening Tool",
    ["PHQ-9 (Depression)", "GAD-7 (Anxiety)", "WERCAP (Psychosis Risk)"]
)

questions = PHQ9 if "PHQ-9" in tool else GAD7 if "GAD-7" in tool else WERCAP

answers = []
st.markdown("### Over the last 2 weeks, how often have you been bothered by:")
for i, q in enumerate(questions):
    val = st.radio(
        q,
        ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        index=0,
        horizontal=True,
        key=f"q{i}"
    )
    answers.append(["Not at all", "Several days", "More than half the days", "Nearly every day"].index(val))

journal = st.text_area(
    "How are you really feeling today?",
    placeholder="Work, exams, relationships, finances…"
)


# SUBMIT

if st.button("Submit & Talk to MentaBot", type="primary"):
    score, level = calculate_score(tool.split()[0], answers)
    st.balloons()

    st.success(f"🧠 Score: {score} → **{level}**")

    trigger = journal.split()[0] if journal.strip() else "general stress"
    st.info(f"Detected trigger: **{trigger.capitalize()}**")

    st.markdown(f"""
    **Pole sana {st.session_state.user_name}.**  
    I see you. What you're feeling makes sense.  
    Breathe in 4… hold 4… breathe out 4 🌬️
    """)

    st.session_state.user_happy = st.text_input(
        "What is one small thing you can do today to feel 1% better?",
        placeholder="Even something tiny counts 💛"
    )

    # Save latest reflection
    st.session_state.latest = {
        "date": datetime.date.today(),
        "tool": tool,
        "score": score,
        "level": level,
        "trigger": trigger,
        "action": st.session_state.user_happy
    }

    st.session_state.submissions.append(st.session_state.latest)


# FUN QUESTIONS 🎉

if st.session_state.latest:
    st.markdown("### 😂 Just for fun — answer these:")
    fun_qs = [
        "If today was a movie, what genre would it be?",
        "How many chapatis could your mood eat today?",
        "If your feeling had a superpower, what would it be?"
    ]

    for i, q in enumerate(fun_qs):
        ans = st.text_input(q, key=f"fun{i}")
        if ans.strip():
            st.balloons()
            st.markdown(f"😂 **{ans}** — I love it!")

    st.success("💪 **Uko sawa sasa. You are stronger than ever before.**")


# WEEKLY AI CARE PLAN 🧠

if st.session_state.submissions:
    st.markdown("## 🧠 AI Weekly Care Plan")
    st.markdown("""
    - 🌱 Sleep at least 7 hours  
    - 🚶 Move your body daily  
    - 🗣️ Talk to someone you trust  
    - 📝 Journal once this week  
    - 😊 Do one thing just for joy
    """)


# REFLECTION SUMMARY 📄

if st.session_state.latest:
    st.markdown("## 📄 Reflection Summary")
    data = st.session_state.latest
    st.write(
        f"On **{data['date']}**, you completed **{data['tool']}**. "
        f"You experienced **{data['level']}** symptoms, mainly triggered by **{data['trigger']}**. "
        f"Your chosen coping action was **{data['action']}**."
    )


# EMOTION GRAPH
import pandas as pd
import matplotlib.pyplot as plt
st.markdown("## 📈 Weekly Mood Trend")

# Prepare data
if st.session_state.submissions:
    df = pd.DataFrame(st.session_state.submissions)
    # Convert dates to datetime
    df['date'] = pd.to_datetime(df['date'])
    # Group by date and take average score (if multiple per day)
    df_daily = df.groupby('date')['score'].mean().reset_index()

    # Keep only last 7 entries for weekly trend
    df_daily = df_daily.sort_values('date').tail(7).reset_index(drop=True)

    # Create Day 1..Day N labels
    df_daily['day_label'] = [f"Day {i+1}" for i in range(len(df_daily))]

    # Plot line chart
    fig, ax = plt.subplots(figsize=(8,5))
    ax.plot(df_daily['day_label'], df_daily['score'], marker='o', linestyle='-', color='dodgerblue')
    ax.set_title("Mood Score Trend Over Last 7 Days")
    ax.set_xlabel("Day")
    ax.set_ylabel("Average Score")
    ax.grid(True)
    st.pyplot(fig)
else:
    st.info("Your weekly mood trend will appear here after submitting reflections.")

st.caption("AFYA-MIND • Mental Health Matters • Eric Jeremiah")
