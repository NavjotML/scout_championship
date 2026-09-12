import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


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