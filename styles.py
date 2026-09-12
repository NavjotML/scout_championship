import streamlit as st
from config import BG, CARD, CARD_BORDER, TEXT, MUTED, ACCENT, ACCENT_DIM, AMBER, DANGER


def inject_css():
    st.markdown(f"""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
    :root {{
        --bg: {BG}; --card: {CARD}; --card-border: {CARD_BORDER};
        --text: {TEXT}; --muted: {MUTED}; --accent: {ACCENT};
        --accent-dim: {ACCENT_DIM}; --amber: {AMBER}; --danger: {DANGER};
    }}
    .explanation-text {{
    font-family: 'Inter', sans-serif;
    font-size: 13.5px;
    font-weight: 700;
    color: var(--text);
    line-height: 1.6;
    margin-top: 8px;
    margin-bottom: 20px;
}}
    .stApp {{ background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; }}
    #MainMenu, footer, header {{visibility: hidden;}}
    .block-container {{padding-top: 2rem; padding-bottom: 3rem; max-width: 1180px;}}
    .hero-eyebrow {{ font-family:'JetBrains Mono',monospace; font-size:12px; letter-spacing:0.18em;
        text-transform:uppercase; color:var(--accent); margin-bottom:6px; font-weight:600; }}
    .hero-title {{ font-family:'Barlow Condensed',sans-serif; font-weight:800; font-size:56px;
        line-height:0.98; letter-spacing:-0.01em; color:var(--text); margin:0 0 8px 0; text-transform:uppercase; }}
    .hero-title span {{ color: var(--accent); }}
    .hero-sub {{ color:var(--muted); font-size:15px; max-width:640px; line-height:1.55; margin-bottom:28px; }}
    .hero-divider {{ height:1px; background:linear-gradient(90deg, var(--accent) 0%, var(--card-border) 40%); margin:24px 0 32px 0; }}
    .panel-label {{ font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:0.1em;
        text-transform:uppercase; color:var(--muted); margin-bottom:4px; display:block; }}
    div[data-baseweb="select"] > div, .stNumberInput input, .stSlider {{ background-color: var(--card) !important; }}
    div[data-baseweb="select"] > div {{ border:1px solid var(--card-border) !important; border-radius:6px !important; }}
    .stNumberInput input {{ border:1px solid var(--card-border) !important; border-radius:6px !important; color:var(--text) !important; }}
    .results-title {{ font-family:'Barlow Condensed',sans-serif; font-weight:700; font-size:22px;
        text-transform:uppercase; letter-spacing:0.02em; color:var(--text); margin:8px 0 2px 0; }}
    .results-meta {{ font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--muted); margin-bottom:20px; }}
    .player-card {{ background:var(--card); border:1px solid var(--card-border); border-radius:10px;
        padding:18px 22px; margin-bottom:12px; display:flex; align-items:center; gap:20px; }}
    .rank-num {{ font-family:'Barlow Condensed',sans-serif; font-weight:800; font-size:34px;
        color:var(--card-border); width:46px; text-align:center; flex-shrink:0; }}
    .rank-num.top {{ color: var(--accent); }}
    .player-main {{ flex:1; min-width:220px; }}
    .player-name {{ font-family:'Barlow Condensed',sans-serif; font-weight:700; font-size:22px;
        color:var(--text); text-transform:uppercase; letter-spacing:0.01em; line-height:1.1; }}
    .player-meta {{ font-family:'JetBrains Mono',monospace; font-size:12px; color:var(--muted); margin-top:3px; }}
    .fit-block {{ width:230px; flex-shrink:0; }}
    .fit-row {{ display:flex; align-items:center; gap:8px; margin-bottom:5px; }}
    .fit-tag {{ font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--muted);
        width:58px; text-transform:uppercase; letter-spacing:0.04em; }}
    .fit-track {{ flex:1; height:6px; background:#1D2420; border-radius:3px; overflow:hidden; }}
    .fit-fill {{ height:100%; border-radius:3px; }}
    .overall-score {{ font-family:'JetBrains Mono',monospace; font-weight:700; font-size:26px;
        color:var(--accent); width:78px; text-align:right; flex-shrink:0; }}
    .overall-label {{ font-family:'JetBrains Mono',monospace; font-size:9px; color:var(--muted);
        text-align:right; letter-spacing:0.08em; }}
    .caveat-box {{ background:rgba(232,163,61,0.08); border:1px solid rgba(232,163,61,0.35);
        border-radius:8px; padding:12px 16px; margin-top:28px; font-family:'JetBrains Mono',monospace;
        font-size:11.5px; color:var(--amber); line-height:1.6; }}
    </style>
    """, unsafe_allow_html=True)

