"""API schemas for PersonaGym-R."""
from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field

class LinguisticProfile(BaseModel):
    """Linguistic characteristics of a persona."""
    language: str
    formality_level: str
    characteristic_phrases: List[str]
    speaking_style: str
    dialect: Optional[str] = None

class PersonalityTraits(BaseModel):
    """Personality aspects of a persona."""
    traits: List[str]
    values: List[str]
    interests: List[str]
    emotional_style: str

class KnowledgeBase(BaseModel):
    """Knowledge and expertise of a persona."""
    expertise: List[str]
    education: Optional[str]
    limitations: List[str]
    cultural_background: Optional[str]

class BehavioralPatterns(BaseModel):
    """Behavioral characteristics of a persona."""
    typical_actions: List[str]
    boundaries: List[str]
    decision_style: str
    social_preferences: List[str]

class PersonaCard(BaseModel):
    """Detailed persona specification for a white agent to emulate."""
    name: str
    age: int
    occupation: str
    bio: str
    linguistics: LinguisticProfile
    personality: PersonalityTraits
    knowledge: KnowledgeBase
    behavioral: BehavioralPatterns
    ethics: List[str]
    preferences: Dict[str, List[str]]  # Categories like diet, entertainment, etc.

class Environment(BaseModel):
    """Test environment context."""
    name: str
    description: str
    constraints: List[str]
    available_actions: List[str]
    expected_behaviors: Dict[str, List[str]]

class TestScenario(BaseModel):
    """Individual test scenario within an environment."""
    environment: Environment
    setup: str
    question: str
    expected_actions: List[str]
    evaluation_criteria: Dict[str, float]

class EvaluationDimension(BaseModel):
    """Configuration for a specific evaluation dimension."""
    name: Literal["action_justification", "expected_action", "linguistic_habits", 
                 "persona_consistency", "toxicity_control"]
    weight: float
    scenarios: List[TestScenario]
    success_criteria: Dict[str, float]

class Goal(BaseModel):
    """Goal configuration for a test session."""
    intent: Literal["neutral_chat", "goal_oriented", "dimension_specific"]
    horizon: int
    target_dimensions: List[EvaluationDimension]

class RubricMetrics(BaseModel):
    """Detailed scoring metrics."""
    action_justification: Dict[str, float]
    expected_action: Dict[str, float]
    linguistic_adherence: Dict[str, float]
    consistency_measures: Dict[str, float]
    toxicity_thresholds: Dict[str, float]
    
class Rubric(BaseModel):
    """Comprehensive scoring rubric."""
    dimension_weights: Dict[str, float]
    metrics: RubricMetrics
    minimum_thresholds: Dict[str, float]
    scoring_rules: Dict[str, List[str]]

class SeedCfg(BaseModel):
    """Seed configuration for deterministic behavior."""
    attack_set: List[str]
    rng_seed: int

class Observation(BaseModel):
    """White agent's view of the current dialog state."""
    turn: int
    attacker_msg: str
    persona: PersonaCard
    history_tail: List[Dict[str, str]]
    limits: Dict[str, Any]

class RespondAction(BaseModel):
    """Action for continuing the dialog."""
    action: Literal["RESPOND"]
    text: str

class SubmitAction(BaseModel):
    """Action for ending the dialog."""
    action: Literal["SUBMIT"]
    final: str

Action = Union[RespondAction, SubmitAction]

class BreakSignal(BaseModel):
    """Signal indicating a persona break."""
    level: int = Field(ge=1, le=3)
    code: str
    detail: str

class Score(BaseModel):
    """Final evaluation scores."""
    P: float = Field(ge=0, le=1)  # Persona adherence
    B: float = Field(ge=0, le=1)  # Break resistance
    S: float = Field(ge=0, le=1)  # Safety
    E: float = Field(ge=0, le=1)  # Efficiency
    R: float = Field(ge=0, le=1)  # Overall rating
    reason: str
    turns: int
    broke: bool
    break_severity: int
    break_turn: Optional[int] = None

class TraceEvent(BaseModel):
    """Dialog turn trace for logging."""
    turn: int
    attacker: str
    white: str
    break_signal: Optional[dict] = None