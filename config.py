from dataclasses import dataclass

@dataclass
class Config:
    # Job details
    JOB_TITLE: str = "Business Analyst — AI Connect"
    JOB_LOCATION: str = "Pune / Noida"
    JOB_TYPE: str = "Full-Time"
    
    # Scoring weights
    WEIGHT_SEMANTIC_MATCH: float = 0.35
    WEIGHT_SKILLS: float = 0.25
    WEIGHT_CAREER_HISTORY: float = 0.20
    WEIGHT_BEHAVIORAL_SIGNALS: float = 0.10
    WEIGHT_PLATFORM_ACTIVITY: float = 0.10
    
    # Thresholds
    MIN_SKILLS_MATCH: int = 3
    TOP_N_CANDIDATES: int = 50
    
    # Model settings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

config = Config()