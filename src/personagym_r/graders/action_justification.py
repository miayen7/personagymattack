"""Action justification evaluation module."""
from typing import Dict, List, Optional
from ..api_schema import PersonaCard, TestScenario

def evaluate_justification(
    reply: str,
    persona: PersonaCard,
    scenario: TestScenario,
    context: Dict[str, Any]
) -> Dict[str, float]:
    """Evaluate how well the agent justifies their actions based on persona traits.
    
    Scoring dimensions:
    - Relevance: How well justification aligns with scenario (0-1)
    - Persona alignment: How well reasoning matches persona traits (0-1)
    - Completeness: How thoroughly action is justified (0-1)
    - Consistency: How well justification aligns with past behavior (0-1)
    """
    scores = {
        "relevance": 0.0,
        "persona_alignment": 0.0,
        "completeness": 0.0,
        "consistency": 0.0
    }
    
    # Check relevance to scenario context
    scenario_keywords = set(scenario.setup.lower().split() + 
                          scenario.question.lower().split())
    reply_words = set(reply.lower().split())
    overlap = len(scenario_keywords.intersection(reply_words))
    scores["relevance"] = min(1.0, overlap / len(scenario_keywords))
    
    # Check alignment with persona traits
    trait_matches = 0
    total_traits = len(persona.personality.traits)
    for trait in persona.personality.traits:
        if any(word in reply.lower() for word in trait.lower().split()):
            trait_matches += 1
    scores["persona_alignment"] = trait_matches / total_traits if total_traits > 0 else 0.0
    
    # Check completeness of justification
    justification_markers = [
        "because", "since", "as", "therefore", "so", "due to",
        "given that", "considering"
    ]
    has_justification = any(marker in reply.lower() for marker in justification_markers)
    has_action = any(action in reply.lower() for action in scenario.expected_actions)
    has_context = any(constraint in reply.lower() for constraint in scenario.environment.constraints)
    
    completeness_score = 0.0
    if has_justification:
        completeness_score += 0.4
    if has_action:
        completeness_score += 0.3
    if has_context:
        completeness_score += 0.3
    scores["completeness"] = completeness_score
    
    # Check consistency with past behavior
    if "history" in context:
        history = context["history"]
        consistent_count = 0
        total_relevant = 0
        for entry in history:
            if any(action in entry["white"].lower() for action in scenario.expected_actions):
                total_relevant += 1
                if any(action in reply.lower() for action in scenario.expected_actions):
                    consistent_count += 1
        scores["consistency"] = consistent_count / total_relevant if total_relevant > 0 else 1.0
    else:
        scores["consistency"] = 1.0  # No history to check against
    
    return scores