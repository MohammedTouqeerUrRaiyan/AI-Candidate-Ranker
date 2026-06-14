import json
import pandas as pd
from pathlib import Path

data_dir = Path("data")

# Load JSONL candidates
candidates_path = data_dir / "candidates.jsonl"
candidates = []
with open(candidates_path, "r", encoding="utf-8") as f:
    for line in f:
        candidates.append(json.loads(line))

print("Candidates loaded:", len(candidates))
print("First candidate keys:", candidates[0].keys())

# Inspect schema
schema_path = data_dir / "candidate_schema.json"
with open(schema_path, "r", encoding="utf-8") as f:
    schema = json.load(f)
print("Schema keys:", schema.keys())

# Inspect sample candidates if present
sample_path = data_dir / "sample_candidates.json"
if sample_path.exists():
    with open(sample_path, "r", encoding="utf-8") as f:
        sample_candidates = json.load(f)
    print("Sample candidates:", len(sample_candidates))

# Inspect sample submission if it is xlsx
sample_submission = data_dir / "sample_submission.xlsx"
if sample_submission.exists():
    df = pd.read_excel(sample_submission)
    print("Sample submission columns:", df.columns.tolist())
    print(df.head())

# Read job description text if it is .txt
job_txt = data_dir / "job_description.txt"
if job_txt.exists():
    job_description = job_txt.read_text(encoding="utf-8")
    print("Job description preview:", job_description[:500])