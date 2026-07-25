const pptxgen = require("pptxgenjs");
const path = require("path");

const IMG = (f) => path.join(__dirname, f);

const COLORS = {
  primary: "2E86AB",
  secondary: "A23B72",
  teal: "3AA6A0",
  alert: "C73E1D",
  dark: "222222",
  gray: "555555",
  lightBg: "F7F7F7",
  white: "FFFFFF",
};

let pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.3 x 7.5

function titleSlide() {
  let s = pres.addSlide();
  s.background = { color: COLORS.dark };
  s.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: 13.33, h: 7.5, fill: { color: COLORS.dark } });
  s.addText("E-COMMERCE SALES &\nCUSTOMER ANALYTICS", {
    x: 0.8, y: 2.3, w: 10, h: 2.0, fontSize: 40, bold: true, color: COLORS.white, fontFace: "Arial",
  });
  s.addText("A data-driven diagnosis of revenue, profitability, and customer value\nusing the Tableau Sample Superstore dataset",
    { x: 0.8, y: 4.1, w: 10, h: 0.8, fontSize: 16, color: "CCCCCC", fontFace: "Arial" });
  s.addShape(pres.ShapeType.rect, { x: 0.8, y: 3.95, w: 1.4, h: 0.04, fill: { color: COLORS.primary } });
  s.addText("Business Analytics Portfolio Project  |  Python  ·  SQL  ·  Power BI", {
    x: 0.8, y: 6.6, w: 10, h: 0.5, fontSize: 12, color: "888888", fontFace: "Arial",
  });
}

function bizProblemSlide() {
  let s = pres.addSlide();
  s.background = { color: COLORS.white };
  s.addText("Business Problem & Objective", { x: 0.6, y: 0.4, w: 11, h: 0.7, fontSize: 28, bold: true, color: COLORS.dark });

  const cards = [
    { t: "The Problem", d: "Superstore generates over $2.3M in revenue but keeps only a 12.5% profit margin. Leadership cannot see which regions, products, or discount practices are quietly destroying profit.", c: COLORS.alert },
    { t: "The Objective", d: "Build an end-to-end analytics pipeline -- cleaning, SQL modeling, and a Power BI executive dashboard -- that pinpoints exactly where profit is won and lost, and what to do about it.", c: COLORS.primary },
    { t: "The Approach", d: "Python for cleaning & feature engineering, MySQL for interview-grade analytical queries, Power BI for an interactive executive dashboard, all built on one verified source of truth.", c: COLORS.teal },
  ];
  cards.forEach((card, i) => {
    const x = 0.6 + i * 4.1;
    s.addShape(pres.ShapeType.roundRect, { x, y: 1.5, w: 3.8, h: 4.8, rectRadius: 0.08,
      fill: { color: COLORS.lightBg }, line: { color: card.c, width: 2 } });
    s.addText(card.t, { x: x + 0.25, y: 1.75, w: 3.3, h: 0.5, fontSize: 16, bold: true, color: card.c });
    s.addText(card.d, { x: x + 0.25, y: 2.35, w: 3.3, h: 3.6, fontSize: 12.5, color: COLORS.gray, valign: "top", lineSpacingMultiple: 1.25 });
  });
}

function datasetSlide() {
  let s = pres.addSlide();
  s.background = { color: COLORS.white };
  s.addText("The Dataset", { x: 0.6, y: 0.4, w: 11, h: 0.7, fontSize: 28, bold: true, color: COLORS.dark });
  s.addText("Tableau Sample Superstore — real order-level retail data, 2018-2021", { x: 0.6, y: 1.05, w: 11, h: 0.4, fontSize: 14, color: COLORS.gray });

  const stats = [
    ["9,994", "Order Line Items"], ["5,009", "Unique Orders"], ["793", "Customers"],
    ["1,862", "Products"], ["3", "Sheets: Orders, People, Returns"], ["4", "Years of Data"],
  ];
  stats.forEach((st, i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = 0.6 + col * 4.05, y = 1.8 + row * 1.7;
    s.addShape(pres.ShapeType.roundRect, { x, y, w: 3.7, h: 1.4, rectRadius: 0.06,
      fill: { color: COLORS.lightBg }, line: { color: "DDDDDD", width: 1 } });
    s.addText(st[0], { x, y: y + 0.12, w: 3.7, h: 0.65, align: "center", fontSize: 26, bold: true, color: COLORS.primary });
    s.addText(st[1], { x, y: y + 0.82, w: 3.7, h: 0.45, align: "center", fontSize: 12, color: COLORS.gray });
  });
  s.addText("21 columns per order line: Order/Ship dates, Ship Mode, Customer, Segment, Region, Product hierarchy, Sales, Quantity, Discount, Profit.",
    { x: 0.6, y: 5.4, w: 12.1, h: 0.6, fontSize: 12, italic: true, color: COLORS.gray });
}

function architectureSlide() {
  let s = pres.addSlide();
  s.background = { color: COLORS.white };
  s.addText("System Architecture", { x: 0.6, y: 0.35, w: 11, h: 0.6, fontSize: 26, bold: true, color: COLORS.dark });
  s.addImage({ path: IMG("architecture.png"), x: 0.5, y: 1.1, w: 12.3, h: 5.7 * (13/13.5) });
}

function workflowSlide() {
  let s = pres.addSlide();
  s.background = { color: COLORS.white };
  s.addText("Analytics Workflow", { x: 0.6, y: 0.4, w: 11, h: 0.6, fontSize: 26, bold: true, color: COLORS.dark });
  s.addImage({ path: IMG("workflow.png"), x: 1.0, y: 1.8, w: 11.3, h: 2.95 });
  s.addText("Every stage is a standalone, testable Python module in src/ -- no notebook-only logic.",
    { x: 0.6, y: 5.3, w: 12, h: 0.5, fontSize: 13, italic: true, color: COLORS.gray, align: "center" });
}

function chartSlide(title, subtitle, imgFile) {
  let s = pres.addSlide();
  s.background = { color: COLORS.white };
  s.addText(title, { x: 0.6, y: 0.35, w: 11.5, h: 0.6, fontSize: 26, bold: true, color: COLORS.dark });
  s.addText(subtitle, { x: 0.6, y: 0.9, w: 11.8, h: 0.5, fontSize: 13, color: COLORS.gray });
  s.addImage({ path: IMG(`../images/${imgFile}`), x: 1.4, y: 1.55, w: 10.5, h: 5.6, sizing: { type: "contain", w: 10.5, h: 5.6 } });
}

function dashboardMockupSlide() {
  let s = pres.addSlide();
  s.background = { color: COLORS.white };
  s.addText("Power BI Executive Dashboard", { x: 0.6, y: 0.3, w: 11, h: 0.55, fontSize: 26, bold: true, color: COLORS.dark });
  s.addText("Full build guide with DAX measures in dashboard/PowerBI_Build_Guide.md", { x: 0.6, y: 0.82, w: 11.5, h: 0.4, fontSize: 12.5, color: COLORS.gray });
  s.addImage({ path: IMG("dashboard_mockup.png"), x: 0.5, y: 1.3, w: 12.3, h: 5.85 * (12.3/15.5) });
}

function insightsSlide() {
  let s = pres.addSlide();
  s.background = { color: COLORS.white };
  s.addText("Key Business Insights", { x: 0.6, y: 0.4, w: 11, h: 0.6, fontSize: 26, bold: true, color: COLORS.dark });

  const items = [
    ["Discount discipline is the #1 lever", "Orders discounted 40%+ average a -109% profit margin -- every one is a loss."],
    ["Furniture is structurally thin-margin", "Tables and Bookcases post negative profit overall, driven by heavy discounting."],
    ["Technology is the profit engine", "Copiers and Accessories deliver the strongest, most reliable margins."],
    ["Revenue concentrates in top customers", "The top spend quartile drives a disproportionate share of total revenue."],
  ];
  items.forEach((it, i) => {
    const y = 1.5 + i * 1.35;
    s.addShape(pres.ShapeType.rect, { x: 0.6, y: y + 0.05, w: 0.08, h: 1.05, fill: { color: [COLORS.primary, COLORS.alert, COLORS.teal, COLORS.secondary][i] } });
    s.addText(it[0], { x: 0.95, y, w: 11.5, h: 0.5, fontSize: 16, bold: true, color: COLORS.dark });
    s.addText(it[1], { x: 0.95, y: y + 0.5, w: 11.5, h: 0.55, fontSize: 13, color: COLORS.gray });
  });
  s.addText("Full 30-insight report: reports/business_insights.md", { x: 0.6, y: 6.9, w: 10, h: 0.4, fontSize: 11, italic: true, color: "999999" });
}

function recommendationsSlide() {
  let s = pres.addSlide();
  s.background = { color: COLORS.dark };
  s.addText("Recommendations for Leadership", { x: 0.6, y: 0.4, w: 11.5, h: 0.6, fontSize: 26, bold: true, color: COLORS.white });

  const recs = [
    "Cap standard discounts at 20%; route anything higher through finance sign-off.",
    "Re-price or delist chronically loss-making SKUs in Tables and Bookcases.",
    "Double down on Technology (Copiers, Accessories) with marketing & inventory priority.",
    "Launch a win-back campaign for customers inactive 90+ days, before the 180-day risk mark.",
    "Move budgeting from flat monthly targets to seasonally-indexed quarterly targets.",
  ];
  recs.forEach((r, i) => {
    const y = 1.5 + i * 1.05;
    s.addShape(pres.ShapeType.ellipse, { x: 0.6, y: y + 0.05, w: 0.4, h: 0.4, fill: { color: COLORS.primary } });
    s.addText(String(i + 1), { x: 0.6, y: y + 0.05, w: 0.4, h: 0.4, align: "center", valign: "middle", fontSize: 14, bold: true, color: COLORS.white });
    s.addText(r, { x: 1.25, y, w: 11.2, h: 0.55, fontSize: 15, color: "EEEEEE", valign: "middle" });
  });
}

function techStackSlide() {
  let s = pres.addSlide();
  s.background = { color: COLORS.white };
  s.addText("Tech Stack & Repository", { x: 0.6, y: 0.4, w: 11, h: 0.6, fontSize: 26, bold: true, color: COLORS.dark });

  const stack = ["Python (pandas, NumPy)", "Matplotlib & Seaborn", "MySQL 8", "Power BI + DAX", "Git & GitHub", "python-pptx / pptxgenjs"];
  stack.forEach((t, i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = 0.6 + col * 4.05, y = 1.6 + row * 1.1;
    s.addShape(pres.ShapeType.roundRect, { x, y, w: 3.7, h: 0.85, rectRadius: 0.5,
      fill: { color: COLORS.lightBg }, line: { color: COLORS.primary, width: 1.5 } });
    s.addText(t, { x, y, w: 3.7, h: 0.85, align: "center", valign: "middle", fontSize: 13, bold: true, color: COLORS.dark });
  });

  s.addText("Repository Structure", { x: 0.6, y: 4.1, w: 6, h: 0.4, fontSize: 15, bold: true, color: COLORS.dark });
  s.addText(
    "data/  src/  sql/  dashboard/  images/  reports/  presentation/\nREADME.md · requirements.txt · .gitignore · LICENSE",
    { x: 0.6, y: 4.55, w: 6.5, h: 1.4, fontSize: 12.5, color: COLORS.gray, fontFace: "Courier New" }
  );
  s.addText("github.com/<your-username>/Ecommerce-Sales-Analytics", { x: 0.6, y: 6.3, w: 8, h: 0.4, fontSize: 12, color: COLORS.primary, bold: true });
}

function closingSlide() {
  let s = pres.addSlide();
  s.background = { color: COLORS.dark };
  s.addText("Thank You", { x: 0.8, y: 2.6, w: 10, h: 1.0, fontSize: 40, bold: true, color: COLORS.white });
  s.addText("E-Commerce Sales & Customer Analytics Dashboard", { x: 0.8, y: 3.6, w: 10, h: 0.5, fontSize: 16, color: "CCCCCC" });
  s.addText("Full code, SQL, dashboard guide, and reports available on GitHub.", { x: 0.8, y: 4.15, w: 10, h: 0.5, fontSize: 13, color: "999999" });
}

titleSlide();
bizProblemSlide();
datasetSlide();
architectureSlide();
workflowSlide();
chartSlide("Top Selling Products", "Revenue leaders by total sales", "top_selling_products.png");
chartSlide("Regional Performance", "Revenue and profit margin by region", "regional_analysis.png");
chartSlide("Category Performance", "Sales vs. profit by category", "category_analysis.png");
chartSlide("Monthly Trend", "Seasonality in revenue and profit, 2018-2021", "monthly_trend.png");
chartSlide("Discount Impact", "How discount depth erodes profit margin", "discount_impact.png");
dashboardMockupSlide();
insightsSlide();
recommendationsSlide();
techStackSlide();
closingSlide();

pres.writeFile({ fileName: path.join(__dirname, "project_presentation.pptx") }).then(() => {
  console.log("Presentation written.");
});
