# app/main.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import (
    load_data,
    plot_boxplot,
    plot_time_series,
    plot_summary_stats,
    perform_anova
)

st.set_page_config(page_title="Solar Data Dashboard", layout="wide")

st.title("Cross-Country Solar Energy Dashboard")
st.markdown("Visualize and compare solar radiation across Benin, Sierra Leone, and Togo.")

# Sidebar country selection
countries = ["Benin", "Sierra Leone", "Togo"]
selected_country = st.sidebar.selectbox("Select a Country for EDA", countries)

# Load data
df = load_data(selected_country)

# EDA Section
st.header(f"Exploratory Data Analysis: {selected_country}")
st.subheader("Time Series: Global Horizontal Irradiance (GHI)")
plot_time_series(df, "GHI")

col1, col2 = st.columns(2)
with col1:
    st.subheader("DNI over Time")
    plot_time_series(df, "DNI")

with col2:
    st.subheader("Temperature (Tamb) over Time")
    plot_time_series(df, "Tamb")

# Summary statistics
st.subheader("Summary Statistics")
st.dataframe(df[["GHI", "DNI", "DHI", "Tamb"]].describe())

# Cross-Country Comparison Section
st.header("Cross-Country Comparison")

# full_df = load_data("All") # select all countries one time

#Specific dynamic selections 
selected_countries = st.sidebar.multiselect(
    "Select Countries for Comparison",
    ["Benin", "Sierra Leone", "Togo"],
    default=["Benin", "Sierra Leone", "Togo"]
)

full_df = load_data("All")
full_df = full_df[full_df["Country"].isin(selected_countries)]

with st.expander("Boxplot Comparisons"):
    for metric in ["GHI", "DNI", "DHI"]:
        st.subheader(f"{metric} Distribution Across Countries")
        plot_boxplot(full_df, metric)

with st.expander("Summary Statistics Table"):
    st.subheader("Metric Summary (Mean, Median, Std) by Country")
    plot_summary_stats(full_df)

with st.expander("ANOVA Test Results"):
    st.subheader("Statistical Test: Is GHI significantly different across countries?")
    anova_results = perform_anova(full_df, "GHI")
    st.markdown(f"""
    - **F-statistic**: {anova_results['F']:.2f}  
    - **p-value**: {anova_results['p']:.4f}  
    """)
    if anova_results["p"] < 0.05:
        st.success("Statistically significant difference in GHI among countries (p < 0.05).")
    else:
        st.warning("No statistically significant difference in GHI (p ≥ 0.05).")
