-- ============================================================
-- Voice of Customer (VoC) Analysis — SQL Queries
-- RetainIQ SaaS | Customer Churn & Retention Research Study
-- Author: Alisha Sharma
-- Table: voc_survey (loaded from voc_analysis_output.csv)
-- ============================================================


-- ── 1. Study Overview ─────────────────────────────────────────────────────

SELECT
    COUNT(*)                                                                        AS total_respondents,
    SUM(CASE WHEN churn_status = 'Churned'  THEN 1 ELSE 0 END)                     AS churned,
    SUM(CASE WHEN churn_status = 'At-Risk'  THEN 1 ELSE 0 END)                     AS at_risk,
    SUM(CASE WHEN churn_status = 'Retained' THEN 1 ELSE 0 END)                     AS retained,
    ROUND(SUM(CASE WHEN churn_status = 'Churned' THEN monthly_recurring_revenue
              ELSE 0 END), 0)                                                       AS mrr_lost_monthly,
    ROUND(SUM(CASE WHEN churn_status = 'At-Risk' THEN monthly_recurring_revenue
              ELSE 0 END), 0)                                                       AS mrr_at_risk_monthly,
    ROUND(AVG(CASE WHEN churn_status = 'Churned' THEN satisfaction_at_exit END),2) AS avg_exit_satisfaction,
    ROUND(AVG(CASE WHEN churn_status = 'Churned' THEN repurchase_intent END),2)    AS avg_repurchase_intent
FROM voc_survey;


-- ── 2. Pain Point Frequency & Severity ───────────────────────────────────

SELECT
    primary_pain_point,
    COUNT(*)                                                                        AS customers_affected,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1)                             AS pct_of_churned,
    ROUND(AVG(satisfaction_at_exit), 2)                                            AS avg_satisfaction,
    ROUND(AVG(repurchase_intent), 2)                                               AS avg_repurchase_intent,
    ROUND(AVG(sentiment_score), 3)                                                 AS avg_sentiment_score,
    SUM(monthly_recurring_revenue)                                                 AS mrr_lost,
    ROUND(
        SUM(CASE WHEN sentiment_category = 'Negative' THEN 1.0 ELSE 0 END)
        / COUNT(*) * 100, 1)                                                       AS pct_negative_feedback
FROM voc_survey
WHERE churn_status = 'Churned'
GROUP BY primary_pain_point
ORDER BY avg_satisfaction ASC;


-- ── 3. Win-Back Opportunity by Subscription Tier ─────────────────────────

SELECT
    subscription_tier,
    COUNT(*)                                                                        AS churned_customers,
    SUM(CASE WHEN win_back_receptive = 'Yes' THEN 1 ELSE 0 END)                   AS win_back_receptive,
    ROUND(
        SUM(CASE WHEN win_back_receptive = 'Yes' THEN 1.0 ELSE 0 END)
        / COUNT(*) * 100, 1)                                                       AS win_back_rate_pct,
    SUM(CASE WHEN win_back_receptive = 'Yes'
        THEN monthly_recurring_revenue ELSE 0 END)                                 AS recoverable_mrr,
    SUM(CASE WHEN win_back_receptive = 'Yes'
        THEN monthly_recurring_revenue * 12 ELSE 0 END)                           AS recoverable_arr,
    ROUND(AVG(repurchase_intent), 2)                                               AS avg_repurchase_intent
FROM voc_survey
WHERE churn_status = 'Churned'
GROUP BY subscription_tier
ORDER BY recoverable_mrr DESC;


-- ── 4. Sentiment Distribution by Churn Status ────────────────────────────

SELECT
    churn_status,
    COUNT(*)                                                                        AS total,
    SUM(CASE WHEN sentiment_category = 'Positive' THEN 1 ELSE 0 END)              AS positive,
    SUM(CASE WHEN sentiment_category = 'Neutral'  THEN 1 ELSE 0 END)              AS neutral,
    SUM(CASE WHEN sentiment_category = 'Negative' THEN 1 ELSE 0 END)              AS negative,
    ROUND(AVG(sentiment_score), 3)                                                 AS avg_sentiment_score,
    ROUND(
        SUM(CASE WHEN sentiment_category = 'Negative' THEN 1.0 ELSE 0 END)
        / COUNT(*) * 100, 1)                                                       AS pct_negative
FROM voc_survey
GROUP BY churn_status
ORDER BY avg_sentiment_score ASC;


-- ── 5. Churn Rate by Industry ─────────────────────────────────────────────

SELECT
    industry,
    COUNT(*)                                                                        AS total_customers,
    SUM(CASE WHEN churn_status = 'Churned'  THEN 1 ELSE 0 END)                    AS churned,
    SUM(CASE WHEN churn_status = 'At-Risk'  THEN 1 ELSE 0 END)                    AS at_risk,
    ROUND(
        SUM(CASE WHEN churn_status = 'Churned' THEN 1.0 ELSE 0 END)
        / COUNT(*) * 100, 1)                                                       AS churn_rate_pct,
    ROUND(AVG(satisfaction_at_exit), 2)                                            AS avg_satisfaction,
    ROUND(AVG(support_tickets_filed), 1)                                           AS avg_support_tickets
FROM voc_survey
GROUP BY industry
ORDER BY churn_rate_pct DESC;


-- ── 6. Tenure Analysis — When Do Customers Churn? ─────────────────────────

SELECT
    CASE
        WHEN tenure_months <= 3  THEN '0-3 months'
        WHEN tenure_months <= 6  THEN '4-6 months'
        WHEN tenure_months <= 12 THEN '7-12 months'
        WHEN tenure_months <= 24 THEN '13-24 months'
        ELSE '25+ months'
    END                                                                             AS tenure_band,
    COUNT(*)                                                                        AS churned_customers,
    ROUND(AVG(satisfaction_at_exit), 2)                                            AS avg_satisfaction,
    ROUND(AVG(support_tickets_filed), 1)                                           AS avg_support_tickets,
    SUM(monthly_recurring_revenue)                                                  AS mrr_lost
FROM voc_survey
WHERE churn_status = 'Churned'
GROUP BY tenure_band
ORDER BY MIN(tenure_months);


-- ── 7. At-Risk Customer Prioritization ───────────────────────────────────

SELECT
    customer_id,
    subscription_tier,
    industry,
    tenure_months,
    primary_pain_point,
    satisfaction_at_exit,
    repurchase_intent,
    support_tickets_filed,
    monthly_recurring_revenue,
    sentiment_category,
    open_ended_feedback
FROM voc_survey
WHERE churn_status = 'At-Risk'
    AND repurchase_intent >= 3
ORDER BY monthly_recurring_revenue DESC, repurchase_intent DESC
LIMIT 20;


-- ── 8. Support Ticket Volume by Pain Point ────────────────────────────────

SELECT
    primary_pain_point,
    ROUND(AVG(support_tickets_filed), 1)                                           AS avg_tickets,
    MAX(support_tickets_filed)                                                     AS max_tickets,
    SUM(support_tickets_filed)                                                     AS total_tickets,
    COUNT(*)                                                                        AS customers
FROM voc_survey
WHERE churn_status = 'Churned'
GROUP BY primary_pain_point
ORDER BY avg_tickets DESC;


-- ── 9. Recommended to Others — NPS Proxy ─────────────────────────────────

SELECT
    churn_status,
    SUM(CASE WHEN recommended_to_others = 'Yes' THEN 1 ELSE 0 END)               AS would_recommend,
    COUNT(*)                                                                       AS total,
    ROUND(
        SUM(CASE WHEN recommended_to_others = 'Yes' THEN 1.0 ELSE 0 END)
        / COUNT(*) * 100, 1)                                                       AS recommendation_rate_pct
FROM voc_survey
GROUP BY churn_status
ORDER BY recommendation_rate_pct DESC;
