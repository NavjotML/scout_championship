import streamlit as st
from config import ACCENT, AMBER, ACCENT_DIM, MUTED


def render_hero():
    st.markdown("""
    <div class="hero-eyebrow">EFL Championship · 2025/26 · Centre-Backs</div>
    <div class="hero-title">Replacement<br><span>Index</span></div>
    <div class="hero-sub">Find statistical successors for any Championship centre-back —
    weighted across tactical style, budget, and age.</div>
    <div class="hero-divider"></div>
    """, unsafe_allow_html=True)


def render_card(i, row, budget, explanation=None):
    rank_class = "top" if i == 0 else ""
    value_color = AMBER if row["Market Value (€m)"] > budget else MUTED
    expl_html = f'<div class="player-meta" style="margin-top:8px;">{explanation}</div>' if explanation else ""

    html = (
        f'<div class="player-card">'
        f'<div class="rank-num {rank_class}">{i+1:02d}</div>'
        f'<div class="player-main">'
        f'<div class="player-name">{row["Name"]}</div>'
        f'<div class="player-meta">{row["Team"]} · AGE {row["Age"]} · '
        f'<span style="color:{value_color}">€{row["Market Value (€m)"]:.1f}M</span> '
        f'· CONTRACT {row["Contract Expiry"]}</div>'
        f'{expl_html}'
        f'</div>'
        f'<div class="fit-block">'
        f'<div class="fit-row"><div class="fit-tag">Tactical</div>'
        f'<div class="fit-track"><div class="fit-fill" style="width:{row["Tactical"]*100:.0f}%; background:{ACCENT};"></div></div></div>'
        f'<div class="fit-row"><div class="fit-tag">Budget</div>'
        f'<div class="fit-track"><div class="fit-fill" style="width:{row["Budget"]*100:.0f}%; background:{AMBER};"></div></div></div>'
        f'<div class="fit-row"><div class="fit-tag">Age</div>'
        f'<div class="fit-track"><div class="fit-fill" style="width:{row["Age fit"]*100:.0f}%; background:{ACCENT_DIM};"></div></div></div>'
        f'</div>'
        f'<div><div class="overall-score">{row["Overall"]*100:.0f}</div>'
        f'<div class="overall-label">FIT SCORE</div></div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)