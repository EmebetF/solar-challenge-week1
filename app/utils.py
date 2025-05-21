# app/utils.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

def load_data(country):
    if country == "Benin":
        return pd.read_csv("data/benin_clean.csv", parse_dates=["Timestamp"])
    elif country == "Sierra Leone":
        return pd.read_csv("data/sierraleone_clean.csv", parse_dates=["Timestamp"])
    elif country == "Togo":
        return pd.read_csv("data/togo-dapaong_qc_clean.csv", parse_dates=["Timestamp"])
    elif country == "All":
        b = pd.read_csv("data/benin_clean.csv")
        b["Country"] = "Benin"
        s = pd.read_csv("data/sierraleone_clean.csv")
        s["Country"] = "Sierra Leone"
        t = pd.read_csv("data/togo-dapaong_qc_clean.csv")
        t["Country"] = "Togo"
        return pd.concat([b, s, t], ignore_index=True)

def plot_time_series(df, column):
    fig, ax = plt.subplots(figsize=(10, 4))
    df = df.sort_values("Timestamp")
    sns.lineplot(x="Timestamp", y=column, data=df, ax=ax)
    ax.set_title(f"{column} Over Time")
    ax.set_ylabel(column)
    ax.set_xlabel("Time")
    st.pyplot(fig)

def plot_boxplot(df, column):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(x="Country", y=column, data=df, ax=ax)
    ax.set_title(f"{column} Distribution Across Countries")
    st.pyplot(fig)

def plot_summary_stats(df):
    summary = df.groupby("Country")[["GHI", "DNI", "DHI"]].agg(["mean", "median", "std"]).round(2)
    st.dataframe(summary) 
    # st.dataframe(summary.style.highlight_max(axis=0, color='lightgreen').format("{:.2f}"))

# app/utils.py (append this at the bottom)

from scipy.stats import f_oneway

# def perform_anova(df, column):
#     benin = df[df["Country"] == "Benin"][column]
#     sierra = df[df["Country"] == "Sierra Leone"][column]
#     togo = df[df["Country"] == "Togo"][column]
    
#     F, p = f_oneway(benin, sierra, togo)
#     return {"F": F, "p": p}

def perform_anova(df, column):
    country_groups = [group[column] for name, group in df.groupby("Country")]
    
    if len(country_groups) < 2:
        return {"F": 0, "p": 1.0}  # Not enough groups for ANOVA

    F, p = f_oneway(*country_groups)
    return {"F": F, "p": p}
