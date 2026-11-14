"""Accounts layered on top of the existing learners table. Learner state stays in services.store."""
import sqlite3, hashlib, hmac, os, re
from services.store import DB, ensure_learner, save_state, load_state

EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
DEMO_PASSWORD = "demo-hunter-1"
DEMOS = [
    ("demo@edupath.app", "Demo Hunter", "Generative AI Engineer", True,
     "Built a RAG chatbot with LangChain and embeddings. Developed FastAPI services in Python, used Git and Docker. Project deployed on Render."),
    ("kael@edupath.app", "Kael", "AI/ML Engineer", False,
     "Python, machine learning with scikit-learn, deep learning with PyTorch. Built and deployed models with Docker, FastAPI, SQL and Git. Designed monitoring for production."),
    ("mira@edupath.app", "Mira", "Data Analyst", False,
     "SQL, Excel and Power BI dashboards. Developed visualization projects in Python with Plotly. Statistics coursework."),
]

def _c():
    c = sqlite3.connect(DB)
    c.execute("CREATE TABLE IF NOT EXISTS users(email TEXT PRIMARY KEY, name TEXT NOT NULL, pw TEXT NOT NULL, learner_id TEXT NOT NULL, demo INTEGER DEFAULT 0)")
    return c

def _hash(p):
    salt = os.urandom(16)
    return salt.hex() + "$" + hashlib.pbkdf2_hmac("sha256", p.encode(), salt, 200_000).hex()

def _verify(p, stored):
    salt, h = stored.split("$")
    return hmac.compare_digest(hashlib.pbkdf2_hmac("sha256", p.encode(), bytes.fromhex(salt), 200_000).hex(), h)

def register(name, email, pw, confirm):
    name, email = name.strip(), email.strip().lower()
    if len(name) < 2: return None, "Hunter name needs at least 2 characters."
    if not EMAIL.match(email): return None, "Enter a valid email address."
    if len(pw) < 8: return None, "Password needs at least 8 characters."
    if pw != confirm: return None, "Passwords do not match."
    c = _c()
    if c.execute("SELECT 1 FROM users WHERE email=?", (email,)).fetchone():
        c.close(); return None, "An account with this email already exists. Log in instead."
    lid = ensure_learner()
    c.execute("INSERT INTO users VALUES(?,?,?,?,0)", (email, name, _hash(pw), lid)); c.commit(); c.close()
    return {"email": email, "name": name, "learner_id": lid, "demo": False}, None

def login(email, pw):
    email = email.strip().lower()
    if not email or not pw: return None, "Enter your email and password."
    c = _c(); r = c.execute("SELECT name,pw,learner_id,demo FROM users WHERE email=?", (email,)).fetchone(); c.close()
    if not r or not _verify(pw, r[1]): return None, "Email or password is incorrect."
    return {"email": email, "name": r[0], "learner_id": r[2], "demo": bool(r[3])}, None

def _analyze(s, full):
    if full:
        try:
            from core.graphs import build_analysis_graph
            return build_analysis_graph().invoke(s)
        except Exception:
            pass
    from core.competency import compute_gaps, readiness, critical_path
    g = compute_gaps(s["document_text"], s["target_role"])
    s.update(gaps=g, readiness=readiness(g), critical_path=critical_path(g, s["target_role"]))
    return s

def ensure_demo():
    """Create demo hunters once, using the real analysis engine on sample evidence."""
    c = _c()
    for email, name, role, full, text in DEMOS:
        if c.execute("SELECT 1 FROM users WHERE email=?", (email,)).fetchone(): continue
        lid = ensure_learner()
        st_ = _analyze({"document_text": text, "current_skills": text, "target_role": role,
                        "career_goal": f"Become job-ready as {role}.", "weekly_hours": 8.0, "job_description": ""}, full)
        objs = st_.get("objectives", [])
        if objs and name != "Demo Hunter":
            st_["progress"] = {o["id"]: True for o in objs[:3]}
        save_state(lid, st_)
        c.execute("INSERT INTO users VALUES(?,?,?,?,1)", (email, name, _hash(DEMO_PASSWORD), lid)); c.commit()
    c.close()

def demo_login():
    ensure_demo()
    return login(DEMOS[0][0], DEMO_PASSWORD)
