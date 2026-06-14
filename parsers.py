import json
from pathlib import Path
from typing import Dict, Any, List

try:
    import docx
except ImportError:
    docx = None


def load_jsonl(path: str) -> List[Dict[str, Any]]:
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_job_description(path: str) -> str:
    path = Path(path)

    if path.suffix.lower() == ".txt":
        return path.read_text(encoding="utf-8")

    if path.suffix.lower() == ".docx":
        if docx is None:
            raise ImportError("python-docx is required to read .docx files")
        document = docx.Document(str(path))
        return "\n".join(p.text for p in document.paragraphs if p.text.strip())

    raise ValueError(f"Unsupported job description format: {path.suffix}")


def _list_to_text(items: List[Any], key: str) -> str:
    parts = []
    for item in items or []:
        if isinstance(item, dict):
            parts.append(str(item.get(key, "")))
        else:
            parts.append(str(item))
    return " ".join(p for p in parts if p).strip()


def flatten_candidate(record: Dict[str, Any]) -> Dict[str, Any]:
    profile = record.get("profile", {}) or {}
    career_history = record.get("career_history", []) or []
    education = record.get("education", []) or []
    skills = record.get("skills", []) or []
    certifications = record.get("certifications", []) or []
    languages = record.get("languages", []) or []
    signals = record.get("redrob_signals", {}) or {}

    career_text_parts = []
    for item in career_history:
        if isinstance(item, dict):
            career_text_parts.extend([
                str(item.get("title", "")),
                str(item.get("company", "")),
                str(item.get("description", "")),
                str(item.get("summary", "")),
            ])

    education_text_parts = []
    for item in education:
        if isinstance(item, dict):
            education_text_parts.extend([
                str(item.get("degree", "")),
                str(item.get("institution", "")),
                str(item.get("field_of_study", "")),
                str(item.get("field", "")),
            ])

    skill_text = _list_to_text(skills, "name")
    cert_text = _list_to_text(certifications, "name")
    lang_text = _list_to_text(languages, "language")

    return {
        "candidate_id": record.get("candidate_id"),
        "name": profile.get("name", ""),
        "current_title": profile.get("title", ""),
        "current_company": profile.get("company", ""),
        "location": profile.get("location", ""),
        "summary": profile.get("summary", ""),
        "skills": skills,
        "skill_text": skill_text,
        "certifications": certifications,
        "cert_text": cert_text,
        "languages": languages,
        "lang_text": lang_text,
        "signals": signals,
        "career_history": career_history,
        "education": education,
        "career_text": " ".join(p for p in career_text_parts if p).strip(),
        "education_text": " ".join(p for p in education_text_parts if p).strip(),
    }


def candidate_to_text(candidate: Dict[str, Any]) -> str:
    parts = [
        candidate.get("name", ""),
        candidate.get("current_title", ""),
        candidate.get("current_company", ""),
        candidate.get("location", ""),
        candidate.get("summary", ""),
        candidate.get("skill_text", ""),
        candidate.get("cert_text", ""),
        candidate.get("lang_text", ""),
        candidate.get("career_text", ""),
        candidate.get("education_text", ""),
        json.dumps(candidate.get("signals", {}), ensure_ascii=False),
    ]
    return " ".join(p for p in parts if p).strip()


def build_job_profile(job_text: str) -> Dict[str, Any]:
    return {
        "text": job_text.strip(),
        "job_text": job_text.strip(),
    }


if __name__ == "__main__":
    records = load_jsonl("data/candidates.jsonl")
    print("Loaded:", len(records))
    sample = flatten_candidate(records[0])
    print(sample)
    print(candidate_to_text(sample)[:1000])