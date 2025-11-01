"""
Causal Chain - Track Cause-Effect Relationships Across Time

The Causal Chain maintains relationships between:
- Inputs → Responses
- Decisions → Outcomes
- Predictions → Reality
- Actions → Feedback

This enables the agent to learn what actually works, not just what seems logical.
"""

from typing import Any, Dict, List, Optional
import json
from datetime import datetime


class CausalChain:
    """
    The Causal Chain links events across time to discover patterns.

    Unlike simple logs, this tracks:
    - What caused what
    - How long effects took to manifest
    - Which predictions were accurate
    - Which actions led to desired outcomes
    """

    def __init__(self):
        self.events = []
        self.links = []

    def record_event(self,
                    event_type: str,
                    content: Any,
                    metadata: Dict[str, Any] = None) -> str:
        """
        Record an event in the chain.

        Args:
            event_type: Type of event (input, decision, action, outcome, etc.)
            content: Event content
            metadata: Additional context

        Returns:
            Event ID
        """
        event_id = f"event_{len(self.events)}_{datetime.now().timestamp()}"

        event = {
            "id": event_id,
            "type": event_type,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }

        self.events.append(event)
        return event_id

    def link_events(self,
                   cause_id: str,
                   effect_id: str,
                   relationship: str = "caused",
                   strength: float = 1.0):
        """
        Link two events as cause-effect.

        Args:
            cause_id: ID of causing event
            effect_id: ID of effect event
            relationship: Type of relationship
            strength: Causal strength (0.0 to 1.0)
        """
        link = {
            "cause": cause_id,
            "effect": effect_id,
            "relationship": relationship,
            "strength": strength,
            "created_at": datetime.now().isoformat()
        }

        self.links.append(link)

    def get_effects(self, cause_id: str) -> List[Dict[str, Any]]:
        """Get all effects of a given cause."""
        effect_links = [l for l in self.links if l["cause"] == cause_id]

        effects = []
        for link in effect_links:
            effect_event = self._get_event_by_id(link["effect"])
            if effect_event:
                effects.append({
                    "event": effect_event,
                    "relationship": link["relationship"],
                    "strength": link["strength"]
                })

        return effects

    def get_causes(self, effect_id: str) -> List[Dict[str, Any]]:
        """Get all causes of a given effect."""
        cause_links = [l for l in self.links if l["effect"] == effect_id]

        causes = []
        for link in cause_links:
            cause_event = self._get_event_by_id(link["cause"])
            if cause_event:
                causes.append({
                    "event": cause_event,
                    "relationship": link["relationship"],
                    "strength": link["strength"]
                })

        return causes

    def trace_chain(self, start_event_id: str, direction: str = "forward") -> List[Dict[str, Any]]:
        """
        Trace causal chain from a starting event.

        Args:
            start_event_id: Starting event
            direction: "forward" (effects) or "backward" (causes)

        Returns:
            List of events in causal order
        """
        chain = []
        visited = set()
        queue = [start_event_id]

        while queue:
            current_id = queue.pop(0)

            if current_id in visited:
                continue

            visited.add(current_id)
            event = self._get_event_by_id(current_id)

            if event:
                chain.append(event)

                # Get next events
                if direction == "forward":
                    next_events = [e["event"]["id"] for e in self.get_effects(current_id)]
                else:
                    next_events = [c["event"]["id"] for c in self.get_causes(current_id)]

                queue.extend(next_events)

        return chain

    def get_recent_events(self, limit: int = 10, event_type: str = None) -> List[Dict[str, Any]]:
        """Get recent events, optionally filtered by type."""
        events = self.events

        if event_type:
            events = [e for e in events if e["type"] == event_type]

        return events[-limit:]

    def analyze_patterns(self) -> Dict[str, Any]:
        """
        Analyze causal patterns in the chain.

        Returns:
            Dict with pattern statistics
        """
        # Count event types
        event_types = {}
        for event in self.events:
            event_type = event["type"]
            event_types[event_type] = event_types.get(event_type, 0) + 1

        # Count relationship types
        relationships = {}
        for link in self.links:
            rel_type = link["relationship"]
            relationships[rel_type] = relationships.get(rel_type, 0) + 1

        # Average causal strength
        if self.links:
            avg_strength = sum(l["strength"] for l in self.links) / len(self.links)
        else:
            avg_strength = 0.0

        return {
            "total_events": len(self.events),
            "total_links": len(self.links),
            "event_types": event_types,
            "relationship_types": relationships,
            "average_causal_strength": avg_strength
        }

    def _get_event_by_id(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Find event by ID."""
        for event in self.events:
            if event["id"] == event_id:
                return event
        return None

    def to_json(self) -> str:
        """Export chain to JSON."""
        return json.dumps({
            "events": self.events,
            "links": self.links,
            "patterns": self.analyze_patterns()
        }, indent=2, default=str)

    def __repr__(self) -> str:
        return f"<CausalChain events={len(self.events)} links={len(self.links)}>"
