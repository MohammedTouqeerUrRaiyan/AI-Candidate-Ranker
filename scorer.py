from typing import List, Dict, Any
from parsers import flatten_candidate, candidate_to_text
from matchers import Matcher
from evaluators import Evaluators
from llm_ranker import LLMRanker


class Scorer:
    def __init__(self):
        self.matcher = Matcher()
        self.evaluators = Evaluators()
        self.llm_ranker = LLMRanker(use_llm=False)

    def _extract_job_skills(self, job_text: str) -> List[str]:
        keywords = [
            "business analyst", "product analyst", "product manager",
            "jira", "scrum", "agile", "user stories", "qa",
            "stakeholder management", "requirements", "testing",
            "collaboration", "communication", "cross-functional"
        ]
        text = job_text.lower()
        return [k for k in keywords if k in text]

    def score_candidate(self, job_text: str, record: Dict[str, Any]) -> Dict[str, Any]:
        candidate = flatten_candidate(record)
        candidate_text = candidate_to_text(candidate)
        job_skills = self._extract_job_skills(job_text)

        semantic_score = self.matcher.semantic_score(job_text, candidate_text)
        skill_overlap = self.matcher.skill_overlap_score(job_skills, candidate.get("skills", []))

        skill_eval = self.evaluators.skill_score(job_skills, candidate.get("skills", []))
        experience_eval = self.evaluators.experience_score(
            candidate.get("career_history", []),
            ["business analyst", "product analyst", "product manager", "scrum master", "qa", "agile"]
        )
        signal_eval = self.evaluators.signal_score(candidate.get("signals", {}))
        cert_eval = self.evaluators.certification_score(candidate.get("certifications", []))
        lang_eval = self.evaluators.language_score(candidate.get("languages", []))

        evaluator_score = self.evaluators.weighted_score(
            {
                "skill": skill_eval,
                "experience": experience_eval,
                "signals": signal_eval,
                "cert": cert_eval,
                "lang": lang_eval,
            },
            {
                "skill": 0.35,
                "experience": 0.30,
                "signals": 0.15,
                "cert": 0.10,
                "lang": 0.10,
            }
        )

        base_score = (
            0.55 * semantic_score +
            0.15 * skill_overlap +
            0.30 * evaluator_score
        )

        llm_result = self.llm_ranker.rank(
            job_text=job_text,
            candidate_text=candidate_text,
            base_score=base_score,
            metadata={
                "title": candidate.get("current_title", ""),
                "skills": [s.get("name", "") if isinstance(s, dict) else str(s) for s in candidate.get("skills", [])],
                "signals": candidate.get("signals", {})
            }
        )

        return {
            "candidate_id": candidate.get("candidate_id"),
            "name": candidate.get("name", ""),
            "current_title": candidate.get("current_title", ""),
            "current_company": candidate.get("current_company", ""),
            "location": candidate.get("location", ""),
            "semantic_score": round(semantic_score, 4),
            "skill_overlap_score": round(skill_overlap, 4),
            "evaluator_score": round(evaluator_score, 4),
            "final_score": round(llm_result.score, 4),
            "rationale": llm_result.rationale,
        }

    def rank_candidates(self, job_text: str, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        scored = [self.score_candidate(job_text, r) for r in records]
        scored.sort(key=lambda x: x["final_score"], reverse=True)
        return scored