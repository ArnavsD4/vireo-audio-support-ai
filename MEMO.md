# Memo — Vireo Audio Support Headcount

**To:** Priya Raman, Head of Customer Experience  
**Subject:** 18-month support-volume headcount recommendation

## Recommendation

Under Vireo's stated rule — **the team with the highest ticket volume receives the next two hires** — the data supports assigning the two hires to **Chat Frontline**.

Across the Jan 2025–Jun 2026 analysis window, there are **11,641 tickets**.

Among Tier 1 teams:

| Rank | Team | Tickets | Share |
|---|---|---:|---:|
| 1 | **Chat Frontline** | **3,030** | **26.0%** |
| 2 | Billing | 2,425 | 20.8% |
| 3 | Logistics | 1,905 | 16.4% |
| 4 | Email Frontline | 1,807 | 15.5% |
| 5 | Returns Desk | 1,049 | 9.0% |
| 6 | Voice Frontline | 900 | 7.7% |

Therefore, **Chat Frontline is the highest-volume Tier 1 team** and should receive the next two hires under the requested decision rule.

This does not support the earlier expectation that Billing would be the largest queue. Billing ranks second in the 18-month data.

## Business case

The email thread states that two hires would cost approximately **₹9 lakh per year**.

The recommendation therefore allocates that staffing investment to the Tier 1 team with the highest observed support volume rather than to Billing based on an initial assumption.

Chat Frontline handled **3,030 tickets**, which is:

- **605 more tickets than Billing**
- approximately **5.2 percentage points higher share of Tier 1 volume**

This provides a direct volume-based justification for the requested hiring decision.

## Important operational caveat

The support policy states that **Tier 2 / Escalations & Warranty should not be compared with Tier 1 teams on ticket-volume metrics**.

Therefore, `Escalations & Warranty` is excluded from the hiring ranking.

Logistics is also a meaningful operational concern because it handled **1,905 tickets (16.4%)** and the email thread highlights resolution-time and hand-off concerns.

However, the requested hiring rule is explicitly volume-based, so Logistics is a secondary operational finding rather than the final hiring recommendation.

## How the tool works

1. Load the support-ticket export and agent roster.
2. Restrict the business analysis to **Jan 2025–Jun 2026**.
3. Combine the customer's opening message with the agent's closing notes.
4. Train a lightweight **TF-IDF + Logistic Regression** classifier on the existing ticket categories.
5. Generate an AI-assisted category for each ticket.
6. Resolve the valid agent roster row at the ticket's creation date.
7. Produce monthly category/team volumes.
8. Exclude Tier 2 from the Tier 1 volume ranking.
9. Export validation and data-quality outputs.

## Validation

The classifier was evaluated in two ways.

### Existing-tag hold-out

A stratified 20% hold-out set was used to measure agreement with the existing category tags.

- Analysis tickets: **11,641**
- Training rows: **9,312**
- Hold-out rows: **2,329**
- Existing-tag agreement: **83.7%**

The existing `category` field is an intake/agent tag rather than independently verified ground truth. Therefore, 83.7% represents agreement with the current tagging system, not definitive real-world accuracy.

### Manual audit

A 100-ticket audit sample was reviewed separately.

- Audit sample: **100 tickets**
- Model/analyst agreement: **86/100**
- Manual audit agreement: **86.0%**

This is reported as an **analyst audit result**, not as an independently established gold-standard accuracy benchmark.

The audit was kept separate from model training and was used for evaluation and error analysis.

## Data-quality considerations

The source export contains several important limitations:

- Tickets outside the Jan 2025–Jun 2026 analysis window are excluded from the business analysis.
- Missing `transfers` values should not automatically be interpreted as zero because transfer history was unavailable for part of the source system history.
- Blank CSAT values represent tickets without a CSAT response rather than a score of zero.
- The existing category labels may contain noise; the model should therefore not be treated as reproducing independently verified truth.
- The `Other` category is heterogeneous and is more difficult for the classifier to predict consistently.

## AI / implementation choice

The submitted implementation deliberately uses a local **TF-IDF + Logistic Regression** model rather than a paid LLM API.

This keeps the tool:

- reproducible
- inexpensive to run
- independent of API keys
- suitable for a small batch-analysis workflow

The implementation produces the same outputs from the same input data and fixed random seed.

## Cost

The submitted classifier runs locally using scikit-learn.

**Incremental API/model cost per run: ₹0.**

This excludes the user's own machine/runtime costs.

## Final decision

Based on the stated volume-based hiring rule:

> **Assign the next two hires to Chat Frontline.**

The recommendation is supported by **3,030 Tier 1 tickets (26.0%)**, the highest volume among the eligible Tier 1 teams in the 18-month analysis window.