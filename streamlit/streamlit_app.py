# streamlit_app.py - AFYA-MIND FINAL WINNER (ERIC JEREMIAH)
# Real questions + Interactive MentaBot + Bubbles + Final message stays forever

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
    "Moving or speaking so slowly that others noticed? Or very fidgety/restless?",
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
st.markdown("**Jaseci Hackathon 2025 – Project 5** | Eric Jeremiah | [GitHub](https://github.com/EricJ-2016/AFYA_MIND_AI)")

tool = st.selectbox("Choose Screening Tool", ["PHQ-9 (Depression)", "GAD-7 (Anxiety)", "WERCAP (Psychosis Risk)"])
questions = PHQ9 if "PHQ-9" in tool else GAD7 if "GAD-7" in tool else WERCAP

st.markdown("### Over the last 2 weeks, how often have you been bothered by:")
answers = []
for i, q in enumerate(questions):
    val = st.radio(q, ["Not at all (0)", "Several days (1)", "More than half the days (2)", "Nearly every day (3)"],
                   index=0, horizontal=True, key=f"q{i}")
    answers.append([0,1,2,3][["Not at all","Several days","More than half","Nearly every day"].index(val.split("(")[0].strip())])

journal = st.text_area("How are you really feeling today?", placeholder="e.g., Work stress, family pressure...")

if st.button("Submit & Talk to MentaBot", type="primary"):
    score, level = calculate_score(tool.split()[0], answers)

    # Real trigger detection
    text = journal.lower()
    trigger = "stress"
    if any(w in text for w in ["work","job","boss"]): trigger = "work stress"
    elif any(w in text for w in ["family","parent","child"]): trigger = "family"
    elif any(w in text for w in ["money","bill"]): trigger = "finances"
    elif any(w in text for w in ["exam","study"]): trigger = "academic pressure"
    elif journal.strip(): trigger = journal.strip().split()[0] + " concern"

    st.success(f"Score: {score} → {level}")
    st.info(f"Detected trigger: **{trigger.capitalize()}**")

    st.subheader("MentaBot is here for you")
    st.write(f"""
**Pole sana rafiki** — I see you're carrying **{trigger}** today.

**Breathing exercise**: Inhale 4 → Hold 4 → Exhale 4 → Repeat 5 times.

**Now tell me —**
    """)

    # INTERACTIVE — USER TYPES → BUBBLES + FINAL MESSAGE STAYS FOREVER
    user_answer = st.text_input(
        "What is one small thing I can do today to feel 1% better?",
        placeholder="Type anything here and press Enter...",
        key="hope_answer"
    )

    if user_answer.strip():
        st.balloons()  # BUBBLES!
        st.success("**Uko sawa, utapita hii.**")
        st.markdown("**You are stronger than you know. I'm here whenever you need me.**")
        st.markdown("— MentaBot")
        st.markdown("")  # Extra space so it doesn't disappear

st.markdown("")  
        st.success("You did it! Keep going. You are enough.")

st.markdown("---")
st.caption("Real PHQ-9 • GAD-7 • WERCAP | Interactive MentaBot | Swahili | Full Jac code in repo | Eric Jeremiah")
