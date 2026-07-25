# Business Insights Report

**Project:** E-Commerce Sales & Customer Analytics Dashboard
**Dataset:** Tableau Sample Superstore (Orders, People, Returns)

Each insight follows the What Happened -> Why -> Business Impact -> Recommendation framework, and every figure below is computed directly from the cleaned dataset (`data/processed/superstore_cleaned.csv`) -- nothing is fabricated or estimated.

---

### 1. Overall business is profitable but margin is thin

- **What happened:** The company generated $2,297,200.86 in revenue and $286,397.02 in profit across 5,009 orders, an overall profit margin of 12.5%.
- **Why it happened:** Margin is compressed because a meaningful share of line items are sold at a loss (19.4% of order lines), often driven by aggressive discounting.
- **Business impact:** A single-digit overall margin leaves little room to absorb rising shipping, returns, or supply costs.
- **Recommendation:** Set a minimum-margin guardrail per order line and route deep discounts through a manager approval workflow.

### 2. Central region is the weakest profit performer

- **What happened:** Central region shows the lowest profit margin among all regions at 7.9%, despite $501,239.89 in sales.
- **Why it happened:** Regional discount policy and product mix differ; certain sub-categories in this region are sold well below cost.
- **Business impact:** Underperforming regions dilute company-wide profitability and distort regional manager performance evaluation.
- **Recommendation:** Audit Central region's discount approval limits and renegotiate pricing on its worst sub-categories.

### 3. West region is the strongest profit performer

- **What happened:** West region delivers the highest profit margin at 14.9% on $725,457.82 of sales.
- **Why it happened:** Lower average discounting and a healthier product mix (more Technology and Office Supplies, less heavily-discounted Furniture) protect margin.
- **Business impact:** This region is a template for what 'healthy' unit economics look like across the network.
- **Recommendation:** Document West's discounting discipline and product-mix approach as a playbook for other regions.

### 4. Tables (Furniture) is the biggest profit drain

- **What happened:** Tables lost $17,725.48 in aggregate profit despite $206,965.53 in sales, at an average discount of 26.1%.
- **Why it happened:** High average discounting on this sub-category pushes many transactions below their cost basis.
- **Business impact:** Continuing to sell this sub-category at current discount levels actively destroys company value with every unit sold.
- **Recommendation:** Cap discounts on Tables and re-price or delist SKUs that cannot be sold profitably.

### 5. Copiers (Technology) is the strongest profit contributor

- **What happened:** Copiers generated $55,617.82 in profit, the highest of any sub-category, on $149,528.03 of sales.
- **Why it happened:** Strong unit economics come from low discount dependency and consistent demand.
- **Business impact:** This sub-category should be prioritized in marketing spend and inventory allocation.
- **Recommendation:** Increase marketing and shelf/homepage visibility for Copiers to grow an already-profitable line.

### 6. Discounts above 40% turn profitable orders into losses

- **What happened:** Orders with no discount average a 34.0% profit margin, while orders discounted 40%+ average -108.9% margin.
- **Why it happened:** Discounting is applied inconsistently across sales reps/regions without a clear floor tied to product cost.
- **Business impact:** Every high-discount order in this tier is very likely losing the company money, not just earning less.
- **Recommendation:** Introduce a hard discount ceiling (e.g. 20%) for standard orders, with anything above requiring finance sign-off.

### 7. Top product by revenue: Canon imageCLASS 2200 Advanced Copier

- **What happened:** The best-selling product generated $61,599.82 in revenue and $25,199.93 in profit.
- **Why it happened:** Strong, consistent demand and likely strong brand/price positioning versus competitors.
- **Business impact:** Stockouts on this SKU carry outsized revenue risk relative to the rest of the catalog.
- **Recommendation:** Protect inventory buffer and supplier lead-time for this SKU; consider bundling it with lower-margin items.

### 8. Worst product by profit: Cubify CubeX 3D Printer Double Head Print

- **What happened:** This single product lost $8,879.97 in aggregate profit at an average discount of 53.3%.
- **Why it happened:** Combination of high unit cost, thin base margin, and heavy discounting.
- **Business impact:** Continued sale at current terms is a direct, quantifiable drag on company profit.
- **Recommendation:** Re-negotiate supplier cost, raise the price floor, or discontinue the SKU if margin cannot be fixed.

### 9. Peak sales month: 2021-11

- **What happened:** 2021-11 was the single highest-revenue month at $118,447.82.
- **Why it happened:** Seasonal demand (back-to-school / year-end business & holiday purchasing) concentrates orders into Q4.
- **Business impact:** Inventory and staffing planned off average monthly demand will under-serve this peak.
- **Recommendation:** Build a seasonal demand plan that pre-positions inventory and staffing ahead of the Q4 peak.

### 10. Revenue is highly seasonal, not steadily growing month over month

- **What happened:** Month-over-month sales growth swings significantly across the year, including a -75.3% change in 2020-01.
- **Why it happened:** Superstore-style B2B/B2C mixed demand follows fiscal quarter-end and holiday purchasing cycles rather than smooth linear growth.
- **Business impact:** Flat annual budgeting misses the operational reality of concentrated demand spikes and troughs.
- **Recommendation:** Move to quarterly, seasonally-indexed revenue targets instead of a flat monthly run-rate assumption.

### 11. Top customer: Sean Miller

- **What happened:** Sean Miller is the single highest-value customer, contributing $25,043.05 in lifetime sales across 5 orders.
- **Why it happened:** Consistent repeat purchasing behavior over the observed period.
- **Business impact:** Losing a top-tier customer would create an outsized, immediate revenue gap.
- **Recommendation:** Assign key-account management and proactive check-ins to the top decile of customers by lifetime value.

### 12. A small share of customers drives a disproportionate share of revenue

- **What happened:** The 'Platinum' customer tier (top quartile by spend) contributes 55.0% of total revenue.
- **Why it happened:** Classic Pareto effect in B2B/B2C retail: a minority of accounts order more frequently and in higher volumes.
- **Business impact:** Revenue concentration means retention economics for top-tier customers matter more than broad-based acquisition.
- **Recommendation:** Launch a loyalty/retention program targeted specifically at Platinum-tier customers before expanding acquisition spend.

### 13. A meaningful share of the customer base is at risk of churn

- **What happened:** 25.5% of customers have not ordered in over 180 days as of the last date in the dataset.
- **Why it happened:** No systematic re-engagement or win-back process is evident from ordering cadence.
- **Business impact:** Reactivating an existing customer is materially cheaper than acquiring a new one.
- **Recommendation:** Launch an automated win-back email/discount campaign triggered at 90 days of inactivity, before the 180-day risk threshold.

### 14. Technology has the highest return rate

- **What happened:** Technology shows a 8.45% return rate, the highest of the three categories.
- **Why it happened:** Could reflect product-quality issues, inaccurate product descriptions, or sizing/fit mismatches versus expectations.
- **Business impact:** Returns carry direct reverse-logistics cost and depress realized (post-return) profit beyond what gross Sales/Profit show.
- **Recommendation:** Commission a root-cause review of Technology returns (QA, listing accuracy, packaging) before the next peak season.

### 15. Consumer segment is the largest revenue contributor

- **What happened:** The Consumer segment consistently accounts for the largest share of both orders and revenue versus Corporate and Home Office.
- **Why it happened:** Broader addressable market size and higher order frequency in the Consumer segment versus B2B-oriented segments.
- **Business impact:** Marketing and product strategy skewed toward B2B risks under-investing in the segment that drives most revenue.
- **Recommendation:** Prioritize Consumer-segment marketing spend and UX/checkout investment, while defending margin in Corporate accounts.

### 16. Furniture has the lowest average profit margin of the three categories

- **What happened:** Furniture consistently shows compressed profit margins versus Technology and Office Supplies, driven largely by high average discount rates on Tables and Bookcases.
- **Why it happened:** Bulky, high-cost items are more commonly discounted to close a sale, eroding already-thin base margins.
- **Business impact:** Furniture volume growth without a pricing fix simply scales losses, not profit.
- **Recommendation:** Introduce category-specific minimum-margin floors for Furniture, especially Tables and Bookcases.

### 17. Technology is the most profitable category per dollar of sales

- **What happened:** Technology consistently posts the strongest profit margin of the three categories, led by Copiers and Accessories.
- **Why it happened:** Lower price sensitivity and lower discount dependency in Technology purchases versus Furniture.
- **Business impact:** Technology should be treated as the margin engine of the business, not just a revenue line.
- **Recommendation:** Expand the Technology assortment (especially Copiers/Accessories) and protect its pricing discipline as it scales.

### 18. Standard Class shipping dominates order volume

- **What happened:** The majority of orders ship via Standard Class rather than Same Day or First Class.
- **Why it happened:** Standard shipping is the default/lowest-cost option and price-sensitive customers self-select into it.
- **Business impact:** Logistics capacity planning should be built primarily around Standard Class throughput, not premium shipping tiers.
- **Recommendation:** Test offering a discounted-but-paid faster-shipping upsell at checkout to capture margin from time-sensitive buyers.

### 19. Corporate segment has the highest average order value

- **What happened:** The Corporate segment tends to place fewer, larger orders compared to Consumer's more frequent, smaller orders.
- **Why it happened:** B2B purchasing patterns (bulk office supply and furniture orders) naturally produce a higher basket size.
- **Business impact:** A one-size-fits-all promotional strategy under-serves Corporate's bulk-order behavior.
- **Recommendation:** Build a tiered bulk-order discount structure for Corporate accounts instead of applying blanket consumer promotions.

### 20. Profit and discount are negatively correlated at the line-item level

- **What happened:** Across order lines, higher discount percentages are associated with lower (and frequently negative) profit.
- **Why it happened:** Discounting is being used as a blunt close-the-sale lever rather than a targeted, margin-aware pricing tool.
- **Business impact:** Uncontrolled discounting is likely the single largest controllable driver of the company's thin overall margin.
- **Recommendation:** Deploy a pricing/discount governance tool that blocks discounts pushing a line item below a defined margin floor.

### 21. A small number of sub-categories account for most of total profit

- **What happened:** Profit contribution across the 17 sub-categories is highly uneven -- a handful of sub-categories (e.g. Copiers, Phones, Accessories) generate the bulk of total company profit.
- **Why it happened:** These sub-categories combine strong demand with low discount dependency.
- **Business impact:** Broad, undifferentiated category-level strategy dilutes focus on the sub-categories that actually make money.
- **Recommendation:** Reallocate marketing and inventory investment toward the profit-concentrated sub-categories identified in category_analysis.csv.

### 22. Shipping delay is short and consistent across ship modes

- **What happened:** Average shipping delay (ship date minus order date) is short and clusters tightly by ship-mode tier, as expected given each mode's SLA.
- **Why it happened:** Fulfillment operations appear to reliably meet the promised service level for each shipping tier.
- **Business impact:** Reliable fulfillment is a retained strength and a valid marketing/trust signal, not a current risk area.
- **Recommendation:** Publish on-time delivery performance by ship mode as a trust signal on the storefront/checkout page.

### 23. Home Office is the smallest but most stable segment

- **What happened:** Home Office consistently contributes the smallest share of orders and revenue of the three segments, but shows relatively stable month-to-month ordering patterns.
- **Why it happened:** Smaller, steadier B2C-style purchasing base without the bulk-order swings seen in Corporate.
- **Business impact:** This segment is a low-risk, low-growth-ceiling part of the portfolio -- not a priority for major investment.
- **Recommendation:** Maintain current service levels for Home Office; focus growth investment on Consumer and Corporate instead.

### 24. Returned orders skew toward specific sub-categories, not evenly distributed

- **What happened:** Return activity concentrates in a subset of sub-categories rather than spreading evenly across the catalog.
- **Why it happened:** Likely product-specific quality, fit, or expectation-mismatch issues rather than a company-wide problem.
- **Business impact:** Blanket return-reduction initiatives waste effort; the fix needs to be targeted at the specific offending SKUs.
- **Recommendation:** Cross-reference product_summary.csv return_rate with profit_margin to find products that are both high-return and low-margin -- these are the first candidates to fix or cut.

### 25. Postal code data quality is materially clean

- **What happened:** Only one city (Burlington, Vermont) had missing postal codes, out of 9,994 order lines -- a data quality issue affecting a fraction of a percent of records.
- **Why it happened:** Consistent upstream data entry / order-management system discipline.
- **Business impact:** Geographic and regional roll-ups in Power BI can be trusted without material distortion from missing location data.
- **Recommendation:** No remediation needed beyond the single documented fix already applied in the cleaning pipeline.

### 26. No duplicate order lines exist in the dataset

- **What happened:** A full-row and Row ID duplicate check found zero duplicate records across all 9,994 order lines.
- **Why it happened:** The source extract appears to be a clean, single export rather than an accumulation of repeated syncs.
- **Business impact:** Aggregate KPIs (revenue, profit, order counts) can be reported with confidence and without a de-duplication step.
- **Recommendation:** Keep the duplicate-check step in the pipeline as a standing data-quality gate for any future data refreshes.

### 27. Quantity per order line is modest and consistent

- **What happened:** Most order lines involve small quantities (typically 2-7 units), rather than large bulk single-line orders.
- **Why it happened:** The Consumer-heavy customer base tends to buy in small quantities per product, spreading spend across multiple SKUs per order.
- **Business impact:** Inventory planning should size safety stock around frequent small-quantity draws rather than occasional bulk orders.
- **Recommendation:** Set reorder points using observed per-line quantity distributions rather than a flat assumed order size.

### 28. First Class and Same Day shipping are used sparingly

- **What happened:** Premium shipping tiers (First Class, Same Day) make up a minority of total orders relative to Standard and Second Class.
- **Why it happened:** Either these options are not well promoted at checkout, or customers are not sufficiently price-motivated to select them.
- **Business impact:** Underused premium shipping represents an untapped upsell / incremental-margin opportunity.
- **Recommendation:** A/B test surfacing Same Day / First Class shipping more prominently at checkout with clear delivery-date messaging.

### 29. Sales and profit are not perfectly correlated

- **What happened:** The correlation matrix shows sales and profit are positively but imperfectly correlated, confirming that high-revenue products are not automatically high-profit products.
- **Why it happened:** Discount rate and product-level cost structure both independently swing profit regardless of sales volume.
- **Business impact:** Revenue-only performance dashboards can mask genuinely unprofitable 'best sellers'.
- **Recommendation:** Ensure every Power BI product/region view pairs a Sales visual with a Profit Margin visual, never Sales alone.

### 30. Executive summary: fix margin leakage before pursuing growth

- **What happened:** With $2,297,200.86 revenue but only 12.5% margin, the business has a profitability problem more than a demand problem.
- **Why it happened:** The recurring driver across regions, categories, and products is the same: uncontrolled, unprofitable discounting.
- **Business impact:** Scaling marketing/acquisition spend on top of the current discount structure would scale losses, not profit.
- **Recommendation:** Sequence fixes in this order: (1) discount governance, (2) fix or delist loss-making SKUs, (3) double down on Technology and top regions, (4) THEN invest in growth.
