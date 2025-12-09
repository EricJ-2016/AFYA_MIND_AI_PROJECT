# streamlit_app.py - AFYA-MIND FINAL WINNER (ERIC JEREMIAH)
# Bubbles twice + 4-message GPT-style chat after screening + Swahili + Full reset

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

# RESET BUTTON
if st.button("Screen Again (New Session)"):
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

    # Trigger detection
    text = journal.lower()
    trigger = "stress"
    if any(w in text for w in ["work","job","boss"]): trigger = "work stress"
    elif any(w in text for w in ["family","parent","child"]): trigger = "family"
    elif any(w in text for w in ["money","bill"]): trigger = "finances"
    elif any(w in text for w in ["exam","study"]): trigger = "academic pressure"
    elif journal.strip(): trigger = journal.strip().split()[0] + " concern"

    # FIRST BUBBLES
    st.balloons()

    st.success(f"Score: {score} → {level}")
    st.info(f"Detected trigger: **{trigger.capitalize()}**")

    st.subheader("MentaBot is here for you")
    st.write(f"""
**Pole sana rafiki** — I see you're carrying **{trigger}** today.

**Breathing exercise**: Inhale 4 → Hold 4 → Exhale 4 → Repeat 5 times.

**Now tell me —**
    """)

    user_answer = st.text_input(
        "What is one small thing I can do today to feel 1% better?",
        placeholder="Type anything and press Enter...",
        key="hope_answer"
    )

    if user_answer.strip():
        # SECOND BUBBLES
        st.balloons()

        # Personalized recovery
        if "PHQ-9" in tool:
            recovery = f"Doing **{user_answer}** is a beautiful step. Small actions like this lift mood and reduce depression."
        elif "GAD-7" in tool:
            recovery = f"Choosing **{user_answer}** calms your nervous system and lowers anxiety naturally."
        else:
            recovery = f"Engaging in **{user_answer}** grounds you and reduces psychosis risk."

        st.success("**Uko sawa, utapita hii.**")
        st.markdown(f"**{recovery}**")
        st.markdown("**You are stronger than you know. I'm here whenever you need me.**")
        st.markdown("— MentaBot")

        # === 4-MESSAGE CHAT STARTS HERE ===
        st.markdown("### Talk more with MentaBot (4 messages)")
        if "chat_count" not in st.session_state:
            st.session_state.chat_count = 0
            st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if st.session_state.chat_count < 4:
            if prompt := st.chat_input("Say anything to MentaBot..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    with st.spinner("MentaBot is thinking..."):
                        reply = f"Thank you for sharing. {prompt} Uko sawa, utapita hii."
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    st.session_state.chat_count += 1
                    st.rerun()
        else:
            st.success("Thank you for talking. You are enough. Take care.")
            st.markdown("**Uko sawa. You're doing great.** — MentaBot")

st.markdown("---")
st.caption("Real PHQ-9 • GAD-7 • WERCAP | 4-message MentaBot chat | Bubbles | Full Jac in repo | Eric Jeremiah")
