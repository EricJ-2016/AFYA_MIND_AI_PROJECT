walker create_user { has username: str; can entry { u = here ++> User(username=self.username); report u; } }
walker get_history { has username: str; can entry { report here; } }
