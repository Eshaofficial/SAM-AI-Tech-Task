"""
TASK 5: Votes Analysis
--------------------------------------------------
- Identify the restaurants with the highest and lowest number of votes.
- Analyze if there is a correlation between the number of votes
  and the rating of a restaurant.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
df = pd.read_csv("zomato_cleaned.csv")

# ---------------------------------------------------------
# 1. Highest voted restaurants
# ---------------------------------------------------------
top_voted = df.sort_values("votes", ascending=False)[
    ["name", "location", "votes", "rate", "cuisines"]
].head(10)
print("Top 10 restaurants by number of votes:")
print(top_voted.to_string(index=False))

# ---------------------------------------------------------
# 2. Lowest voted restaurants (excluding zero-vote listings,
#    since those are just "unreviewed" not meaningfully "lowest")
# ---------------------------------------------------------
lowest_voted_nonzero = df[df["votes"] > 0].sort_values("votes")[
    ["name", "location", "votes", "rate", "cuisines"]
].head(10)
print("\nBottom 10 restaurants by number of votes (excluding 0-vote listings):")
print(lowest_voted_nonzero.to_string(index=False))

zero_vote_count = (df["votes"] == 0).sum()
print(f"\nRestaurants with 0 votes: {zero_vote_count} ({zero_vote_count/len(df)*100:.1f}% of dataset)")

# ---------------------------------------------------------
# 3. Correlation between votes and rating
# ---------------------------------------------------------
corr_df = df.dropna(subset=["rate", "votes"])
correlation = corr_df["votes"].corr(corr_df["rate"])
print(f"\nCorrelation between votes and rating: {correlation:.3f}")

# Also check with log(votes) since votes is heavily right-skewed
import numpy as np
corr_df = corr_df[corr_df["votes"] > 0].copy()
corr_df["log_votes"] = np.log1p(corr_df["votes"])
log_correlation = corr_df["log_votes"].corr(corr_df["rate"])
print(f"Correlation between log(votes) and rating: {log_correlation:.3f}")

# ---------------------------------------------------------
# 4. Bucket votes into ranges and compare average rating
# ---------------------------------------------------------
bins = [0, 10, 50, 100, 500, 1000, 5000, corr_df["votes"].max()]
labels = ["0-10", "11-50", "51-100", "101-500", "501-1000", "1001-5000", "5000+"]
corr_df["vote_bucket"] = pd.cut(corr_df["votes"], bins=bins, labels=labels)

bucket_stats = corr_df.groupby("vote_bucket", observed=True)["rate"].agg(["mean", "count"])
print("\nAverage rating by vote-count bucket:")
print(bucket_stats)

# ---------------------------------------------------------
# 5. VISUALS
# ---------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Chart 1: scatter of votes vs rating (log scale for votes, since heavily skewed)
sample = corr_df.sample(min(5000, len(corr_df)), random_state=42)  # sample for readability
axes[0].scatter(sample["votes"], sample["rate"], alpha=0.15, s=10, color="#2980b9")
axes[0].set_xscale("log")
axes[0].set_title(f"Votes vs Rating (r = {correlation:.2f})", fontsize=13, fontweight="bold")
axes[0].set_xlabel("Number of Votes (log scale)")
axes[0].set_ylabel("Rating")

# Chart 2: average rating by vote bucket
axes[1].bar(bucket_stats.index.astype(str), bucket_stats["mean"], color="#8e44ad")
axes[1].set_title("Average Rating by Vote-Count Bucket", fontsize=13, fontweight="bold")
axes[1].set_xlabel("Number of Votes")
axes[1].set_ylabel("Average Rating")
axes[1].tick_params(axis="x", rotation=30)

plt.tight_layout()
plt.savefig("task5_votes_analysis.png", dpi=150, bbox_inches="tight")
print("\nSaved chart: task5_votes_analysis.png")
