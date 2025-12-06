node User { has username: str; has created_at: str = now(); has screenings: list = []; }
node Screening { has tool: str; has answers: list; has score: int = 0; has result: str = ""; has created_at: str = now(); }

walker ping { can entry { report {"status": "AFYA-MIND backend alive", "time": now()}; } }
