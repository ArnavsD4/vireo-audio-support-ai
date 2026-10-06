# Vireo Audio Support AI

Small, reproducible AI-assisted support analytics tool built for the Vireo Audio support headcount take-home assignment.

## Business objective

Vireo wants to decide which support team should receive the next two hires.

The stated decision rule is:

> The eligible team with the highest support-ticket volume receives the next two hires.

The analysis covers **Jan 2025–Jun 2026**.

## What the tool does

The tool:

1. Filters tickets to the required 18-month analysis window.
2. Combines `customer_message` and `agent_notes`.
3. Trains a lightweight **TF-IDF + Logistic Regression** text classifier.
4. Generates AI-assisted support categories.
5. Resolves the agent's team/tier using the roster valid at ticket creation.
6. Produces monthly category/team ticket volumes.
7. Excludes Tier 2 / `Escalations & Warranty` from the Tier 1 hiring comparison.
8. Ranks Tier 1 teams by ticket volume.
9. Produces validation and audit outputs.

## Result

The analysis contains **11,641 tickets**.

### Tier 1 team ranking

| Rank | Team | Tickets | Share |
|---|---|---:|---:|
| 1 | **Chat Frontline** | **3,030** | **26.0%** |
| 2 | Billing | 2,425 | 20.8% |
| 3 | Logistics | 1,905 | 16.4% |
| 4 | Email Frontline | 1,807 | 15.5% |
| 5 | Returns Desk | 1,049 | 9.0% |
| 6 | Voice Frontline | 900 | 7.7% |

### Recommendation

**Chat Frontline should receive the next two hires.**

Chat Frontline handled 3,030 tickets, the highest volume among eligible Tier 1 teams.

The email thread states that two hires would cost approximately **₹9 lakh/year**.

`Escalations & Warranty` is Tier 2 and is excluded from the volume comparison according to the support policy.

## AI approach

The classifier uses:

- Python
- pandas
- scikit-learn
- TF-IDF vectorization
- Logistic Regression

Input text:

```text
customer_message + agent_notes