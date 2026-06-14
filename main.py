from pathlib import Path
import json
import pandas as pd

from parsers import load_job_description
from scorer import Scorer

DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def save_ranked_output(ranked_candidates, output_path):
    rows = []
    for i, c in enumerate(ranked_candidates, start=1):
        rows.append({
            "candidate_id": c["candidate_id"],
            "rank": i,
            "score": round(c["final_score"], 4),
            "reasoning": c["rationale"],
        })

    pd.DataFrame(rows).to_csv(output_path, index=False)


def main():

    print("Program started")

    candidates_path = DATA_DIR / "sample_candidates.json"
    job_path = DATA_DIR / "job_description.docx"

    print("Loading candidates...")
    with open(candidates_path, "r", encoding="utf-8") as f:
        candidates = json.load(f)

    print(f"Loaded {len(candidates)} candidates")

    print("Loading job description...")
    job_text = load_job_description(str(job_path))

    print("Initializing scorer...")
    scorer = Scorer()

    print("Ranking candidates...")
    ranked = scorer.rank_candidates(job_text, candidates)

    print("Saving results...")
    save_ranked_output(
        ranked,
        OUTPUT_DIR / "sample_submission.csv"
    )

    print("\nTop 5 candidates:")
    for r in ranked[:5]:
        print(
            r["candidate_id"],
            r["name"],
            r["final_score"]
        )


if __name__ == "__main__":
    main()