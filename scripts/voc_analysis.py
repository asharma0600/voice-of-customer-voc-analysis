"""
Voice of Customer (VoC) Analysis
RetainIQ SaaS | Customer Churn & Retention Research Study
Author: Alisha Sharma
GitHub: https://github.com/asharma0600/voice-of-customer-voc-analysis

Research objectives:
  1. Identify the primary pain points driving customer churn
  2. Score exit feedback sentiment using VADER
  3. Quantify repurchase intent and win-back opportunity by segment
  4. Size the recoverable revenue opportunity
  5. Deliver prioritized retention recommendations
"""

import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

df = pd.read_csv("data/voc_survey_data.csv")
print(f"Loaded {len(df)} VoC survey respondents\n")

analyzer = SentimentIntensityAnalyzer()

def sentiment_score(text):
    return analyzer.polarity_scores(str(text))["compound"]

def sentiment_label(score):
    if score >= 0.05:    return "Positive"
    elif score <= -0.05: return "Negative"
    else:                return "Neutral"

df["sentiment_score"]    = df["open_ended_feedback"].apply(sentiment_score)
df["sentiment_category"] = df["sentiment_score"].apply(sentiment_label)

# ── 1. Study Overview ─────────────────────────────────────────────────────

churned  = df[df["churn_status"] == "Churned"]
at_risk  = df[df["churn_status"] == "At-Risk"]
retained = df[df["churn_status"] == "Retained"]

print("=" * 62)
print("RETAINIQ VOC STUDY — EXECUTIVE SUMMARY")
print("=" * 62)
print(f"Total Respondents    : {len(df)}")
print(f"Churned Customers    : {len(churned)} ({round(len(churned)/len(df)*100,1)}%)")
print(f"At-Risk Customers    : {len(at_risk)} ({round(len(at_risk)/len(df)*100,1)}%)")
print(f"Retained Customers   : {len(retained)} ({round(len(retained)/len(df)*100,1)}%)")
print()

total_mrr_lost = churned["monthly_recurring_revenue"].sum()
total_mrr_risk = at_risk["monthly_recurring_revenue"].sum()
winback_df     = churned[churned["win_back_receptive"] == "Yes"]
winback_mrr    = winback_df["monthly_recurring_revenue"].sum()

print(f"MRR Lost (Churned)   : ${total_mrr_lost:,}/month (${total_mrr_lost*12:,} annualized)")
print(f"MRR At Risk          : ${total_mrr_risk:,}/month (${total_mrr_risk*12:,} annualized)")
print(f"Win-Back Opportunity : ${winback_mrr:,}/month (${winback_mrr*12:,} annualized)")
print(f"Win-Back Rate        : {round(len(winback_df)/len(churned)*100,1)}% of churned customers receptive")

# ── 2. Pain Point Analysis ────────────────────────────────────────────────

print("\n" + "=" * 62)
print("PAIN POINT ANALYSIS — ALL CHURNED CUSTOMERS")
print("=" * 62)
print(f"{'Pain Point':<26} {'Count':>6} {'%':>6} {'Avg Sat':>8} {'Avg Repurchase':>15} {'Neg Sentiment%':>15}")
print("-" * 80)

pain_order = churned["primary_pain_point"].value_counts().index
for pain in pain_order:
    s    = churned[churned["primary_pain_point"] == pain]
    neg  = round(len(s[s["sentiment_category"]=="Negative"])/len(s)*100,1)
    print(f"{pain:<26} {len(s):>6} {str(round(len(s)/len(churned)*100,1))+'%':>6} "
          f"{round(s['satisfaction_at_exit'].mean(),2):>8} "
          f"{round(s['repurchase_intent'].mean(),2):>15} {str(neg)+'%':>15}")

# ── 3. Sentiment Analysis ─────────────────────────────────────────────────

print("\n" + "=" * 62)
print("EXIT FEEDBACK SENTIMENT BY CHURN STATUS")
print("=" * 62)
for status in ["Churned", "At-Risk", "Retained"]:
    s   = df[df["churn_status"] == status]
    pos = len(s[s["sentiment_category"]=="Positive"])
    neg = len(s[s["sentiment_category"]=="Negative"])
    neu = len(s[s["sentiment_category"]=="Neutral"])
    avg = round(s["sentiment_score"].mean(), 3)
    print(f"\n  {status} (n={len(s)})")
    print(f"    Positive : {pos} ({round(pos/len(s)*100,1)}%)")
    print(f"    Neutral  : {neu} ({round(neu/len(s)*100,1)}%)")
    print(f"    Negative : {neg} ({round(neg/len(s)*100,1)}%)")
    print(f"    Avg Sentiment Score: {avg}")

# ── 4. Repurchase Intent & Win-Back Opportunity ───────────────────────────

print("\n" + "=" * 62)
print("REPURCHASE INTENT & WIN-BACK OPPORTUNITY BY TIER")
print("=" * 62)
print(f"{'Tier':<12} {'Churned':>8} {'Win-Back%':>10} {'Win-Back MRR':>14} {'Annualized':>12}")
print("-" * 60)
for tier in ["Basic", "Pro", "Enterprise"]:
    c   = churned[churned["subscription_tier"] == tier]
    wb  = c[c["win_back_receptive"] == "Yes"]
    mrr = wb["monthly_recurring_revenue"].sum()
    pct = round(len(wb)/len(c)*100,1) if len(c) > 0 else 0
    print(f"{tier:<12} {len(c):>8} {str(pct)+'%':>10} ${mrr:>12,} ${mrr*12:>10,}")

# ── 5. Satisfaction by Pain Point ─────────────────────────────────────────

print("\n" + "=" * 62)
print("SATISFACTION & SENTIMENT SEVERITY BY PAIN POINT")
print("(Sorted by severity — most urgent first)")
print("=" * 62)
pain_summary = churned.groupby("primary_pain_point").agg(
    count=("customer_id","count"),
    avg_satisfaction=("satisfaction_at_exit","mean"),
    avg_repurchase=("repurchase_intent","mean"),
    avg_sentiment=("sentiment_score","mean"),
    mrr_lost=("monthly_recurring_revenue","sum")
).round(2).sort_values("avg_satisfaction")

for pain, row in pain_summary.iterrows():
    print(f"\n  {pain}")
    print(f"    Customers affected : {int(row['count'])}")
    print(f"    Avg satisfaction   : {row['avg_satisfaction']} / 5.0")
    print(f"    Avg repurchase     : {row['avg_repurchase']} / 5.0")
    print(f"    Avg sentiment score: {row['avg_sentiment']}")
    print(f"    MRR lost           : ${int(row['mrr_lost']):,}/month")

# ── 6. Tenure Analysis ────────────────────────────────────────────────────

print("\n" + "=" * 62)
print("CHURN BY TENURE — WHEN DO CUSTOMERS LEAVE?")
print("=" * 62)
def tenure_band(m):
    if m <= 3:   return "0-3 months"
    elif m <= 6: return "4-6 months"
    elif m <= 12: return "7-12 months"
    elif m <= 24: return "13-24 months"
    else:        return "25+ months"

churned["tenure_band"] = churned["tenure_months"].apply(tenure_band)
tenure_order = ["0-3 months","4-6 months","7-12 months","13-24 months","25+ months"]
tc = churned["tenure_band"].value_counts()
for band in tenure_order:
    count = tc.get(band, 0)
    pain = churned[churned["tenure_band"]==band]["primary_pain_point"].value_counts()
    top_pain = pain.index[0] if len(pain) > 0 else "N/A"
    print(f"  {band:<15}: {count:>3} customers | Top issue: {top_pain}")

# ── 7. Industry Breakdown ─────────────────────────────────────────────────

print("\n" + "=" * 62)
print("CHURN RATE BY INDUSTRY")
print("=" * 62)
for ind in df["industry"].unique():
    total_ind = df[df["industry"]==ind]
    churn_ind = total_ind[total_ind["churn_status"]=="Churned"]
    rate = round(len(churn_ind)/len(total_ind)*100,1)
    top_pain = churn_ind["primary_pain_point"].value_counts()
    tp = top_pain.index[0] if len(top_pain) > 0 else "N/A"
    print(f"  {ind:<12}: {rate}% churn rate | Top pain point: {tp}")

# ── 8. Export ─────────────────────────────────────────────────────────────

df.to_csv("data/voc_analysis_output.csv", index=False)
print("\n" + "=" * 62)
print("OUTPUT SAVED: data/voc_analysis_output.csv")
print("=" * 62)
