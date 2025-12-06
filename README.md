# AFYA-MIND Hackathon 
# AFYA-MIND: AI-Driven Mental Health Early Screening and Support System

## Overview
This project is based on Hackathon Project 5 (MindMate Harmony Space). It tracks moods via screenings (PHQ-9, GAD-7, ARM-16, WERCAP), identifies patterns using OSP graphs, and offers personalized coping strategies via byLLM (MentaBot). Targeted at Kenyan users with cultural adaptations (e.g., Swahili encouragements).

## Agent Interaction Diagram
- Logger Agent (log_mood walker): User inputs mood/screening → Creates nodes/edges in OSP graph → Calls Analyzer.
- Analyzer Agent (analyze_trends walker): Traverses graph → Uses byLLM for sentiment classification/scoring → Reports patterns.
- Suggester Agent (generate_suggestion walker): Takes Analyzer output → Uses byLLM to generate empathetic responses/exercises → Returns to frontend.

## Setup Instructions
1. Activate venv: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows).
2. Start Jaseci shell: `jsctl`.
3. Load graphs/actions: `actions load local actions.py` (if custom actions needed; skip for now).
4. Register sentinel: `register sentinel -name afya_mind -mode code main.jac mental_health.jac llm_agent.jac users.jac graph_setup.jac seed_data.jac`.
5. Activate sentinel: `sentinel active set -snt afya_mind`.
6. Create graph: `graph create -set_active true`.
7. Seed data: `walker run init_graph` then `walker run seed_data`.
8. Run frontend: Compile Jac Client code with `jac build frontend/app.jac -o frontend/build` (assumes Jac Client setup; run in browser via `jaseci-serv run`).
9. Serve app: `jaseci-serv run -host 0.0.0.0 -port 8000`.

## Demo Workflow
- Log complete screening.
- View trends and MentaBot suggestions.
- Recorded demo: Upload video showing end-to-end (mood log → analysis → suggestion).

## Evaluation
- Metrics: Trend precision (e.g., 80% match on seed triggers), byLLM response relevance (qualitative).
- Seed data: Generates 5 demo users with entries.

GitHub: https://github.com/EricJ-2016/AFYA_MIND_AI
LinkedIn: www.linkedin.com/in/eric-jeremiah-59260b198
Video link: https://drive.google.com/file/d/1bM6R-fKlKZyZg4m4vAgHk_cmQLC7QUzl/view?usp=drive_link



