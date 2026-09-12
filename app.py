import streamlit as st
from data import load_data
from scoring import rank_candidates
from explain import get_explanation
from styles import inject_css
from ui import render_hero, render_card

st.set_page_config(page_title="Replacement Index — Championship CBs",
                    page_icon="⌖", layout="wide", initial_sidebar_state="collapsed")
inject_css()

df, X, feature_cols = load_data()
render_hero()

c1, c2, c3 = st.columns([1.4, 1, 1])
names = sorted(df["Name"].unique())
with c1:
    st.markdown('<span class="panel-label">Target player</span>', unsafe_allow_html=True)
    target_player = st.selectbox("target_player", names,
        index=names.index("Jannik Vestergaard") if "Jannik Vestergaard" in names else 0,
        label_visibility="collapsed")
with c2:
    st.markdown('<span class="panel-label">Budget (€m)</span>', unsafe_allow_html=True)
    budget = st.number_input("budget", min_value=0.1, max_value=30.0, value=4.0, step=0.5, label_visibility="collapsed")
with c3:
    st.markdown('<span class="panel-label">Target age</span>', unsafe_allow_html=True)
    target_age = st.number_input("age", min_value=18, max_value=40, value=25, step=1, label_visibility="collapsed")

st.markdown('<span class="panel-label">Weighting — tactical / budget / age</span>', unsafe_allow_html=True)
w1, w2, w3 = st.columns(3)
w_tactical = w1.slider("Tactical weight", 0.0, 1.0, 0.5, 0.05, label_visibility="collapsed")
w_budget = w2.slider("Budget weight", 0.0, 1.0, 0.3, 0.05, label_visibility="collapsed")
w_age = w3.slider("Age weight", 0.0, 1.0, 0.2, 0.05, label_visibility="collapsed")

total_w = (w_tactical + w_budget + w_age) or 1
weights = {"tactical": w_tactical / total_w, "budget": w_budget / total_w, "age": w_age / total_w}

results = rank_candidates(df, X, target_player, budget, target_age, weights, top_n=8)
st.markdown(f'<div class="results-title">Closest replacements for {target_player}</div>', unsafe_allow_html=True)

if "shown_explanation" not in st.session_state:
    st.session_state.shown_explanation = None

for i, row in results.iterrows():
    render_card(i, row, budget)

    if st.button(f"Explain {row['Name']}", key=f"explain_{row['Name']}"):
        st.session_state.shown_explanation = row["Name"]

    if st.session_state.shown_explanation == row["Name"]:
        with st.spinner("Generating explanation..."):
            try:
                expl = get_explanation(
                    row,
                    target_player,
                    df,
                    X,
                    feature_cols
                )
            except Exception as e:
                st.error(f"Explanation failed: {e}")
                expl = None

        if expl:
            st.markdown(f'<div class="explanation-text">{expl}</div>', unsafe_allow_html=True)