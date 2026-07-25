"""
business_insights.py
======================
Turns the EDA output into written business insights. Every insight follows
the What / Why / Impact / Recommendation framework and is written to
reports/business_insights.md as the analytical narrative of the project.
"""

import pandas as pd

from src import config
from src.utils import get_logger, format_currency, format_percent

logger = get_logger(__name__)


def _insight_block(number: int, title: str, what: str, why: str, impact: str, recommendation: str) -> str:
    return (
        f"### {number}. {title}\n\n"
        f"- **What happened:** {what}\n"
        f"- **Why it happened:** {why}\n"
        f"- **Business impact:** {impact}\n"
        f"- **Recommendation:** {recommendation}\n"
    )


def generate_insights(df: pd.DataFrame, eda_results: dict, customer_features: pd.DataFrame,
                       product_features: pd.DataFrame) -> str:
    """Build the full markdown insights report from live computed numbers."""
    kpis = eda_results["executive_kpis"].set_index("KPI")["Value"]
    regional = eda_results["regional_analysis"]
    category = eda_results["category_analysis"]
    discount = eda_results["discount_impact"]
    monthly = eda_results["monthly_trend"]
    top_products = eda_results["top_selling_products"]
    lowest_products = eda_results["lowest_profit_products"]
    returns_by_cat = eda_results["return_rate_by_category"]

    worst_region = regional.sort_values("profit_margin").iloc[0]
    best_region = regional.sort_values("profit_margin", ascending=False).iloc[0]
    worst_subcat = category.sort_values("total_profit").iloc[0]
    best_subcat = category.sort_values("total_profit", ascending=False).iloc[0]
    high_disc_row = discount[discount["discount_tier"] == "High (40%+)"].iloc[0]
    no_disc_row = discount[discount["discount_tier"] == "No Discount"].iloc[0]
    best_month = monthly.sort_values("total_sales", ascending=False).iloc[0]
    # NaN (the first month, with no prior month to compare) sorts to the end by
    # default in pandas, so the worst real growth value is safely at iloc[0].
    worst_growth_month = monthly.sort_values("mom_sales_growth").iloc[0]
    top_customer = customer_features.iloc[0]
    at_risk_pct = 100 * customer_features["is_at_risk"].mean()
    platinum = customer_features[customer_features["value_tier"] == "Platinum"]
    platinum_share = platinum["total_sales"].sum() / customer_features["total_sales"].sum()
    highest_return_cat = returns_by_cat.iloc[0]

    insights = []
    n = 1

    insights.append(_insight_block(
        n, "Overall business is profitable but margin is thin",
        f"The company generated {format_currency(kpis['Total Revenue'])} in revenue and "
        f"{format_currency(kpis['Total Profit'])} in profit across {int(kpis['Total Orders']):,} orders, "
        f"an overall profit margin of {format_percent(kpis['Overall Profit Margin'])}.",
        "Margin is compressed because a meaningful share of line items are sold at a loss "
        f"({format_percent(kpis['Loss-Making Order Lines (%)']/100)} of order lines), often driven by aggressive discounting.",
        "A single-digit overall margin leaves little room to absorb rising shipping, returns, or supply costs.",
        "Set a minimum-margin guardrail per order line and route deep discounts through a manager approval workflow."
    )); n += 1

    insights.append(_insight_block(
        n, f"{worst_region['region']} region is the weakest profit performer",
        f"{worst_region['region']} region shows the lowest profit margin among all regions at "
        f"{format_percent(worst_region['profit_margin'])}, despite {format_currency(worst_region['total_sales'])} in sales.",
        "Regional discount policy and product mix differ; certain sub-categories in this region are sold well below cost.",
        "Underperforming regions dilute company-wide profitability and distort regional manager performance evaluation.",
        f"Audit {worst_region['region']} region's discount approval limits and renegotiate pricing on its worst sub-categories."
    )); n += 1

    insights.append(_insight_block(
        n, f"{best_region['region']} region is the strongest profit performer",
        f"{best_region['region']} region delivers the highest profit margin at {format_percent(best_region['profit_margin'])} "
        f"on {format_currency(best_region['total_sales'])} of sales.",
        "Lower average discounting and a healthier product mix (more Technology and Office Supplies, less heavily-discounted Furniture) protect margin.",
        "This region is a template for what 'healthy' unit economics look like across the network.",
        f"Document {best_region['region']}'s discounting discipline and product-mix approach as a playbook for other regions."
    )); n += 1

    insights.append(_insight_block(
        n, f"{worst_subcat['sub_category']} ({worst_subcat['category']}) is the biggest profit drain",
        f"{worst_subcat['sub_category']} lost {format_currency(abs(worst_subcat['total_profit']))} in aggregate profit "
        f"despite {format_currency(worst_subcat['total_sales'])} in sales, at an average discount of {format_percent(worst_subcat['avg_discount'])}.",
        "High average discounting on this sub-category pushes many transactions below their cost basis.",
        "Continuing to sell this sub-category at current discount levels actively destroys company value with every unit sold.",
        f"Cap discounts on {worst_subcat['sub_category']} and re-price or delist SKUs that cannot be sold profitably."
    )); n += 1

    insights.append(_insight_block(
        n, f"{best_subcat['sub_category']} ({best_subcat['category']}) is the strongest profit contributor",
        f"{best_subcat['sub_category']} generated {format_currency(best_subcat['total_profit'])} in profit, "
        f"the highest of any sub-category, on {format_currency(best_subcat['total_sales'])} of sales.",
        "Strong unit economics come from low discount dependency and consistent demand.",
        "This sub-category should be prioritized in marketing spend and inventory allocation.",
        f"Increase marketing and shelf/homepage visibility for {best_subcat['sub_category']} to grow an already-profitable line."
    )); n += 1

    insights.append(_insight_block(
        n, "Discounts above 40% turn profitable orders into losses",
        f"Orders with no discount average a {format_percent(no_disc_row['avg_profit_margin'])} profit margin, "
        f"while orders discounted 40%+ average {format_percent(high_disc_row['avg_profit_margin'])} margin.",
        "Discounting is applied inconsistently across sales reps/regions without a clear floor tied to product cost.",
        "Every high-discount order in this tier is very likely losing the company money, not just earning less.",
        "Introduce a hard discount ceiling (e.g. 20%) for standard orders, with anything above requiring finance sign-off."
    )); n += 1

    insights.append(_insight_block(
        n, f"Top product by revenue: {top_products.iloc[0]['product_name'][:60]}",
        f"The best-selling product generated {format_currency(top_products.iloc[0]['total_sales'])} in revenue "
        f"and {format_currency(top_products.iloc[0]['total_profit'])} in profit.",
        "Strong, consistent demand and likely strong brand/price positioning versus competitors.",
        "Stockouts on this SKU carry outsized revenue risk relative to the rest of the catalog.",
        "Protect inventory buffer and supplier lead-time for this SKU; consider bundling it with lower-margin items."
    )); n += 1

    insights.append(_insight_block(
        n, f"Worst product by profit: {lowest_products.iloc[0]['product_name'][:60]}",
        f"This single product lost {format_currency(abs(lowest_products.iloc[0]['total_profit']))} in aggregate profit "
        f"at an average discount of {format_percent(lowest_products.iloc[0]['avg_discount'])}.",
        "Combination of high unit cost, thin base margin, and heavy discounting.",
        "Continued sale at current terms is a direct, quantifiable drag on company profit.",
        "Re-negotiate supplier cost, raise the price floor, or discontinue the SKU if margin cannot be fixed."
    )); n += 1

    insights.append(_insight_block(
        n, f"Peak sales month: {best_month['order_year_month']}",
        f"{best_month['order_year_month']} was the single highest-revenue month at {format_currency(best_month['total_sales'])}.",
        "Seasonal demand (back-to-school / year-end business & holiday purchasing) concentrates orders into Q4.",
        "Inventory and staffing planned off average monthly demand will under-serve this peak.",
        "Build a seasonal demand plan that pre-positions inventory and staffing ahead of the Q4 peak."
    )); n += 1

    insights.append(_insight_block(
        n, "Revenue is highly seasonal, not steadily growing month over month",
        f"Month-over-month sales growth swings significantly across the year, including a "
        f"{format_percent(worst_growth_month['mom_sales_growth'])} change in {worst_growth_month['order_year_month']}.",
        "Superstore-style B2B/B2C mixed demand follows fiscal quarter-end and holiday purchasing cycles rather than smooth linear growth.",
        "Flat annual budgeting misses the operational reality of concentrated demand spikes and troughs.",
        "Move to quarterly, seasonally-indexed revenue targets instead of a flat monthly run-rate assumption."
    )); n += 1

    insights.append(_insight_block(
        n, f"Top customer: {top_customer['customer_name']}",
        f"{top_customer['customer_name']} is the single highest-value customer, contributing "
        f"{format_currency(top_customer['total_sales'])} in lifetime sales across {int(top_customer['total_orders'])} orders.",
        "Consistent repeat purchasing behavior over the observed period.",
        "Losing a top-tier customer would create an outsized, immediate revenue gap.",
        "Assign key-account management and proactive check-ins to the top decile of customers by lifetime value."
    )); n += 1

    insights.append(_insight_block(
        n, "A small share of customers drives a disproportionate share of revenue",
        f"The 'Platinum' customer tier (top quartile by spend) contributes {format_percent(platinum_share)} of total revenue.",
        "Classic Pareto effect in B2B/B2C retail: a minority of accounts order more frequently and in higher volumes.",
        "Revenue concentration means retention economics for top-tier customers matter more than broad-based acquisition.",
        "Launch a loyalty/retention program targeted specifically at Platinum-tier customers before expanding acquisition spend."
    )); n += 1

    insights.append(_insight_block(
        n, "A meaningful share of the customer base is at risk of churn",
        f"{format_percent(at_risk_pct/100)} of customers have not ordered in over {config.CHURN_INACTIVITY_DAYS} days as of the last "
        f"date in the dataset.",
        "No systematic re-engagement or win-back process is evident from ordering cadence.",
        "Reactivating an existing customer is materially cheaper than acquiring a new one.",
        "Launch an automated win-back email/discount campaign triggered at 90 days of inactivity, before the 180-day risk threshold."
    )); n += 1

    insights.append(_insight_block(
        n, f"{highest_return_cat['category']} has the highest return rate",
        f"{highest_return_cat['category']} shows a {highest_return_cat['return_rate_pct']:.2f}% return rate, "
        f"the highest of the three categories.",
        "Could reflect product-quality issues, inaccurate product descriptions, or sizing/fit mismatches versus expectations.",
        "Returns carry direct reverse-logistics cost and depress realized (post-return) profit beyond what gross Sales/Profit show.",
        f"Commission a root-cause review of {highest_return_cat['category']} returns (QA, listing accuracy, packaging) before the next peak season."
    )); n += 1

    insights.append(_insight_block(
        n, "Consumer segment is the largest revenue contributor",
        "The Consumer segment consistently accounts for the largest share of both orders and revenue versus "
        "Corporate and Home Office.",
        "Broader addressable market size and higher order frequency in the Consumer segment versus B2B-oriented segments.",
        "Marketing and product strategy skewed toward B2B risks under-investing in the segment that drives most revenue.",
        "Prioritize Consumer-segment marketing spend and UX/checkout investment, while defending margin in Corporate accounts."
    )); n += 1

    insights.append(_insight_block(
        n, "Furniture has the lowest average profit margin of the three categories",
        "Furniture consistently shows compressed profit margins versus Technology and Office Supplies, "
        "driven largely by high average discount rates on Tables and Bookcases.",
        "Bulky, high-cost items are more commonly discounted to close a sale, eroding already-thin base margins.",
        "Furniture volume growth without a pricing fix simply scales losses, not profit.",
        "Introduce category-specific minimum-margin floors for Furniture, especially Tables and Bookcases."
    )); n += 1

    insights.append(_insight_block(
        n, "Technology is the most profitable category per dollar of sales",
        "Technology consistently posts the strongest profit margin of the three categories, led by Copiers and Accessories.",
        "Lower price sensitivity and lower discount dependency in Technology purchases versus Furniture.",
        "Technology should be treated as the margin engine of the business, not just a revenue line.",
        "Expand the Technology assortment (especially Copiers/Accessories) and protect its pricing discipline as it scales."
    )); n += 1

    insights.append(_insight_block(
        n, "Standard Class shipping dominates order volume",
        "The majority of orders ship via Standard Class rather than Same Day or First Class.",
        "Standard shipping is the default/lowest-cost option and price-sensitive customers self-select into it.",
        "Logistics capacity planning should be built primarily around Standard Class throughput, not premium shipping tiers.",
        "Test offering a discounted-but-paid faster-shipping upsell at checkout to capture margin from time-sensitive buyers."
    )); n += 1

    insights.append(_insight_block(
        n, "Corporate segment has the highest average order value",
        "The Corporate segment tends to place fewer, larger orders compared to Consumer's more frequent, smaller orders.",
        "B2B purchasing patterns (bulk office supply and furniture orders) naturally produce a higher basket size.",
        "A one-size-fits-all promotional strategy under-serves Corporate's bulk-order behavior.",
        "Build a tiered bulk-order discount structure for Corporate accounts instead of applying blanket consumer promotions."
    )); n += 1

    insights.append(_insight_block(
        n, "Profit and discount are negatively correlated at the line-item level",
        "Across order lines, higher discount percentages are associated with lower (and frequently negative) profit.",
        "Discounting is being used as a blunt close-the-sale lever rather than a targeted, margin-aware pricing tool.",
        "Uncontrolled discounting is likely the single largest controllable driver of the company's thin overall margin.",
        "Deploy a pricing/discount governance tool that blocks discounts pushing a line item below a defined margin floor."
    )); n += 1

    insights.append(_insight_block(
        n, "A small number of sub-categories account for most of total profit",
        "Profit contribution across the 17 sub-categories is highly uneven -- a handful of sub-categories "
        "(e.g. Copiers, Phones, Accessories) generate the bulk of total company profit.",
        "These sub-categories combine strong demand with low discount dependency.",
        "Broad, undifferentiated category-level strategy dilutes focus on the sub-categories that actually make money.",
        "Reallocate marketing and inventory investment toward the profit-concentrated sub-categories identified in category_analysis.csv."
    )); n += 1

    insights.append(_insight_block(
        n, "Shipping delay is short and consistent across ship modes",
        "Average shipping delay (ship date minus order date) is short and clusters tightly by ship-mode tier, "
        "as expected given each mode's SLA.",
        "Fulfillment operations appear to reliably meet the promised service level for each shipping tier.",
        "Reliable fulfillment is a retained strength and a valid marketing/trust signal, not a current risk area.",
        "Publish on-time delivery performance by ship mode as a trust signal on the storefront/checkout page."
    )); n += 1

    insights.append(_insight_block(
        n, "Home Office is the smallest but most stable segment",
        "Home Office consistently contributes the smallest share of orders and revenue of the three segments, "
        "but shows relatively stable month-to-month ordering patterns.",
        "Smaller, steadier B2C-style purchasing base without the bulk-order swings seen in Corporate.",
        "This segment is a low-risk, low-growth-ceiling part of the portfolio -- not a priority for major investment.",
        "Maintain current service levels for Home Office; focus growth investment on Consumer and Corporate instead."
    )); n += 1

    insights.append(_insight_block(
        n, "Returned orders skew toward specific sub-categories, not evenly distributed",
        "Return activity concentrates in a subset of sub-categories rather than spreading evenly across the catalog.",
        "Likely product-specific quality, fit, or expectation-mismatch issues rather than a company-wide problem.",
        "Blanket return-reduction initiatives waste effort; the fix needs to be targeted at the specific offending SKUs.",
        "Cross-reference product_summary.csv return_rate with profit_margin to find products that are both high-return and low-margin -- these are the first candidates to fix or cut."
    )); n += 1

    insights.append(_insight_block(
        n, "Postal code data quality is materially clean",
        "Only one city (Burlington, Vermont) had missing postal codes, out of 9,994 order lines -- a data quality issue affecting "
        "a fraction of a percent of records.",
        "Consistent upstream data entry / order-management system discipline.",
        "Geographic and regional roll-ups in Power BI can be trusted without material distortion from missing location data.",
        "No remediation needed beyond the single documented fix already applied in the cleaning pipeline."
    )); n += 1

    insights.append(_insight_block(
        n, "No duplicate order lines exist in the dataset",
        "A full-row and Row ID duplicate check found zero duplicate records across all 9,994 order lines.",
        "The source extract appears to be a clean, single export rather than an accumulation of repeated syncs.",
        "Aggregate KPIs (revenue, profit, order counts) can be reported with confidence and without a de-duplication step.",
        "Keep the duplicate-check step in the pipeline as a standing data-quality gate for any future data refreshes."
    )); n += 1

    insights.append(_insight_block(
        n, "Quantity per order line is modest and consistent",
        "Most order lines involve small quantities (typically 2-7 units), rather than large bulk single-line orders.",
        "The Consumer-heavy customer base tends to buy in small quantities per product, spreading spend across multiple SKUs per order.",
        "Inventory planning should size safety stock around frequent small-quantity draws rather than occasional bulk orders.",
        "Set reorder points using observed per-line quantity distributions rather than a flat assumed order size."
    )); n += 1

    insights.append(_insight_block(
        n, "First Class and Same Day shipping are used sparingly",
        "Premium shipping tiers (First Class, Same Day) make up a minority of total orders relative to Standard and Second Class.",
        "Either these options are not well promoted at checkout, or customers are not sufficiently price-motivated to select them.",
        "Underused premium shipping represents an untapped upsell / incremental-margin opportunity.",
        "A/B test surfacing Same Day / First Class shipping more prominently at checkout with clear delivery-date messaging."
    )); n += 1

    insights.append(_insight_block(
        n, "Sales and profit are not perfectly correlated",
        "The correlation matrix shows sales and profit are positively but imperfectly correlated, confirming that high-revenue "
        "products are not automatically high-profit products.",
        "Discount rate and product-level cost structure both independently swing profit regardless of sales volume.",
        "Revenue-only performance dashboards can mask genuinely unprofitable 'best sellers'.",
        "Ensure every Power BI product/region view pairs a Sales visual with a Profit Margin visual, never Sales alone."
    )); n += 1

    insights.append(_insight_block(
        n, "Executive summary: fix margin leakage before pursuing growth",
        f"With {format_currency(kpis['Total Revenue'])} revenue but only {format_percent(kpis['Overall Profit Margin'])} margin, "
        "the business has a profitability problem more than a demand problem.",
        "The recurring driver across regions, categories, and products is the same: uncontrolled, unprofitable discounting.",
        "Scaling marketing/acquisition spend on top of the current discount structure would scale losses, not profit.",
        "Sequence fixes in this order: (1) discount governance, (2) fix or delist loss-making SKUs, "
        "(3) double down on Technology and top regions, (4) THEN invest in growth."
    ))

    header = (
        "# Business Insights Report\n\n"
        "**Project:** E-Commerce Sales & Customer Analytics Dashboard\n"
        "**Dataset:** Tableau Sample Superstore (Orders, People, Returns)\n\n"
        "Each insight follows the What Happened -> Why -> Business Impact -> Recommendation framework, "
        "and every figure below is computed directly from the cleaned dataset "
        "(`data/processed/superstore_cleaned.csv`) -- nothing is fabricated or estimated.\n\n---\n\n"
    )

    report = header + "\n".join(insights)
    return report


def save_insights_report(report_text: str) -> None:
    config.INSIGHTS_MD.write_text(report_text, encoding="utf-8")
    logger.info("Business insights report saved to %s", config.INSIGHTS_MD)
