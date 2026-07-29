# Replacement Index — Championship Centre-Back Recruitment Tool

A statistical replacement-finder for EFL Championship centre-backs. Given a
target player, a budget, and a target age, the tool returns a ranked
shortlist of the closest statistical matches — combining tactical style
similarity, budget fit, and age fit into one transparent, explainable score.

Built as part of a larger Recruitment Recommendation System project
(archetype clustering -> similarity engine -> multi-objective ranking ->
full recommendation system).

---

## What it does

- Represents every Championship centre-back (min. 900 minutes, 2025/26) as
  a 17-dimensional per-90 statistical vector: defensive actions, duels,
  errors, and passing/progression.
- Standardizes and compares players using cosine similarity ("tactical fit").
- Scores budget fit against a stated transfer budget (market value used as
  a proxy).
- Scores age fit against a target age using a smooth Gaussian falloff.
- Blends all three into one adjustable, weighted "Overall fit" score, with
  every sub-score shown separately so the ranking is auditable, not a
  black box.

## Data

- Source: Sofascore (2025/26 Championship season), manually collected across
  multiple passes (defensive actions, duels, passing, minutes, market value,
  contract data).
- 220 players collected, filtered to 144 with 900+ minutes played to avoid
  small-sample noise.
- `Book1.xlsx` in this repo is the underlying dataset the app loads at
  startup.

## Model

No trained/supervised model is used for the ranking itself — this is by
design. There's no reliable historical label for "successful transfer,"
so building a supervised model on a shaky target would be less honest than
a transparent similarity + rules-based system. Tactical fit is pure
cosine-similarity geometry on standardized features; budget and age fit
are deterministic, interpretable functions. See `app.py` for the full
scoring logic.

## Known limitations

- Market value is a valuation proxy, not a confirmed transfer fee — real
  fees can diverge significantly (release clauses, distressed sales, etc.).
- Tactical fit is based on defensive + passing per-90 output only. It does
  not capture physicality, off-ball intelligence, communication, leadership,
  or character — factors a human scout would weigh heavily.
- Centre-back position was manually cross-checked against Sofascore listings,
  not inferred from formation data — a small number of edge cases (converted
  fullbacks, wing-back CBs) may be borderline.
- Season sample is single-season only; no multi-season trend data yet.

## Run locally (no Docker)

```
pip install -r requirements.txt
streamlit run app.py
```
Open http://localhost:8501

## Run with Docker

```
docker build -t cb-replacement-index .
docker run -p 8501:8501 cb-replacement-index
```
Open http://localhost:8501

## Deploy on Render (Docker-based Web Service)

1. Push this folder to a GitHub repo (must include `Dockerfile`, `app.py`,
   `requirements.txt`, `Book1.xlsx`).
2. On Render: **New -> Web Service** -> connect the repo.
3. Render auto-detects the Dockerfile:
   - Environment: Docker
   - Instance type: Free is fine for a demo/portfolio tool (spins down after
     inactivity, ~30-60s cold start on next visit) — Starter ($7/mo) keeps
     it always warm.
   - Health check path: `/_stcore/health`
4. No environment variables are required for this app.
5. Deploy. Render builds the image and exposes it on the assigned URL.

## Project structure

```
scout_app/
├── app.py              # Streamlit app: data pipeline, scoring, UI
├── Book1.xlsx           # Underlying dataset (Sofascore, 2025/26)
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container build definition
├── .dockerignore
├── .gitignore
└── README.md
```

## Roadmap

- [ ] Swap static Excel file for a Supabase-backed dataset (live updates
      without redeploying)
- [ ] Add per-comparison explanation layer (which specific stats drove the
      tactical fit score)
- [ ] Add radar chart comparing target player vs. top match
- [ ] Extend beyond centre-backs to full-backs, midfielders, forwards
- [ ] Add a Pareto-front view alongside the weighted blend, so trade-offs
      are visible rather than collapsed into one score
- [ ] Multi-season data for trend stability

---

Analysis by Navjot Singh
