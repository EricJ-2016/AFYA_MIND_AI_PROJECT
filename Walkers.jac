// AGENT 1: Logger Agent
walker log_screening {
    has username: str;
    has tool: str;
    has answers: list<int>;
    has journal: str;

    root {
        take --> node::user(username==self.username);
        if(!here) {
            spawn here ++> node::user(username=self.username);
            take -->;
        }
    }

    user {
        score = std.sum(self.answers);
        result = match self.tool {
            "PHQ-9" => score <=4 ?"Minimal": score<=9?"Mild": score<=14?"Moderate": score<=19?"Moderately Severe":"Severe",
            "GAD-7" => score <=4 ?"Minimal": score<=9?"Mild": score<=14?"Moderate":"Severe Anxiety",
            "WERCAP" => score <=20?"Low Risk": score<=40?"Moderate Risk":"High Risk",
            => "Unknown"
        };

        emo = spawn here ++> node::emotion(
            mood_score=score, tool=self.tool, result=result, journal_text=self.journal
        );

        // Analytical byLLM: Extract trigger
        trigger_name = byllm(prompt="FromFile=prompts/trigger.txt", context=self.journal);

        trig = here --> node::trigger(name=trigger_name);
        if(!trig) {
            trig = spawn here ++> node::trigger(name=trigger_name, count=1);
        } else { trig.count += 1; }
        spawn trig triggers--> emo;

        // Call Agent 2
        trends = spawn here walker analyze_trends(username=self.username);

        // Call Agent 3
        suggestion = spawn here walker generate_suggestion(username=self.username, recent_result=result, trigger=trigger_name);

        report {score, result, trigger_name, trends, suggestion};
    }
}

// AGENT 2: Analyzer Agent — NON-TRIVIAL OSP TRAVERSAL
walker analyze_trends {
    has username: str;
    root { take --> node::user(username==self.username); }
    user {
        emotions = here --> node::emotion;
        top_trigger = null; max_count = 0;

        visit here -[triggers]-> node::trigger {
            if(visitor.count > max_count) {
                max_count = visitor.count;
                top_trigger = visitor.name;
            }
        }

        report {
            "total_screenings": emotions.length,
            "most_common_trigger": top_trigger,
            "avg_mood_score": std.avg([e.mood_score for e in emotions])
        };
    }
}

// AGENT 3: Suggester Agent — GENERATIVE byLLM
walker generate_suggestion {
    has username: str;
    has recent_result: str;
    has trigger: str;

    root { take --> node::user(username==self.username); }
    user {
        response = byllm(
            promptFromFile="prompts/suggestion.txt",
            context={"result": self.recent_result, "trigger": self.trigger}
        );

        spawn here ++> node::suggestion(text=response);
        report response;
    }
}
