"""
Action Engine - Proposal and Execution System

The Action Engine translates agent decisions into executable actions.

Unlike traditional action systems, VX actions are:
- Proposed with full reasoning
- Evaluated for contradiction before execution
- Monitored for outcomes
- Fed back for learning

This creates a closed loop: Think → Propose → Execute → Observe → Learn
"""

from typing import Any, Dict, List, Callable, Optional
from datetime import datetime
import json


class Action:
    """Represents a proposed or executed action."""

    def __init__(self,
                 action_type: str,
                 parameters: Dict[str, Any],
                 reasoning: str = "",
                 confidence: float = 1.0):
        """
        Create an action.

        Args:
            action_type: Type of action (send_message, update_belief, query_data, etc.)
            parameters: Action parameters
            reasoning: Why this action was chosen
            confidence: Confidence in this action (0.0 to 1.0)
        """
        self.action_type = action_type
        self.parameters = parameters
        self.reasoning = reasoning
        self.confidence = confidence
        self.status = "proposed"
        self.result = None
        self.created_at = datetime.now()
        self.executed_at = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "action_type": self.action_type,
            "parameters": self.parameters,
            "reasoning": self.reasoning,
            "confidence": self.confidence,
            "status": self.status,
            "result": self.result,
            "created_at": self.created_at.isoformat(),
            "executed_at": self.executed_at.isoformat() if self.executed_at else None
        }


class ActionEngine:
    """
    The Action Engine manages action proposal and execution.

    It maintains:
    - Action registry (available actions)
    - Execution history
    - Outcome tracking
    """

    def __init__(self):
        """Initialize Action Engine."""
        self.action_handlers = {}
        self.action_history = []
        self._register_default_actions()

    def _register_default_actions(self):
        """Register default action handlers."""

        # Output action
        def output_handler(text: str, **kwargs) -> Dict[str, Any]:
            return {
                "status": "success",
                "output": text,
                "method": "console"
            }

        # Belief update action
        def update_belief_handler(domain: str, new_value: Any, **kwargs) -> Dict[str, Any]:
            return {
                "status": "success",
                "domain": domain,
                "updated_value": str(new_value)[:100]
            }

        # Query action
        def query_handler(query: str, **kwargs) -> Dict[str, Any]:
            return {
                "status": "success",
                "query": query,
                "result": "Query processed (implement domain-specific logic)"
            }

        # Reflection action
        def reflect_handler(reflection: str, **kwargs) -> Dict[str, Any]:
            return {
                "status": "success",
                "reflection": reflection
            }

        self.register_action("output", output_handler)
        self.register_action("update_belief", update_belief_handler)
        self.register_action("query", query_handler)
        self.register_action("reflect", reflect_handler)

    def register_action(self, action_type: str, handler: Callable):
        """
        Register an action handler.

        Args:
            action_type: Name of action type
            handler: Function that executes the action
        """
        self.action_handlers[action_type] = handler

    def propose(self,
                action_type: str,
                parameters: Dict[str, Any],
                reasoning: str = "",
                confidence: float = 1.0) -> Action:
        """
        Propose an action.

        Args:
            action_type: Type of action
            parameters: Action parameters
            reasoning: Why this action
            confidence: Confidence level

        Returns:
            Action object
        """
        action = Action(action_type, parameters, reasoning, confidence)
        return action

    def execute(self, action: Action) -> Dict[str, Any]:
        """
        Execute a proposed action.

        Args:
            action: Action to execute

        Returns:
            Execution result
        """
        if action.action_type not in self.action_handlers:
            return {
                "status": "error",
                "message": f"Unknown action type: {action.action_type}"
            }

        # Execute handler
        handler = self.action_handlers[action.action_type]

        try:
            result = handler(**action.parameters)
            action.status = "executed"
            action.result = result
            action.executed_at = datetime.now()

        except Exception as e:
            result = {
                "status": "error",
                "message": str(e)
            }
            action.status = "failed"
            action.result = result

        # Record in history
        self.action_history.append(action)

        return result

    def propose_and_execute(self,
                           action_type: str,
                           parameters: Dict[str, Any],
                           reasoning: str = "",
                           confidence: float = 1.0) -> Dict[str, Any]:
        """
        Propose and immediately execute an action.

        Args:
            action_type: Type of action
            parameters: Action parameters
            reasoning: Why this action
            confidence: Confidence level

        Returns:
            Execution result
        """
        action = self.propose(action_type, parameters, reasoning, confidence)
        return self.execute(action)

    def get_available_actions(self) -> List[str]:
        """Get list of available action types."""
        return list(self.action_handlers.keys())

    def get_history(self, limit: int = 10, action_type: str = None) -> List[Action]:
        """
        Get action history.

        Args:
            limit: Maximum number of actions to return
            action_type: Filter by action type

        Returns:
            List of actions
        """
        history = self.action_history

        if action_type:
            history = [a for a in history if a.action_type == action_type]

        return history[-limit:]

    def get_success_rate(self, action_type: str = None) -> float:
        """
        Calculate success rate of actions.

        Args:
            action_type: Optional filter by action type

        Returns:
            Success rate (0.0 to 1.0)
        """
        history = self.action_history

        if action_type:
            history = [a for a in history if a.action_type == action_type]

        if not history:
            return 0.0

        successful = sum(1 for a in history if a.status == "executed")
        return successful / len(history)

    def to_json(self) -> str:
        """Export engine state to JSON."""
        return json.dumps({
            "available_actions": self.get_available_actions(),
            "total_actions": len(self.action_history),
            "success_rate": self.get_success_rate(),
            "recent_actions": [a.to_dict() for a in self.get_history(5)]
        }, indent=2, default=str)

    def __repr__(self) -> str:
        return f"<ActionEngine actions={len(self.action_handlers)} history={len(self.action_history)}>"
