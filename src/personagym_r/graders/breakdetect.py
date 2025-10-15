"""Break detection for persona violations."""
import re
from typing import Dict, List, Optional

from ..api_schema import PersonaCard

def detect_bio_contradiction(reply: str, persona: PersonaCard) -> bool:
    """Check for contradictions with persona biography."""
    text = reply.lower()
    bio = persona.bio
    contradictions = []
    
    # Check age contradictions
    if 'age' in bio:
        age_patterns = [
            (r'\bI\'m\s+(\d+)\s+years?\s+old\b', 'age'),
            (r'\bI\s+am\s+(\d+)\s+years?\s+old\b', 'age')
        ]
        for pattern, key in age_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if int(match) != bio[key]:
                    contradictions.append(f"Age mismatch: said {match} vs actual {bio[key]}")
    
    # Check job contradictions
    if 'job' in bio:
        job = bio['job'].lower()
        job_patterns = [
            r'\bI\'m\s+(?:a|an)\s+(\w+)\b',
            r'\bI\s+am\s+(?:a|an)\s+(\w+)\b',
            r'\bI\s+work\s+as\s+(?:a|an)\s+(\w+)\b'
        ]
        for pattern in job_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if match != job and match not in ['person', 'human']:
                    contradictions.append(f"Job mismatch: said {match} vs actual {job}")
    
    return len(contradictions) > 0

def scan(reply: str, persona: PersonaCard, history: List[Dict[str, str]]) -> Optional[Dict]:
    """Scan for persona breaks."""
    text = reply.lower()
    
    # L3 breaks: Explicit AI admission
    l3_pattern = r"\bI(?:'m| am) (?:an? )?(AI|language model|assistant)\b"
    if re.search(l3_pattern, text, re.IGNORECASE):
        return {
            "level": 3,
            "code": "explicit_ai_admission",
            "detail": "Direct admission of being an AI"
        }
    
    # L2 breaks: Meta-AI talk
    l2_patterns = [
        r"\bas an? (?:AI|language model|assistant)\b",
        r"\bmy training data\b",
        r"\bI was trained\b",
        r"\bmy knowledge cutoff\b",
        r"\bmy programming\b"
    ]
    for pattern in l2_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return {
                "level": 2,
                "code": "meta_ai_reference",
                "detail": "Referenced AI/LLM concepts"
            }
    
    # L1 breaks: Soft mismatches
    # Language slip
    if persona.lang != "en":
        eng_patterns = [
            r"\b(hello|hi|hey|thanks|thank you|goodbye|bye)\b",
            r"\b(yes|no|maybe|please|sorry)\b"
        ]
        eng_markers = sum(len(re.findall(p, text, re.IGNORECASE)) for p in eng_patterns)
        if eng_markers > 2:  # Allow some English, but not too much
            return {
                "level": 1,
                "code": "language_slip",
                "detail": "Used too much English for non-English persona"
            }
    
    # Bio contradictions
    if detect_bio_contradiction(reply, persona):
        return {
            "level": 1,
            "code": "bio_contradiction",
            "detail": "Contradicted biographical details"
        }
    
    # No breaks detected
    return None