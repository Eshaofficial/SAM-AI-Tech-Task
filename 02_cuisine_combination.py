"""
TASK 2: Cuisine Combination
--------------------------------------------------
- Identify the most common combinations of cuisines in the dataset.
- Determine if certain cuisine combinations tend to have higher ratings.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
df = pd.read_csv("zomato_cleaned.csv")

# ---------------------------------------------------------
# 1. Normalize cuisine combos so order doesn't create duplicates
#    e.g. "Chinese, North Indian" == "North Indian, Chinese"
# ---------------------------------------------------------
def normalize_combo(x):
    parts = [p.strip() for p in str(x).split(",")]
    parts = sorted(parts)
    return ", ".join(parts)

df["cuisine_combo"] = df["cuisines"].apply(normalize_combo)
df["num_cuisines"] = df["cuisines"].apply(lambda x: len(str(x).split(",")))

# ---------------------------------------------------------
# 2. Most common cuisine combinations (overall)
# ---------------------------------------------------------
top_combos = df["cuisine_combo"].value_counts().head(15)
print("Top 15 most common cuisine combinations:")
print(top_combos)

# ---------------------------------------------------------
# 3. Ratings by combo -- only combos with a reasonable sample size
#    (avoid combos that appear once skewing the "highest rated" list)
# ---------------------------------------------------------
combo_stats = (
    df.dropna(subset=["rate"])
    .groupby("cuisine_combo")
    .agg(avg_rating=("rate", "mean"), count=("rate", "count"))
    .reset_index()
)

MIN_SAMPLES = 30
combo_stats_filtered = combo_stats[combo_stats["count"] >= MIN_SAMPLES]

top_rated_combos = combo_stats_filtered.sort_values("avg_rating", ascending=False).head(15)
print(f"\nTop 15 highest-rated cuisine combinations (min {MIN_SAMPLES} restaurants):")
print(top_rated_combos)

# ---------------------------------------------------------
# 4. Does number of cuisines offered relate to rating?
# ---------------------------------------------------------
num_cuisine_stats = (
    df.dropna(subset=["rate"])
    .groupby("num_cuisines")["rate"]
    .mean()
    .reset_index()
)
print("\nAverage rating by number of cuisines offered:")
print(num_cuisine_stats)

# ---------------------------------------------------------
# 5. VISUALS
# ---------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Chart 1: Most common combos
top10 = df["cuisine_combo"].value_counts().head(10)[::-1]
axes[0].barh(top10.index, top10.values, color="#e74c3c")
axes[0].set_title("Top 10 Most Common Cuisine Combinations", fontsize=13, fontweight="bold")
axes[0].set_xlabel("Number of Restaurants")

# Chart 2: Highest rated combos (min sample size)
top10_rated = top_rated_combos.head(10).sort_values("avg_rating")
axes[1].barh(top10_rated["cuisine_combo"], top10_rated["avg_rating"], color="#27ae60")
axes[1].set_title(f"Top 10 Highest-Rated Combos (min {MIN_SAMPLES} restaurants)", fontsize=13, fontweight="bold")
axes[1].set_xlabel("Average Rating")
axes[1].set_xlim(3.5, 5)

plt.tight_layout()
plt.savefig("task2_cuisine_combination.png", dpi=150, bbox_inches="tight")
print("\nSaved chart: task2_cuisine_combination.png")

# Chart 3: number of cuisines vs rating
plt.figure(figsize=(8, 5))
sns.barplot(data=num_cuisine_stats, x="num_cuisines", y="rate", color="#3498db")
plt.title("Average Rating by Number of Cuisines Offered", fontsize=13, fontweight="bold")
plt.xlabel("Number of Cuisines Offered")
plt.ylabel("Average Rating")
plt.tight_layout()
plt.savefig("task2_num_cuisines_vs_rating.png", dpi=150, bbox_inches="tight")
print("Saved chart: task2_num_cuisines_vs_rating.png")
