"""
Vireo Audio Support AI — small, reproducible CLI.

Usage:
    python app.py --tickets tickets.csv --agents agents.csv --out output

Optional manual audit:
    python app.py --tickets tickets.csv --agents agents.csv \
        --validation validation_review_100_completed.csv --out output
"""

import argparse
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score


def main():
    p = argparse.ArgumentParser()

    p.add_argument("--tickets", required=True)
    p.add_argument("--agents", required=True)
    p.add_argument("--validation", default=None)
    p.add_argument("--out", default="output")

    args = p.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------
    # 1. Load data
    # ---------------------------------------------------------
    t = pd.read_csv(args.tickets)
    a = pd.read_csv(args.agents)

    t["created_at"] = pd.to_datetime(
        t["created_at"], errors="coerce"
    )

    a["from_date"] = pd.to_datetime(
        a["from_date"], errors="coerce"
    )

    a["to_date"] = pd.to_datetime(
        a["to_date"], errors="coerce"
    )

    # ---------------------------------------------------------
    # 2. Restrict analysis to Jan 2025 - Jun 2026
    # ---------------------------------------------------------
    t = t[
        (t["created_at"] >= "2025-01-01")
        & (t["created_at"] < "2026-07-01")
    ].copy()

    # ---------------------------------------------------------
    # 3. Build text used by classifier
    # ---------------------------------------------------------
    t["text"] = (
        t["customer_message"].fillna("").astype(str)
        + " "
        + t["agent_notes"].fillna("").astype(str)
    ).str.strip()

    # ---------------------------------------------------------
    # 4. Train / holdout split
    # ---------------------------------------------------------
    Xtr, Xte, ytr, yte = train_test_split(
        t["text"],
        t["category"],
        test_size=0.20,
        random_state=42,
        stratify=t["category"]
    )

    # ---------------------------------------------------------
    # 5. TF-IDF + Logistic Regression classifier
    # ---------------------------------------------------------
    model = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                ngram_range=(1, 2),
                min_df=2,
                max_features=50000,
                sublinear_tf=True,
                strip_accents="unicode"
            )
        ),
        (
            "clf",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced"
            )
        )
    ])

    model.fit(Xtr, ytr)

    # ---------------------------------------------------------
    # 6. Existing-tag holdout agreement
    # ---------------------------------------------------------
    pred = model.predict(Xte)

    existing_tag_agreement = accuracy_score(yte, pred)

    print(
        f"Agreement with existing category tags: "
        f"{existing_tag_agreement:.1%}"
    )

    # ---------------------------------------------------------
    # 7. Predict categories for all analysis tickets
    # ---------------------------------------------------------
    t["ai_category"] = model.predict(t["text"])

    # Confidence score
    probabilities = model.predict_proba(t["text"])
    t["ai_confidence"] = probabilities.max(axis=1)

    t["month"] = (
        t["created_at"]
        .dt.to_period("M")
        .astype(str)
    )

    # ---------------------------------------------------------
    # 8. Optional manual validation
    # ---------------------------------------------------------
    validation_summary = []

    if args.validation:
        validation_path = Path(args.validation)

        if not validation_path.exists():
            raise FileNotFoundError(
                f"Validation file not found: {validation_path}"
            )

        v = pd.read_csv(validation_path)

        required_columns = {
            "ticket_id",
            "ai_category",
            "reviewed_category"
        }

        missing = required_columns - set(v.columns)

        if missing:
            raise ValueError(
                "Validation file is missing columns: "
                + ", ".join(sorted(missing))
            )

        # Use the model's current predictions rather than trusting
        # the copied ai_category column in the audit file.
        model_predictions = t[
            ["ticket_id", "ai_category"]
        ].copy()

        audit = v[
            ["ticket_id", "reviewed_category"]
        ].merge(
            model_predictions,
            on="ticket_id",
            how="left"
        )

        audit = audit.dropna(
            subset=["reviewed_category", "ai_category"]
        )

        if len(audit) > 0:
            manual_audit_agreement = accuracy_score(
                audit["reviewed_category"],
                audit["ai_category"]
            )

            audit["correct"] = (
                audit["reviewed_category"]
                == audit["ai_category"]
            )

            validation_summary = pd.DataFrame([
                {
                    "metric": "Existing-tag holdout agreement",
                    "value": existing_tag_agreement,
                    "sample_size": len(Xte)
                },
                {
                    "metric": "Manual audit agreement",
                    "value": manual_audit_agreement,
                    "sample_size": len(audit)
                }
            ])

            validation_summary.to_csv(
                out / "validation_summary.csv",
                index=False
            )

            audit.to_csv(
                out / "validation_audit_results.csv",
                index=False
            )

            print(
                f"Manual audit agreement: "
                f"{manual_audit_agreement:.1%} "
                f"({len(audit)} tickets)"
            )

    # ---------------------------------------------------------
    # 9. Resolve valid agent roster row
    # ---------------------------------------------------------
    m = t.merge(
        a[
            [
                "agent_id",
                "team",
                "tier",
                "from_date",
                "to_date"
            ]
        ],
        on="agent_id",
        how="left"
    )

    m = m[
        (m["from_date"] <= m["created_at"])
        & (
            m["to_date"].isna()
            | (m["to_date"] >= m["created_at"])
        )
    ].copy()

    # ---------------------------------------------------------
    # 10. Exclude Tier 2 from volume-based hiring ranking
    # ---------------------------------------------------------
    tier1 = m[
        m["assigned_team"] != "Escalations & Warranty"
    ]

    summary = (
        tier1.groupby("assigned_team")
        .size()
        .reset_index(name="tickets")
        .sort_values("tickets", ascending=False)
    )

    summary["share_pct"] = (
        summary["tickets"] / len(tier1) * 100
    )

    print("\nTier 1 team ranking:")
    print(summary.to_string(index=False))

    print(
        f"\nRecommendation: "
        f"{summary.iloc[0]['assigned_team']} "
        f"receives the next two hires."
    )

    # ---------------------------------------------------------
    # 11. Export outputs
    # ---------------------------------------------------------
    m.drop(columns=["text"]).to_csv(
        out / "classified_tickets.csv",
        index=False
    )

    summary.to_csv(
        out / "team_summary.csv",
        index=False
    )

    (
        m.groupby(
            [
                "month",
                "assigned_team",
                "ai_category"
            ]
        )
        .size()
        .reset_index(name="ticket_volume")
        .to_csv(
            out / "monthly_category_team.csv",
            index=False
        )
    )


if __name__ == "__main__":
    main()