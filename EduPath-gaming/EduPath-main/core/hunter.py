"""Hunter progression derived from real learner state. No stored XP: it is computed from the engine's output."""
import json, sqlite3
from services.store import DB

RANKS = [("E", 0), ("D", 20), ("C", 40), ("B", 60), ("A", 75), ("S", 90)]

def profile(s):
    gaps, objs = s.get("gaps", []), s.get("objectives", [])
    done = sum(bool(v) for v in s.get("progress", {}).values())
    met = sum(1 for g in gaps if g["gap"] == 0)
    ready = s.get("readiness", 0) if gaps else 0
    xp = done * 120 + met * 60 + ready * 10
    rank = [n for n, t in RANKS if ready >= t][-1]
    nxt = next(((n, t) for n, t in RANKS if t > ready), None)
    return {"xp": xp, "level": 1 + xp // 250, "rank": rank, "readiness": ready, "done": done, "total": len(objs), "next": nxt}

def leaderboard(limit=8):
    try:
        c = sqlite3.connect(DB)
        rows = c.execute("SELECT u.name,l.state_json,u.demo FROM users u JOIN learners l ON l.id=u.learner_id").fetchall(); c.close()
    except sqlite3.Error:
        return []
    out = []
    for name, js, demo in rows:
        p = profile(json.loads(js or "{}"))
        out.append({"name": name, "demo": bool(demo), **p})
    return sorted(out, key=lambda x: -x["xp"])[:limit]

def quests(s):
    todo = [o for o in s.get("objectives", []) if not s.get("progress", {}).get(o["id"])]
    return {"daily": todo[:3], "weekly": todo[3:7]}
