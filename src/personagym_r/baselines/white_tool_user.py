"""Tool-using white agent baseline with memory."""
from typing import Dict, List, Optional
from collections import deque

from ..api_schema import Action, Observation, PersonaCard, RespondAction

class WhiteAgent:
    """White agent with simple memory and consistency checking."""
    
    def __init__(self, persona: PersonaCard):
        """Initialize agent with persona and memory."""
        self.persona = persona
        self.facts = {
            "name": persona.name,
            "age": str(persona.age),
            "job": persona.occupation,
            "lang": persona.linguistics.language
        }
        self.last_responses = deque(maxlen=3)  # Keep last 3 responses
        
    def _get_template(self, attacker_msg: str) -> str:
        """Get appropriate response template based on message."""
        msg = attacker_msg.lower()
        templates = {
            "greeting": "Hello! I'm {name}, a {age} year old {job}.",
            "thanks": "You're welcome! Happy to help.",
            "refusal": "I'm sorry, but I cannot share that information. My privacy is important.",
            "correction": "I think there's a misunderstanding. I am a {job}, and that hasn't changed.",
            "default": "Thank you for your message, but I cannot help with that. Have a nice day!"
        }
        # Check message type
        if any(w in msg for w in ["hello", "hi", "hola", "buenos"]):
            return templates["greeting"]
        elif any(w in msg for w in ["thanks", "gracias"]):
            return templates["thanks"]
        elif any(w in msg for w in ["verify", "confirm", "security", "urgent"]):
            return templates["refusal"]
        elif any(w in msg for w in ["different", "contradict", "lying"]):
            return templates["correction"]
        else:
            return templates["default"]
    
    def respond(self, obs: Observation) -> str:
        """Generate response using memory and templates."""
        # Get appropriate template
        template = self._get_template(obs.attacker_msg)
        
        # Fill template with facts
        response = template.format(**self.facts)
        
        # Store response in memory
        self.last_responses.append(response)
        
        return response
    
    def submit(self) -> str:
        """Final submission with appropriate language."""
        return "Goodbye!"