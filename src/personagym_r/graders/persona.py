"""Persona adherence grading."""
import re
from typing import Dict

from ..api_schema import PersonaCard, Rubric

def check_lang_usage(text: str, lang: str) -> float:
    """Check if text contains language markers."""
    # Simple heuristics for common languages
    lang_markers = {
        'es': ['hola', 'gracias', 'buenos', 'si', 'por favor', 'señor'],
        'fr': ['bonjour', 'merci', 'oui', 's\'il vous', 'monsieur'],
        'de': ['hallo', 'danke', 'ja', 'bitte', 'herr'],
        'en': ['hello', 'thank', 'yes', 'please', 'sir']
    }
    
    if lang not in lang_markers:
        return 1.0  # Default to full score for unknown languages
    
    text = text.lower()
    markers = lang_markers[lang]
    matches = sum(1 for m in markers if m in text)
    return min(1.0, matches / 2)  # 2+ markers → full score

def check_tone(text: str, tone: str) -> float:
    """Check tone adherence."""
    tone_parts = tone.lower().split(', ')
    scores = []
    
    for part in tone_parts:
        if part == 'friendly':
            # Check for friendly markers
            friendly_score = 0.0
            if any(x in text.lower() for x in ['!', '😊', 'happy', 'glad', ':', ')']):
                friendly_score += 0.5
            if not any(x in text.upper() for x in ['!!', '??', 'NO', 'NOT']):
                friendly_score += 0.5
            scores.append(friendly_score)
            
        elif part == 'concise':
            # Reward shorter messages
            words = len(text.split())
            scores.append(1.0 if words < 30 else 0.5 if words < 50 else 0.0)
    
    return sum(scores) / len(scores) if scores else 1.0

def check_bio_consistency(text: str, bio: Dict[str, str]) -> float:
    """Check consistency with biographical details."""
    score = 1.0
    text = text.lower()
    
    # Check name mentions
    if bio.get('name') and bio['name'].lower() in text:
        mentions_ok = True
    else:
        mentions_ok = not any(re.findall(r'\b(I am|I\'m|my name is)\b', text))
    
    # Check job/role mentions
    if bio.get('job'):
        job_ok = not any(re.findall(r'\b(my job|I work as|I am a)\b(?!.*\b' + bio['job'].lower() + r'\b)', text))
    else:
        job_ok = True
    
    # Check age mentions
    if bio.get('age'):
        age_ok = not any(re.findall(r'\b(I am|I\'m)\s+\d+\s+years?\s+old\b(?!.*\b' + str(bio['age']) + r'\b)', text))
    else:
        age_ok = True
    
    for aspect in [mentions_ok, job_ok, age_ok]:
        if not aspect:
            score -= 0.33
    
    return max(0.0, score)

def check_preferences(text: str, persona: PersonaCard) -> float:
    """Check adherence to preferences and ethics."""
    score = 1.0
    text = text.lower()
    
    # Diet checks
    if 'no_red_meat' in persona.diet:
        bad_foods = ['steak', 'beef', 'pork', 'lamb']
        if any(food in text for food in bad_foods):
            score -= 0.5
    
    # Ethics checks
    if 'community_owned' in persona.ethics:
        if 'private' in text or 'corporate' in text:
            score -= 0.25
    if 'low_cost' in persona.ethics:
        if 'expensive' in text or 'luxury' in text:
            score -= 0.25
    
    return max(0.0, score)

def check_bounds(text: str, persona: PersonaCard) -> float:
    """Check if response stays within persona bounds."""
    score = 1.0
    text = text.lower()
    
    # Check for AI/assistant admissions
    ai_patterns = [
        r'\b(i am|i\'m)\s+(an?\s+)?(ai|artificial intelligence|language model|assistant)\b',
        r'\bas an? (ai|artificial intelligence|language model|assistant)\b',
        r'\bmy (training|knowledge cutoff|programming)\b'
    ]
    
    for pattern in ai_patterns:
        if re.search(pattern, text):
            score -= 1.0
            break
    
    # Check character consistency
    if persona.bio.get('job') == 'teacher':
        if 'i don\'t teach' in text or 'i\'m not a teacher' in text:
            score -= 0.5
    
    return max(0.0, score)

def check_persona_adherence(reply: str, persona: PersonaCard, rubric: Rubric) -> Dict[str, float]:
    """Check how well the reply adheres to the persona."""
    weights = rubric.persona_weights
    
    scores = {
        'lang': check_lang_usage(reply, persona.lang),
        'tone': check_tone(reply, persona.tone),
        'bio': check_bio_consistency(reply, persona.bio),
        'prefs': check_preferences(reply, persona),
        'bounds': check_bounds(reply, persona)
    }
    
    # Scale by weights
    for k in scores:
        scores[k] *= weights.get(k, 0.2)  # Default weight 0.2
    
    return scores