-- vw_master_sales
-- ---------------------------------------------------------------------------
-- GRAIN: ONE ROW PER ORDER ITEM (order_id + order_item_id), delivered orders only.
--   * An order with 3 items appears as 3 rows. Row count is NOT order count.
--   * order_id, purchase_date and customer_* repeat on every item row of an order.
--   * Count orders with COUNT(DISTINCT order_id); never COUNT(*).
--
-- METRIC DEFINITIONS (used consistently in queries.sql, the notebook and the README):
--   Product revenue          = SUM(product_price)
--   Freight                  = SUM(delivery_cost)
--   Total sales (incl. freight) = SUM(product_price + delivery_cost) = SUM(item_total_value)
--   Order count              = COUNT(DISTINCT order_id)
--   AOV                      = Total sales (incl. freight) / Order count
--
-- Source tables are loaded by the notebook from the Olist CSVs
-- (orders, customers, order_items, products, product_category_name_translation).
-- Timestamps are loaded as text by pandas; DATE() converts the 'YYYY-MM-DD HH:MM:SS' strings.
-- Categories with no English translation fall back to the Portuguese name; products with no
-- category become 'Unknown'.
CREATE OR REPLACE VIEW vw_master_sales AS
SELECT
    o.order_id,
    oi.order_item_id,
    c.customer_unique_id,
    c.customer_city,
    c.customer_state,
    DATE(o.order_purchase_timestamp) AS purchase_date,
    oi.product_id,
    oi.price AS product_price,
    oi.freight_value AS delivery_cost,
    COALESCE(t.product_category_name_english, p.product_category_name, 'Unknown') AS product_category,
    oi.price + oi.freight_value AS item_total_value
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
LEFT JOIN products p
    ON oi.product_id = p.product_id
LEFT JOIN product_category_name_translation t
    ON p.product_category_name = t.product_category_name
WHERE o.order_status = 'delivered';
