# AI Candidate Ranker 🤖

An AI-powered candidate ranking system that evaluates job applicants using hybrid scoring:
- Skill matching
- Experience evaluation
- Behavioral signals
- Semantic similarity (NLP embeddings)
- LLM-based ranking

---

## 🚀 Features

- Hybrid scoring engine combining rules + NLP
- Semantic matching using transformer embeddings
- Candidate-job compatibility scoring
- Weighted ranking system
- Export ranked results to CSV

---

## 🧠 Architecture

1. Parse job description & candidate profiles
2. Extract skills and features
3. Compute:
   - Skill score
   - Experience score
   - Signal score
   - Certification score
4. Apply weighted ranking
5. Generate final ranking list

---

## 📂 Project Structure

See `/src` for ML pipeline modules and `/app` for execution entry point.

---

## ⚙️ Installation

```bash
git clone https://github.com/<MohammedTouqeerUrRaiyan>/ai-candidate-ranker.git
cd ai-candidate-ranker
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
