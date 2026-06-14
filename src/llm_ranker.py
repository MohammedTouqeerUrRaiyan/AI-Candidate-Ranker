from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class LLMRankResult:
    score: float
    rationale: str

class LLMRanker:
    def __init__(self, use_llm: bool = False):
        self.use_llm = use_llm

    def build_prompt(self, job_text: str, candidate_text: str, base_score: float) -> str:
        return f"""
You are a recruiter-style ranking model.
Job:
{job_text}

Candidate:
{candidate_text}

Base score:
{base_score:.3f}

Return:
1. fit score from 0 to 1
2. short rationale
"""

    def rank(self, job_text: str, candidate_text: str, base_score: float, metadata: Dict[str, Any] = None) -> LLMRankResult:
        metadata = metadata or {}

        score = base_score
        rationale_parts = []

        title = metadata.get("title", "").lower()
        skills = [s.lower() for s in metadata.get("skills", [])]
        signals = metadata.get("signals", {})

        if any(k in title for k in ["business analyst", "product analyst", "product manager"]):
            score += 0.08
            rationale_parts.append("Relevant role title")

        if any(k in skills for k in ["jira", "agile", "scrum", "user stories", "qa"]):
            score += 0.10
            rationale_parts.append("Strong process and delivery skills")

        if signals.get("cross_functional", False):
            score += 0.05
            rationale_parts.append("Shows cross-functional collaboration")

        if signals.get("leadership", False):
            score += 0.03
            rationale_parts.append("Has leadership signals")

        score = max(0.0, min(1.0, score))

        if not rationale_parts:
            rationale_parts.append("Moderate semantic fit based on profile text")

        return LLMRankResult(score=score, rationale="; ".join(rationale_parts))