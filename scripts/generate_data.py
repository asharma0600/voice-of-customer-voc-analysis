"""
Voice of Customer (VoC) Analysis — Data Generation
RetainIQ SaaS | Customer Churn & Retention Research Study
Author: Alisha Sharma
"""

import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

N = 600

# ── Pools ─────────────────────────────────────────────────────────────────

tiers       = ["Basic", "Pro", "Enterprise"]
regions     = ["Northeast", "Midwest", "South", "West"]
industries  = ["Technology", "Healthcare", "Retail", "Finance", "Education"]
pain_cats   = ["Product Quality", "Customer Support", "Pricing & Value",
               "Onboarding & Usability", "Competitor Switch"]
churn_stats = ["Churned", "At-Risk", "Retained"]
company_sizes = ["1-10 employees", "11-50 employees", "51-200 employees", "201+ employees"]

# ── Open-ended feedback by pain point ─────────────────────────────────────

feedback_product = [
    "The platform crashes frequently and bugs have never been resolved despite multiple reports.",
    "Core features promised during the sales process are still not available after months of waiting.",
    "Performance has deteriorated significantly and the product is slower than when we started.",
    "We keep encountering the same technical issues with no permanent fix from the team.",
    "The product does not integrate with our existing tools which makes it very difficult to use.",
    "Too many features are broken or incomplete. The product feels like it is still in beta.",
    "We experienced significant data sync issues that impacted our daily operations.",
    "The mobile app is essentially unusable compared to the desktop version.",
]

feedback_support = [
    "Support response times are unacceptably slow. We wait days for simple issue resolution.",
    "Every time we contact support we are passed between agents with no continuity.",
    "Issues are closed without being resolved and we have to reopen the same tickets repeatedly.",
    "The support team does not understand our use case and the advice is often unhelpful.",
    "We feel ignored. Critical issues sit open for weeks with no meaningful updates.",
    "There is no dedicated account manager for Pro tier which is frustrating given our spend.",
    "The help documentation is outdated and support often contradicts what the docs say.",
    "Live chat support is unavailable during our business hours which are not US Eastern time.",
]

feedback_pricing = [
    "The price increased 30% at renewal with no new features or improvements to justify it.",
    "We found a competitor offering the same core functionality at half the price.",
    "The ROI is simply not there. We cannot justify this cost to our leadership team.",
    "Add-on fees for features we assumed were included made the total cost far higher than expected.",
    "Our budget was cut and the pricing tier options do not offer a meaningful downgrade path.",
    "The annual contract pricing is not competitive. Monthly flexibility would help retain smaller teams.",
    "We were not informed about the price increase until 2 weeks before renewal. Very poor communication.",
    "Value for money compared to competitors has declined significantly over the past year.",
]

feedback_onboarding = [
    "The onboarding process was rushed and our team never felt fully trained on the platform.",
    "Setup took far longer than expected and we never received adequate implementation support.",
    "The learning curve is too steep for our non-technical staff to adopt comfortably.",
    "Onboarding resources are scattered and there is no structured path for new users.",
    "We were handed off from sales to a junior CSM who did not understand our configuration needs.",
    "The product is powerful but too complex for our team size without better guided onboarding.",
    "Training materials are outdated and do not reflect the current version of the product.",
    "We were left to figure things out on our own after the first two weeks of setup.",
]

feedback_competitor = [
    "A competitor offered a significantly better onboarding experience and comparable features.",
    "We evaluated three alternatives and another platform won on both price and support quality.",
    "Our industry peers have migrated to a competing platform and we followed after their recommendation.",
    "A competitor approached us with a migration offer that made the switch financially compelling.",
    "The competing platform integrates natively with our CRM which made the decision straightforward.",
    "We piloted an alternative solution and the team preferred it unanimously over RetainIQ.",
    "A competitor's new release addressed all the feature gaps we had flagged with RetainIQ.",
    "After two years we decided to consolidate our tools and RetainIQ did not make the final cut.",
]

feedback_retained = [
    "Despite some issues the platform generally meets our needs and the team has adapted well.",
    "Support has improved recently and we are seeing more value from the Enterprise features.",
    "We are monitoring the situation but currently plan to renew pending the upcoming feature release.",
    "The onboarding was rough but once we were set up the product has been reliable.",
    "Our account manager has been excellent and that relationship keeps us with RetainIQ.",
    "We evaluated alternatives but the switching cost and migration risk outweighed the benefits.",
    "Recent product updates have addressed several of our key concerns from last quarter.",
]

feedback_at_risk = [
    "We are currently evaluating alternatives and will decide at the next renewal in 60 days.",
    "Unless pricing improves at renewal we will likely not continue past this contract period.",
    "The product has potential but we need to see significant support improvements to stay.",
    "We have submitted a list of critical feature requests. If unaddressed we will reconsider.",
    "Our team satisfaction with the platform has dropped significantly over the past quarter.",
    "We are on the fence. A proactive outreach from our account team would help retain us.",
    "Pricing transparency needs to improve or we will explore other options at renewal.",
]

def get_feedback(churn_status, pain_cat):
    if churn_status == "Retained":
        return random.choice(feedback_retained)
    elif churn_status == "At-Risk":
        return random.choice(feedback_at_risk + feedback_at_risk)
    else:
        mapping = {
            "Product Quality":      feedback_product,
            "Customer Support":     feedback_support,
            "Pricing & Value":      feedback_pricing,
            "Onboarding & Usability": feedback_onboarding,
            "Competitor Switch":    feedback_competitor,
        }
        return random.choice(mapping[pain_cat])

# ── Build dataset ─────────────────────────────────────────────────────────

rows = []
for i in range(1, N + 1):

    churn = np.random.choice(churn_stats, p=[0.47, 0.30, 0.23])
    tier  = np.random.choice(tiers, p=[0.42, 0.38, 0.20])

    # Tenure: churned customers tend to leave earlier or after a long time
    if churn == "Churned":
        tenure = int(np.random.choice(
            [np.random.randint(1,7), np.random.randint(12,36)],
            p=[0.55, 0.45]))
    elif churn == "At-Risk":
        tenure = np.random.randint(3, 24)
    else:
        tenure = np.random.randint(6, 48)

    # Pain point — retained customers have lower severity issues
    if churn == "Churned":
        pain = np.random.choice(pain_cats, p=[0.28, 0.25, 0.22, 0.15, 0.10])
    elif churn == "At-Risk":
        pain = np.random.choice(pain_cats, p=[0.25, 0.28, 0.25, 0.15, 0.07])
    else:
        pain = np.random.choice(pain_cats, p=[0.20, 0.22, 0.28, 0.20, 0.10])

    # Satisfaction at exit: churned = low, at-risk = moderate, retained = higher
    if churn == "Churned":
        sat = np.random.choice([1, 2, 3], p=[0.45, 0.40, 0.15])
    elif churn == "At-Risk":
        sat = np.random.choice([2, 3, 4], p=[0.35, 0.45, 0.20])
    else:
        sat = np.random.choice([3, 4, 5], p=[0.20, 0.50, 0.30])

    # Repurchase intent: churned = low, at-risk = moderate, retained = high
    if churn == "Churned":
        repurchase = np.random.choice([1, 2, 3], p=[0.50, 0.35, 0.15])
    elif churn == "At-Risk":
        repurchase = np.random.choice([2, 3, 4], p=[0.30, 0.45, 0.25])
    else:
        repurchase = np.random.choice([3, 4, 5], p=[0.15, 0.45, 0.40])

    # Win-back receptiveness: only relevant for churned
    if churn == "Churned":
        # More likely if repurchase intent >= 2 and pain is pricing
        if repurchase >= 2 and pain in ["Pricing & Value", "Onboarding & Usability"]:
            winback = np.random.choice(["Yes", "No"], p=[0.65, 0.35])
        else:
            winback = np.random.choice(["Yes", "No"], p=[0.30, 0.70])
    elif churn == "At-Risk":
        winback = np.random.choice(["Yes", "No"], p=[0.75, 0.25])
    else:
        winback = "N/A"

    # Support tickets: proxy for engagement / frustration level
    if pain == "Customer Support":
        tickets = np.random.randint(4, 15)
    elif churn == "Churned":
        tickets = np.random.randint(2, 8)
    else:
        tickets = np.random.randint(0, 5)

    # MRR by tier (monthly recurring revenue)
    mrr_map = {"Basic": np.random.randint(49, 100),
               "Pro":   np.random.randint(149, 300),
               "Enterprise": np.random.randint(499, 1200)}
    mrr = mrr_map[tier]

    rows.append({
        "customer_id":              f"C{str(i).zfill(4)}",
        "churn_status":             churn,
        "subscription_tier":        tier,
        "tenure_months":            tenure,
        "industry":                 np.random.choice(industries, p=[0.28,0.22,0.18,0.20,0.12]),
        "company_size":             np.random.choice(company_sizes, p=[0.25,0.35,0.25,0.15]),
        "region":                   np.random.choice(regions, p=[0.25,0.22,0.30,0.23]),
        "primary_pain_point":       pain,
        "satisfaction_at_exit":     sat,
        "repurchase_intent":        repurchase,
        "win_back_receptive":       winback,
        "support_tickets_filed":    tickets,
        "recommended_to_others":    np.random.choice(["Yes","No"],
                                        p=[0.70,0.30] if churn=="Retained"
                                        else ([0.35,0.65] if churn=="At-Risk" else [0.15,0.85])),
        "monthly_recurring_revenue": mrr,
        "open_ended_feedback":      get_feedback(churn, pain),
    })

df = pd.DataFrame(rows)
df.to_csv("/home/claude/voice-of-customer-voc-analysis/data/voc_survey_data.csv", index=False)

print(f"Dataset generated: {len(df)} respondents")
print("\nChurn status distribution:")
print(df["churn_status"].value_counts())
print("\nPain point distribution (Churned only):")
print(df[df["churn_status"]=="Churned"]["primary_pain_point"].value_counts())
print("\nAvg repurchase intent by churn status:")
print(df.groupby("churn_status")["repurchase_intent"].mean().round(2))
total_mrr_at_risk = df[df["churn_status"].isin(["Churned","At-Risk"])]["monthly_recurring_revenue"].sum()
print(f"\nTotal MRR at risk: ${total_mrr_at_risk:,}/month (${total_mrr_at_risk*12:,} annualized)")
