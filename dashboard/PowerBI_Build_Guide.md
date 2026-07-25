# Power BI Executive Dashboard — Build Guide

> **Note on scope:** Power BI Desktop (`.pbix`) is a Windows GUI application and
> cannot be produced by a headless script. This guide gives you the exact data
> model, every DAX measure, and the page-by-page layout so the dashboard can be
> assembled in Power BI Desktop in under an hour. Everything here is
> copy-paste ready.

## 1. Data Source

Import the following files from `data/processed/` using **Get Data → Text/CSV**:

| File | Role in the model |
|---|---|
| `superstore_cleaned.csv` | Fact table (`Orders`) |
| `customer_summary.csv` | Customer dimension / pre-aggregated features |
| `product_summary.csv` | Product dimension / pre-aggregated features |
| `monthly_trend.csv` | Optional — pre-aggregated trend (can also be built live with DAX) |

Also create a **Date table** (Model view → New Table):

```
DateTable =
CALENDAR ( DATE(2018,1,1), DATE(2021,12,31) )
```
Mark it as a Date Table (Table tools → Mark as Date Table) using `[Date]`.

## 2. Relationships (Model view)

- `Orders[order_date]` → `DateTable[Date]` (Many-to-One)
- `Orders[customer_id]` → `customer_summary[customer_id]` (Many-to-One)
- `Orders[product_id]` → `product_summary[product_id]` (Many-to-One)

## 3. DAX Measures

Create a dedicated measures table (`_Measures`) and add all of these:

```dax
Total Revenue = SUM ( Orders[sales] )

Total Profit = SUM ( Orders[profit] )

Total Orders = DISTINCTCOUNT ( Orders[order_id] )

Total Customers = DISTINCTCOUNT ( Orders[customer_id] )

Average Order Value = DIVIDE ( [Total Revenue], [Total Orders], 0 )

Profit Margin % = DIVIDE ( [Total Profit], [Total Revenue], 0 )

Average Discount % = AVERAGE ( Orders[discount] )

Return Rate % =
DIVIDE (
    DISTINCTCOUNT ( FILTER ( Orders, Orders[is_returned] = 1 )[order_id] ),
    [Total Orders],
    0
)

Loss-Making Order Lines % =
DIVIDE (
    COUNTROWS ( FILTER ( Orders, Orders[profit] <= 0 ) ),
    COUNTROWS ( Orders ),
    0
)

Prior Month Revenue =
CALCULATE ( [Total Revenue], DATEADD ( DateTable[Date], -1, MONTH ) )

MoM Revenue Growth % =
DIVIDE ( [Total Revenue] - [Prior Month Revenue], [Prior Month Revenue], 0 )

YTD Revenue = TOTALYTD ( [Total Revenue], DateTable[Date] )

YoY Revenue Growth % =
VAR PriorYear = CALCULATE ( [Total Revenue], SAMEPERIODLASTYEAR ( DateTable[Date] ) )
RETURN DIVIDE ( [Total Revenue] - PriorYear, PriorYear, 0 )

Running Total Revenue =
CALCULATE (
    [Total Revenue],
    FILTER ( ALLSELECTED ( DateTable[Date] ), DateTable[Date] <= MAX ( DateTable[Date] ) )
)

Top Customer Rank =
RANKX ( ALL ( customer_summary[customer_name] ), [Total Revenue], , DESC )

High Discount Flag =
IF ( [Average Discount %] >= 0.30, "High Discount", "Normal" )

Profit per Order = DIVIDE ( [Total Profit], [Total Orders], 0 )

Sales Contribution % =
DIVIDE ( [Total Revenue], CALCULATE ( [Total Revenue], ALL ( Orders[category] ) ), 0 )
```

## 4. Report Pages & Layout

### Page 1 — Executive Overview
- **KPI cards (top row):** Total Revenue, Total Profit, Profit Margin %, Total Orders, Average Order Value
- **Line chart:** Monthly Revenue & Profit trend (dual-axis), with MoM Revenue Growth % as a tooltip measure
- **Map (Filled Map):** Revenue by State
- **Donut chart:** Revenue by Category
- **Slicers:** Region, Segment, Year (all pinned to the left rail, synced across pages)

### Page 2 — Customer Analysis
- **Table/Matrix:** Top 10 customers by Total Revenue, Total Profit, Orders, Value Tier (Top Customer Rank measure)
- **Bar chart:** Revenue by Customer Value Tier (Bronze/Silver/Gold/Platinum)
- **Scatter chart:** Recency (days) vs. Total Sales, sized by Total Orders — visually surfaces at-risk high-value customers
- **Card:** Return Rate %

### Page 3 — Product & Category Analysis
- **Bar chart:** Top 10 products by Revenue
- **Bar chart:** Bottom 10 products by Profit (profit-destroying SKUs)
- **Treemap:** Category → Sub-Category by Revenue, colored by Profit Margin %
- **Table:** Sub-category discount vs. margin trade-off

### Page 4 — Regional & Discount Analysis
- **Bar chart:** Revenue & Profit Margin % by Region
- **Bar chart:** Profit Margin % by Discount Tier (No/Low/Medium/High)
- **Heatmap matrix:** Segment × Ship Mode → Profit Margin %
- **Card:** Loss-Making Order Lines %

## 5. Interactivity Checklist

- [ ] Cross-filtering enabled between all visuals on a page
- [ ] Slicers (Region, Segment, Category, Year) synced across all 4 pages (View → Sync Slicers)
- [ ] Drillthrough page: "Customer Detail" — right-click a customer anywhere to jump to their full order history
- [ ] Tooltips customized to show Profit Margin % alongside Revenue on every chart
- [ ] Bookmarks: "Default View" and "Loss-Making Products Only" (filtered bookmark) for quick presentation toggles

## 6. Theme

Use a custom JSON theme (Power BI → View → Themes → Browse for themes) with:
- Primary: `#2E86AB` (revenue/positive)
- Secondary: `#A23B72` (profit)
- Alert/negative: `#C73E1D`
- Neutral background: `#F5F5F5`

See `presentation/dashboard_mockup.png` for the visual target layout referenced above.
