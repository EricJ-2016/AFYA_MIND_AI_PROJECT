# AFYA-MIND – Project 5: MindMate Harmony Space

**Requirements**:
- Jac core + OSP graph + byLLM + Jac Client + spawn()
- 3 agents: Logger → Analyzer → Suggester
- Real PHQ-9, GAD-7, WERCAP
- Swahili MentaBot
- Bubbles + personalized recovery
- Full reset + repeat
- Seed data + metrics

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
4. Activate sentinel: `sentinel active set -snt afya_mind`.
5. Create graph: `graph create -set_active true`.
7. Seed data: `walker run init_graph` then `walker run seed_data`.
8. Run frontend: Compile Jac Client code with `jac build frontend/app.jac -o frontend/build` (assumes Jac Client setup; run in browser via `jaseci-serv run`).

## Demo Workflow
- Log complete screening.
- View trends and MentaBot suggestions.
- Recorded demo: Upload video showing end-to-end (mood log → analysis → suggestion).

## Evaluation
- Metrics: Trend precision (e.g., 80% match on seed triggers), byLLM response relevance (qualitative).
- Seed data: Generates 5 demo users with entries.

**GitHub**: https://github.com/EricJ-2016/AFYA_MIND_AI_PROJECT  
**Demo Video**: https://drive.google.com/file/d/1bM6R-fKlKZyZg4m4vAgHk_cmQLC7QUzl/view  
**Live App**: https://afyamindaiproject-dwoadxep52evxo9q3jkkak.streamlit.app/

