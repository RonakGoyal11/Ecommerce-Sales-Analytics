# Olist E-Commerce Sales & Customer Analytics

An end-to-end business intelligence project analyzing e-commerce sales performance, customer purchasing behavior, repeat purchases, product categories, and delivery performance using **MySQL, Python, and Power BI**.

[Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) · SQL Analytics · Customer Segmentation · Business Intelligence

## Project Overview

E-commerce businesses need reliable metrics to understand sales performance, identify customer segments, and evaluate operational efficiency.

This project transforms the public Brazilian E-Commerce dataset by Olist into an analytical workflow combining relational data modeling, SQL-based business analysis, Python-powered Recency–Frequency–Monetary (RFM) segmentation, automated testing, and Power BI reporting.

The objective is to demonstrate how transactional data can be structured into meaningful metrics that support business analysis and evidence-based decision-making.

## Business Questions

The analysis investigates the following questions:

- How do sales and order volumes change over time?
- Which product categories contribute the most product revenue?
- How does sales performance vary across customer states?
- What proportion of customers place repeat orders?
- Which customer groups exhibit different purchasing patterns?
- How long do delivered orders take to arrive, and how often are deliveries late?
- How does revenue vary across customer segments?

## Technology Stack

| Technology | Application |
|---|---|
| MySQL 8 | Relational data storage, joins, views, and indexes |
| SQL | KPI calculations, aggregations, time-series analysis, and business queries |
| Python | Data preparation, data-quality validation, and RFM segmentation |
| pandas and NumPy | Data manipulation and numerical analysis |
| Jupyter Notebook | Exploratory analysis and end-to-end workflow |
| Power BI | Interactive KPI reporting and visual analysis |
| pytest | Automated testing of analytical functions |

## Project Architecture

The project follows a structured analytics workflow:

1. **Data ingestion:** Load the Olist CSV datasets into MySQL.
2. **Data modeling:** Join orders, customers, order items, products, and category translations into a reusable sales view.
3. **Data-quality validation:** Check missing keys, invalid dates, negative values, and duplicate order-item identifiers.
4. **Business analysis:** Use SQL to investigate revenue, order volumes, category performance, repeat purchasing, geographic patterns, and delivery performance.
5. **Customer segmentation:** Calculate customer-level RFM metrics and assign rule-based segments in Python.
6. **Business intelligence:** Explore sales and customer metrics through Power BI.
7. **Testing:** Validate core Python functionality using automated tests.

## Key Analytical Components

### 1. SQL Business Analytics

The `vw_master_sales` view establishes an order-item-level analytical dataset, with one row per order item and a filter for delivered orders.

The SQL queries cover:

- Headline sales and order KPIs
- Monthly sales trends
- Product-category revenue comparisons
- Sales and average order value by customer state
- Repeat-customer rate
- Delivery time and late-delivery rate
- Customer-segment performance

**Metric integrity:** Order-item rows are not equivalent to unique orders. Order counts use distinct `order_id` values to prevent multi-item orders from being counted more than once.

Implementation:
- `sql/db_create.sql`
- `sql/fact_table.sql`
- `sql/indexes.sql`
- `sql/queries.sql`

### 2. Python RFM Customer Segmentation

The project implements customer-level RFM analysis using three metrics:

- **Recency:** Days since a customer's most recent purchase, measured relative to the analysis reference date.
- **Frequency:** Number of distinct delivered orders placed by the customer.
- **Monetary:** Sum of product prices and associated freight across analyzed order items.

The resulting metrics feed a rule-based segmentation framework with six customer groups:

| Segment | Analytical purpose |
|---|---|
| Champions | Identify customers with strong recent purchasing behavior and high RFM scores |
| Loyal Customers | Identify customers meeting the project's loyalty classification rules |
| Potential Loyalists | Highlight customers who may warrant retention or engagement analysis |
| New Customers | Identify relatively recent customers |
| At Risk | Flag customers whose purchasing behavior meets the project's risk rules |
| Lost / One-Time | Identify customers classified as inactive or having limited purchase frequency |

These categories are analytical classifications based on the project's scoring rules. They are not independently validated predictions of future customer behavior.

Implementation: `python/rfm.py`

### 3. Power BI Dashboard

The Power BI report provides a visual interface for exploring:

- Revenue and order KPIs
- Revenue by product category
- Revenue distribution across customer segments
- Revenue trends over time
- Customer-state filtering

Files are available in the `PowerBI/` directory, with dashboard preview assets in `gif/`.

Dashboard values and visuals should be refreshed and reconciled against the SQL definitions before being used in external presentations.

## Key Business Findings

The following figures are recorded in the project's analytical outputs for delivered orders. They should be interpreted within the dataset and metric definitions described below.

| Metric | Recorded result |
|---|---:|
| Order-item rows analyzed | 110,197 |
| Distinct delivered orders | 96,478 |
| Distinct customers | 93,358 |
| Product revenue | 13,221,498.11 |
| Freight charges | 2,198,275.64 |
| Sales including freight | 15,419,773.75 |
| Repeat-customer rate | 3.00% |
| Average delivery time | 12.50 days |
| Late-delivery rate | 8.11% |

**Interpretation**

- **Customer retention:** The recorded repeat-customer rate indicates an opportunity to investigate repeat purchasing and retention behavior further.
- **Delivery performance:** The recorded late-delivery rate provides a starting point for investigating delivery reliability and potential operational improvements.
- **Revenue reporting:** Product revenue and freight-inclusive sales differ materially, so reports should clearly state which measure is being presented.
- **Customer segmentation:** RFM groups provide a framework for comparing purchasing patterns and developing hypotheses for further analysis.

These findings are descriptive, not evidence of causation. Retention and delivery recommendations would require additional investigation.

**Before using these figures in a resume or interview:** Re-run the relevant SQL queries against the final database, confirm the repeat-customer and delivery-rate denominators, and reconcile the Power BI measures with the SQL definitions. The figures above are transcribed from the supplied project README; they are not independently revalidated by this document rewrite. Confirm the currency and formatting before presenting monetary values externally.

## Metric Definitions

| Metric | Definition |
|---|---|
| Product revenue | Sum of item product prices |
| Freight charges | Sum of item freight charges |
| Sales including freight | Product revenue plus freight charges |
| Order count | Number of distinct delivered orders |
| Average order value including freight | Sales including freight divided by distinct delivered orders |
| Product-only average order value | Product revenue divided by distinct delivered orders |
| Repeat-customer rate | Customers with at least two distinct delivered orders divided by the analyzed customer population |
| Average delivery time | Average time between purchase and delivery for eligible records |
| Late-delivery rate | Eligible delivered orders arriving after their estimated delivery dates divided by the eligible delivery population |

Delivery metrics exclude records missing the required timestamps. The exact eligible populations used in the SQL calculations should be checked when reconciling reported results.

## Repository Structure

```text
Ecommerce-Sales-Analytics/
├── data/
│   └── raw/                  # Local source datasets; not committed
├── gif/                      # Dashboard preview assets
├── PowerBI/
│   ├── olist ecommerce.pbix
│   └── olist ecommerce.pdf
├── python/
│   ├── config.py             # Database and dataset configuration
│   ├── notebook.ipynb        # Analysis workflow
│   └── rfm.py                # RFM logic and segmentation
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

The repository may evolve as the project is finalized.

## Getting Started

### Prerequisites

- Python 3.10 or later
- MySQL 8
- Git
- Power BI Desktop (optional, for exploring the report)

### 1. Clone the repository

```bash
git clone https://github.com/RonakGoyal11/Ecommerce-Sales-Analytics.git
cd Ecommerce-Sales-Analytics
```

### 2. Create a Python environment

```bash
python -m venv .venv
```

On Windows CMD:

```cmd
.venv\Scripts\activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

### 3. Obtain the dataset

Download the [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) and extract the required CSV files into `data/raw/`.

The dataset is not included in this repository. Keep the raw files out of Git commits and follow the dataset's applicable terms.

### 4. Configure environment variables

Copy `.env.example` to `.env` and configure your local MySQL connection.

Example:

```dotenv
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=olist_ecommerce
OLIST_DATA_DIR=data/raw
```

Use your own database credentials. Never commit `.env` or expose passwords in notebooks, screenshots, or logs.

### 5. Prepare the database

Create the project database using `sql/db_create.sql`. Load the source tables through the notebook's data-ingestion workflow, then create the sales view and run the analysis.

**Important:** The notebook's CSV-loading cell uses table replacement. Re-running it replaces the existing source tables in the configured database. Confirm the database target and back up any important data before running it.

Follow the notebook's documented execution order rather than executing cells arbitrarily.

### 6. Run the automated tests

From the repository root:

```bash
python -m pytest tests -q
```

The project test suite has previously passed **20 tests** in the local development environment. Re-run the command after making changes to confirm the current result.

### 7. Open the Power BI report

Open the `.pbix` file from `PowerBI/` in Power BI Desktop. Configure the required data connection, refresh the report where appropriate, and validate measures and visuals before relying on the displayed values.

## Testing and Validation

The automated tests cover core RFM calculations and selected data-quality behavior.

Testing is one part of the validation process. Passing unit tests does not independently verify:

- Every SQL query against the complete dataset
- All Power BI measures and relationships
- Consistency between dashboard values and SQL outputs
- Reproducibility of the complete notebook from a clean environment

## Limitations and Interpretation

- The project analyzes historical transactions rather than live e-commerce activity.
- The primary sales view includes delivered orders only; results may differ when other order statuses are included.
- Category-level order counts can overlap because a single order may contain products from multiple categories.
- RFM segments depend on the selected scoring thresholds and business rules.
- Delivery metrics depend on the availability and validity of timestamp fields.
- Results are descriptive and should not be interpreted as proof that one factor caused another.
- Dashboard exports can become stale when the underlying data or analytical logic changes.

## Dataset Attribution

**Dataset:** Brazilian E-Commerce Public Dataset by Olist
**Publisher:** Olist
**Source:** [Kaggle dataset page](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

This is an independent portfolio project and is not affiliated with or endorsed by Olist.

## License

The project code is distributed under the MIT License. See `LICENSE` for details.

The project license does not automatically grant rights to the Olist dataset or third-party assets. Their respective terms remain applicable.

## Author

**Ronak Goyal**

**Project focus:** SQL Analytics · Python · Customer Segmentation · Business Intelligence · Power BI
