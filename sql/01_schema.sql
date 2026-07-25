-- =============================================================================
-- 01_schema.sql
-- E-Commerce Sales & Customer Analytics -- MySQL 8 Schema
-- Mirrors data/processed/superstore_cleaned.csv (Orders + People + Returns merged)
-- =============================================================================

DROP DATABASE IF EXISTS ecommerce_analytics;
CREATE DATABASE ecommerce_analytics CHARACTER SET utf8mb4;
USE ecommerce_analytics;

-- -----------------------------------------------------------------------------
-- Core fact table: one row per order line item
-- -----------------------------------------------------------------------------
CREATE TABLE orders (
    row_id              INT PRIMARY KEY,
    order_id            VARCHAR(20)  NOT NULL,
    order_date          DATE         NOT NULL,
    ship_date           DATE         NOT NULL,
    ship_mode           VARCHAR(20)  NOT NULL,
    customer_id         VARCHAR(20)  NOT NULL,
    customer_name       VARCHAR(100) NOT NULL,
    segment             VARCHAR(20)  NOT NULL,
    country             VARCHAR(50)  NOT NULL,
    city                VARCHAR(50)  NOT NULL,
    state               VARCHAR(50)  NOT NULL,
    postal_code         VARCHAR(10),
    region              VARCHAR(20)  NOT NULL,
    product_id          VARCHAR(20)  NOT NULL,
    category             VARCHAR(30)  NOT NULL,
    sub_category         VARCHAR(30)  NOT NULL,
    product_name        VARCHAR(255) NOT NULL,
    sales               DECIMAL(12, 4) NOT NULL,
    quantity            INT          NOT NULL,
    discount            DECIMAL(5, 2)  NOT NULL,
    profit              DECIMAL(12, 4) NOT NULL,
    returned            VARCHAR(3)   DEFAULT 'No',
    INDEX idx_order_id (order_id),
    INDEX idx_customer_id (customer_id),
    INDEX idx_product_id (product_id),
    INDEX idx_order_date (order_date),
    INDEX idx_region_category (region, category)
);

-- -----------------------------------------------------------------------------
-- Reference table: Regional Manager per Region
-- -----------------------------------------------------------------------------
CREATE TABLE regional_managers (
    region             VARCHAR(20) PRIMARY KEY,
    regional_manager   VARCHAR(100) NOT NULL
);

-- -----------------------------------------------------------------------------
-- Reference table: Returned orders (one row per returned Order ID)
-- -----------------------------------------------------------------------------
CREATE TABLE returns (
    order_id   VARCHAR(20) PRIMARY KEY,
    returned   VARCHAR(3) NOT NULL DEFAULT 'Yes'
);

-- -----------------------------------------------------------------------------
-- Load data (adjust path for your local MySQL secure_file_priv directory)
--
-- NOTE: data/processed/superstore_cleaned.csv is the fully feature-engineered
-- export (35 columns -- it includes derived columns like profit_margin and
-- discount_tier used by the Python/Power BI layers). The `orders` table above
-- only models the 22 base transactional columns, so the LOAD statement below
-- maps the extra engineered columns to @dummy placeholders and discards them --
-- MySQL recomputes anything it needs (margins, tiers, etc.) directly in SQL.
-- -----------------------------------------------------------------------------
-- LOAD DATA INFILE '/path/to/data/processed/superstore_cleaned.csv'
-- INTO TABLE orders
-- FIELDS TERMINATED BY ',' ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS
-- (row_id, order_id, order_date, ship_date, ship_mode, customer_id, customer_name,
--  segment, country, city, state, postal_code, region, product_id, category,
--  sub_category, product_name, sales, quantity, discount, profit, @regional_manager,
--  returned, @is_returned, @order_year, @order_month, @order_month_name,
--  @order_year_month, @order_quarter, @order_weekday, @shipping_delay_days,
--  @profit_margin, @is_loss_making, @is_high_discount, @discount_tier);
--
-- Load the People sheet's regional-manager mapping (verified against the
-- actual uploaded workbook's People sheet):
-- INSERT INTO regional_managers (region, regional_manager) VALUES
--   ('West', 'Sadie Pawthorne'), ('East', 'Chuck Magee'),
--   ('Central', 'Roxanne Rodriguez'), ('South', 'Fred Suzuki');
