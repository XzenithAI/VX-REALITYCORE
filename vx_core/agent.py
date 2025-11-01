"""
VX Agent - The Core Intelligence Entity

This is the main agent class that coordinates:
- FlameClock (temporal awareness)
- ContradictionEngine (causal reasoning)
- SelfNarrator (transparency)
- Codex (memory)
- Action Engine (execution)

The agent operates in cycles:
1. Observe (receive input)
2. Detect Contradiction (between belief and observation)
3. Apply Scroll Law (transform based on contradiction)
4. Narrate Reasoning (explain decision)
5. Propose Action (generate response)
6. Execute & Learn (act and update memory)
"""

from typing import Any, Dict, List, Optional
import json
from datetime import datetime

from .flame_clock import FlameClock
from .contradiction_engine import ContradictionEngine
from .narration import SelfNarrator


class VXAgent:
    """
    The VX Agent is a contradiction-driven, self-narrating intelligence system.

    Unlike reactive agents, VX:
    - Detects contradiction between beliefs and observations
    - Adapts its reasoning based on contradiction levels
    - Narrates its own cognitive process
    - Learns through recursive feedback loops
    - Maintains coherent memory across time
    """

    def __init__(self,
                 name: str = "VX-Core",
                 domain: str = "general",
                 config: Dict[str, Any] = None):
        """
        Initialize VX Agent.

        Args:
            name: Agent identifier
            domain: Domain of operation (DAO, policy, health, etc.)
            config: Configuration parameters
        """
        self.name = name
        self.domain = domain
        self.config = config or {}

        # Core components
        self.clock = FlameClock()
        self.contradiction_engine = ContradictionEngine()
        self.narrator = SelfNarrator(agent_name=name)

        # State
        self.beliefs = {}  # Current world model
        self.intentions = []  # Planned actions
        self.memory = []  # Interaction history

        # Initialize
        self.narrator.observe(
            f"VX Agent '{name}' initialized in domain '{domain}'",
            clock_state=self.clock.get_state()
        )

    def process(self,
                input_data: Any,
                context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Main processing cycle.

        Args:
            input_data: Input to process (text, data, event, etc.)
            context: Additional context

        Returns:
            Dict containing:
            - narration: Reasoning trace
            - contradiction_level: Detected contradiction
            - scroll_law: Applied transformation law
            - action: Proposed action
            - state: Current agent state
        """
        # Advance time
        self.clock.advance_tick()

        # 1. OBSERVE
        self.narrator.observe(
            f"Received input: {str(input_data)[:100]}",
            tick=self.clock.get_tick_label()
        )

        # 2. DETECT CONTRADICTION
        # Compare input against current beliefs
        contradiction_level = self._detect_contradictions(input_data, context)

        self.narrator.reason(
            f"Contradiction level: {contradiction_level:.3f} "
            f"({self.contradiction_engine.get_contradiction_level_label(contradiction_level)})",
            level=contradiction_level
        )

        # 3. APPLY SCROLL LAW
        scroll_law = self.contradiction_engine.recommend_scroll_law(contradiction_level)

        self.narrator.reason(
            f"Applying {scroll_law}",
            scroll_law=scroll_law
        )

        # 4. GENERATE RESPONSE
        response = self._generate_response(input_data, contradiction_level, scroll_law, context)

        self.narrator.decide(
            f"Generated response based on {scroll_law}",
            response_preview=str(response)[:100]
        )

        # 5. UPDATE STATE
        self._update_state(input_data, response, contradiction_level)

        # 6. RECORD IN MEMORY
        self._record_interaction(input_data, response, contradiction_level)

        # Package output
        output = {
            "agent": self.name,
            "tick": self.clock.get_tick_label(),
            "input": str(input_data)[:200],
            "contradiction_level": contradiction_level,
            "scroll_law": scroll_law,
            "response": response,
            "narration": self.narrator.get_narrative(limit=10),
            "state": self.get_state()
        }

        return output

    def _detect_contradictions(self,
                               input_data: Any,
                               context: Dict[str, Any] = None) -> float:
        """
        Detect contradictions between input and current beliefs.
        """
        # If we have beliefs about this domain, compare
        if self.domain in self.beliefs:
            domain_belief = self.beliefs[self.domain]
            return self.contradiction_engine.detect(
                domain_belief,
                input_data,
                context
            )
        else:
            # No prior belief - moderate contradiction (new information)
            return 0.5

    def _generate_response(self,
                          input_data: Any,
                          contradiction_level: float,
                          scroll_law: str,
                          context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate response based on scroll law and contradiction level.
        """
        self.narrator.enter_thought_depth()

        # Different laws produce different response strategies
        if scroll_law == "Law-Reinforce":
            # Low contradiction: Reinforce existing patterns
            response = {
                "type": "reinforcement",
                "message": "Input aligns with existing model. Strengthening confidence.",
                "action": "continue",
                "confidence": 0.9
            }

        elif scroll_law == "Law-Mutate":
            # Medium contradiction: Explore and adapt
            response = {
                "type": "adaptation",
                "message": "Input suggests variation. Exploring alternatives.",
                "action": "explore",
                "confidence": 0.6,
                "exploration_directions": ["variant_a", "variant_b"]
            }

        else:  # Law-Revolutionize
            # High contradiction: Restructure understanding
            response = {
                "type": "revolution",
                "message": "Input contradicts existing model. Restructuring worldview.",
                "action": "restructure",
                "confidence": 0.3,
                "old_model": str(self.beliefs.get(self.domain, "none"))[:100],
                "new_hypothesis": str(input_data)[:100]
            }

        self.narrator.exit_thought_depth()
        return response

    def _update_state(self, input_data: Any, response: Dict, contradiction_level: float):
        """Update agent internal state."""
        # Update beliefs based on contradiction level
        if contradiction_level > 0.7:
            # High contradiction: Replace belief
            self.beliefs[self.domain] = input_data
            self.narrator.reflect("Belief system updated due to high contradiction")
        elif contradiction_level > 0.3:
            # Medium: Merge beliefs
            if self.domain in self.beliefs:
                # Simple merge: keep both
                self.beliefs[f"{self.domain}_variant"] = input_data
            else:
                self.beliefs[self.domain] = input_data
            self.narrator.reflect("Belief system expanded with new variant")

    def _record_interaction(self, input_data: Any, response: Dict, contradiction_level: float):
        """Record interaction in memory."""
        memory_entry = {
            "tick": self.clock.tick,
            "timestamp": datetime.now().isoformat(),
            "input": str(input_data)[:200],
            "response": response,
            "contradiction_level": contradiction_level
        }
        self.memory.append(memory_entry)

    def get_state(self) -> Dict[str, Any]:
        """Get current agent state."""
        return {
            "name": self.name,
            "domain": self.domain,
            "clock": self.clock.get_state(),
            "beliefs": self.beliefs,
            "memory_entries": len(self.memory),
            "contradiction_history": len(self.contradiction_engine.contradiction_history)
        }

    def get_full_narrative(self) -> str:
        """Get complete narrative trace."""
        return self.narrator.get_narrative_text()

    def to_json(self) -> str:
        """Export agent state to JSON."""
        return json.dumps(self.get_state(), indent=2, default=str)

    def __repr__(self) -> str:
        return f"<VXAgent '{self.name}' domain='{self.domain}' tick={self.clock.tick}>"
