-- ============================================================
-- ZOMATO RESTAURANT ANALYSIS — SQL VERSION
-- ============================================================
-- Bonus SQL implementation of Tasks 2, 4, and 5 (same analysis
-- as the Python/pandas notebook, expressed as SQL queries).
--
-- Database: zomato.db (SQLite)
-- Table:    restaurants
--
-- To run:
--   1. python 06_build_sqlite_db.py     (creates zomato.db)
--   2. sqlite3 zomato.db < zomato_sql_analysis.sql
--   (or open zomato.db in DB Browser for SQLite / any SQL client
--    and run each query block individually)
-- ============================================================


-- ============================================================
-- TASK 2: CUISINE COMBINATION
-- ============================================================

-- 2a. Most common cuisine combinations
-- Note: unlike the pandas version, this does NOT normalize
-- "A, B" and "B, A" as the same combo (SQL string grouping is
-- literal) — so counts here are slightly more granular than
-- the Python notebook's normalized version.
SELECT
    cuisines,
    COUNT(*) AS num_restaurants
FROM restaurants
WHERE cuisines IS NOT NULL
GROUP BY cuisines
ORDER BY num_restaurants DESC
LIMIT 10;

-- 2b. Highest-rated cuisine combinations (min 10 restaurants,
-- to avoid single-restaurant combos skewing the top of the list)
SELECT
    cuisines,
    ROUND(AVG(rate), 2) AS avg_rating,
    COUNT(*) AS num_restaurants
FROM restaurants
WHERE rate IS NOT NULL
GROUP BY cuisines
HAVING COUNT(*) >= 10
ORDER BY avg_rating DESC
LIMIT 10;


-- ============================================================
-- TASK 4: RESTAURANT CHAINS
-- ============================================================

-- 4a. Top chains by number of outlets
-- (a "chain" = a restaurant name appearing 2+ times, i.e. at
-- multiple outlets/locations in the dataset)
SELECT
    name,
    COUNT(*) AS num_outlets
FROM restaurants
GROUP BY name
HAVING COUNT(*) > 1
ORDER BY num_outlets DESC
LIMIT 10;

-- 4b. Chain vs standalone — average rating & votes comparison
WITH chain_flag AS (
    SELECT
        *,
        CASE
            WHEN name IN (
                SELECT name FROM restaurants
                GROUP BY name
                HAVING COUNT(*) > 1
            ) THEN 'Chain'
            ELSE 'Standalone'
        END AS restaurant_type
    FROM restaurants
)
SELECT
    restaurant_type,
    ROUND(AVG(rate), 2)  AS avg_rating,
    ROUND(AVG(votes), 1) AS avg_votes,
    COUNT(*)             AS count
FROM chain_flag
WHERE rate IS NOT NULL
GROUP BY restaurant_type;

-- 4c. Best-rated chains (min 10 outlets, so the ranking reflects
-- an established chain rather than a lucky small sample)
SELECT
    name,
    ROUND(AVG(rate), 2) AS avg_rating,
    COUNT(*) AS num_outlets
FROM restaurants
WHERE rate IS NOT NULL
GROUP BY name
HAVING COUNT(*) >= 10
ORDER BY avg_rating DESC
LIMIT 10;


-- ============================================================
-- TASK 5: VOTES ANALYSIS
-- ============================================================

-- 5a. Top 10 restaurants by number of votes
SELECT
    name,
    location,
    votes,
    rate
FROM restaurants
ORDER BY votes DESC
LIMIT 10;

-- 5b. Bottom 10 restaurants by number of votes (excluding
-- zero-vote listings, since those are unreviewed, not "lowest")
SELECT
    name,
    location,
    votes,
    rate
FROM restaurants
WHERE votes > 0
ORDER BY votes ASC
LIMIT 10;

-- 5c. Average rating by vote-count bucket
-- (shows the relationship between popularity/votes and rating —
-- SQL doesn't compute a Pearson correlation coefficient natively,
-- so this bucketed view is the SQL-native way to see the trend;
-- see the Python notebook for the exact r = 0.43 / r = 0.64 values)
SELECT
    CASE
        WHEN votes BETWEEN 0 AND 10        THEN '0-10'
        WHEN votes BETWEEN 11 AND 50       THEN '11-50'
        WHEN votes BETWEEN 51 AND 100      THEN '51-100'
        WHEN votes BETWEEN 101 AND 500     THEN '101-500'
        WHEN votes BETWEEN 501 AND 1000    THEN '501-1000'
        WHEN votes BETWEEN 1001 AND 5000   THEN '1001-5000'
        ELSE '5000+'
    END AS vote_bucket,
    ROUND(AVG(rate), 2) AS avg_rating,
    COUNT(*) AS count
FROM restaurants
WHERE rate IS NOT NULL AND votes > 0
GROUP BY vote_bucket
ORDER BY MIN(votes);
