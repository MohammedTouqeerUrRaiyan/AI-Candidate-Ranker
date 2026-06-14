from typing import Dict, List, Any


class Evaluators:
    def __init__(self):
        self.skill_keywords = {
            "business analyst": ["business analyst", "ba", "requirements", "user stories"],
            "product": ["product", "roadmap", "stakeholder", "discovery"],
            "agile": ["agile", "scrum", "sprint", "jira"],
            "qa": ["qa", "testing", "quality assurance", "test cases"],
            "communication": ["communication", "collaboration", "presentation", "stakeholder"],
        }

    def _normalize(self, item: Any) -> str:
        """Safe text normalization helper"""
        if isinstance(item, dict):
            return str(item.get("name", "")).lower().strip()
        return str(item).lower().strip()

    # ---------------- SKILL SCORE ----------------
    def skill_score(self, job_skills, candidate_skills) -> float:
        job_set = {self._normalize(s) for s in job_skills if s}
        cand_set = {self._normalize(s) for s in candidate_skills if s}

        if not job_set:
            return 0.0

        return len(job_set & cand_set) / len(job_set)

    # ---------------- EXPERIENCE SCORE ----------------
    def experience_score(self, career_history: List[Dict[str, Any]], target_titles: List[str]) -> float:
        if not career_history:
            return 0.0

        target_titles = [t.lower() for t in target_titles]
        hits = 0

        for item in career_history:
            title = str(item.get("title", "")).lower()
            desc = " ".join([
                str(item.get("title", "")),
                str(item.get("company", "")),
                str(item.get("description", ""))
            ]).lower()

            if any(t in title or t in desc for t in target_titles):
                hits += 1

        return hits / len(career_history)

    # ---------------- BEHAVIOR SIGNALS ----------------
    def signal_score(self, signals: Dict[str, Any]) -> float:
        if not signals:
            return 0.0

        text = str(signals).lower()

        keywords = [
            "leadership",
            "collaboration",
            "communication",
            "agile",
            "ownership",
            "stakeholder"
        ]

        score = sum(0.2 for kw in keywords if kw in text)
        return min(score, 1.0)

    # ---------------- CERTIFICATIONS ----------------
    def certification_score(self, certifications: List[Any]) -> float:
        if not certifications:
            return 0.0

        cert_text = " ".join(
            self._normalize(c) for c in certifications
        )

        bonus_terms = ["pmp", "scrum", "csm", "product", "ba", "six sigma"]
        hits = sum(1 for t in bonus_terms if t in cert_text)

        return min(hits / len(bonus_terms), 1.0)

    # ---------------- LANGUAGE SCORE ----------------
    def language_score(self, languages: List[str]) -> float:
        if not languages:
            return 0.0
        return min(len(languages) / 3.0, 1.0)

    # ---------------- FINAL WEIGHTED SCORE ----------------
    def weighted_score(self, scores: Dict[str, float], weights: Dict[str, float]) -> float:
        return sum(scores.get(k, 0.0) * w for k, w in weights.items())