# Voice of Customer (VoC) Analysis

**Tools:** Python · SQL · Excel · VADER Sentiment Analysis  
**Domain:** Market Research · Consumer Insights · Customer Experience (CX) · Churn Analysis  
**Dataset:** 600-respondent synthetic VoC survey  
**Business Context:** RetainIQ SaaS — Customer Churn & Retention Research Study

---

## About This Project

### What is Voice of Customer (VoC) Research?

Voice of Customer (VoC) is a market research methodology used to capture customers' expectations, preferences, and pain points in their own words. Companies use VoC programs to understand *why* customers leave, *what* would bring them back, and *where* the product or service experience is breaking down.

VoC research is standard practice in marketing, SaaS, healthcare, and financial services — anywhere customer retention directly impacts revenue. The output of a VoC study is not just data — it is a prioritized action plan that leadership can act on immediately.

---

### The Fictional Company — RetainIQ

**RetainIQ** is a fictional B2B SaaS company that provides customer relationship management (CRM) tools for mid-size businesses. With approximately 2,400 active subscribers across three pricing tiers (Basic, Pro, Enterprise), RetainIQ experienced an **18% spike in customer churn in Q3 2024** — significantly above their historical baseline of 11%.

To understand the root cause, RetainIQ's research team commissioned this Voice of Customer study. The goal was to survey a cross-section of churned, at-risk, and retained customers to:

- Identify which pain points are driving the highest volume of churn
- Understand which churned customers are recoverable (win-back opportunity)
- Quantify the revenue at stake from at-risk customers
- Deliver a prioritized set of retention recommendations the product, support, and customer success teams can act on

*RetainIQ is a fictional company created for this portfolio project. The dataset, company name, product, and all figures are synthetic and generated for research methodology demonstration purposes.*

---

## Key Findings

| Metric | Result |
|---|---|
| Total Respondents | 600 |
| Churned Customers | 271 (45.2%) |
| At-Risk Customers | 188 (31.3%) |
| MRR Lost to Churn | $77,138/month ($925,656 annualized) |
| MRR Currently At Risk | $56,671/month ($680,052 annualized) |
| Win-Back Opportunity | $26,397/month ($316,764 ARR) |
| Win-Back Receptive Rate | 36.9% of churned customers |
| Top Churn Driver | Product Quality (32.5% of churned customers) |
| Second Churn Driver | Pricing & Value (23.2%) |

---

## The Five Pain Points Identified

This study identified five distinct categories of customer pain that drive churn. Each category represents a different failure in the customer experience — and each requires a different retention response.

| Pain Point | % of Churned | Avg Exit Satisfaction | MRR Lost |
|---|---|---|---|
| Product Quality | 32.5% | 1.69 / 5.0 | $25,039/month |
| Pricing & Value | 23.2% | 1.59 / 5.0 | $17,494/month |
| Customer Support | 20.3% | 1.69 / 5.0 | $15,579/month |
| Onboarding & Usability | 13.7% | 1.76 / 5.0 | $11,625/month |
| Competitor Switch | 10.3% | 1.64 / 5.0 | $7,401/month |

**Product Quality** is the leading driver — frequent bugs, missing features, and performance issues are causing nearly one in three churned customers to leave. **Pricing transparency** is the second driver, particularly around unexpected price increases at renewal.

---

## What Makes This Different from a Standard Churn Analysis

Most churn analyses stop at identifying *who* churned. This study goes further:

1. **Pain point severity scoring** — not just frequency, but which pain points have the lowest satisfaction scores and highest negative sentiment
2. **Win-back segmentation** — identifying which churned customers are still recoverable and quantifying that revenue opportunity by tier
3. **VADER sentiment analysis** — automated scoring of 600 open-ended exit feedback responses to surface emotional intensity behind each pain point
4. **Tenure analysis** — identifying *when* in the customer lifecycle churn is most likely to occur (early-stage vs long-term customers have different root causes)
5. **Industry breakdown** — Technology (50.9%) and Healthcare (50.0%) show the highest churn rates, indicating industry-specific intervention strategies are needed

---

## Project Structure

```
voice-of-customer-voc-analysis/
│
├── data/
│   ├── voc_survey_data.csv            # Raw 600-respondent VoC survey dataset
│   └── voc_analysis_output.csv        # Enriched dataset with sentiment scores
│
├── scripts/
│   ├── generate_data.py               # Synthetic VoC dataset generation
│   ├── voc_analysis.py                # Pain point analysis + VADER sentiment scoring
│   ├── voc_queries.sql                # SQL queries for churn, win-back, and sentiment analysis
│   └── generate_excel_report.py       # 4-tab Excel VoC research brief
│
├── output/
│   └── RetainIQ_VoC_Research_Brief.xlsx   # Executive deliverable (4 tabs)
│
├── requirements.txt
└── README.md
```

---

## Analysis Workflow

```
VoC Survey Data (600 respondents — Churned / At-Risk / Retained)
                         ↓
         Python — voc_analysis.py
         • Categorize pain points by frequency and severity
         • Run VADER sentiment analysis on 600 open-ended responses
         • Identify win-back opportunity by tier and pain point
         • Size revenue at risk and recoverable MRR
         • Analyze churn by tenure band, industry, and region
                         ↓
         SQL — voc_queries.sql
         • Pain point frequency and severity (avg satisfaction, avg repurchase intent)
         • Win-back opportunity by subscription tier
         • Sentiment distribution by churn status
         • Churn rate by industry
         • Tenure band analysis — when do customers leave?
         • At-risk customer prioritization by MRR
                         ↓
         Excel — RetainIQ_VoC_Research_Brief.xlsx
         • Tab 1: VoC Summary — overview KPIs and churn by tier
         • Tab 2: Pain Point Analysis — severity ranking and sentiment breakdown
         • Tab 3: Win-Back Opportunity — recovery sizing by tier and pain point
         • Tab 4: Retention Recommendations — 11 prioritized action items
```

---

## Dataset Columns

| Column | Description |
|---|---|
| customer_id | Unique customer identifier |
| churn_status | Churned / At-Risk / Retained |
| subscription_tier | Basic / Pro / Enterprise |
| tenure_months | Length of customer relationship |
| industry | Technology / Healthcare / Finance / Retail / Education |
| company_size | Employee band of the customer's organization |
| region | Northeast / Midwest / South / West |
| primary_pain_point | Main driver of churn or dissatisfaction |
| satisfaction_at_exit | 1–5 scale — satisfaction at time of churn |
| repurchase_intent | 1–5 scale — likelihood to return |
| win_back_receptive | Yes / No — open to a win-back offer |
| support_tickets_filed | Number of tickets submitted during tenure |
| recommended_to_others | Yes / No — NPS proxy |
| monthly_recurring_revenue | Customer MRR at time of churn |
| open_ended_feedback | Free-text exit feedback |
| sentiment_score | VADER compound score (−1 to +1) |
| sentiment_category | Positive / Neutral / Negative |

---

## How to Run

```bash
# 1. Clone the repository
git clone https://github.com/asharma0600/voice-of-customer-voc-analysis.git
cd voice-of-customer-voc-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate synthetic VoC dataset
python scripts/generate_data.py

# 4. Run VoC and sentiment analysis
python scripts/voc_analysis.py

# 5. Generate Excel research brief
python scripts/generate_excel_report.py
```

---

## Top Retention Recommendations

1. **Fix Product Quality first** — 32.5% of churned customers cite this as their primary driver, representing $25,039 in lost MRR monthly. A bug resolution sprint and formal product feedback loop are the highest-ROI retention investments.
2. **Launch a win-back campaign** — 36.9% of churned customers are receptive to returning. Enterprise win-back alone represents $147,408 in recoverable ARR.
3. **Improve pricing transparency** — communicate increases 60 days before renewal with documented feature improvements. Pricing surprises are a leading driver of negative exit sentiment.
4. **Redesign onboarding** — a 30-60-90 day structured program with milestone check-ins would significantly reduce early-stage churn (0-6 months cohort).
5. **Build industry-specific CS playbooks** — Technology and Healthcare verticals show 50%+ churn rates, indicating generic retention strategies are insufficient for these segments.

---

## Skills Demonstrated

- **VoC Research Methodology** — pain point categorization, severity scoring, win-back segmentation
- **Churn Analysis** — tenure-based churn timing, industry and tier breakdown, MRR impact quantification
- **Python** — pandas for data analysis, VADER for automated sentiment scoring of open-ended feedback
- **SQL** — multi-dimensional churn queries, revenue at risk sizing, at-risk customer prioritization
- **Excel** — 4-tab stakeholder-ready research brief with conditional formatting and revenue sizing
- **Business Impact Translation** — converting research findings into prioritized, revenue-linked recommendations

---

*Synthetic dataset generated for portfolio purposes. RetainIQ is a fictional company. All figures, names, and scenarios are illustrative.*
