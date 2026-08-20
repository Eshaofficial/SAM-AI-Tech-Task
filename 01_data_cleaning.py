"""
STEP 1: Data Cleaning
Zomato Bangalore Restaurants Dataset
--------------------------------------------------
Cleans the raw zomato.csv and saves a cleaned version
that will be reused across all 3 analysis tasks:
  - Task 2: Cuisine Combination
  - Task 4: Restaurant Chains
  - Task 5: Votes Analysis
"""

import pandas as pd

# ---------------------------------------------------------
# 1. Load raw data
# ---------------------------------------------------------
df = pd.read_csv("extracted/zomato.csv", encoding="latin-1")
print("Raw shape:", df.shape)

# ---------------------------------------------------------
# 2. Drop columns we don't need for our 3 tasks
#    (keeps things light and focused)
# ---------------------------------------------------------
cols_to_drop = ["url", "address", "phone", "reviews_list", "menu_item", "dish_liked"]
df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])

# ---------------------------------------------------------
# 3. Clean 'rate' column
#    "4.1/5" -> 4.1 ; "NEW" / "-" / NaN -> NaN
# ---------------------------------------------------------
def clean_rate(x):
    if pd.isna(x):
        return None
    x = str(x).strip()
    if x in ("NEW", "-"):
        return None
    if "/" in x:
        x = x.split("/")[0].strip()
    try:
        return float(x)
    except ValueError:
        return None

df["rate"] = df["rate"].apply(clean_rate)

# ---------------------------------------------------------
# 4. Clean 'approx_cost(for two people)'
#    "1,200" -> 1200 (numeric)
# ---------------------------------------------------------
df["approx_cost(for two people)"] = (
    df["approx_cost(for two people)"]
    .astype(str)
    .str.replace(",", "", regex=False)
)
df["approx_cost(for two people)"] = pd.to_numeric(
    df["approx_cost(for two people)"], errors="coerce"
)

# ---------------------------------------------------------
# 5. Drop rows with no cuisines info (needed for Task 2)
#    Do this BEFORE string conversion so real NaNs are caught.
# ---------------------------------------------------------
df = df.dropna(subset=["cuisines"])

# ---------------------------------------------------------
# 6. Clean text columns (strip whitespace)
# ---------------------------------------------------------
text_cols = ["name", "location", "rest_type", "cuisines", "listed_in(city)", "listed_in(type)"]
for c in text_cols:
    df[c] = df[c].astype("string").str.strip()

# ---------------------------------------------------------
# 7. Remove exact duplicate rows (common in this dataset -
#    same restaurant scraped multiple times identically)
# ---------------------------------------------------------
before = len(df)
df = df.drop_duplicates()
print(f"Dropped {before - len(df)} exact duplicate rows")

# ---------------------------------------------------------
# 8. Save cleaned dataset
# ---------------------------------------------------------
df.to_csv("zomato_cleaned.csv", index=False)

print("\nCleaned shape:", df.shape)
print("\nColumns:", list(df.columns))
print("\nMissing values after cleaning:")
print(df.isnull().sum()[df.isnull().sum() > 0])
print("\nRate range:", df["rate"].min(), "-", df["rate"].max())
print("Votes range:", df["votes"].min(), "-", df["votes"].max())
