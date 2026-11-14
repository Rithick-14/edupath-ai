import streamlit as st
from dotenv import load_dotenv
from core.llm import groq_service
from core.graphs import build_analysis_graph
from core.coach_graph import build_coach_graph
from services.auth import ensure_demo
from core.hunter import profile
import landing
from ui import css, header, PAGES

load_dotenv()
st.set_page_config(page_title="EduPath", page_icon="assets/logo.svg", layout="wide", initial_sidebar_state="collapsed")
if "user" not in st.session_state:
    ensure_demo(); landing.render(); landing.open_if_requested(); st.stop()
css()
if "chat" not in st.session_state:
    st.session_state.chat=[]
if "interview_nonce" not in st.session_state:
    st.session_state.interview_nonce=0

header(groq_service.live)
hp=profile(st.session_state.state); u=st.session_state.user
nx=f"{hp['next'][1]-hp['readiness']} readiness to {hp['next'][0]}-Rank" if hp["next"] else "Max rank"
a,b=st.columns([6,1])
a.markdown(f'<div class="card" style="padding:12px 18px"><b>{u["name"]}</b> &nbsp;<span class="pill">{hp["rank"]}-Rank</span><span class="pill">Level {hp["level"]}</span><span class="pill">{hp["xp"]:,} XP</span><span class="muted"> {nx} · {hp["done"]}/{hp["total"]} quests cleared</span></div>',unsafe_allow_html=True)
if b.button("Log out",use_container_width=True):
    st.session_state.clear(); st.rerun()
# IMPORTANT: st.navigation treats a dict as a section -> [pages] mapping.
# Passing {page_name: StreamlitPage} makes Streamlit try to iterate a single
# StreamlitPage, which causes: "TypeError: 'StreamlitPage' object is not iterable".
# Use a list for a flat navigation bar.
pages=[
    st.Page(
        f"pages/{name.split(' ',1)[1].lower().replace(' ','_')}.py",
        title=name.split(' ',1)[1],
    )
    for name in PAGES
]
selected=st.navigation(pages, position="top")
selected.run()
