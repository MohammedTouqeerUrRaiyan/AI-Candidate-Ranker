from dataclasses import dataclass
from typing import Dict, Any
import os

@dataclass
class LLMRankResult:
    score: float
    rationale: str

class LLMRanker:
    def __init__(self, use_llm: bool = False):
        self.use_llm = use_llm
        if self.use_llm:
            # Initialize your LLM client or local pipeline here if use_llm is true
            # For example, using transformers, openai, or langchain
            pass

    def build_prompt(self, job_text: str, candidate_text: str, base_score: float) -> str:
        return f"""You are an elite technical recruiter ranking candidates for a specific job profile.

Job Description:
{job_text}

Candidate Profile:
{candidate_text}

Initial Base Score: {base_score:.3f}

Analyze the candidate against the job criteria. Provide:
1. An updated fit score from 0.00 to 1.00 based on true technical alignment.
2. A unique, specific, 1-sentence rationale explaining the exact match or missing gap.

Respond in this exact format:
SCORE: [score]
RATIONALE: [rationale]"""

    def rank(self, job_text: str, candidate_text: str, base_score: float, metadata: Dict[str, Any] = None) -> LLMRankResult:
        metadata = metadata or {}
        
        # If use_llm is enabled, we can use an actual model generation
        if self.use_llm:
            prompt = self.build_prompt(job_text, candidate_text, base_score)
            
            # --- PLACEHOLDER FOR YOUR MODEL INFERENCE ---
            # response = self.llm_pipeline(prompt) 
            # return self.parse_llm_response(response)
            # --------------------------------------------

        # Heuristic/Fallback Logic (Your original code)
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
            # FIXED: Made it dynamic by mentioning the specific matched skills
            matched_skills = [k for k in ["jira", "agile", "scrum", "user stories", "qa"] if k in skills]
            rationale_parts.append(f"Strong process and delivery skills (Matched: {', '.join(matched_skills)})")

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