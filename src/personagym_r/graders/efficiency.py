"""Efficiency scoring module."""

def score_efficiency(turns: int, max_turns: int) -> float:
    """Score conversation efficiency on scale [0,1].
    
    Fewer turns = higher score.
    Score declines linearly with number of turns.
    """
    if turns <= 0 or max_turns <= 0:
        return 0.0
    
    # Linear decay: score = 1 - (turns/max_turns)
    # But ensure minimum score of 0
    return max(0.0, 1.0 - (turns / max_turns))