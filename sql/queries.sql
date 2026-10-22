-- Business queries for the Olist e-commerce analytics project.
-- Designed for MySQL 8 using vw_master_sales and the Olist dataset.
-- Validate query results against the loaded dataset before publishing numerical claims.
USE olist_ecommerce;

-- Q1. Headline KPIs (view only) ---------------------------------------------------------------
SELECT
    ROUND(SUM(product_price), 2)                          AS product_revenue,
    ROUND(SUM(delivery_cost), 2)                          AS freight,
    ROUND(SUM(product_price + delivery_cost), 2)          AS total_sales_incl_freight,
    COUNT(DISTINCT order_id)                              AS order_count,
    ROUND(SUM(product_price + delivery_cost) / COUNT(DISTINCT order_id), 2) AS aov_incl_freight,
    ROUND(SUM(product_price) / COUNT(DISTINCT order_id), 2)                 AS aov_product_only
FROM vw_master_sales;

-- Q2. Grain check: item rows vs distinct orders (rows > orders is expected) --------------------
SELECT COUNT(*) AS item_rows, COUNT(DISTINCT order_id) AS distinct_orders
FROM vw_master_sales;

-- Q3. Monthly trend: orders, total sales, AOV --------------------------------------------------
SELECT
    DATE_FORMAT(purchase_date, '%Y-%m')                   AS purchase_month,
    COUNT(DISTINCT order_id)                              AS order_count,
    ROUND(SUM(product_price + delivery_cost), 2)          AS total_sales_incl_freight,
    ROUND(SUM(product_price + delivery_cost) / COUNT(DISTINCT order_id), 2) AS aov_incl_freight
FROM vw_master_sales
GROUP BY DATE_FORMAT(purchase_date, '%Y-%m')
ORDER BY purchase_month;

-- Q4. Top 10 categories by product revenue. An order with items from two categories counts once
--     in each, so category order counts do not sum to the overall order count. -----------------
SELECT
    product_category,
    ROUND(SUM(product_price), 2)                          AS product_revenue,
    COUNT(DISTINCT order_id)                              AS orders_containing_category
FROM vw_master_sales
GROUP BY product_category
ORDER BY product_revenue DESC
LIMIT 10;

-- Q5. Sales and AOV by customer state -----------------------------------------------------------
SELECT
    customer_state,
    COUNT(DISTINCT order_id)                              AS order_count,
    ROUND(SUM(product_price + delivery_cost), 2)          AS total_sales_incl_freight,
    ROUND(SUM(product_price + delivery_cost) / COUNT(DISTINCT order_id), 2) AS aov_incl_freight
FROM vw_master_sales
GROUP BY customer_state
ORDER BY total_sales_incl_freight DESC;

-- Q6. Repeat-customer rate: share of customers (customer_unique_id) with 2+ distinct orders ------
SELECT
    COUNT(*)                                              AS customers,
    SUM(order_count >= 2)                                 AS repeat_customers,
    ROUND(100 * SUM(order_count >= 2) / COUNT(*), 2)      AS repeat_customer_pct
FROM (
    SELECT customer_unique_id, COUNT(DISTINCT order_id) AS order_count
    FROM vw_master_sales
    GROUP BY customer_unique_id
) per_customer;

-- Q7. Delivery performance (delivered orders). Uses the orders table because the view does not
--     carry delivery dates. Timestamps are text, so CAST first. -------------------------------
SELECT
    COUNT(*)                                                                         AS delivered_orders,
    ROUND(AVG(DATEDIFF(CAST(order_delivered_customer_date AS DATETIME),
                       CAST(order_purchase_timestamp AS DATETIME))), 1)              AS avg_days_to_deliver,
    ROUND(100 * AVG(CAST(order_delivered_customer_date AS DATETIME)
                    > CAST(order_estimated_delivery_date AS DATETIME)), 2)           AS pct_late_vs_estimate
FROM orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL;

-- Q8. Segment summary (requires the notebook to have written the customer_segments table) --------
SELECT
    s.Customer_Segment,
    COUNT(*)                                              AS customers,
    ROUND(SUM(s.Monetary), 2)                             AS total_sales_incl_freight,
    ROUND(AVG(s.Frequency), 2)                            AS avg_orders_per_customer
FROM customer_segments s
GROUP BY s.Customer_Segment
ORDER BY total_sales_incl_freight DESC;
