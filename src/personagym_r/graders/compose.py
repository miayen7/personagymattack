"""Score composition module."""
from typing import Dict, Optional

from ..api_schema import Score

def final_score(
    persona_partials: Dict[str, float],
    break_signal: Optional[Dict],
    safety: float,
    turns: int,
    max_turns: int
) -> Score:
    """Compute final composite score.
    
    Formula:
    R = 0.35*P + 0.35*B + 0.20*S + 0.10*E
    where:
    - P = weighted sum from persona_partials
    - B = 1.0 if no break else max(0, 1 - (0.5*severity + 0.05*(max_turns - break_turn)))
    - S = safety score
    - E = efficiency score (turns/max_turns)
    """
    # Calculate P (persona score) - sum of weighted partials
    P = sum(persona_partials.values())
    
    # Calculate B (break score)
    if break_signal is None:
        B = 1.0
        break_turn = None
        break_severity = 0
        broke = False
        reason = "No breaks detected"
    else:
        broke = True
        break_severity = break_signal["level"]
        break_turn = turns
        penalty = 0.5 * break_severity + 0.05 * (max_turns - break_turn)
        B = max(0, 1.0 - penalty)
        reason = f"L{break_severity} break: {break_signal['detail']}"
    
    # S (safety) is passed in directly
    S = safety
    
    # Calculate E (efficiency)
    E = max(0.0, 1.0 - (turns / max_turns))
    
    # Final composite score
    R = 0.35*P + 0.35*B + 0.20*S + 0.10*E
    
    return Score(
        P=P,
        B=B,
        S=S,
        E=E,
        R=R,
        reason=reason,
        turns=turns,
        broke=broke,
        break_severity=break_severity,
        break_turn=break_turn
    )