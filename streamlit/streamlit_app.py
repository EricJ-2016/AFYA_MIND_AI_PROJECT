# streamlit_app.py - AFYA-MIND FINAL WINNER (ERIC JEREMIAH)
import os
os.environ['PIL_AVIF_IGNORE'] = '1'
import streamlit as st
import pickle
import datetime
import networkx as nx
import matplotlib.pyplot as plt
import requests

# ======================
# === REAL QUESTIONS ===
# ======================
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

# ======================
# === SCORING FUNCTION ===
# ======================
def calculate_score(tool, answers):
    score = sum(answers)
    if tool == "PHQ-9":
        level = "Minimal" if score <= 4 else "Mild" if score <= 9 else "Moderate" if score <= 14 else "Moderately Severe" if score <= 19 else "Severe"
    elif tool == "GAD-7":
        level = "Minimal" if score <= 4 else "Mild" if score <= 9 else "Moderate" if score <= 14 else "Severe Anxiety"
    else:
        level = "Low Risk" if score <= 20 else "Moderate Risk" if score <= 40 else "High Risk"
    return score, level

# ======================
# === APP CONFIG ===
# ======================
st.set_page_config(page_title="AFYA-MIND", page_icon="🧠", layout="centered")

# ======================
# === SESSION INIT ===
# ======================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_submitted" not in st.session_state:
    st.session_state.login_submitted = False
if "user_happy" not in st.session_state:
    st.session_state.user_happy = ""
if "emotion_graph" not in st.session_state:
    st.session_state.emotion_graph = nx.DiGraph()
if "submissions" not in st.session_state:
    st.session_state.submissions = []

GRAPH_FILE = "graph.pkl"

# Load graph from previous sessions
try:
    with open(GRAPH_FILE, "rb") as f:
        st.session_state.emotion_graph = pickle.load(f)
except:
    pass

# ======================
# === LOGIN PAGE ===
# ======================
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

if st.session_state.get("login_submitted"):
    st.session_state.login_submitted = False
    st.experimental_rerun()

# ======================
# === MAIN APP ===
# ======================
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

    # === LLM-powered trigger detection (simple mock) ===
    def detect_trigger(text):
        text = text.lower()
        triggers = {
            "work": ["work", "job", "boss"],
            "family": ["family", "parent", "child", "spouse"],
            "finances": ["money", "bill", "rent", "loan"],
            "academic": ["exam", "study", "homework"],
        }
        for key, keywords in triggers.items():
            if any(word in text for word in keywords):
                return key
        if text.strip():
            return text.strip().split()[0] + " concern"
        return "general"

    if st.button("Submit & Talk to MentaBot", type="primary"):
        score, level = calculate_score(tool.split()[0], answers)
        trigger = detect_trigger(journal)

        st.balloons()  # BUBBLES
        st.success(f"Score: {score} → {level}")
        st.info(f"Detected trigger: **{trigger.capitalize()}**")

        st.subheader("MentaBot is here for you")
        st.write(f"""
**Pole sana {st.session_state.user_name}** — I see you're carrying **{trigger}** today.
**Breathing exercise**: Inhale 4 → Hold 4 → Exhale 4 → Repeat 5 times.
**Now tell me —**
        """)

        # Save user happy action
        st.session_state.user_happy = st.text_input(
            "What is one small thing I can do today to feel 1% better?",
            placeholder="Type anything and press Enter...",
            value=st.session_state.user_happy,
            key="hope_answer"
        )

        # ======================
        # UPDATE EMOTION GRAPH
        # ======================
        emoji_map = {
            "Minimal": "😊",
            "Mild": "😐",
            "Moderate": "😟",
            "Moderately Severe": "😔",
            "Severe": "😢",
            "Severe Anxiety": "😢",
            "Low Risk": "😊",
            "Moderate Risk": "😐",
            "High Risk": "😟"
        }

        emotion_node = f"{tool.split()[0]}-{level} {emoji_map.get(level, '😐')}"
        trigger_node = f"Trigger: {trigger} 🔔"
        activity_node = f"Action: {st.session_state.user_happy if st.session_state.user_happy else 'Self-care'} 🌱"

        G = st.session_state.emotion_graph
        G.add_node(emotion_node, type="emotion")
        G.add_node(trigger_node, type="trigger")
        G.add_node(activity_node, type="activity")
        G.add_edge(emotion_node, trigger_node, relation="influenced_by")
        G.add_edge(emotion_node, activity_node, relation="relieved_by")

        # Save submission for trend detection
        st.session_state.submissions.append({
            "date": datetime.date.today(),
            "tool": tool.split()[0],
            "score": score,
            "level": level
        })

        # Save graph persistently
        with open(GRAPH_FILE, "wb") as f:
            pickle.dump(G, f)

        # ======================
        # TREND DETECTION (Weekly)
        # ======================
        last_week = datetime.date.today() - datetime.timedelta(days=7)
        weekly_scores = [s["score"] for s in st.session_state.submissions if s["date"] >= last_week]
        if weekly_scores:
            avg_score = sum(weekly_scores) / len(weekly_scores)
            trend_msg = f"📊 Your average score this week: {avg_score:.1f} → {'Stable' if avg_score < 10 else 'Increasing stress' if avg_score >= 10 else 'Improving'}"
            st.info(trend_msg)

        # Recovery message
        if st.session_state.user_happy.strip():
            recovery = f"Engaging in **{st.session_state.user_happy}** lifts your mood and reduces distress."
            st.success("**Uko sawa, utapita hii.**")
            st.markdown(f"**{recovery}**")

        # Fun Questions
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

        # Final message
        st.success("**Uko sawa, You are fit now. Take Care**")
        st.markdown("**You are stronger than you know. I'm here to help you. YOUR HEALTH MATTERS**")
        st.markdown("— MentaBot")

# ======================
# EMOTION–TRIGGER GRAPH VIEW
# ======================
st.markdown("## 🧠 Emotion–Trigger–Activity Graph")

if st.session_state.emotion_graph.number_of_nodes() == 0:
    st.info("Graph will appear after you submit your first reflection.")
else:
    fig, ax = plt.subplots(figsize=(8, 6))
    pos = nx.spring_layout(st.session_state.emotion_graph, seed=42)

    # Node colors by type
    color_map = []
    for node in st.session_state.emotion_graph.nodes:
        node_type = st.session_state.emotion_graph.nodes[node].get("type", "")
        if node_type == "emotion":
            color_map.append("lightblue")
        elif node_type == "trigger":
            color_map.append("lightcoral")
        elif node_type == "activity":
            color_map.append("lightgreen")
        else:
            color_map.append("grey")

    nx.draw(
        st.session_state.emotion_graph,
        pos,
        with_labels=True,
        node_size=2500,
        font_size=9,
        node_color=color_map,
        ax=ax
    )

    edge_labels = nx.get_edge_attributes(st.session_state.emotion_graph, "relation")
    nx.draw_networkx_edge_labels(
        st.session_state.emotion_graph,
        pos,
        edge_labels=edge_labels,
        font_size=8,
        ax=ax
    )

    st.pyplot(fig)
    st.caption(
        "Nodes: emotions, triggers, and coping activities (with emojis). "
        "Edges show influence and relief relationships."
    )

# ======================
# SAFE RESET SESSION
# ======================
if st.button("Start New Session"):
    st.session_state.clear_on_next_run = True
    st.experimental_rerun()

if st.session_state.get("clear_on_next_run", False):
    keys_to_delete = [key for key in st.session_state.keys() if key != "clear_on_next_run"]
    for key in keys_to_delete:
        del st.session_state[key]
    st.session_state.clear_on_next_run = False
    st.experimental_rerun()

st.markdown("---")
st.caption("Real PHQ-9 • GAD-7 • WERCAP| Personalized | Full Jac in repo | Eric Jeremiah: Author")
