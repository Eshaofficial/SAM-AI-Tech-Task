# Zomato Restaurant Data Analysis

A data analysis project completed as part of the **Data Analyst Internship** at **SAM AI Technologies**. This project explores the Zomato Bangalore Restaurants dataset to uncover insights around cuisine trends, restaurant chains, and customer engagement.

## 📌 Project Overview

This project covers 3 of the internship's task list, using a single cleaned dataset:

| Task | Focus |
|------|-------|
| Task 2 | **Cuisine Combination** — most common cuisine pairings, and whether certain combinations correlate with higher ratings |
| Task 4 | **Restaurant Chains** — identifying chains in the dataset and comparing their ratings/popularity to standalone restaurants |
| Task 5 | **Votes Analysis** — highest/lowest voted restaurants, and the correlation between votes and rating |

## 🗂️ Dataset

- **Source:** [Zomato Bangalore Restaurants dataset](https://www.kaggle.com/datasets/himanshupoddar/zomato-bangalore-restaurants) (Kaggle)
- **Size:** ~51,700 restaurant listings across Bangalore
- **Key columns used:** `name`, `cuisines`, `rate`, `votes`, `location`, `approx_cost(for two people)`

## 🛠️ Tools Used

- **Python** — pandas, matplotlib, seaborn
- **Jupyter Notebook** for analysis and reporting
- **Streamlit + Plotly** for the bonus interactive dashboard
- **SQL (SQLite)** for the bonus query-based analysis

## 📊 Bonus: Live Interactive Dashboard

In addition to the notebook analysis, I built a live, filterable dashboard using Streamlit + Plotly — letting users explore the data interactively by location, restaurant type, online ordering, and rating range. All 3 tasks (Cuisine Combination, Restaurant Chains, Votes Analysis) are represented as interactive charts that update in real time based on the selected filters, plus 6 live KPI cards summarizing the filtered dataset.

**🔗 Live app:** [your-streamlit-link-here](https://your-app-name.streamlit.app)

**Run it locally:**
```bash
pip install streamlit plotly pandas
streamlit run app.py
```

## 🗃️ Bonus: SQL Analysis

To complement the Python/pandas workflow, I also implemented all 3 tasks as SQL queries against a SQLite database — the same dataset, the same questions, answered a different way. This includes cuisine combination counts, chain detection via `GROUP BY ... HAVING COUNT(*) > 1`, chain vs. standalone comparisons using a CTE, and votes analysis with bucketed aggregations.

**Run it locally:**
```bash
python 06_build_sqlite_db.py            # builds zomato.db from the cleaned CSV
sqlite3 zomato.db < zomato_sql_analysis.sql
```
(Or open `zomato.db` in a free GUI tool like **DB Browser for SQLite** and run each query block interactively.)

> **Note:** SQL's string-based `GROUP BY` treats `"North Indian, Chinese"` and `"Chinese, North Indian"` as different values, unlike the pandas version which normalizes cuisine order — so cuisine-combo counts are slightly more granular in the SQL results. This is documented as a comment directly in the `.sql` file.

## 📁 Repository Structure

```
├── app.py                            # Bonus: interactive Streamlit dashboard
├── requirements.txt                  # Dependencies for the Streamlit dashboard
├── 06_build_sqlite_db.py             # Bonus: builds zomato.db for SQL analysis
├── zomato_sql_analysis.sql           # Bonus: Tasks 2, 4, 5 as SQL queries
├── zomato_analysis.ipynb             # Main notebook — all 3 tasks with code, charts, and findings
├── zomato_cleaned.csv                # Cleaned dataset used across all tasks
├── task2_cuisine_combination.png     # Chart: top cuisine combos + highest rated combos
├── task2_num_cuisines_vs_rating.png
├── task4_restaurant_chains.png       # Chart: top chains + chain vs standalone comparison
├── task4_top_rated_chains.png
├── task5_votes_analysis.png          # Chart: votes vs rating scatter + bucketed averages
└── README.md
```

## 🔍 Key Insights

**Cuisine Combination**
- North Indian, North Indian + Chinese, and South Indian are the most common cuisine offerings.
- Restaurants offering more cuisine types tend to have higher average ratings (3.62 for 1 cuisine → 4.05 for 7 cuisines).
- Top-rated cuisine combinations are mostly multi-cuisine fusion restaurants (Cafe/Continental/Japanese/Thai, BBQ/European/Mediterranean).

**Restaurant Chains**
- 87.7% of unique restaurant names in the dataset are chains (2+ outlets), covering 97.9% of all listings.
- Chains outperform standalone restaurants: 3.70 vs 3.53 average rating, and ~355 vs ~85 average votes.
- Top chains by outlet count: Cafe Coffee Day, Onesta, Just Bake.

**Votes Analysis**
- Most-voted restaurants are pub/brewery-style venues (Byg Brewski Brewing Company, Toit, Truffles).
- Moderate positive correlation between votes and rating (r = 0.43), rising to r = 0.64 using log(votes).
- Average rating climbs steadily from 3.31 (0–10 votes) to 4.52 (5000+ votes).

## ▶️ How to Run

**Notebook analysis:**
1. Clone this repo
2. Install dependencies: `pip install pandas matplotlib seaborn notebook`
3. Launch Jupyter: `jupyter notebook`
4. Open `zomato_analysis.ipynb` and run all cells

**Interactive dashboard:**
1. Install dependencies: `pip install streamlit plotly pandas`
2. Run: `streamlit run app.py`
3. Opens automatically at `http://localhost:8501`

**SQL analysis:**
1. Run: `python 06_build_sqlite_db.py` to build `zomato.db`
2. Run the queries: `sqlite3 zomato.db < zomato_sql_analysis.sql`, or open `zomato.db` in DB Browser for SQLite

## 🎓 About

This project was completed as part of the Data Analyst Internship Program at **SAM AI Technologies**.

---
*Feel free to explore, fork, or reach out with feedback!*
