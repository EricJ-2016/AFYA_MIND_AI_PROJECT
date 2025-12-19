# AFYA-MIND – Project 5: MindMate Harmony Space

 HEAD
# **Requirements**
- Jac core + OSP graph + byLLM + Jac Client + spawn()
- 3 agents: Logger → Analyzer → Suggester
- Real PHQ-9, GAD-7, WERCAP
- Swahili MentaBot
- Bubbles + personalized recovery
- Full reset + repeat
- Seed data + metrics
- Weekly AI-generated care plans and reflection summaries

## Architecture Overview

- **Backend**: JacLang (OSP graph with emotions, triggers, activities)
- **Walkers**: log_mood, weekly_trend
- **Frontend 1**: Streamlit (user-facing UI)
- **Frontend 2**: Jac-Client (Jaseci stack interface)
- **LLM**: Used for trigger detection and empathetic responses
 643ff339 (Add Jac-Client frontend, clean legacy files, and document architecture)

# **Overview**
This project is based on Hackathon Project 5 (MindMate Harmony Space).  
AFYA-MIND tracks moods via screenings (PHQ-9, GAD-7, ARM-16, WERCAP), identifies patterns using OSP graphs, and offers personalized coping strategies via byLLM (MentaBot). It is culturally adapted for Kenyan users with Swahili encouragements and positive prompts.

# **Agent Interaction Diagram**
- Logger Agent (log_mood walker): Captures user mood/screening input → Updates OSP graph → Calls Analyzer.  
- Analyzer Agent (analyze_trends walker): Traverses the graph → Uses byLLM for sentiment classification/scoring → Reports patterns.  
- Suggester Agent (generate_suggestion walker): Receives Analyzer output → Uses byLLM to generate empathetic responses, coping exercises, weekly AI plans → Returns to frontend.

# **Setup Instructions**
1. Activate virtual environment:  
   Mac/Linux: `source venv/bin/activate`  
   Windows: `venv\Scripts\activate`  
2. Start Jaseci shell: `jsctl`  
3. Load custom actions (optional): `actions load local actions.py`  
4. Activate sentinel: `sentinel active set -snt afya_mind`  
5. Create graph: `graph create -set_active true`  
6. Seed initial data:  
   `walker run init_graph`  
   `walker run seed_data`  
7. Run frontend (Streamlit + Jac Client):  
   Compile Jac Client code if needed: `jac build frontend/app.jac -o frontend/build`  
   Then run in browser via: `jaseci-serv run`  
8. Install Python dependencies: `pip install -r requirements.txt`

# **Demo Workflow**
- Enter your name on the welcome page for an encouraging start.  
- Choose a screening tool: PHQ-9, GAD-7, or WERCAP.  
- Complete the screening questions.  
- Submit your journal entries for AI trigger detection.  
- Receive MentaBot feedback, fun questions with emoji bubbles, and personalized coping suggestions.  
- View your **Emotion–Trigger–Activity Graph**, showing nodes for emotions, triggers, and coping actions.  
- Check weekly trends, AI-generated care plans, and reflection summaries.  
- Start a new session for a fresh journey at any time.

# **Live Demo & GitHub Links**
- **GitHub Repository:** https://github.com/EricJ-2016/AFYA_MIND_AI_PROJECT  
- **Live App on Streamlit:** https://afyamindaiproject-dwoadxep52evxo9q3jkkak.streamlit.app/  
- **Demo Video:** https://drive.google.com/file/d/1bM6R-fKlKZyZg4m4vAgHk_cmQLC7QUzl/view

