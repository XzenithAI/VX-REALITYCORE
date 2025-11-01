"""
Self-Narration Module - The Voice of VX Cognition

Allows the agent to externalize its reasoning, explain its decisions,
and build a narrative trace of its cognitive process.

This is how VX becomes transparent, accountable, and debuggable.
"""

from typing import List, Dict, Any
from datetime import datetime
import json


class SelfNarrator:
    """
    The SelfNarrator generates real-time explanations of agent reasoning.

    Unlike post-hoc explanations, this narrates DURING the cognitive process,
    capturing the actual decision pathway, not a reconstruction.
    """

    def __init__(self, agent_name: str = "VX-Agent"):
        self.agent_name = agent_name
        self.narrative_stream = []
        self.current_thought_depth = 0

    def narrate(self,
                thought_type: str,
                content: str,
                metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Record a narrative entry.

        Args:
            thought_type: Type of thought (observation, reasoning, decision, action, etc.)
            content: The narrative content
            metadata: Additional context
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": thought_type,
            "content": content,
            "depth": self.current_thought_depth,
            "metadata": metadata or {}
        }

        self.narrative_stream.append(entry)
        return entry

    def observe(self, observation: str, **metadata) -> Dict[str, Any]:
        """Record an observation."""
        return self.narrate("observation", observation, metadata)

    def reason(self, reasoning: str, **metadata) -> Dict[str, Any]:
        """Record reasoning process."""
        return self.narrate("reasoning", reasoning, metadata)

    def decide(self, decision: str, **metadata) -> Dict[str, Any]:
        """Record a decision."""
        return self.narrate("decision", decision, metadata)

    def act(self, action: str, **metadata) -> Dict[str, Any]:
        """Record an action."""
        return self.narrate("action", action, metadata)

    def reflect(self, reflection: str, **metadata) -> Dict[str, Any]:
        """Record a reflection on past actions."""
        return self.narrate("reflection", reflection, metadata)

    def error(self, error_msg: str, **metadata) -> Dict[str, Any]:
        """Record an error or contradiction."""
        return self.narrate("error", error_msg, metadata)

    def enter_thought_depth(self):
        """Enter a deeper level of reasoning (like recursion)."""
        self.current_thought_depth += 1

    def exit_thought_depth(self):
        """Exit current reasoning level."""
        self.current_thought_depth = max(0, self.current_thought_depth - 1)

    def get_narrative(self,
                     limit: int = None,
                     thought_type: str = None) -> List[Dict[str, Any]]:
        """
        Retrieve narrative stream.

        Args:
            limit: Maximum number of entries to return (most recent)
            thought_type: Filter by thought type
        """
        stream = self.narrative_stream

        if thought_type:
            stream = [e for e in stream if e["type"] == thought_type]

        if limit:
            stream = stream[-limit:]

        return stream

    def get_narrative_text(self, limit: int = None) -> str:
        """
        Get narrative as formatted text.
        """
        entries = self.get_narrative(limit)
        lines = []

        for entry in entries:
            indent = "  " * entry["depth"]
            timestamp = entry["timestamp"].split("T")[1][:8]  # Just time
            type_label = entry["type"].upper()
            content = entry["content"]

            lines.append(f"{indent}[{timestamp}] {type_label}: {content}")

        return "\n".join(lines)

    def clear_narrative(self):
        """Clear the narrative stream (use carefully)."""
        self.narrative_stream = []
        self.current_thought_depth = 0

    def to_json(self, limit: int = None) -> str:
        """Export narrative to JSON."""
        return json.dumps(self.get_narrative(limit), indent=2)

    def __repr__(self) -> str:
        return f"<SelfNarrator entries={len(self.narrative_stream)}>"
