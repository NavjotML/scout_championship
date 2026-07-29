import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="Replacement Index — Championship CBs",
    page_icon="⌖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Design tokens
# ---------------------------------------------------------------------------
BG = "#0B0F0D"
CARD = "#141917"
CARD_BORDER = "#232A26"
TEXT = "#E9EDE9"
MUTED = "#8A9691"
ACCENT = "#3ECF8E"
ACCENT_DIM = "#2A8F63"
AMBER = "#E8A33D"
DANGER = "#D9614F"

st.markdown(f"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">

<style>
:root {{
    --bg: {BG}; --card: {CARD}; --card-border: {CARD_BORDER};
    --text: {TEXT}; --muted: {MUTED}; --accent: {ACCENT};
    --accent-dim: {ACCENT_DIM}; --amber: {AMBER}; --danger: {DANGER};
}}

.stApp {{
    background: var(--bg);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}}
#MainMenu, footer, header {{visibility: hidden;}}
.block-container {{padding-top: 2rem; padding-bottom: 3rem; max-width: 1180px;}}

/* Hero */
.hero-eyebrow {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px; letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--accent); margin-bottom: 6px; font-weight: 600;
}}
.hero-title {{
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 800; font-size: 56px; line-height: 0.98;
    letter-spacing: -0.01em; color: var(--text); margin: 0 0 8px 0;
    text-transform: uppercase;
}}
.hero-title span {{ color: var(--accent); }}
.hero-sub {{
    color: var(--muted); font-size: 15px; max-width: 640px; line-height: 1.55;
    margin-bottom: 28px;
}}
.hero-divider {{
    height: 1px; background: linear-gradient(90deg, var(--accent) 0%, var(--card-border) 40%);
    margin: 24px 0 32px 0;
}}

/* Control panel */
.panel-label {{
    font-family: 'JetBrains Mono', monospace; font-size: 11px;
    letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted);
    margin-bottom: 4px; display: block;
}}

div[data-baseweb="select"] > div, .stNumberInput input, .stSlider {{
    background-color: var(--card) !important;
}}
div[data-baseweb="select"] > div {{
    border: 1px solid var(--card-border) !important; border-radius: 6px !important;
}}
.stNumberInput input {{
    border: 1px solid var(--card-border) !important; border-radius: 6px !important;
    color: var(--text) !important;
}}

/* Results header */
.results-title {{
    font-family: 'Barlow Condensed', sans-serif; font-weight: 700;
    font-size: 22px; text-transform: uppercase; letter-spacing: 0.02em;
    color: var(--text); margin: 8px 0 2px 0;
}}
.results-meta {{
    font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--muted);
    margin-bottom: 20px;
}}

/* Result card */
.player-card {{
    background: var(--card); border: 1px solid var(--card-border);
    border-radius: 10px; padding: 18px 22px; margin-bottom: 12px;
    display: flex; align-items: center; gap: 20px;
}}
.rank-num {{
    font-family: 'Barlow Condensed', sans-serif; font-weight: 800;
    font-size: 34px; color: var(--card-border); width: 46px; text-align: center;
    flex-shrink: 0;
}}
.rank-num.top {{ color: var(--accent); }}
.player-main {{ flex: 1; min-width: 220px; }}
.player-name {{
    font-family: 'Barlow Condensed', sans-serif; font-weight: 700;
    font-size: 22px; color: var(--text); text-transform: uppercase;
    letter-spacing: 0.01em; line-height: 1.1;
}}
.player-meta {{
    font-family: 'JetBrains Mono', monospace; font-size: 12px;
    color: var(--muted); margin-top: 3px;
}}
.fit-block {{ width: 230px; flex-shrink: 0; }}
.fit-row {{ display: flex; align-items: center; gap: 8px; margin-bottom: 5px; }}
.fit-tag {{
    font-family: 'JetBrains Mono', monospace; font-size: 10px; color: var(--muted);
    width: 58px; text-transform: uppercase; letter-spacing: 0.04em;
}}
.fit-track {{
    flex: 1; height: 6px; background: #1D2420; border-radius: 3px; overflow: hidden;
}}
.fit-fill {{ height: 100%; border-radius: 3px; }}
.overall-score {{
    font-family: 'JetBrains Mono', monospace; font-weight: 700;
    font-size: 26px; color: var(--accent); width: 78px; text-align: right; flex-shrink: 0;
}}
.overall-label {{
    font-family: 'JetBrains Mono', monospace; font-size: 9px; color: var(--muted);
    text-align: right; letter-spacing: 0.08em;
}}

.caveat-box {{
    background: rgba(232, 163, 61, 0.08); border: 1px solid rgba(232, 163, 61, 0.35);
    border-radius: 8px; padding: 12px 16px; margin-top: 28px;
    font-family: 'JetBrains Mono', monospace; font-size: 11.5px; color: var(--amber);
    line-height: 1.6;
}}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Data + model logic
# ---------------------------------------------------------------------------
@st.cache_data
def load_data(min_minutes=900):
    df = pd.read_excel("Book1.xlsx")
    df = df[df["Minutes played"] >= min_minutes].reset_index(drop=True).copy()

    count_features = [
        "Tackles", "Interceptions", "Clearances", "Blocked shots",
        "Errors leading to goal", "Errors leading to shot", "Dribbled past",
        "Aerial duels won", "Fouls", "Dispossessed",
        "Accurate passes", "Long balls (accurate)", "Key passes", "Clean sheets"
    ]
    per90 = df["Minutes played"] / 90
    for col in count_features:
        df[col + "_p90"] = df[col] / per90

    rate_features = ["Aerial duels won %", "Accurate passes %", "Accurate long balls %"]
    feature_cols = [c + "_p90" for c in count_features] + rate_features

    scaler = StandardScaler()
    X = scaler.fit_transform(df[feature_cols].fillna(0))
    return df, X, feature_cols


def tactical_fit_score(df, X, target_name):
    idx = df.index[df["Name"] == target_name][0]
    sims = cosine_similarity(X[idx].reshape(1, -1), X).flatten()
    return pd.Series((sims + 1) / 2, index=df.index)


def budget_fit_score(df, budget_eur_m):
    value = df["Market Value (€m)"]
    score = np.where(value <= budget_eur_m, 1.0,
                      np.maximum(0, 1 - (value - budget_eur_m) / budget_eur_m))
    return pd.Series(score, index=df.index)


def age_fit_score(df, target_age, tolerance=4):
    age = df["Age"]
    return pd.Series(np.exp(-((age - target_age) ** 2) / (2 * tolerance ** 2)), index=df.index)


def rank_candidates(df, X, target_style_player, budget_eur_m, target_age, weights, top_n=8):
    tactical = tactical_fit_score(df, X, target_style_player)
    budget = budget_fit_score(df, budget_eur_m)
    age = age_fit_score(df, target_age)
    blended = weights["tactical"] * tactical + weights["budget"] * budget + weights["age"] * age

    out = df[["Name", "Team", "Age", "Market Value (€m)", "Contract Expiry"]].copy()
    out["Tactical"] = tactical
    out["Budget"] = budget
    out["Age fit"] = age
    out["Overall"] = blended
    out = out[out["Name"] != target_style_player]
    return out.sort_values("Overall", ascending=False).head(top_n).reset_index(drop=True)


df, X, feature_cols = load_data()

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown("""
<div class="hero-eyebrow">EFL Championship · 2025/26 · Centre-Backs</div>
<div class="hero-title">Replacement<br><span>Index</span></div>
<div class="hero-sub">
Find statistical successors for any Championship centre-back — weighted across
tactical style, budget, and age. Built on 144 players (min. 900 minutes),
17 per-90 normalized features, standardized and compared by cosine similarity.
</div>
<div class="hero-divider"></div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Control panel
# ---------------------------------------------------------------------------
c1, c2, c3 = st.columns([1.4, 1, 1])
with c1:
    st.markdown('<span class="panel-label">Target player</span>', unsafe_allow_html=True)
    target_player = st.selectbox(
        "target_player", sorted(df["Name"].unique()),
        index=sorted(df["Name"].unique()).index("Jannik Vestergaard") if "Jannik Vestergaard" in df["Name"].values else 0,
        label_visibility="collapsed"
    )
with c2:
    st.markdown('<span class="panel-label">Budget (€m)</span>', unsafe_allow_html=True)
    budget = st.number_input("budget", min_value=0.1, max_value=30.0, value=4.0, step=0.5, label_visibility="collapsed")
with c3:
    st.markdown('<span class="panel-label">Target age</span>', unsafe_allow_html=True)
    target_age = st.number_input("age", min_value=18, max_value=40, value=25, step=1, label_visibility="collapsed")

st.markdown('<span class="panel-label" style="margin-top:14px; display:block;">Weighting — tactical / budget / age</span>', unsafe_allow_html=True)
w1, w2, w3 = st.columns(3)
with w1:
    w_tactical = st.slider("Tactical weight", 0.0, 1.0, 0.5, 0.05, label_visibility="collapsed")
with w2:
    w_budget = st.slider("Budget weight", 0.0, 1.0, 0.3, 0.05, label_visibility="collapsed")
with w3:
    w_age = st.slider("Age weight", 0.0, 1.0, 0.2, 0.05, label_visibility="collapsed")

total_w = w_tactical + w_budget + w_age
if total_w == 0:
    total_w = 1
weights = {"tactical": w_tactical / total_w, "budget": w_budget / total_w, "age": w_age / total_w}

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
results = rank_candidates(df, X, target_player, budget, target_age, weights, top_n=8)

st.markdown(f'<div class="results-title">Closest replacements for {target_player}</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="results-meta">WEIGHTS &nbsp;·&nbsp; TACTICAL {weights["tactical"]:.0%} &nbsp;·&nbsp; '
    f'BUDGET {weights["budget"]:.0%} &nbsp;·&nbsp; AGE {weights["age"]:.0%}</div>',
    unsafe_allow_html=True
)

for i, row in results.iterrows():
    rank_class = "top" if i == 0 else ""
    over_budget = row["Market Value (€m)"] > budget
    value_color = AMBER if over_budget else MUTED

    st.markdown(f"""
    <div class="player-card">
        <div class="rank-num {rank_class}">{i+1:02d}</div>
        <div class="player-main">
            <div class="player-name">{row['Name']}</div>
            <div class="player-meta">{row['Team']} &nbsp;·&nbsp; AGE {row['Age']} &nbsp;·&nbsp;
                <span style="color:{value_color}">€{row['Market Value (€m)']:.1f}M</span>
                &nbsp;·&nbsp; CONTRACT {row['Contract Expiry']}</div>
        </div>
        <div class="fit-block">
            <div class="fit-row">
                <div class="fit-tag">Tactical</div>
                <div class="fit-track"><div class="fit-fill" style="width:{row['Tactical']*100:.0f}%; background:{ACCENT};"></div></div>
            </div>
            <div class="fit-row">
                <div class="fit-tag">Budget</div>
                <div class="fit-track"><div class="fit-fill" style="width:{row['Budget']*100:.0f}%; background:{AMBER};"></div></div>
            </div>
            <div class="fit-row">
                <div class="fit-tag">Age</div>
                <div class="fit-track"><div class="fit-fill" style="width:{row['Age fit']*100:.0f}%; background:{ACCENT_DIM};"></div></div>
            </div>
        </div>
        <div>
            <div class="overall-score">{row['Overall']*100:.0f}</div>
            <div class="overall-label">FIT SCORE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="caveat-box">
⚠ MARKET VALUE IS A VALUATION PROXY, NOT A CONFIRMED TRANSFER FEE. TACTICAL FIT
IS DERIVED FROM DEFENSIVE + PASSING PER-90 OUTPUT ONLY — IT DOES NOT CAPTURE
PHYSICALITY, OFF-BALL INTELLIGENCE, OR CHARACTER. TREAT AS A SHORTLISTING TOOL,
NOT A FINAL RECOMMENDATION.
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div style="margin-top:24px; font-family:JetBrains Mono, monospace; font-size:11px; '
    'color:#5A6660; text-align:right;">ANALYSIS BY NAVJOT SINGH</div>',
    unsafe_allow_html=True
)
