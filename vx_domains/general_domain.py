"""
General Domain - Default Domain for Open-Ended Interaction

The General Domain handles:
- Text-based conversations
- General reasoning tasks
- Information synthesis
- Open-ended queries

This is the default domain when no specific domain is specified.
"""

from typing import Any, Dict, List
from .base_domain import BaseDomain


class GeneralDomain(BaseDomain):
    """
    General-purpose domain for open-ended interaction.
    """

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("general", config)

    def process_input(self, raw_input: Any, context: Dict[str, Any] = None) -> Any:
        """
        Process input for general domain.

        In general domain, we mostly pass through the input as-is,
        but we can add metadata.
        """
        processed = {
            "content": raw_input,
            "type": self._infer_input_type(raw_input),
            "domain": self.name,
            "context": context or {}
        }

        return processed

    def _infer_input_type(self, raw_input: Any) -> str:
        """Infer input type."""
        if isinstance(raw_input, str):
            if "?" in raw_input:
                return "question"
            elif any(cmd in raw_input.lower() for cmd in ["create", "build", "make", "generate"]):
                return "command"
            else:
                return "statement"
        elif isinstance(raw_input, dict):
            return "structured_data"
        elif isinstance(raw_input, list):
            return "sequence"
        else:
            return "unknown"

    def get_available_actions(self) -> List[str]:
        """Get available actions in general domain."""
        return [
            "respond",
            "query",
            "synthesize",
            "reflect",
            "clarify"
        ]

    def register_actions(self, action_engine):
        """Register general domain actions."""

        def respond_handler(message: str, **kwargs) -> Dict[str, Any]:
            return {
                "status": "success",
                "action": "respond",
                "message": message
            }

        def query_handler(query: str, **kwargs) -> Dict[str, Any]:
            return {
                "status": "success",
                "action": "query",
                "query": query,
                "note": "Query processed (implement specific logic as needed)"
            }

        def synthesize_handler(sources: List[str], **kwargs) -> Dict[str, Any]:
            return {
                "status": "success",
                "action": "synthesize",
                "sources_count": len(sources),
                "synthesis": f"Synthesized {len(sources)} sources"
            }

        def clarify_handler(clarification: str, **kwargs) -> Dict[str, Any]:
            return {
                "status": "success",
                "action": "clarify",
                "clarification": clarification
            }

        action_engine.register_action("respond", respond_handler)
        action_engine.register_action("query", query_handler)
        action_engine.register_action("synthesize", synthesize_handler)
        action_engine.register_action("clarify", clarify_handler)

    def evaluate_outcome(self,
                        action: Dict[str, Any],
                        outcome: Any,
                        context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Evaluate outcome in general domain."""
        return {
            "success": outcome.get("status") == "success",
            "domain": self.name,
            "action_type": action.get("action_type"),
            "evaluation": "General domain evaluation"
        }
