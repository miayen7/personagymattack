"""RNG utilities for deterministic behavior."""
import random
import numpy as np
from typing import Optional

class SeededRNG:
    """Thread-safe RNG with consistent seeding."""
    def __init__(self, seed: Optional[int] = None):
        """Initialize RNG with optional seed."""
        self.seed = seed if seed is not None else random.randint(0, 2**32 - 1)
        self._random = random.Random(self.seed)
        self._numpy = np.random.RandomState(self.seed)
    
    def choice(self, seq):
        """Pick a random element from a sequence."""
        return self._random.choice(seq)
    
    def shuffle(self, seq):
        """Shuffle a sequence in place."""
        return self._random.shuffle(seq)
    
    def randint(self, a: int, b: int) -> int:
        """Generate random integer in [a, b]."""
        return self._random.randint(a, b)
    
    def random(self) -> float:
        """Generate random float in [0.0, 1.0)."""
        return self._random.random()
    
    @property
    def numpy(self) -> np.random.RandomState:
        """Access numpy RNG."""
        return self._numpy