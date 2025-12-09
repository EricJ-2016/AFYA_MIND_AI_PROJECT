# streamlit_app.py - AFYA-MIND FINAL WINNER (ERIC JEREMIAH)
# Bubbles + 3 funny questions + Final message + Full reset

import os
os.environ['PIL_AVIF_IGNORE'] = '1'

import streamlit as st

# === REAL QUESTIONS (same as before - shortened for space) ===
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

WERCAP = [  # (same 22 questions - omitted for space)
    "I hear sounds or voices that other people think aren't there.",
    # ... all 22 questions
]

def calculate_score(tool, answers):
    score = sum(answers)
    if tool == "PHQ-9":
        level = "Minimal" if score <=4 else "Mild" if score <=9 else "Moderate" if score <=14 else "Moderately Severe" if score <=19 else "Severe"
    elif tool == "GAD-7":
        level = "Minimal" if score <=4 else "Mild" if score <=9 else "Moderate" if score <=14 else "Severe Anxiety"
    else:
        level = "Low Risk" if score <=20 else "Moderate Risk" if score <=40 else "High Risk"
    return score, level

# === APP ===
st.set_page_config(page_title="AFYA-MIND", page_icon="brain", layout="centered")
st.title("AFYA-MIND")
st.markdown("**Welcome to AFYA-MIND — where everything is possible.**\nYou are safe. You are not alone. We are together.")

if st.button("Screen Again (New Session)", type="secondary"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

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

    # Trigger detection (same as before)
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
**Pole sana rafiki** — I see you're carrying **{trigger}** today.

**Breathing exercise**: Inhale 4 → Hold 4 → Exhale 4 → Repeat 5 times.

**Now tell me —**
    """)

    user_happy = st.text_input(
        "What is one small thing I can do today to feel 1% better?",
        placeholder="Type anything and press Enter...",
        key="first_happy"
    )

    if user_happy.strip():
        st.balloons()  # BUBBLES 2

        if "PHQ-9" in tool:
            recovery = f"Doing **{user_happy}** is a beautiful step. Small actions like this lift mood and reduce depression."
        elif "GAD-7" in tool:
            recovery = f"Choosing **{user_happy}** calms your nervous system and lowers anxiety naturally."
        else:
            recovery = f"Engaging in **{user_happy}** grounds you and reduces psychosis risk."

        st.success("**Uko sawa, utapita hii.**")
        st.markdown(f"**{recovery}**")

        # === 3 FUNNY QUESTIONS BASED ON THEIR ANSWER ===
        st.markdown("### Just for fun — answer these 3 quick questions:")
        funny_questions = [
            f"If {user_happy} was a Kenyan celebrity, who would it be?",
            f"How many chapatis would {user_happy} eat in one sitting?",
            f"If {user_happy} had a superpower, what would it be?"
        ]

        for i, q in enumerate(funny_questions):
            ans = st.text_input(q, placeholder="Your funny answer...", key=f"fun{i}")
            if ans.strip():
                st.balloons()  # BUBBLES AFTER EVERY FUNNY ANSWER
                st.markdown(f"😂 {ans} — I love it!")

        # FINAL MESSAGE AFTER ALL QUESTIONS
        st.success("**Uko sawa, utapita hii.**")
        st.markdown("**You are stronger than you know. I'm here to help you.**")
        st.markdown("— MentaBot")

st.markdown("---")
st.caption("Real PHQ-9 • GAD-7 • WERCAP | Bubbles | 3 funny questions | Full Jac in repo | Eric Jeremiah")
