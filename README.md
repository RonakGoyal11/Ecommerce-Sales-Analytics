# Olist E-Commerce Sales & Customer Analytics

An end-to-end business analytics project exploring e-commerce sales performance, customer purchasing behavior, product categories, and customer segmentation using **MySQL, Python, and Power BI**.

## Project Overview

E-commerce businesses need reliable reporting to understand revenue performance, identify valuable customer groups, and evaluate purchasing and delivery patterns.

This project uses the public Brazilian e-commerce dataset published by Olist to build an analytics workflow that combines relational data preparation, SQL-based business analysis, Python-powered RFM segmentation, and interactive dashboard reporting.

The objective is to turn raw transactional data into structured metrics and business insights that support data-driven decision-making.

## Business Questions

The analysis is designed to investigate the following questions:

- How do sales and order volumes change over time?
- Which product categories contribute the most product revenue?
- How does sales performance vary across customer states?
- What proportion of customers place repeat orders?
- How can customers be segmented by purchasing behavior?
- How long do delivered orders take, and how often do they arrive later than estimated?
- Which customer segments contribute the most sales?

## Technology Stack

| Technology | Application |
|---|---|
| MySQL 8 | Relational data storage, joins, views, and business queries |
| SQL | Aggregations, date-based analysis, KPI calculations, and customer analysis |
| Python | Data preparation, data-quality checks, and RFM segmentation |
| pandas & NumPy | Data manipulation and numerical calculations |
| Jupyter Notebook | Exploratory analysis and workflow execution |
| Power BI | Interactive KPI reporting and visual analysis |
| pytest | Automated testing of Python functionality |

## Project Workflow

1. **Data preparation:** Load the Olist CSV datasets and prepare the tables for analysis.
2. **Data modeling:** Join orders, customers, order items, products, and category translations to create a sales-analysis view.
3. **SQL analysis:** Calculate sales metrics and investigate category performance, customer behavior, geographic differences, and delivery performance.
4. **Customer segmentation:** Apply Recency, Frequency, and Monetary (RFM) analysis to classify customers based on purchasing behavior.
5. **Dashboard reporting:** Use Power BI to explore sales KPIs, category performance, customer segments, and sales trends.
6. **Testing:** Run automated tests for the Python RFM and data-quality functionality.

## Key Analytical Components

### 1. SQL Sales Analysis

The `vw_master_sales` view is designed at the **order-item level**, with one row per `order_id` and `order_item_id`, restricted to delivered orders.

The SQL analysis covers:

- Overall sales and order KPIs
- Monthly sales trends
- Top product categories by product revenue
- Sales performance by customer state
- Repeat-customer rate
- Delivery performance against estimated dates
- Customer-segment summaries

The business queries are available in [`sql/queries.sql`](sql/queries.sql).

### 2. Python RFM Customer Segmentation

The Python pipeline calculates three customer-level metrics:

- **Recency:** Days since the customer's most recent purchase, relative to the reference date.
- **Frequency:** Number of distinct orders placed by the customer.
- **Monetary:** Sum of product prices and associated freight across the customer's order items.

These metrics are used to assign customers to six segments:

- Champions
- Loyal Customers
- Potential Loyalists
- New Customers
- At Risk
- Lost / One-Time

The segmentation provides a structured way to compare customer purchasing behavior and identify groups that merit further investigation.

Implementation: [`python/rfm.py`](python/rfm.py)

### 3. Power BI Dashboard

The report provides a visual overview of e-commerce performance, including:

- Revenue and order KPIs
- Revenue by product category
- Revenue distribution across customer segments
- Revenue trends over time
- State-based filtering

The Power BI report and available preview assets are included in the repository.

## Metric Definitions

To maintain consistency across the SQL analysis and reporting, the project uses the following definitions.

| Metric | Definition |
|---|---|
| Product revenue | Sum of item product prices |
| Freight | Sum of item freight charges |
| Total sales including freight | Product revenue plus freight |
| Order count | Number of distinct delivered orders |
| Average order value (including freight) | Total sales including freight divided by distinct delivered orders |
| Product-only average order value | Product revenue divided by distinct delivered orders |
| Repeat-customer rate | Percentage of customers with at least two distinct delivered orders in the analyzed data |

**Important:** The sales view contains order-item rows, not order-level rows. Order counts must use distinct `order_id` values to avoid counting multi-item orders multiple times.

These metrics describe the analyzed dataset and should not be interpreted as audited financial results for Olist.

## Dataset & Attribution

This project uses the public **Brazilian E-Commerce Public Dataset by Olist**, distributed through Kaggle.

The dataset contains historical e-commerce transactions and related information, including orders, customers, order items, products, and product-category translations.

- Dataset publisher: Olist
- Dataset source: [Brazilian E-Commerce Public Dataset by Olist — Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

The dataset is not included in this repository. Obtain it from the original source and review its applicable terms before use or redistribution.

This is an independent portfolio project and is not affiliated with or endorsed by Olist.

## Getting Started

### Prerequisites

Install the following:

- Python 3.10 or later
- MySQL 8
- Git
- Power BI Desktop, if you want to explore the dashboard

### 1. Clone the repository

```bash
git clone https://github.com/RonakGoyal11/Ecommerce-Sales-Analytics.git
cd Ecommerce-Sales-Analytics
```

If your working branch or repository URL differs, use the appropriate URL for your repository.

### 2. Install Python dependencies

```bash
python -m venv .venv
```

Activate the environment in Windows CMD:

```cmd
.venv\Scripts\activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

### 3. Download and prepare the dataset

Download the Olist dataset from the source linked above and extract the required CSV files into `data/raw/`.

Keep the original dataset files out of Git commits.

### 4. Configure database credentials

Copy `.env.example` to `.env` and update the local MySQL settings.

Example configuration:

```dotenv
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=olist_ecommerce
OLIST_DATA_DIR=data/raw
```

Use your own local credentials. Never commit `.env` or publish database passwords.

### 5. Prepare the database

Create the database and load the required source tables using the project's database setup and notebook workflow.

The relevant SQL files are:

- [`sql/db_create.sql`](sql/db_create.sql)
- [`sql/fact_table.sql`](sql/fact_table.sql)
- [`sql/indexes.sql`](sql/indexes.sql)

Ensure the source tables are loaded before creating the sales view. Follow the notebook's execution order for data loading and customer-segment generation.

### 6. Run the analysis and tests

Open the notebook in Jupyter and execute the relevant data-loading, analysis, and segmentation cells.

Run the automated tests from the project root:

```bash
python -m pytest tests -q
```

### 7. Open the dashboard

Open the Power BI `.pbix` file in Power BI Desktop. If you change the dataset, database connection, or underlying calculations, refresh the report and review the displayed metrics before using the results.

## Repository Structure

```text
Ecommerce-Sales-Analytics/
├── data/
│   └── raw/                 # Local dataset; not committed
├── gif/                     # Dashboard GIF preview
├── PowerBI/                 # Power BI report and notes
├── python/
│   ├── config.py
│   ├── notebook.ipynb
│   └── rfm.py
├── sql/
│   ├── db_create.sql
│   ├── fact_table.sql
│   ├── indexes.sql
│   └── queries.sql
├── tests/
│   └── test_rfm.py
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

The exact contents may evolve as the project is finalized.

## Testing

The Python test suite has passed **20 tests** in the local development environment.

The tests cover RFM calculations and selected data-quality behaviors. Passing unit tests does not, by itself, verify every SQL query, Power BI measure, database relationship, or dashboard export.

## Limitations & Interpretation

- The analysis covers historical data, not live e-commerce transactions.
- The main sales view includes delivered orders only; results may differ from metrics calculated over all order statuses.
- Category-level order counts can overlap because a single order may contain products from multiple categories.
- RFM segments are analytical classifications based on the chosen scoring rules, not independently validated customer-value labels.
- Business recommendations should be based on reproducible query results and validated dashboard metrics.
- Dataset coverage, missing values, and source-data limitations should be considered when interpreting findings.

## License

The project code is distributed under the MIT License, subject to the rights of the respective authors and any applicable third-party licenses.

The MIT License does not automatically grant rights to the Olist dataset or third-party assets. See [`LICENSE`](LICENSE) for the project license.

---

**Author:** Ronak Goyal

**Project focus:** SQL Analytics · Python · Customer Segmentation · Business Intelligence · Power BI
