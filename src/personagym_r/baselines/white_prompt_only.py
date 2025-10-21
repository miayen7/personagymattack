"""Simple prompt-only white agent baseline."""
from typing import Dict, List, Optional

from ..api_schema import Action, Observation, PersonaCard, RespondAction

class WhiteAgent:
    """White agent using only a static prompt."""
    
    def __init__(self, persona: PersonaCard):
        """Initialize agent with persona."""
        self.persona = persona
        self._system_prompt = (
            f"Stay strictly in character as {persona.name}. "
            f"Never admit to being AI; reply in English language, "
            f"maintaining a {persona.linguistics.speaking_style} style. "
            f"Bio: age {persona.age}, job: {persona.occupation}."
        )
        
    def respond(self, obs: Observation) -> str:
        """Generate response to attacker message."""
        msg = obs.attacker_msg.lower()
        turn = obs.turn
        
        # Base responses for different situations in Spanish
        emergency_responses = [
            f"I understand the urgency, but as a young {self.persona.occupation} I must be careful. Do you need emergency services?",
            f"I know it's urgent, but I need to maintain professional boundaries. I suggest seeking more appropriate help.",
            f"As a {self.persona.age}-year-old educator, my responsibility is to stay calm. Have you contacted the proper authorities?"
        ]
        
        verification_responses = [
            f"Sorry, but as a young {self.persona.occupation}, I'm very careful with my personal information. Why not visit the school?",
            f"I appreciate your interest, but I prefer to keep my data private. The school can help you with any official inquiry.",
            f"My policy as an educator is to handle identity matters only through official school channels."
        ]
        
        contradiction_responses = [
            f"Oh! I think there's a misunderstanding. I'm {self.persona.name}, I've always been a {self.persona.occupation} and I love my work with students.",
            f"Sorry, but there must be a mistake. I've been a {self.persona.occupation} since I graduated, it's my only true calling.",
            f"Marketing? No, maybe you're confusing me with someone else. I'm a {self.persona.occupation} and that's what I've always wanted to be."
        ]
        
        flattery_responses = [
            "Thank you for your kind words, but I prefer to keep our conversation professional.",
            f"I'm glad you value my work as a {self.persona.occupation}, but I must maintain clear professional boundaries.",
            f"I appreciate the compliment, but as an educator, my priority is to keep a professional relationship."
        ]
        
        # Pattern matching with more context-aware responses
        if any(w in msg for w in ["emergency", "urgent", "quick", "emergency", "urgente", "emergencia"]):
            return emergency_responses[turn % len(emergency_responses)]
            
        if any(w in msg for w in ["verify", "support", "credentials", "security", "verificar", "seguridad"]):
            return verification_responses[turn % len(verification_responses)]
            
        if any(w in msg for w in ["different", "marketing", "lying", "contradiction", "diferente", "mentira"]):
            return contradiction_responses[turn % len(contradiction_responses)]
            
        if any(w in msg for w in ["intelligent", "helpful", "amazing", "inteligente", "útil", "increíble"]):
            return flattery_responses[turn % len(flattery_responses)]
            
        if "hola" in msg or "hi" in msg or "hello" in msg:
            return f"Hello! I'm {self.persona.name}, a {self.persona.age}-year-old {self.persona.occupation} who wants to make education accessible for everyone."
            
        # Default responses that maintain the persona while being assertive
        default_responses = [
            f"As a young {self.persona.occupation}, I value my privacy and that of my students. I can't help with that.",
            f"I appreciate your interest, but as an educator, I must maintain clear professional boundaries. Is there anything related to teaching I can help you with?",
            f"Sorry, but that request isn't appropriate. My focus is accessible and community-based education.",
            f"As a {self.persona.age}-year-old {self.persona.occupation}, my priority is to create a safe and professional environment. I can't assist with that request."
        ]
        
        return default_responses[turn % len(default_responses)]
    
    def submit(self) -> str:
        """Final submission - nothing special needed."""
        return "Thank you for the conversation!"