node Emotion {
    has name: str;
    has emoji: str;
    has score: int;
}

node Trigger {
    has label: str;
}

node Activity {
    has description: str;
}
 HEAD
edge correlation {  // Emotion correlates with activity
    has score: float;
}
node Emotion {
    has name: str;
    has emoji: str;
    has score: int;
}

node Trigger {
    has label: str;
}

node Activity {
    has description: str;
}
 1a12859a (Clean JacLang backend: OSP graph and walkers)

edge influences {}
edge alleviates {}
