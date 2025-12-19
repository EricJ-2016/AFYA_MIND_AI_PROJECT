import { JacClient } from "@jaseci/jac-client";

const client = new JacClient({
  serverUrl: "http://localhost:8000"
});

async function logMood(emotion, score) {
  await client.spawn("log_mood", {
    emotion: emotion,
    score: score
  });
}

window.logMood = logMood;
