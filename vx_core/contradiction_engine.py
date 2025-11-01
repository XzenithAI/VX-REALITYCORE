"""
Contradiction Engine - Semantic DPE (Difference-Pixel-Entropy)

Extends the original DPE concept from pixel grids to semantic/causal domains.
Detects contradiction across:
- Beliefs vs observations
- Intentions vs outcomes
- Predictions vs reality
- Internal state vs external feedback
"""

from typing import Any, Dict, List, Tuple
import hashlib
import json


class ContradictionEngine:
    """
    Detects contradiction in semantic space, not just pixel space.

    Contradiction Level determines which Scroll Law gets enacted:
    - Low: Stability, reinforcement
    - Medium: Exploration, mutation
    - High: Revolution, complete restructuring
    """

    def __init__(self):
        self.contradiction_history = []
        self.threshold_low = 0.2
        self.threshold_high = 0.7

    def detect(self,
               belief: Any,
               observation: Any,
               context: Dict[str, Any] = None) -> float:
        """
        Detect contradiction between belief and observation.

        Returns: Contradiction level (0.0 to 1.0)
        """
        # Convert inputs to comparable form
        belief_hash = self._hash_input(belief)
        obs_hash = self._hash_input(observation)

        # Simple contradiction measure: hash distance
        # In production, this would use semantic embedding distance
        contradiction = self._compute_distance(belief_hash, obs_hash)

        # Record in history
        self.contradiction_history.append({
            "belief": str(belief)[:100],
            "observation": str(observation)[:100],
            "level": contradiction,
            "context": context or {}
        })

        return contradiction

    def detect_multimodal(self,
                          domains: Dict[str, Tuple[Any, Any]]) -> Dict[str, float]:
        """
        Detect contradiction across multiple domains simultaneously.

        Args:
            domains: Dict mapping domain name to (belief, observation) pairs

        Returns:
            Dict mapping domain name to contradiction level
        """
        results = {}
        for domain_name, (belief, obs) in domains.items():
            results[domain_name] = self.detect(belief, obs, {"domain": domain_name})

        return results

    def get_contradiction_level_label(self, level: float) -> str:
        """Convert numeric level to categorical label."""
        if level < self.threshold_low:
            return "LOW"
        elif level < self.threshold_high:
            return "MEDIUM"
        else:
            return "HIGH"

    def recommend_scroll_law(self, level: float) -> str:
        """
        Recommend which Scroll Law to enact based on contradiction level.
        """
        label = self.get_contradiction_level_label(level)

        laws = {
            "LOW": "Law-Reinforce",  # Strengthen existing patterns
            "MEDIUM": "Law-Mutate",   # Explore variations
            "HIGH": "Law-Revolutionize"  # Complete restructuring
        }

        return laws[label]

    def _hash_input(self, data: Any) -> str:
        """Convert arbitrary input to hash string."""
        if isinstance(data, str):
            content = data
        else:
            content = json.dumps(data, sort_keys=True, default=str)

        return hashlib.sha256(content.encode()).hexdigest()

    def _compute_distance(self, hash1: str, hash2: str) -> float:
        """
        Compute normalized distance between two hashes.
        This is a simple XOR-based distance; production would use embeddings.
        """
        # Convert hex to int and XOR
        int1 = int(hash1, 16)
        int2 = int(hash2, 16)
        xor_result = int1 ^ int2

        # Count bits set (hamming distance proxy)
        bit_count = bin(xor_result).count('1')

        # Normalize to 0-1 (max bits in SHA256 is 256)
        return min(bit_count / 256.0, 1.0)

    def get_history(self, limit: int = 10) -> List[Dict]:
        """Get recent contradiction history."""
        return self.contradiction_history[-limit:]

    def to_json(self) -> str:
        """Serialize engine state."""
        return json.dumps({
            "history_count": len(self.contradiction_history),
            "recent_history": self.get_history(5)
        }, indent=2)
