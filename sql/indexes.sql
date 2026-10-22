-- OPTIONAL: speeds up vw_master_sales joins and the queries in queries.sql.
-- Run ONCE, after the notebook has loaded the CSVs (tables created by pandas have no keys and
-- use TEXT columns, hence the prefix lengths). MySQL has no "CREATE INDEX IF NOT EXISTS";
-- re-running raises "Duplicate key name", which is harmless.
USE olist_ecommerce;

CREATE INDEX idx_orders_order_id         ON orders (order_id(32));
CREATE INDEX idx_orders_customer_id      ON orders (customer_id(32));
CREATE INDEX idx_customers_customer_id   ON customers (customer_id(32));
CREATE INDEX idx_customers_unique_id     ON customers (customer_unique_id(32));
CREATE INDEX idx_order_items_order_id    ON order_items (order_id(32));
CREATE INDEX idx_order_items_product_id  ON order_items (product_id(32));
CREATE INDEX idx_products_product_id     ON products (product_id(32));
CREATE INDEX idx_translation_category    ON product_category_name_translation (product_category_name(64));
