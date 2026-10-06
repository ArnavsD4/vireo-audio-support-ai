# Vireo Audio Support AI — Submission Form Draft

## 1. What did you build?

I built a small, reproducible support-analytics tool that analyzes Vireo Audio support tickets over the Jan 2025–Jun 2026 period.

The tool:

- filters tickets to the required 18-month analysis window
- combines customer messages and agent notes
- uses a local TF-IDF + Logistic Regression classifier to generate AI-assisted issue categories
- joins tickets to the valid agent roster at the ticket creation date
- produces monthly category/team ticket volumes
- ranks Tier 1 teams by ticket volume
- excludes Tier 2 / Escalations & Warranty from the Tier 1 hiring comparison
- exports validation and data-quality outputs

The resulting business recommendation is to assign the next two hires to **Chat Frontline**.

---

## 2. What was the business outcome?

The analysis covers **11,641 tickets** from Jan 2025 through Jun 2026.

Among Tier 1 teams:

| Team | Tickets | Share |
|---|---:|---:|
| Chat Frontline | 3,030 | 26.0% |
| Billing | 2,425 | 20.8% |
| Logistics | 1,905 | 16.4% |
| Email Frontline | 1,807 | 15.5% |
| Returns Desk | 1,049 | 9.0% |
| Voice Frontline | 900 | 7.7% |

Under the client's stated rule that the highest-volume eligible team receives the next two hires, **Chat Frontline is the recommended team**.

The email thread states that two hires cost approximately **₹9 lakh/year**.

---

## 3. How did you use AI?

I used a local machine-learning text classification pipeline:

**TF-IDF + Logistic Regression**

The model uses:

`customer_message + agent_notes`

as its input text and predicts one of the existing support categories.

I chose a local model rather than a paid LLM API because the task can be completed reproducibly without API keys or token costs.

---

## 4. How did you validate it?

Two forms of validation were used.

### Existing-tag hold-out

A stratified 20% hold-out set was used to measure agreement with the existing category tags.

- Training rows: 9,312
- Hold-out rows: 2,329
- Agreement with existing tags: **83.7%**

This is agreement with the existing tagging system, not independently verified real-world accuracy.

### Manual audit

A separate 100-ticket analyst audit was used for an additional quality check.

- Audit sample: 100 tickets
- Agreement: **86/100**
- Manual audit agreement: **86.0%**

This is reported as an analyst audit result rather than an independently established gold-standard benchmark.

The audit sample was not used to train the model.

---

## 5. What are the main limitations?

The most important limitation is that the source `category` field is an intake/agent tag and may contain incorrect or inconsistent labels.

Other limitations include:

- the manual audit contains only 100 tickets
- the `Other` category is heterogeneous and harder to classify consistently
- this is a lightweight batch-analysis tool rather than a production real-time routing system
- transfer data is missing for a substantial portion of historical tickets and should not be interpreted as zero
- blank CSAT values represent no response rather than a zero score

A production version should maintain a manually reviewed gold-standard dataset and monitor model performance over time.

---

## 6. Why did you exclude Escalations & Warranty?

The support policy states that Tier 2 / Escalations & Warranty should not be compared with Tier 1 teams using ticket-volume metrics.

Therefore, it was excluded from the Tier 1 hiring ranking.

---

## 7. What did you intentionally not build?

I kept the implementation focused on the decision requested in the assignment.

I did not build:

- a real-time production API
- a dashboard
- a paid LLM integration
- an MLOps pipeline
- automated ticket routing
- a cloud deployment

The goal was to produce a small, reproducible working analysis that directly supports the headcount decision.

---

## 8. Cost

The submitted classifier runs locally using scikit-learn.

**Incremental API/model cost per run: ₹0.**

No paid LLM API or external inference service is required.

---

## 9. How can the reviewer reproduce it?

From the project root:

```bash
python app.py --tickets tickets.csv --agents agents.csv --validation validation_review_100_completed_final.csv --out output