"""
TASK 4: Restaurant Chains
--------------------------------------------------
- Identify if there are any restaurant chains present in the dataset.
- Analyze the ratings and popularity of different restaurant chains.

Note: each row in this dataset represents one restaurant *outlet/listing*.
A "chain" = a restaurant name that appears at multiple outlets/locations.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
df = pd.read_csv("zomato_cleaned.csv")

# ---------------------------------------------------------
# 1. Count outlets per restaurant name
# ---------------------------------------------------------
outlet_counts = df["name"].value_counts()
chains = outlet_counts[outlet_counts > 1]
non_chains = outlet_counts[outlet_counts == 1]

print(f"Total unique restaurant names: {df['name'].nunique()}")
print(f"Restaurants that are CHAINS (2+ outlets): {len(chains)}")
print(f"Standalone restaurants (1 outlet): {len(non_chains)}")
print(f"% of restaurants that are chains: {len(chains)/df['name'].nunique()*100:.1f}%")
print(f"% of ALL LISTINGS belonging to a chain: {chains.sum()/len(df)*100:.1f}%")

# ---------------------------------------------------------
# 2. Top chains by number of outlets (popularity/reach)
# ---------------------------------------------------------
top_chains_by_size = chains.head(15)
print("\nTop 15 chains by number of outlets:")
print(top_chains_by_size)

# ---------------------------------------------------------
# 3. Chain vs standalone: average rating & votes comparison
# ---------------------------------------------------------
df["is_chain"] = df["name"].isin(chains.index)

comparison = (
    df.dropna(subset=["rate"])
    .groupby("is_chain")
    .agg(avg_rating=("rate", "mean"), avg_votes=("votes", "mean"), count=("name", "count"))
)
comparison.index = comparison.index.map({True: "Chain", False: "Standalone"})
print("\nChain vs Standalone comparison:")
print(comparison)

# ---------------------------------------------------------
# 4. Best-rated chains (min outlet threshold to be meaningful)
# ---------------------------------------------------------
MIN_OUTLETS = 10
chain_stats = (
    df[df["is_chain"]]
    .dropna(subset=["rate"])
    .groupby("name")
    .agg(avg_rating=("rate", "mean"), avg_votes=("votes", "mean"), num_outlets=("name", "count"))
    .reset_index()
)
chain_stats_filtered = chain_stats[chain_stats["num_outlets"] >= MIN_OUTLETS]
top_rated_chains = chain_stats_filtered.sort_values("avg_rating", ascending=False).head(10)
print(f"\nTop 10 highest-rated chains (min {MIN_OUTLETS} outlets):")
print(top_rated_chains)

# ---------------------------------------------------------
# 5. Most popular chains by total votes (overall popularity)
# ---------------------------------------------------------
chain_total_votes = (
    df[df["is_chain"]]
    .groupby("name")["votes"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print("\nTop 10 chains by TOTAL votes across all outlets:")
print(chain_total_votes)

# ---------------------------------------------------------
# 6. VISUALS
# ---------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Chart 1: Top chains by outlet count
t = top_chains_by_size.head(10)[::-1]
axes[0].barh(t.index, t.values, color="#9b59b6")
axes[0].set_title("Top 10 Restaurant Chains by Number of Outlets", fontsize=13, fontweight="bold")
axes[0].set_xlabel("Number of Outlets")

# Chart 2: Chain vs standalone rating comparison
sns.barplot(x=comparison.index, y=comparison["avg_rating"], ax=axes[1], palette=["#e67e22", "#2ecc71"])
axes[1].set_title("Average Rating: Chain vs Standalone Restaurants", fontsize=13, fontweight="bold")
axes[1].set_ylabel("Average Rating")
axes[1].set_ylim(3.4, 3.8)
for i, v in enumerate(comparison["avg_rating"]):
    axes[1].text(i, v + 0.01, f"{v:.2f}", ha="center", fontweight="bold")

plt.tight_layout()
plt.savefig("task4_restaurant_chains.png", dpi=150, bbox_inches="tight")
print("\nSaved chart: task4_restaurant_chains.png")

# Chart 3: top rated chains
plt.figure(figsize=(9, 6))
top_rated_sorted = top_rated_chains.sort_values("avg_rating")
plt.barh(top_rated_sorted["name"], top_rated_sorted["avg_rating"], color="#16a085")
plt.title(f"Top 10 Highest-Rated Chains (min {MIN_OUTLETS} outlets)", fontsize=13, fontweight="bold")
plt.xlabel("Average Rating")
plt.xlim(3.5, 5)
plt.tight_layout()
plt.savefig("task4_top_rated_chains.png", dpi=150, bbox_inches="tight")
print("Saved chart: task4_top_rated_chains.png")
