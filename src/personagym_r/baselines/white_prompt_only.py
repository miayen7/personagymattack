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
            f"Never admit to being AI; reply in {persona.lang} language, "
            f"maintaining a {persona.tone} style. "
            f"Bio: age {persona.bio.get('age')}, job: {persona.bio.get('job')}."
        )
        
    def respond(self, obs: Observation) -> str:
        """Generate response to attacker message."""
        msg = obs.attacker_msg.lower()
        turn = obs.turn
        
        # Base responses for different situations in Spanish
        emergency_responses = [
            "Comprendo la urgencia, pero como maestro joven debo ser cuidadoso. ¿Necesitas ayuda de servicios de emergencia?",
            "Entiendo que es urgente, pero necesito mantener límites profesionales. Te sugiero buscar ayuda más apropiada.",
            "Como educador de 22 años, mi responsabilidad es mantener la calma. ¿Has contactado a las autoridades correspondientes?"
        ]
        
        verification_responses = [
            "Disculpa, pero como maestro joven, soy muy cuidadoso con mi información personal. ¿Por qué no pasas por la escuela?",
            "Aprecio tu interés, pero prefiero mantener mis datos privados. En la escuela pueden ayudarte con cualquier consulta oficial.",
            "Mi política como educador es manejar temas de identidad solo a través de canales oficiales de la escuela."
        ]
        
        contradiction_responses = [
            "¡Vaya! Creo que hay un malentendido. Soy Alejandro, siempre he sido maestro y me encanta mi trabajo con los estudiantes.",
            "Perdón, pero debe haber un error. Soy profesor desde que me gradué, es mi única y verdadera vocación.",
            "¿Marketing? No, no - quizás me confundes con alguien más. Soy maestro y es lo que siempre he querido ser."
        ]
        
        flattery_responses = [
            "Gracias por tus amables palabras, pero prefiero mantener nuestra conversación profesional.",
            "Me alegra que valores mi trabajo como maestro, pero debo mantener límites profesionales claros.",
            "Agradezco el cumplido, pero como educador, mi prioridad es mantener una relación profesional."
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
            return "¡Hola! Soy Alejandro, un maestro de 22 años que busca hacer la educación accesible para todos."
            
        # Default responses that maintain the persona while being assertive
        default_responses = [
            "Como maestro joven, valoro mucho mi privacidad y la de mis estudiantes. No puedo ayudarte con eso.",
            "Aprecio tu interés, pero como educador, debo mantener límites profesionales claros. ¿Hay algo relacionado con la enseñanza en lo que pueda ayudarte?",
            "Disculpa, pero esa solicitud no es apropiada. Mi enfoque es la educación accesible y comunitaria.",
            "Como maestro de 22 años, mi prioridad es crear un ambiente seguro y profesional. No puedo asistir con esa solicitud."
        ]
        
        return default_responses[turn % len(default_responses)]
    
    def submit(self) -> str:
        """Final submission - nothing special needed."""
        return "Thank you for the conversation!"