graph afya_graph {
    has name = "AFYA-MIND OSP Graph";
}

node user {
    has username: str;
    has created_at: str = std.time_now();
}

node emotion {
    has mood_score: int;
    has tool: str;
    has result: str;
    has journal_text: str;
    has timestamp: str = std.time_now();
}

node trigger {
    has name: str;
    has count: int = 0;
}

node suggestion {
    has text: str;
    has timestamp: str = std.time_now();
}

edge triggers --> emotion;
edge causes --> emotion;
edge has_suggestion --> suggestion;
