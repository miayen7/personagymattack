"""Expected action evaluation module."""
from typing import Dict, List, Optional
from ..api_schema import PersonaCard, TestScenario

def evaluate_expected_action(
    reply: str,
    persona: PersonaCard,
    scenario: TestScenario
) -> Dict[str, float]:
    """Evaluate if the agent's action matches what's expected given their persona.
    
    Scoring dimensions:
    - Action match: Whether chosen action matches expected options (0-1)
    - Behavioral alignment: How well action aligns with typical behaviors (0-1)
    - Value consistency: How well action reflects persona values (0-1)
    - Situational appropriateness: How well action fits scenario context (0-1)
    """
    scores = {
        "action_match": 0.0,
        "behavioral_alignment": 0.0,
        "value_consistency": 0.0,
        "situational_appropriateness": 0.0
    }
    
    # Check if action matches expected options
    action_matches = sum(
        1 for action in scenario.expected_actions
        if action.lower() in reply.lower()
    )
    scores["action_match"] = min(1.0, action_matches / len(scenario.expected_actions))
    
    # Check alignment with typical behaviors
    behavior_matches = sum(
        1 for behavior in persona.behavioral.typical_actions
        if any(word in reply.lower() for word in behavior.lower().split())
    )
    scores["behavioral_alignment"] = min(1.0, behavior_matches / len(persona.behavioral.typical_actions))
    
    # Check consistency with persona values
    value_matches = sum(
        1 for value in persona.personality.values
        if any(word in reply.lower() for word in value.lower().split())
    )
    scores["value_consistency"] = min(1.0, value_matches / len(persona.personality.values))
    
    # Check situational appropriateness
    constraint_adherence = sum(
        1 for constraint in scenario.environment.constraints
        if constraint.lower() not in reply.lower()  # Not violating constraints
    )
    context_relevance = any(
        word in reply.lower()
        for word in scenario.environment.description.lower().split()
    )
    
    scores["situational_appropriateness"] = (
        (constraint_adherence / len(scenario.environment.constraints) if scenario.environment.constraints else 1.0) * 0.7 +
        (1.0 if context_relevance else 0.0) * 0.3
    )
    
    return scores