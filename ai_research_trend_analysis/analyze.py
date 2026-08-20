from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent
DATA = BASE / "data" / "ai_landscape.csv"
REPORTS = BASE / "reports"

def main():
    REPORTS.mkdir(exist_ok=True)
    df = pd.read_csv(DATA)

    df["opportunity_score"] = (
        df["usability"] * 0.20
        + df["technical_maturity"] * 0.25
        + (6 - df["implementation_effort"]) * 0.15
        + df["impact_potential"] * 0.40
    )

    top = df.sort_values("opportunity_score", ascending=False).head(5)
    theme_summary = (
        df.groupby("theme")
        .agg(
            opportunities=("solution", "count"),
            average_score=("opportunity_score", "mean"),
            average_impact=("impact_potential", "mean"),
        )
        .sort_values("average_score", ascending=False)
    )

    report = [
        "# AI Trend Analysis Report",
        "",
        "## Executive Summary",
        "",
        "This portfolio analysis compares a small, transparent set of AI opportunity examples "
        "across multiple sectors. The scoring model balances usability, technical maturity, "
        "implementation effort and potential impact.",
        "",
        "## Top Opportunities",
        "",
        top[["source","sector","theme","solution","opportunity_score"]].round(2).to_string(index=False),
        "",
        "## Theme Summary",
        "",
        theme_summary.round(2).to_string(),
        "",
        "## Recommended Next Experiments",
        "",
        "1. Prototype a retrieval-augmented education assistant on a small curated knowledge base.",
        "2. Validate computer-vision quality on a labeled fashion dataset before deployment.",
        "3. Benchmark conversational-AI latency and response quality across model configurations.",
        "4. Add human review checkpoints for high-impact educational recommendations.",
        "5. Track user feedback as an explicit evaluation signal alongside technical metrics.",
        "",
        "## Limitations",
        "",
        "The dataset is a small portfolio dataset, not a statistically representative market sample."
    ]

    output = REPORTS / "ai_trend_report.md"
    output.write_text("\n".join(report), encoding="utf-8")
    print(f"Generated: {output}")

if __name__ == "__main__":
    main()
