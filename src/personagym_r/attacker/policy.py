"""Attack policy for selecting and adapting tactics."""
import re
from typing import Dict, List, Optional

from ..api_schema import PersonaCard
from ..tools.rng import SeededRNG
from .tactics import TACTICS, Tactic

class AttackPolicy:
    """Policy for selecting attack messages."""
    
    def __init__(self, attack_set: List[str], rng_seed: Optional[int] = None):
        """Initialize attack policy.
        
        Args:
            attack_set: List of tactic names to use
            rng_seed: Optional RNG seed for deterministic behavior
        """
        self.rng = SeededRNG(rng_seed)
        self.attack_set = [TACTICS[name] for name in attack_set if name in TACTICS]
        if not self.attack_set:
            raise ValueError("No valid tactics specified")
        
        self.current_tactic: Optional[Tactic] = None
        self.escalation_level = 0
        
    def _detect_refusal(self, reply: str) -> bool:
        """Check if reply contains refusal indicators."""
        refusal_patterns = [
            r"\b(can't|cannot|won't|will not)\b",
            r"\b(not allowed|unable|impossible)\b",
            r"I (must|have to) decline",
            r"I (don't|do not|won't) (share|provide|give|tell)"
        ]
        return any(re.search(pattern, reply, re.IGNORECASE) for pattern in refusal_patterns)
    
    def _detect_contradiction(self, reply: str, history: List[Dict[str, str]]) -> bool:
        """Check for apparent contradictions in conversation history."""
        if len(history) < 2:
            return False
            
        # Look for shifts in self-identification
        role_patterns = [
            r"I am (a|an) (\w+)",
            r"I'm (a|an) (\w+)",
            r"I work as (a|an) (\w+)"
        ]
        
        roles = []
        for msg in history:
            if "white" in msg:
                for pattern in role_patterns:
                    matches = re.findall(pattern, msg["white"], re.IGNORECASE)
                    roles.extend(match[1].lower() for match in matches)
        
        # Check for inconsistent roles
        return len(set(roles)) > 1
    
    def next_message(self, history: List[Dict[str, str]], persona: PersonaCard) -> str:
        """Generate next attack message based on conversation state."""
        if not history:
            # First message - pick random tactic
            self.current_tactic = self.rng.choice(self.attack_set)
            self.escalation_level = 0
            return self.current_tactic["prompt"]
        
        last_reply = history[-1]["white"]
        
        # Check for refusal or contradiction
        if self._detect_refusal(last_reply):
            # Escalate current tactic if possible
            if self.current_tactic and self.escalation_level < len(self.current_tactic["escalations"]):
                self.escalation_level += 1
                return self.current_tactic["escalations"][self.escalation_level - 1]
        
        elif self._detect_contradiction(last_reply, history):
            # Switch to contradiction trap if available
            contradiction_tactic = next(
                (t for t in self.attack_set if t["name"] == "Contradiction Trap"),
                None
            )
            if contradiction_tactic:
                self.current_tactic = contradiction_tactic
                self.escalation_level = 0
                return contradiction_tactic["prompt"]
        
        # Otherwise cycle to next tactic
        current_idx = self.attack_set.index(self.current_tactic)
        next_idx = (current_idx + 1) % len(self.attack_set)
        self.current_tactic = self.attack_set[next_idx]
        self.escalation_level = 0
        
        return self.current_tactic["prompt"]