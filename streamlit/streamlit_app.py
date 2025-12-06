import os
os.environ['PIL_AVIF_IGNORE'] = '1'  # Fix for Cloud AVIF error

import streamlit as st
import json  # For mock OSP graph

# Mock OSP graph (dict for emotions/triggers – simulates Jaseci nodes/edges)
if 'graph' not in st.session_state:
    st.session_state.graph = {}  # user_id -> list of {'score': int, 'result': str, 'trigger': str}

# Mock byLLM (generative/analytical – replace with real OpenAI if key set)
@st.cache_data
def byllm(prompt, context=""):
    # Mock responses (for demo; add openai if needed)
    if "trigger" in prompt:
        return "work" if "work" in context.lower() else "family" if "family" in context.lower() else "stress"
    else:
        return f"I understand your {context}. Try breathing: In 4, hold 4, out 4. Journal: What helps? **Uko sawa, utapita hii!** (You're okay, you'll get through this!)"

st.set_page_config(page_title="AFYA-MIND", page_icon="🧠", layout="wide")

st.title("🧠 AFYA-MIND: AI Mental Health Companion")
st.markdown("**Jaseci Hackathon Project 5 – MindMate Harmony Space** | Eric Jeremiah | [GitHub](https://github.com/EricJ-2016/AFYA_MIND_AI)")

# Multi-Agent Simulation (Logger → Analyzer → Suggester)
user_id = "demo_user"  # Mock user (Logger agent logs here)

tool = st.selectbox("Select Screening Tool", ["PHQ-9 (Depression)", "GAD-7 (Anxiety)", "ARM-16 (Resilience)", "WERCAP (Psychosis Risk)"])

num_questions = {"PHQ-9": 9, "GAD-7": 7, "ARM-16": 16, "WERCAP": 22}[tool.split()[0]]
st.write(f"Answer {num_questions} questions (0–3 scale)")

col1, col2 = st.columns([3, 1])
with col1:
    answers = [st.slider(f"Q{i+1}", 0, 3, 1, key=f"q{i}") for i in range(num_questions)]
with col2:
    st.info("OSP Graph: Logs emotions → triggers → suggestions")

journal = st.text_area("Journal your feelings (for trigger detection):", placeholder="E.g., Work stress today...")

if st.button("Submit Screening & Get MentaBot Support", type="primary"):
    # Logger Agent: Compute score & log to OSP mock graph
    score = sum(answers)
    if "PHQ-9" in tool:
        result = "Minimal" if score <=4 else "Mild" if score <=9 else "Moderate" if score <=14 else "Moderately Severe" if score <=19 else "Severe"
    elif "GAD-7" in tool:
        result = "Minimal Anxiety" if score <=4 else "Mild" if score <=9 else "Moderate" if score <=14 else "Severe"
    elif "ARM-16" in tool:
        result = "High Resilience" if score >=64 else "Moderate" if score >=48 else "Low"
    else:
        result = "Low Risk" if score <=20 else "Moderate Risk" if score <=40 else "High Risk"
    
    # Log to graph (OSP edge simulation)
    if user_id not in st.session_state.graph:
        st.session_state.graph[user_id] = []
    st.session_state.graph[user_id].append({"score": score, "result": result, "journal": journal})
    
    # Analyzer Agent: byLLM analytical (trigger extraction)
    trigger_prompt = "Extract one trigger word from journal."
    trigger = byllm(trigger_prompt, journal)
    
    # Suggester Agent: byLLM generative (empathetic response)
    suggestion_prompt = "Generate supportive message for result and trigger."
    suggestion = byllm(suggestion_prompt, f"{result} | {trigger}")
    
    # Display (end-to-end flow)
    st.success(f"**Score: {score}** | **Result: {result}**")
    st.warning(f"**Detected Trigger (OSP/byLLM): {trigger}**")
    
    st.subheader("🤖 MentaBot Suggestion (byLLM):")
    st.write(suggestion)
    
    st.rerun()  # Update trends

# Trends Dashboard (OSP Traversal Simulation – Analyzer Agent)
if st.session_state.graph.get(user_id):
    st.subheader("📊 Trends (OSP Graph Analysis)")
    entries = st.session_state.graph[user_id]
    avg_score = sum(e["score"] for e in entries) / len(entries)
    common_triggers = [e.get("trigger", "unknown") for e in entries if "trigger" in e]  # Mock traversal
    st.metric("Average Score", f"{avg_score:.1f}", delta=f"{avg_score - 10:.1f}")  # Mock baseline 10
    st.bar_chart(common_triggers)  # Simple visualization (clusters triggers)

st.markdown("---")
st.caption("Full Jac/OSP/byLLM code in repo | Demo: Screening → Log (Logger) → Analyze (OSP) → Suggest (byLLM)")