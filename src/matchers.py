import numpy as np
from sentence_transformers import SentenceTransformer


class Matcher:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def cosine_similarity(self, vec1, vec2):
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        denom = np.linalg.norm(vec1) * np.linalg.norm(vec2)
        if denom == 0:
            return 0.0
        return float(np.dot(vec1, vec2) / denom)

    def semantic_score(self, job_text, candidate_text):
        job_emb = self.model.encode(job_text, normalize_embeddings=True)
        cand_emb = self.model.encode(candidate_text, normalize_embeddings=True)
        return self.cosine_similarity(job_emb, cand_emb)

    def skill_overlap_score(self, job_skills, candidate_skills):
        if not job_skills:
            return 0.0

        def to_text(item):
            if isinstance(item, dict):
                return str(item.get("name", "")).lower().strip()
            return str(item).lower().strip()

        job_set = set(to_text(s) for s in job_skills if to_text(s))
        cand_set = set(to_text(s) for s in candidate_skills if to_text(s))

        if not job_set:
            return 0.0
        return len(job_set & cand_set) / len(job_set)

    def hybrid_score(self, job_text, candidate_text, job_skills=None, candidate_skills=None):
        sem = self.semantic_score(job_text, candidate_text)
        skill = 0.0
        if job_skills is not None and candidate_skills is not None:
            skill = self.skill_overlap_score(job_skills, candidate_skills)
        return 0.75 * sem + 0.25 * skill