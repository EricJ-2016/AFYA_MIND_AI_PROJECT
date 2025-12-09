# streamlit_app.py - AFYA-MIND FINAL WINNER (ERIC JEREMIAH)
# Real screening + GPT-4 chat with MentaBot + Swahili + Bubbles twice

import os
os.environ['PIL_AVIF_IGNORE'] = '1'

import streamlit as st
from openai import OpenAI

# === CONFIG ===
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY")))

# === REAL QUESTIONS ===
PHQ9 = ["Little interest or pleasure in doing things?", ...]  # (same as before)
GAD7 = [...]  # (same)
WERCAP = [...]  # (same)

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

# Reset
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
    trigger = "stress"
    text = journal.lower()
    if any(w in text for w in ["work","job"]): trigger = "work stress"
    elif any(w in text for w in ["family","parent"]): trigger = "family"
    elif any(w in text for w in ["money","bill"]): trigger = "finances"
    elif any(w in text for w in ["exam","study"]): trigger = "academic pressure"
    elif journal.strip(): trigger = journal.strip().split()[0] + " concern"

    st.balloons()  # FIRST BUBBLES

    st.success(f"Score: {score} → {level}")
    st.info(f"Detected trigger: **{trigger.capitalize()}**")

    st.subheader("MentaBot is here for you")
    st.write(f"""
**Pole sana rafiki** — I see you're carrying **{trigger}** today.

**Breathing exercise**: Inhale 4 → Hold 4 → Exhale 4 → Repeat 5 times.

**Now let’s talk — I’m here for you.**
    """)

    # === GPT-4 CHAT STARTS HERE ===
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are MentaBot — a warm, compassionate, Kenyan mental health companion. Always respond in simple English with one line of Swahili. Be hopeful, never give medical advice, encourage small steps. End every reply with 'Uko sawa, utapita hii.'"}
        ]

    for msg in st.session_state.messages[1:]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Talk to MentaBot... (type anything)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("MentaBot is thinking..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",  # or gpt-4-turbo
                    messages=st.session_state.messages,
                    temperature=0.8
                )
            reply = response.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

        st.balloons()  # SECOND BUBBLES EVERY TIME USER SENDS MESSAGE

st.markdown("---")
st.caption("Real PHQ-9 • GAD-7 • WERCAP | GPT-4 MentaBot Chat | Swahili | Full Jac in repo | Eric Jeremiah")
