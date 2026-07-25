-- =============================================================================
-- 02_business_queries.sql
-- 35 interview-quality SQL queries against the ecommerce_analytics schema.
-- Every query states its business purpose before the statement.
-- Compatible with MySQL 8 (CTEs and window functions require MySQL 8.0+).
-- =============================================================================

USE ecommerce_analytics;

-- =============================================================================
-- SECTION A: FOUNDATIONAL AGGREGATION (GROUP BY / HAVING)
-- =============================================================================

-- Q1. Business purpose: total revenue, profit, and order count by region --
--     the first slide of any executive review.
SELECT region,
       ROUND(SUM(sales), 2)      AS total_sales,
       ROUND(SUM(profit), 2)     AS total_profit,
       COUNT(DISTINCT order_id)  AS total_orders
FROM orders
GROUP BY region
ORDER BY total_sales DESC;

-- Q2. Business purpose: sub-categories that are net loss-makers overall --
--     candidates for re-pricing or delisting.
SELECT sub_category,
       ROUND(SUM(sales), 2)  AS total_sales,
       ROUND(SUM(profit), 2) AS total_profit
FROM orders
GROUP BY sub_category
HAVING SUM(profit) < 0
ORDER BY total_profit ASC;

-- Q3. Business purpose: customers who have placed more than 10 orders --
--     the loyal, high-frequency base worth retaining.
SELECT customer_id, customer_name,
       COUNT(DISTINCT order_id) AS order_count,
       ROUND(SUM(sales), 2)     AS lifetime_sales
FROM orders
GROUP BY customer_id, customer_name
HAVING COUNT(DISTINCT order_id) > 10
ORDER BY lifetime_sales DESC;

-- Q4. Business purpose: average discount and margin by ship mode --
--     do faster shipping tiers correlate with different discounting behavior?
SELECT ship_mode,
       ROUND(AVG(discount), 3)                    AS avg_discount,
       ROUND(SUM(profit) / SUM(sales), 3)         AS profit_margin,
       COUNT(*)                                   AS order_lines
FROM orders
GROUP BY ship_mode
ORDER BY profit_margin DESC;

-- Q5. Business purpose: states generating over $50,000 in sales --
--     the geographic core of the business.
SELECT state,
       ROUND(SUM(sales), 2) AS total_sales
FROM orders
GROUP BY state
HAVING SUM(sales) > 50000
ORDER BY total_sales DESC;

-- =============================================================================
-- SECTION B: CONDITIONAL LOGIC (CASE WHEN)
-- =============================================================================

-- Q6. Business purpose: bucket every order line into a discount tier for
--     tiered discount-vs-margin reporting.
SELECT
    CASE
        WHEN discount = 0 THEN 'No Discount'
        WHEN discount <= 0.20 THEN 'Low (0-20%)'
        WHEN discount <= 0.40 THEN 'Medium (20-40%)'
        ELSE 'High (40%+)'
    END AS discount_tier,
    ROUND(SUM(sales), 2)             AS total_sales,
    ROUND(SUM(profit), 2)            AS total_profit,
    ROUND(AVG(profit / NULLIF(sales,0)), 3) AS avg_margin
FROM orders
GROUP BY discount_tier
ORDER BY avg_margin DESC;

-- Q7. Business purpose: flag every order line as profitable or loss-making
--     for a simple binary KPI used in Power BI's KPI card.
SELECT order_id, product_name, profit,
       CASE WHEN profit > 0 THEN 'Profitable' ELSE 'Loss' END AS profit_flag
FROM orders
ORDER BY profit ASC
LIMIT 20;

-- Q8. Business purpose: classify customers into value tiers using CASE
--     on their lifetime sales (a simpler, SQL-native alternative to NTILE).
SELECT customer_id, customer_name, SUM(sales) AS lifetime_sales,
    CASE
        WHEN SUM(sales) >= 10000 THEN 'Platinum'
        WHEN SUM(sales) >= 5000  THEN 'Gold'
        WHEN SUM(sales) >= 1000  THEN 'Silver'
        ELSE 'Bronze'
    END AS value_tier
FROM orders
GROUP BY customer_id, customer_name
ORDER BY lifetime_sales DESC;

-- Q9. Business purpose: shipping speed compliance flag -- did the order ship
--     within 3 days of being placed?
SELECT order_id, order_date, ship_date,
       DATEDIFF(ship_date, order_date) AS shipping_days,
       CASE WHEN DATEDIFF(ship_date, order_date) <= 3 THEN 'Fast' ELSE 'Slow' END AS shipping_flag
FROM orders
GROUP BY order_id, order_date, ship_date;

-- =============================================================================
-- SECTION C: COMMON TABLE EXPRESSIONS (CTEs)
-- =============================================================================

-- Q10. Business purpose: identify the single best-selling product per category
--      using a CTE + window function, avoiding a correlated subquery.
WITH product_sales AS (
    SELECT category, product_name, SUM(sales) AS total_sales,
           ROW_NUMBER() OVER (PARTITION BY category ORDER BY SUM(sales) DESC) AS rn
    FROM orders
    GROUP BY category, product_name
)
SELECT category, product_name, ROUND(total_sales, 2) AS total_sales
FROM product_sales
WHERE rn = 1;

-- Q11. Business purpose: month-over-month revenue growth using a CTE to
--      pre-aggregate before computing the LAG-based growth rate.
WITH monthly AS (
    SELECT DATE_FORMAT(order_date, '%Y-%m') AS year_month,
           SUM(sales) AS total_sales
    FROM orders
    GROUP BY year_month
)
SELECT year_month, ROUND(total_sales, 2) AS total_sales,
       ROUND(total_sales - LAG(total_sales) OVER (ORDER BY year_month), 2) AS mom_change,
       ROUND(100 * (total_sales - LAG(total_sales) OVER (ORDER BY year_month))
             / LAG(total_sales) OVER (ORDER BY year_month), 2) AS mom_growth_pct
FROM monthly
ORDER BY year_month;

-- Q12. Business purpose: customers whose average order value beats the
--      company-wide average -- a CTE isolates the benchmark cleanly.
WITH company_avg AS (
    SELECT SUM(sales) / COUNT(DISTINCT order_id) AS avg_order_value FROM orders
),
customer_avg AS (
    SELECT customer_id, customer_name,
           SUM(sales) / COUNT(DISTINCT order_id) AS customer_aov
    FROM orders
    GROUP BY customer_id, customer_name
)
SELECT c.customer_id, c.customer_name, ROUND(c.customer_aov, 2) AS customer_aov,
       ROUND(a.avg_order_value, 2) AS company_avg_aov
FROM customer_avg c
CROSS JOIN company_avg a
WHERE c.customer_aov > a.avg_order_value
ORDER BY c.customer_aov DESC;

-- Q13. Business purpose: recursive-free multi-level CTE calculating category,
--      then sub-category profit share within category (part-to-whole analysis).
WITH cat_totals AS (
    SELECT category, SUM(profit) AS category_profit
    FROM orders GROUP BY category
),
subcat_totals AS (
    SELECT category, sub_category, SUM(profit) AS subcat_profit
    FROM orders GROUP BY category, sub_category
)
SELECT s.category, s.sub_category,
       ROUND(s.subcat_profit, 2) AS subcat_profit,
       ROUND(100 * s.subcat_profit / c.category_profit, 2) AS pct_of_category_profit
FROM subcat_totals s
JOIN cat_totals c ON s.category = c.category
ORDER BY s.category, pct_of_category_profit DESC;

-- =============================================================================
-- SECTION D: WINDOW FUNCTIONS, RANKING, RUNNING TOTALS, MOVING AVERAGES
-- =============================================================================

-- Q14. Business purpose: rank products within each region by total sales --
--      powers a "Top 5 products per region" Power BI slicer view.
SELECT region, product_name, ROUND(SUM(sales), 2) AS total_sales,
       RANK() OVER (PARTITION BY region ORDER BY SUM(sales) DESC) AS sales_rank
FROM orders
GROUP BY region, product_name;

-- Q15. Business purpose: dense rank of customers by lifetime profit
--      (DENSE_RANK avoids gaps when customers tie in profit).
SELECT customer_name, ROUND(SUM(profit), 2) AS lifetime_profit,
       DENSE_RANK() OVER (ORDER BY SUM(profit) DESC) AS profit_rank
FROM orders
GROUP BY customer_name;

-- Q16. Business purpose: running total of monthly revenue across the whole
--      timeline -- the cumulative-revenue line for a Power BI trend chart.
WITH monthly AS (
    SELECT DATE_FORMAT(order_date, '%Y-%m') AS year_month, SUM(sales) AS total_sales
    FROM orders GROUP BY year_month
)
SELECT year_month, ROUND(total_sales, 2) AS total_sales,
       ROUND(SUM(total_sales) OVER (ORDER BY year_month), 2) AS running_total_sales
FROM monthly
ORDER BY year_month;

-- Q17. Business purpose: 3-month moving average of sales to smooth seasonal
--      spikes for trend-line forecasting.
WITH monthly AS (
    SELECT DATE_FORMAT(order_date, '%Y-%m') AS year_month, SUM(sales) AS total_sales
    FROM orders GROUP BY year_month
)
SELECT year_month, ROUND(total_sales, 2) AS total_sales,
       ROUND(AVG(total_sales) OVER (ORDER BY year_month
             ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS moving_avg_3mo
FROM monthly
ORDER BY year_month;

-- Q18. Business purpose: percentile bucket (NTILE quartile) of customers by
--      spend, powering the Bronze/Silver/Gold/Platinum tiering used in Power BI.
SELECT customer_id, customer_name, ROUND(SUM(sales), 2) AS total_sales,
       NTILE(4) OVER (ORDER BY SUM(sales)) AS spend_quartile
FROM orders
GROUP BY customer_id, customer_name;

-- Q19. Business purpose: each order line's profit compared to the previous
--      order line for the same customer (chronological), to spot volatility.
SELECT customer_id, order_date, profit,
       LAG(profit) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_order_profit,
       profit - LAG(profit) OVER (PARTITION BY customer_id ORDER BY order_date) AS profit_change
FROM orders
ORDER BY customer_id, order_date;

-- Q20. Business purpose: first and last order date per customer (recency /
--      tenure analysis) using FIRST_VALUE / LAST_VALUE window functions.
SELECT DISTINCT customer_id, customer_name,
       FIRST_VALUE(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS first_order,
       LAST_VALUE(order_date) OVER (PARTITION BY customer_id ORDER BY order_date
             ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_order
FROM orders;

-- Q21. Business purpose: cumulative % of total profit contributed as products
--      are ranked from highest to lowest profit -- classic Pareto (80/20) check.
WITH product_profit AS (
    SELECT product_name, SUM(profit) AS total_profit
    FROM orders GROUP BY product_name
),
ranked AS (
    SELECT product_name, total_profit,
           SUM(total_profit) OVER (ORDER BY total_profit DESC) AS running_profit,
           SUM(total_profit) OVER () AS grand_total_profit
    FROM product_profit
)
SELECT product_name, ROUND(total_profit, 2) AS total_profit,
       ROUND(100 * running_profit / grand_total_profit, 2) AS cumulative_pct_of_profit
FROM ranked
ORDER BY total_profit DESC;

-- =============================================================================
-- SECTION E: SUBQUERIES
-- =============================================================================

-- Q22. Business purpose: products that sell above the company-wide average
--      unit price -- a premium-tier product screen.
SELECT product_name, ROUND(SUM(sales) / SUM(quantity), 2) AS avg_unit_price
FROM orders
GROUP BY product_name
HAVING AVG(sales / quantity) > (
    SELECT AVG(sales / quantity) FROM orders
)
ORDER BY avg_unit_price DESC;

-- Q23. Business purpose: customers whose total sales exceed the average
--      customer's total sales -- an above-average-value customer list.
SELECT customer_id, customer_name, ROUND(SUM(sales), 2) AS total_sales
FROM orders
GROUP BY customer_id, customer_name
HAVING SUM(sales) > (
    SELECT AVG(customer_total) FROM (
        SELECT SUM(sales) AS customer_total FROM orders GROUP BY customer_id
    ) AS per_customer
)
ORDER BY total_sales DESC;

-- Q24. Business purpose: orders that contain at least one returned line item
--      (correlated subquery against the returns table).
SELECT DISTINCT o.order_id, o.customer_name, o.order_date
FROM orders o
WHERE EXISTS (
    SELECT 1 FROM returns r WHERE r.order_id = o.order_id
)
ORDER BY o.order_date DESC;

-- Q25. Business purpose: the single most profitable order in each region
--      (subquery in the WHERE clause to match the regional max).
SELECT region, order_id, profit
FROM (
    SELECT region, order_id, SUM(profit) AS profit
    FROM orders GROUP BY region, order_id
) t
WHERE profit = (
    SELECT MAX(profit) FROM (
        SELECT region AS r2, order_id, SUM(profit) AS profit
        FROM orders GROUP BY region, order_id
    ) t2 WHERE t2.r2 = t.region
);

-- =============================================================================
-- SECTION F: JOINS ACROSS TABLES (People / Returns integration)
-- =============================================================================

-- Q26. Business purpose: revenue and profit by regional manager -- ties
--      performance directly to the accountable owner.
SELECT rm.regional_manager, o.region,
       ROUND(SUM(o.sales), 2)  AS total_sales,
       ROUND(SUM(o.profit), 2) AS total_profit
FROM orders o
JOIN regional_managers rm ON o.region = rm.region
GROUP BY rm.regional_manager, o.region
ORDER BY total_sales DESC;

-- Q27. Business purpose: return rate by category using a LEFT JOIN against
--      the returns table (LEFT JOIN preserves non-returned lines as NULL).
SELECT o.category,
       COUNT(DISTINCT o.order_id) AS total_orders,
       COUNT(DISTINCT r.order_id) AS returned_orders,
       ROUND(100 * COUNT(DISTINCT r.order_id) / COUNT(DISTINCT o.order_id), 2) AS return_rate_pct
FROM orders o
LEFT JOIN returns r ON o.order_id = r.order_id
GROUP BY o.category
ORDER BY return_rate_pct DESC;

-- Q28. Business purpose: profit lost specifically on returned orders --
--      quantifies the true cost of returns beyond shipping.
SELECT ROUND(SUM(o.profit), 2) AS profit_on_returned_orders,
       COUNT(DISTINCT o.order_id) AS returned_order_count
FROM orders o
JOIN returns r ON o.order_id = r.order_id;

-- =============================================================================
-- SECTION G: TIME-BASED / COHORT-STYLE ANALYSIS
-- =============================================================================

-- Q29. Business purpose: year-over-year revenue growth by category --
--      the standard board-deck "YoY by line of business" table.
SELECT category, YEAR(order_date) AS order_year,
       ROUND(SUM(sales), 2) AS total_sales
FROM orders
GROUP BY category, order_year
ORDER BY category, order_year;

-- Q30. Business purpose: average shipping delay by ship mode --
--      validates whether SLA promises are being met operationally.
SELECT ship_mode,
       ROUND(AVG(DATEDIFF(ship_date, order_date)), 2) AS avg_shipping_days,
       MAX(DATEDIFF(ship_date, order_date)) AS max_shipping_days
FROM orders
GROUP BY ship_mode
ORDER BY avg_shipping_days;

-- Q31. Business purpose: quarter-over-quarter profit trend -- feeds
--      quarterly board reporting cadence.
SELECT YEAR(order_date) AS yr, QUARTER(order_date) AS qtr,
       ROUND(SUM(sales), 2)  AS total_sales,
       ROUND(SUM(profit), 2) AS total_profit
FROM orders
GROUP BY yr, qtr
ORDER BY yr, qtr;

-- Q32. Business purpose: new vs. returning customer revenue split per month
--      (a customer's first-ever order month vs. subsequent months).
WITH first_orders AS (
    SELECT customer_id, MIN(DATE_FORMAT(order_date, '%Y-%m')) AS first_month
    FROM orders GROUP BY customer_id
)
SELECT DATE_FORMAT(o.order_date, '%Y-%m') AS order_month,
       CASE WHEN DATE_FORMAT(o.order_date, '%Y-%m') = f.first_month
            THEN 'New Customer' ELSE 'Returning Customer' END AS customer_type,
       ROUND(SUM(o.sales), 2) AS total_sales
FROM orders o
JOIN first_orders f ON o.customer_id = f.customer_id
GROUP BY order_month, customer_type
ORDER BY order_month, customer_type;

-- =============================================================================
-- SECTION H: VIEWS (reusable analytical objects for Power BI / BI tools)
-- =============================================================================

-- Q33. Business purpose: a reusable view exposing executive KPIs so Power BI
--      (or any BI tool) can connect directly without re-writing aggregation logic.
CREATE OR REPLACE VIEW vw_executive_kpis AS
SELECT
    ROUND(SUM(sales), 2)                          AS total_revenue,
    ROUND(SUM(profit), 2)                         AS total_profit,
    ROUND(SUM(profit) / SUM(sales), 4)            AS overall_profit_margin,
    COUNT(DISTINCT order_id)                      AS total_orders,
    COUNT(DISTINCT customer_id)                   AS total_customers,
    ROUND(SUM(sales) / COUNT(DISTINCT order_id), 2) AS avg_order_value
FROM orders;

-- Q34. Business purpose: a reusable "customer 360" view combining lifetime
--      value, recency, and return behavior for CRM / retention tooling.
CREATE OR REPLACE VIEW vw_customer_360 AS
SELECT o.customer_id, o.customer_name, o.segment,
       COUNT(DISTINCT o.order_id)               AS total_orders,
       ROUND(SUM(o.sales), 2)                   AS total_sales,
       ROUND(SUM(o.profit), 2)                  AS total_profit,
       MAX(o.order_date)                        AS last_order_date,
       DATEDIFF(CURDATE(), MAX(o.order_date))   AS days_since_last_order,
       COUNT(DISTINCT r.order_id)               AS returned_orders
FROM orders o
LEFT JOIN returns r ON o.order_id = r.order_id
GROUP BY o.customer_id, o.customer_name, o.segment;

-- Q35. Business purpose: a reusable monthly performance view -- the single
--      source of truth for every "trend over time" chart in Power BI.
CREATE OR REPLACE VIEW vw_monthly_performance AS
SELECT DATE_FORMAT(order_date, '%Y-%m') AS year_month,
       ROUND(SUM(sales), 2)  AS total_sales,
       ROUND(SUM(profit), 2) AS total_profit,
       COUNT(DISTINCT order_id) AS total_orders,
       ROUND(SUM(sales) / COUNT(DISTINCT order_id), 2) AS avg_order_value
FROM orders
GROUP BY year_month;

-- =============================================================================
-- SECTION I: INDEXES (query performance)
-- =============================================================================

-- Q36. Business purpose: speed up the very common "filter by region + date
--      range" query pattern used in nearly every regional dashboard filter.
CREATE INDEX idx_region_orderdate ON orders (region, order_date);

-- Q37. Business purpose: speed up customer-level lookups (used by every
--      customer-360 / CRM query joining on customer_id).
CREATE INDEX idx_customer_lookup ON orders (customer_id, order_date);

-- Q38. Business purpose: speed up product-level profitability lookups,
--      the most frequent filter in the product performance dashboard page.
CREATE INDEX idx_product_category ON orders (product_id, category, sub_category);

-- =============================================================================
-- SECTION J: EXPLAIN / QUERY TUNING EXAMPLE
-- =============================================================================

-- Q39. Business purpose: verify the optimizer is using idx_region_orderdate
--      rather than a full table scan for the most common dashboard filter.
EXPLAIN
SELECT region, SUM(sales)
FROM orders
WHERE region = 'West' AND order_date BETWEEN '2020-01-01' AND '2020-12-31'
GROUP BY region;

-- Q40. Business purpose: full "Top N per group" report -- top 3 sub-categories
--      by profit within every category, a common ask in leadership reviews.
WITH ranked_subcat AS (
    SELECT category, sub_category, SUM(profit) AS total_profit,
           RANK() OVER (PARTITION BY category ORDER BY SUM(profit) DESC) AS rnk
    FROM orders
    GROUP BY category, sub_category
)
SELECT category, sub_category, ROUND(total_profit, 2) AS total_profit
FROM ranked_subcat
WHERE rnk <= 3
ORDER BY category, rnk;
