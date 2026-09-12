import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from config import COUNT_FEATURES, RATE_FEATURES


@st.cache_data
def load_data(min_minutes=900):
    df = pd.read_excel("Book1.xlsx")
    df = df[df["Minutes played"] >= min_minutes].reset_index(drop=True).copy()

    per90 = df["Minutes played"] / 90
    for col in COUNT_FEATURES:
        df[col + "_p90"] = df[col] / per90

    feature_cols = [c + "_p90" for c in COUNT_FEATURES] + RATE_FEATURES
    scaler = StandardScaler()
    X = scaler.fit_transform(df[feature_cols].fillna(0))
    return df, X, feature_cols