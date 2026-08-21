"""
SQL SETUP: Load cleaned Zomato data into a SQLite database
--------------------------------------------------
Run this once to create zomato.db from zomato_cleaned.csv.
The .sql file (zomato_sql_analysis.sql) can then be run against
this database using any SQLite client, or via sqlite3 CLI:

    sqlite3 zomato.db < zomato_sql_analysis.sql
"""

import pandas as pd
import sqlite3

df = pd.read_csv("zomato_cleaned.csv")

conn = sqlite3.connect("zomato.db")
df.to_sql("restaurants", conn, if_exists="replace", index=False)

# Index commonly filtered/grouped columns for faster queries
conn.execute("CREATE INDEX IF NOT EXISTS idx_name ON restaurants(name);")
conn.execute("CREATE INDEX IF NOT EXISTS idx_cuisines ON restaurants(cuisines);")
conn.execute("CREATE INDEX IF NOT EXISTS idx_rate ON restaurants(rate);")
conn.execute("CREATE INDEX IF NOT EXISTS idx_votes ON restaurants(votes);")
conn.commit()

print(f"✅ Loaded {len(df):,} rows into zomato.db (table: restaurants)")
conn.close()
