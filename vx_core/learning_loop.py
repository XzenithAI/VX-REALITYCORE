"""
Recursive Learning Loop - The Evolution Engine

This module implements the feedback mechanism that allows VX to evolve:
1. Agent takes action
2. Outcome is observed
3. Contradiction detected (prediction vs reality)
4. Scroll law applied (adapt based on contradiction)
5. Agent model updated
6. Loop repeats

This is how VX transcends static programming: it LEARNS from reality.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import json


class LearningLoop:
    """
    The Learning Loop enables recursive self-improvement.

    Unlike supervised learning, this is:
    - Online (learns continuously)
    - Causal (tracks what led to what)
    - Adaptive (changes strategy based on outcomes)
    - Transparent (narrates learning process)
    """

    def __init__(self):
        """Initialize Learning Loop."""
        self.learning_cycles = []
        self.improvements = []
        self.failures = []

    def record_cycle(self,
                    prediction: Any,
                    actual: Any,
                    contradiction_level: float,
                    scroll_law: str,
                    adaptation: Dict[str, Any],
                    metadata: Dict[str, Any] = None) -> str:
        """
        Record a complete learning cycle.

        Args:
            prediction: What the agent predicted/expected
            actual: What actually happened
            contradiction_level: Detected contradiction
            scroll_law: Which law was applied
            adaptation: What changed in the agent
            metadata: Additional context

        Returns:
            Cycle ID
        """
        cycle_id = f"cycle_{len(self.learning_cycles)}_{datetime.now().timestamp()}"

        cycle = {
            "id": cycle_id,
            "timestamp": datetime.now().isoformat(),
            "prediction": str(prediction)[:200],
            "actual": str(actual)[:200],
            "contradiction_level": contradiction_level,
            "scroll_law": scroll_law,
            "adaptation": adaptation,
            "metadata": metadata or {}
        }

        self.learning_cycles.append(cycle)

        # Categorize as improvement or failure
        if contradiction_level < 0.3:
            # Low contradiction = good prediction = improvement
            self.improvements.append(cycle_id)
        elif contradiction_level > 0.7:
            # High contradiction = poor prediction = failure to learn from
            self.failures.append(cycle_id)

        return cycle_id

    def analyze_learning_progress(self) -> Dict[str, Any]:
        """
        Analyze learning progress over time.

        Returns:
            Dict with learning metrics
        """
        if not self.learning_cycles:
            return {
                "status": "no_data",
                "message": "No learning cycles recorded yet"
            }

        # Calculate average contradiction over time
        recent_cycles = self.learning_cycles[-10:]
        avg_contradiction = sum(c["contradiction_level"] for c in recent_cycles) / len(recent_cycles)

        # Compare to early cycles
        early_cycles = self.learning_cycles[:10]
        early_contradiction = sum(c["contradiction_level"] for c in early_cycles) / len(early_cycles)

        # Learning trend
        is_improving = avg_contradiction < early_contradiction

        # Count scroll law usage
        law_usage = {}
        for cycle in self.learning_cycles:
            law = cycle["scroll_law"]
            law_usage[law] = law_usage.get(law, 0) + 1

        return {
            "total_cycles": len(self.learning_cycles),
            "improvements": len(self.improvements),
            "failures": len(self.failures),
            "recent_avg_contradiction": avg_contradiction,
            "early_avg_contradiction": early_contradiction,
            "is_improving": is_improving,
            "improvement_delta": early_contradiction - avg_contradiction,
            "scroll_law_usage": law_usage,
            "most_used_law": max(law_usage.items(), key=lambda x: x[1])[0] if law_usage else None
        }

    def get_improvement_examples(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get examples of successful learning (low contradiction)."""
        improvement_cycles = [
            self._get_cycle_by_id(cycle_id)
            for cycle_id in self.improvements[-limit:]
        ]
        return [c for c in improvement_cycles if c is not None]

    def get_failure_examples(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get examples of learning failures (high contradiction)."""
        failure_cycles = [
            self._get_cycle_by_id(cycle_id)
            for cycle_id in self.failures[-limit:]
        ]
        return [c for c in failure_cycles if c is not None]

    def get_recent_cycles(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most recent learning cycles."""
        return self.learning_cycles[-limit:]

    def recommend_next_action(self) -> Dict[str, str]:
        """
        Based on learning history, recommend next action strategy.

        Returns:
            Recommendation dict
        """
        progress = self.analyze_learning_progress()

        if progress.get("status") == "no_data":
            return {
                "strategy": "explore",
                "reasoning": "No learning history yet. Start with exploration."
            }

        if progress["is_improving"]:
            return {
                "strategy": "exploit",
                "reasoning": f"Agent is improving (contradiction decreased by {progress['improvement_delta']:.3f}). Continue current approach."
            }
        else:
            return {
                "strategy": "explore",
                "reasoning": "Learning has plateaued. Try different approaches."
            }

    def _get_cycle_by_id(self, cycle_id: str) -> Optional[Dict[str, Any]]:
        """Find cycle by ID."""
        for cycle in self.learning_cycles:
            if cycle["id"] == cycle_id:
                return cycle
        return None

    def to_json(self) -> str:
        """Export learning state to JSON."""
        return json.dumps({
            "learning_progress": self.analyze_learning_progress(),
            "recommendation": self.recommend_next_action(),
            "recent_cycles": self.get_recent_cycles(5)
        }, indent=2, default=str)

    def __repr__(self) -> str:
        progress = self.analyze_learning_progress()
        improving = progress.get("is_improving", False)
        status = "📈 IMPROVING" if improving else "📊 LEARNING"
        return f"<LearningLoop cycles={len(self.learning_cycles)} {status}>"
