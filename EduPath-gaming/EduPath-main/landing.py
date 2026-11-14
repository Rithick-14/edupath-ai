import html, streamlit as st
from core.hunter import leaderboard, quests, RANKS
from services.auth import register, login, demo_login, DEMOS
from services.store import load_state
from services.auth import _c

CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;700&family=Barlow:wght@400;500;600&display=swap');
:root{--bg:#07060d;--ch:#121019;--ln:#2a2340;--bl:#38a3ff;--vi:#8b5cf6;--mg:#f01fd0;--tx:#f3f0ff;--mu:#9a93b5}
html{scroll-behavior:smooth}
.stApp{background:var(--bg);color:var(--tx);font-family:Barlow,system-ui,sans-serif}
header[data-testid=stHeader],[data-testid=stSidebar],[data-testid=stToolbar],footer{display:none!important}
.block-container{max-width:100%!important;padding:0!important}
.nav{position:fixed;top:0;left:0;right:0;z-index:50;display:flex;align-items:center;gap:28px;padding:14px 5vw;background:#07060dcc;backdrop-filter:blur(14px);border-bottom:1px solid var(--ln)}
.nav .logo{font:700 22px 'Chakra Petch';letter-spacing:1px;color:var(--tx);text-decoration:none;display:flex;align-items:center;gap:10px}
.logo i{width:30px;height:30px;border-radius:8px;background:linear-gradient(135deg,var(--bl),var(--mg));display:inline-block;box-shadow:0 0 18px var(--vi)}
.nav .links{display:flex;gap:24px;margin-left:24px;flex:1}.nav .links a{color:var(--mu);text-decoration:none;font-weight:600;font-size:15px}.nav .links a:hover{color:var(--tx)}
.btn{font:700 14px 'Chakra Petch';letter-spacing:1.2px;padding:11px 22px;border-radius:8px;text-decoration:none!important;display:inline-block;transition:.2s}
.b1{background:linear-gradient(90deg,var(--vi),var(--mg));color:#fff!important;box-shadow:0 0 22px #8b5cf666}.b1:hover{box-shadow:0 0 36px #f01fd0aa;transform:translateY(-2px)}
.b2{border:1px solid var(--bl);color:var(--bl)!important}.b2:hover{background:#38a3ff22;box-shadow:0 0 22px #38a3ff55}
.hero{min-height:100vh;display:grid;grid-template-columns:1.05fr 1fr;align-items:center;gap:2vw;padding:110px 5vw 60px;position:relative;overflow:hidden;background:radial-gradient(ellipse at 75% 45%,#3b1a7a88,transparent 60%),radial-gradient(ellipse at 15% 90%,#0b3a7a55,transparent 55%)}
.hero h1{font:700 clamp(44px,6.4vw,92px)/.98 'Chakra Petch';margin:0 0 22px;letter-spacing:-1px}
.hero h1 span{display:block}.hero h1 .g{background:linear-gradient(90deg,var(--bl),var(--vi),var(--mg));-webkit-background-clip:text;color:transparent}
.hero p{color:var(--mu);font-size:19px;line-height:1.6;max-width:560px;margin-bottom:32px}.cta{display:flex;gap:16px;flex-wrap:wrap}
.art{position:relative;aspect-ratio:1;max-width:640px;width:100%;justify-self:center}.art svg{width:100%;height:100%}
.r1{transform-origin:50% 50%;animation:sp 40s linear infinite}.r2{transform-origin:50% 50%;animation:sp 26s linear infinite reverse}
@keyframes sp{to{transform:rotate(360deg)}}
.pt{fill:#c9b8ff;animation:fl 6s ease-in-out infinite}@keyframes fl{50%{transform:translateY(-14px);opacity:.2}}
@media(prefers-reduced-motion:reduce){.r1,.r2,.pt{animation:none}}
.sec{padding:96px 5vw;border-top:1px solid var(--ln)}.sec h2{font:700 clamp(32px,4vw,52px)/1.05 'Chakra Petch';margin:0 0 12px}.sec .lead{color:var(--mu);max-width:640px;margin-bottom:38px;font-size:17px}
.rows{display:grid;gap:10px;max-width:900px}.row{display:grid;grid-template-columns:54px 1fr 90px 110px;align-items:center;gap:14px;padding:16px 20px;background:var(--ch);border:1px solid var(--ln);border-radius:12px;transition:.2s}
.row:hover{border-color:var(--vi);box-shadow:0 0 24px #8b5cf633}.pos{font:700 26px 'Chakra Petch';color:var(--mg)}.rk{font:700 22px 'Chakra Petch';color:var(--bl);text-align:center}.xp{color:var(--mu);text-align:right}
.two{display:grid;grid-template-columns:1fr 1fr;gap:22px}.panel{background:var(--ch);border:1px solid var(--ln);border-radius:14px;padding:26px}.panel h3{font:700 22px 'Chakra Petch';margin:0 0 14px;color:var(--bl)}
.q{padding:12px 0;border-top:1px solid var(--ln)}.q b{display:block}.q small{color:var(--mu)}
.three{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}.m{padding:28px;border-radius:14px;background:linear-gradient(160deg,#1c1432,var(--ch));border:1px solid var(--ln);transition:.25s}.m:hover{transform:translateY(-6px);border-color:var(--mg);box-shadow:0 10px 40px #f01fd033}.m h3{font:700 22px 'Chakra Petch';margin:0 0 8px}.m p{color:var(--mu);margin:0}
.bar{margin:0 0 16px}.bar div:first-child{display:flex;justify-content:space-between;font-weight:600;margin-bottom:6px}.bt{height:9px;background:#201a33;border-radius:9px;overflow:hidden}.bt i{display:block;height:100%;background:linear-gradient(90deg,var(--bl),var(--mg));border-radius:9px}
.ranks{display:grid;grid-template-columns:repeat(6,1fr);gap:14px}.rkc{text-align:center;padding:30px 8px;border-radius:14px;background:var(--ch);border:1px solid var(--ln)}.rkc b{font:700 54px 'Chakra Petch';display:block}.rkc small{color:var(--mu)}
.fin{text-align:center;padding:130px 5vw;background:radial-gradient(ellipse at 50% 50%,#5b1a9a77,transparent 65%)}.fin h2{font:700 clamp(40px,6vw,84px)/1 'Chakra Petch';margin:0 0 28px}
@media(max-width:900px){.hero{grid-template-columns:1fr;padding-top:100px}.nav .links{display:none}.nav{justify-content:space-between}.two,.three{grid-template-columns:1fr}.ranks{grid-template-columns:repeat(3,1fr)}.row{grid-template-columns:40px 1fr 60px}.row .xp{display:none}}
</style>"""

ART = """<svg viewBox="0 0 600 600"><defs><radialGradient id="gl"><stop offset="0" stop-color="#8b5cf6" stop-opacity=".7"/><stop offset="1" stop-color="#8b5cf6" stop-opacity="0"/></radialGradient>
<linearGradient id="rg" x1="0" x2="1"><stop offset="0" stop-color="#38a3ff"/><stop offset=".5" stop-color="#8b5cf6"/><stop offset="1" stop-color="#f01fd0"/></linearGradient>
<linearGradient id="bd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b1230"/><stop offset="1" stop-color="#05040a"/></linearGradient></defs>
<circle cx="300" cy="300" r="290" fill="url(#gl)"/>
<g class="r1"><circle cx="300" cy="300" r="270" fill="none" stroke="url(#rg)" stroke-width="2" stroke-dasharray="3 14"/></g>
<g class="r2"><circle cx="300" cy="300" r="225" fill="none" stroke="url(#rg)" stroke-width="3" stroke-dasharray="120 40 10 40"/></g>
<circle cx="300" cy="300" r="180" fill="none" stroke="#38a3ff" stroke-opacity=".5" stroke-width="1.5"/>
<path d="M300 110 C340 110 355 150 350 185 L390 270 L470 520 L130 520 L210 270 L250 185 C245 150 260 110 300 110Z" fill="url(#bd)" stroke="#8b5cf6" stroke-width="2"/>
<path d="M250 185 C270 215 330 215 350 185 L338 160 C320 178 280 178 262 160Z" fill="#05040a"/>
<ellipse cx="278" cy="168" rx="9" ry="4" fill="#38a3ff"/><ellipse cx="322" cy="168" rx="9" ry="4" fill="#38a3ff"/>
<path d="M400 190 L452 420" stroke="#f01fd0" stroke-width="5" stroke-linecap="round"/><path d="M400 190 L452 420" stroke="#fff" stroke-width="1.5"/>
<circle cx="150" cy="200" r="3" class="pt"/><circle cx="470" cy="150" r="4" class="pt" style="animation-delay:-2s"/><circle cx="520" cy="330" r="3" class="pt" style="animation-delay:-4s"/><circle cx="90" cy="380" r="4" class="pt" style="animation-delay:-1s"/><circle cx="230" cy="70" r="3" class="pt" style="animation-delay:-3s"/></svg>"""

def _demo_state():
    c = _c(); r = c.execute("SELECT learner_id FROM users WHERE email=?", (DEMOS[0][0],)).fetchone(); c.close()
    return load_state(r[0]) if r else {}

def render():
    e = html.escape
    s = _demo_state(); q = quests(s)
    lb = "".join(f'<div class="row"><span class="pos">{i}</span><span><b>{e(p["name"])}</b><br><small style="color:#9a93b5">Level {p["level"]} · readiness {p["readiness"]}/100</small></span><span class="rk">{p["rank"]}</span><span class="xp">{p["xp"]:,} XP</span></div>' for i, p in enumerate(leaderboard(), 1))
    def ql(items, empty): return "".join(f'<div class="q"><b>{e(o["title"])}</b><small>{e(o["skill"])} · {o["minutes"]} min</small></div>' for o in items) or f'<div class="q"><small>{empty}</small></div>'
    bars = "".join(f'<div class="bar"><div><span>{e(g["skill"])}</span><span>{g["current"]}/{g["target"]}</span></div><div class="bt"><i style="width:{int(g["current"]/g["target"]*100)}%"></i></div></div>' for g in s.get("gaps", [])[:6])
    ranks = "".join(f'<div class="rkc"><b>{n}</b><small>{t}+ readiness</small></div>' for n, t in RANKS)
    page = CSS + f"""
<nav class="nav"><a class="logo" href="?" target="_self"><i></i>EDUPATH</a><div class="links"><a href="#home">Home</a><a href="#features">Features</a><a href="#rankings">Player Rankings</a><a href="#quests">Quests</a><a href="#paths">Learning Paths</a></div>
<a class="btn b2" href="?auth=login" target="_self">LOGIN</a><a class="btn b1" href="?auth=signup" target="_self">SIGN UP</a></nav>
<section class="hero" id="home"><div><h1><span>ARISE.</span><span>LEVEL UP.</span><span class="g">BECOME THE BEST.</span></h1>
<p>EduPath reads your resume and projects, measures every skill against your target role, then turns the gaps into quests. Complete them, earn XP and climb from E-Rank to S-Rank while AI agents re-plan your path as you grow.</p>
<div class="cta"><a class="btn b1" href="?auth=signup" target="_self">AWAKEN NOW</a><a class="btn b2" href="#features" target="_self">EXPLORE THE SYSTEM</a></div></div><div class="art">{ART}</div></section>
<section class="sec" id="rankings"><h2>Player rankings</h2><p class="lead">Hunters ranked by XP earned from completed quests, skills mastered and role readiness.</p><div class="rows">{lb}</div></section>
<section class="sec" id="quests"><h2>Upcoming quests</h2><p class="lead">Every quest comes from a real skill gap in your own profile.</p><div class="two"><div class="panel"><h3>Daily missions</h3>{ql(q["daily"], "Sign up to receive your first daily quests.")}</div><div class="panel"><h3>Weekly missions</h3>{ql(q["weekly"], "Weekly quests unlock after your first analysis.")}</div></div></section>
<section class="sec" id="features"><h2>Learning missions</h2><p class="lead">AI agents design hands-on challenges that prove skill, not just course completion.</p><div class="three"><div class="m"><h3>Build Sprint</h3><p>Ship a working project that closes a priority gap.</p></div><div class="m"><h3>Debug Lab</h3><p>Fix broken systems and learn the common mistakes.</p></div><div class="m"><h3>Interview-to-Code</h3><p>Answer role-specific questions with hints and model answers.</p></div></div></section>
<section class="sec" id="paths"><h2>Career progression</h2><p class="lead">Current capability against what your target role requires.</p><div class="panel" style="max-width:760px">{bars or '<div class="q"><small>Your skill map appears after your first analysis.</small></div>'}</div></section>
<section class="sec"><h2>Hunter ranks</h2><p class="lead">Rank comes from your role readiness score.</p><div class="ranks">{ranks}</div></section>
<section class="fin"><h2>Your awakening begins here.</h2><a class="btn b1" href="?auth=signup" target="_self">AWAKEN NOW</a></section>"""
    st.markdown(page, unsafe_allow_html=True)

def _enter(user):
    st.session_state.user = user
    st.session_state.learner_id = user["learner_id"]
    st.session_state.state = load_state(user["learner_id"])
    st.query_params.clear(); st.rerun()

@st.dialog("Enter the System")
def auth_dialog(mode):
    pick = st.radio("Access", ["Log in", "Sign up", "Demo"], index={"login": 0, "signup": 1}.get(mode, 0), horizontal=True, label_visibility="collapsed")
    if pick == "Log in":
        em = st.text_input("Email", key="li_e"); pw = st.text_input("Password", type="password", key="li_p")
        if st.button("Log in", type="primary", use_container_width=True):
            u, err = login(em, pw)
            _enter(u) if u else st.error(err)
    elif pick == "Sign up":
        nm = st.text_input("Hunter name", key="su_n"); em = st.text_input("Email", key="su_e")
        pw = st.text_input("Password (8+ characters)", type="password", key="su_p"); cf = st.text_input("Confirm password", type="password", key="su_c")
        if st.button("Create hunter account", type="primary", use_container_width=True):
            u, err = register(nm, em, pw, cf)
            _enter(u) if u else st.error(err)
    else:
        st.write("Explore a pre-analyzed hunter profile with real quests, skill gaps and rank. No sign-up needed.")
        if st.button("Enter as Demo Hunter", type="primary", use_container_width=True):
            u, err = demo_login()
            _enter(u) if u else st.error(err)
    if st.button("Close", use_container_width=True):
        st.query_params.clear(); st.rerun()

def open_if_requested():
    m = st.query_params.get("auth")
    if m: auth_dialog(m)
