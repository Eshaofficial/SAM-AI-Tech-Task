"""
ZOMATO RESTAURANT ANALYSIS — LIVE DASHBOARD
--------------------------------------------------
An interactive Streamlit dashboard covering:
  - Task 2: Cuisine Combination
  - Task 4: Restaurant Chains
  - Task 5: Votes Analysis

To run:
    pip install streamlit plotly pandas
    streamlit run app.py
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Zomato Restaurant Dashboard",
    page_icon="🍽️",
    layout="wide",
)

PLOT_BG = "#ffffff"
PAPER_BG = "#ffffff"
FONT_COLOR = "#1a1a1a"

# Vivid color palette used across charts
PALETTE_CUISINE = ["#FF6B6B", "#FF8E53", "#FFB84C", "#F9C80E", "#EF476F", "#FF9F1C", "#E63946", "#F77F00", "#D62828", "#FCBF49"]
PALETTE_CHAINS = ["#4ECDC4", "#1A936F", "#06D6A0", "#118AB2", "#00B4D8", "#43AA8B", "#2EC4B6", "#0081A7", "#00A8E8", "#26A69A"]
PALETTE_VOTES = ["#9D4EDD", "#7B2CBF", "#C77DFF", "#5A189A", "#E0AAFF", "#3C096C", "#B5179E", "#F72585", "#7209B7", "#560BAD"]

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f7f7fb 0%, #eef2f7 100%);
        color: #1a1a1a;
    }
    .kpi-card-1 { background: linear-gradient(135deg, #FF6B6B, #EE5A6F); }
    .kpi-card-2 { background: linear-gradient(135deg, #4ECDC4, #1A936F); }
    .kpi-card-3 { background: linear-gradient(135deg, #9D4EDD, #7B2CBF); }
    .kpi-card-4 { background: linear-gradient(135deg, #F9C80E, #FF9F1C); }
    .kpi-card-5 { background: linear-gradient(135deg, #118AB2, #00B4D8); }
    .kpi-card-6 { background: linear-gradient(135deg, #F72585, #B5179E); }
    .kpi-card {
        border-radius: 14px;
        padding: 18px;
        text-align: center;
        margin-bottom: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .kpi-label {
        font-size: 13px; color: rgba(255,255,255,0.9); letter-spacing: 1px;
        text-transform: uppercase; font-weight: 700;
    }
    .kpi-value { font-size: 28px; font-weight: 800; color: #ffffff; margin-top: 4px; }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #240046 0%, #3c096c 50%, #5a189a 100%);
        border-right: 3px solid #F72585;
    }
    section[data-testid="stSidebar"] * { color: #f5f0ff !important; }
    section[data-testid="stSidebar"] label { color: #ffd6ff !important; font-weight: 600; }
    h1 { color: #3c096c !important; }
    h2 {
        color: #ffffff !important;
        background: linear-gradient(90deg, #3c096c, #7b2cbf);
        padding: 8px 16px;
        border-radius: 8px;
        display: inline-block;
    }
    h3, h4, h5, p, span, .stMarkdown { color: #1a1a1a !important; }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# HELPER: safe chart wrapper
# ============================================================
def show_chart_or_message(condition, message, chart_fn):
    """If condition is True, run chart_fn() and display it. Otherwise show an info message.
    Any unexpected exception is caught so the whole app never crashes."""
    if not condition:
        st.info(message)
        return
    try:
        fig = chart_fn()
        if fig is not None:
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.info(f"Chart unavailable for this filter selection. ({e})")


def style_fig(fig):
    fig.update_layout(plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG, font_color=FONT_COLOR)
    return fig


# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    df = pd.read_csv("zomato_cleaned.csv")

    def normalize_combo(x):
        parts = sorted([p.strip() for p in str(x).split(",")])
        return ", ".join(parts)

    df["cuisine_combo"] = df["cuisines"].apply(normalize_combo)
    df["num_cuisines"] = df["cuisines"].apply(lambda x: len(str(x).split(",")))

    outlet_counts = df["name"].value_counts()
    chains = outlet_counts[outlet_counts > 1].index
    df["is_chain"] = df["name"].isin(chains)
    df["chain_label"] = df["is_chain"].map({True: "Chain", False: "Standalone"})

    return df

df = load_data()

# ============================================================
# HEADER
# ============================================================
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("## 🍽️")
with col2:
    st.markdown("# ZOMATO RESTAURANT DASHBOARD")
    st.markdown("##### Bangalore Restaurants — Cuisine, Chains & Votes Analysis")

st.markdown("---")

# ============================================================
# SIDEBAR FILTERS
# ============================================================
st.sidebar.header("🔍 Filters")

locations = ["All"] + sorted(df["location"].dropna().unique().tolist())
selected_location = st.sidebar.selectbox("Location", locations)

chain_options = ["All", "Chain", "Standalone"]
selected_chain = st.sidebar.selectbox("Restaurant Type", chain_options)

online_options = ["All"] + sorted(df["online_order"].dropna().unique().tolist())
selected_online = st.sidebar.selectbox("Online Order", online_options)

if df["rate"].notna().sum() > 0:
    min_rate, max_rate = float(df["rate"].min(skipna=True)), float(df["rate"].max(skipna=True))
else:
    min_rate, max_rate = 1.0, 5.0
rating_range = st.sidebar.slider("Rating Range", min_rate, max_rate, (min_rate, max_rate))

# Apply filters
filtered = df.copy()
if selected_location != "All":
    filtered = filtered[filtered["location"] == selected_location]
if selected_chain != "All":
    filtered = filtered[filtered["chain_label"] == selected_chain]
if selected_online != "All":
    filtered = filtered[filtered["online_order"] == selected_online]
filtered = filtered[
    (filtered["rate"].isna()) | (filtered["rate"].between(rating_range[0], rating_range[1]))
]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Showing {len(filtered):,} of {len(df):,} restaurants**")

if st.sidebar.button("🔄 Reset Filters"):
    st.rerun()

# ============================================================
# GLOBAL GUARD: no data at all
# ============================================================
if len(filtered) == 0:
    st.warning(
        "⚠️ No restaurants match the current filter combination. "
        "Try widening your filters — e.g. set Location back to **All**, "
        "or loosen the Rating Range — then the dashboard will populate again."
    )
    st.stop()

# ============================================================
# KPI CARDS
# ============================================================
total_restaurants = len(filtered)
avg_rating = filtered["rate"].mean()
avg_votes = filtered["votes"].mean()
chain_pct = (filtered["is_chain"].sum() / len(filtered) * 100) if len(filtered) else 0
avg_cost = filtered["approx_cost(for two people)"].mean()
online_pct = (
    (filtered["online_order"] == "Yes").sum() / len(filtered) * 100
    if len(filtered) else 0
)

def fmt(val, suffix="", prefix="", decimals=2, is_pct=False):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return "N/A"
    if is_pct:
        return f"{val:.1f}%"
    return f"{prefix}{val:,.{decimals}f}{suffix}"

kpis = [
    ("TOTAL RESTAURANTS", f"{total_restaurants:,}"),
    ("AVG RATING", fmt(avg_rating, suffix=" ★")),
    ("AVG VOTES", fmt(avg_votes, decimals=0)),
    ("% CHAINS", fmt(chain_pct, is_pct=True)),
    ("AVG COST (for 2)", fmt(avg_cost, prefix="₹", decimals=0)),
    ("ONLINE ORDER %", fmt(online_pct, is_pct=True)),
]

kpi_cols = st.columns(6)
for i, (col, (label, value)) in enumerate(zip(kpi_cols, kpis)):
    card_class = f"kpi-card-{(i % 6) + 1}"
    col.markdown(f"""
        <div class="kpi-card {card_class}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# TASK 2: Cuisine Combination
# ============================================================
st.markdown("## 🍜 Cuisine Combination Analysis")
c1, c2 = st.columns(2)

with c1:
    top_combos = filtered["cuisine_combo"].value_counts().head(10)

    def chart_top_combos():
        d = top_combos.sort_values().reset_index()
        d.columns = ["cuisine_combo", "count"]
        fig = px.bar(
            d, x="count", y="cuisine_combo", orientation="h",
            labels={"count": "Number of Restaurants", "cuisine_combo": ""},
            title="Top Cuisine Combinations",
            color="cuisine_combo",
            color_discrete_sequence=PALETTE_CUISINE,
        )
        fig.update_layout(showlegend=False)
        return style_fig(fig)

    show_chart_or_message(
        len(top_combos) > 0,
        "No cuisine data available for this filter selection.",
        chart_top_combos,
    )

with c2:
    rated_df = filtered.dropna(subset=["rate"])
    combo_stats = pd.DataFrame()
    if len(rated_df) > 0:
        combo_stats = (
            rated_df.groupby("cuisine_combo")
            .agg(avg_rating=("rate", "mean"), count=("rate", "count"))
            .reset_index()
        )
        min_samples = 10 if len(filtered) >= 200 else 1  # relax threshold for small filtered sets
        combo_stats = combo_stats[combo_stats["count"] >= min_samples].sort_values(
            "avg_rating", ascending=False
        ).head(10)

    def chart_top_rated_combos():
        fig = px.bar(
            combo_stats.sort_values("avg_rating"),
            x="avg_rating", y="cuisine_combo", orientation="h",
            labels={"avg_rating": "Average Rating", "cuisine_combo": ""},
            title="Highest-Rated Cuisine Combos",
            color="cuisine_combo",
            color_discrete_sequence=PALETTE_CHAINS,
        )
        fig.update_layout(showlegend=False)
        return style_fig(fig)

    show_chart_or_message(
        len(combo_stats) > 0,
        "Not enough rated restaurants in this filter selection to compare combo ratings.",
        chart_top_rated_combos,
    )

# Num cuisines vs rating trend
num_cuisine_stats = pd.DataFrame()
rated_df = filtered.dropna(subset=["rate"])
if len(rated_df) > 0:
    num_cuisine_stats = rated_df.groupby("num_cuisines")["rate"].mean().reset_index()

def chart_num_cuisine_trend():
    fig = px.line(
        num_cuisine_stats, x="num_cuisines", y="rate", markers=True,
        labels={"num_cuisines": "Number of Cuisines Offered", "rate": "Average Rating"},
        title="Average Rating by Number of Cuisines Offered",
        color_discrete_sequence=["#F72585"],
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=9, color="#7B2CBF"))
    return style_fig(fig)

show_chart_or_message(
    len(num_cuisine_stats) > 0,
    "Not enough rated restaurants in this filter selection for this trend.",
    chart_num_cuisine_trend,
)

st.markdown("---")

# ============================================================
# TASK 4: Restaurant Chains
# ============================================================
st.markdown("## 🏢 Restaurant Chains Analysis")
c3, c4 = st.columns(2)

with c3:
    chain_counts = filtered[filtered["is_chain"]]["name"].value_counts().head(10)

    def chart_chain_outlets():
        d = chain_counts.sort_values().reset_index()
        d.columns = ["name", "outlets"]
        fig = px.bar(
            d, x="outlets", y="name", orientation="h",
            labels={"outlets": "Number of Outlets", "name": ""},
            title="Top Chains by Number of Outlets",
            color="name",
            color_discrete_sequence=PALETTE_VOTES,
        )
        fig.update_layout(showlegend=False)
        return style_fig(fig)

    show_chart_or_message(
        len(chain_counts) > 0,
        "No restaurant chains found in the current filter selection.",
        chart_chain_outlets,
    )

with c4:
    rated_df = filtered.dropna(subset=["rate"])
    chain_vs_standalone = pd.DataFrame()
    if len(rated_df) > 0 and rated_df["chain_label"].nunique() > 0:
        chain_vs_standalone = (
            rated_df.groupby("chain_label")
            .agg(avg_rating=("rate", "mean"), avg_votes=("votes", "mean"))
            .reset_index()
        )

    def chart_chain_vs_standalone():
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=chain_vs_standalone["chain_label"], y=chain_vs_standalone["avg_rating"],
            name="Avg Rating",
            marker_color=["#F72585", "#4CC9F0"][:len(chain_vs_standalone)]
        ))
        fig.update_layout(title="Chain vs Standalone — Average Rating", yaxis_title="Average Rating")
        return style_fig(fig)

    show_chart_or_message(
        len(chain_vs_standalone) > 0,
        "Not enough rated restaurants in this filter selection to compare chain vs standalone.",
        chart_chain_vs_standalone,
    )

st.markdown("---")

# ============================================================
# TASK 5: Votes Analysis
# ============================================================
st.markdown("## 🗳️ Votes Analysis")
c5, c6 = st.columns(2)

corr_df = filtered.dropna(subset=["rate", "votes"])
corr_df = corr_df[corr_df["votes"] > 0]

with c5:
    def chart_votes_scatter():
        correlation = corr_df["votes"].corr(corr_df["rate"])
        sample_n = min(3000, len(corr_df))
        sample = corr_df.sample(sample_n, random_state=42) if sample_n > 0 else corr_df
        fig = px.scatter(
            sample, x="votes", y="rate", opacity=0.55,
            log_x=True,
            labels={"votes": "Number of Votes (log scale)", "rate": "Rating"},
            title=f"Votes vs Rating (r = {correlation:.2f})" if not np.isnan(correlation) else "Votes vs Rating",
            color="rate",
            color_continuous_scale=["#4CC9F0", "#7B2CBF", "#F72585", "#FFB703"],
        )
        return style_fig(fig)

    show_chart_or_message(
        len(corr_df) >= 2,
        "Not enough data points in this filter selection to compute a votes-rating correlation.",
        chart_votes_scatter,
    )

with c6:
    bucket_stats = pd.DataFrame()
    if len(corr_df) >= 2:
        max_votes = corr_df["votes"].max()
        bins = sorted(set([0, 10, 50, 100, 500, 1000, 5000, max(max_votes, 5001)]))
        labels_ = [f"{bins[i]}-{bins[i+1]}" for i in range(len(bins) - 1)]
        tmp = corr_df.copy()
        tmp["vote_bucket"] = pd.cut(tmp["votes"], bins=bins, labels=labels_, include_lowest=True)
        bucket_stats = tmp.groupby("vote_bucket", observed=True)["rate"].mean().reset_index()

    def chart_vote_buckets():
        fig = px.bar(
            bucket_stats, x="vote_bucket", y="rate",
            labels={"vote_bucket": "Vote Count Bucket", "rate": "Average Rating"},
            title="Average Rating by Vote-Count Bucket",
            color="vote_bucket",
            color_discrete_sequence=PALETTE_VOTES,
        )
        fig.update_layout(showlegend=False)
        return style_fig(fig)

    show_chart_or_message(
        len(bucket_stats) > 0,
        "Not enough data points in this filter selection to show vote-count buckets.",
        chart_vote_buckets,
    )

# ============================================================
# TOP/BOTTOM VOTED TABLE
# ============================================================
st.markdown("### 📋 Highest & Lowest Voted Restaurants")
t1, t2 = st.columns(2)

with t1:
    st.markdown("**Top 10 by Votes**")
    top_table = filtered.sort_values("votes", ascending=False)[
        ["name", "location", "votes", "rate"]
    ].head(10)
    if len(top_table) > 0:
        st.dataframe(top_table, hide_index=True, use_container_width=True)
    else:
        st.info("No data to display.")

with t2:
    st.markdown("**Bottom 10 by Votes (excl. 0)**")
    bottom_table = filtered[filtered["votes"] > 0].sort_values("votes")[
        ["name", "location", "votes", "rate"]
    ].head(10)
    if len(bottom_table) > 0:
        st.dataframe(bottom_table, hide_index=True, use_container_width=True)
    else:
        st.info("No restaurants with votes > 0 in this filter selection.")

st.markdown("---")
st.caption("Built with Streamlit + Plotly | Data Analyst Internship — SAM AI Technologies")
