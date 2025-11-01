"""
Base Domain - Abstract Interface for All Domains

All domain adapters inherit from BaseDomain and implement:
- Input processing
- Action registration
- Evaluation metrics
- Custom scroll laws (optional)
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseDomain(ABC):
    """
    Abstract base class for VX domain adapters.

    Each domain specializes VX for a specific context.
    """

    def __init__(self, name: str, config: Dict[str, Any] = None):
        """
        Initialize domain.

        Args:
            name: Domain identifier
            config: Domain-specific configuration
        """
        self.name = name
        self.config = config or {}

    @abstractmethod
    def process_input(self, raw_input: Any, context: Dict[str, Any] = None) -> Any:
        """
        Process raw input into domain-specific format.

        Args:
            raw_input: Raw input data
            context: Additional context

        Returns:
            Processed input suitable for VX Agent
        """
        pass

    @abstractmethod
    def get_available_actions(self) -> List[str]:
        """
        Get list of actions available in this domain.

        Returns:
            List of action names
        """
        pass

    @abstractmethod
    def register_actions(self, action_engine):
        """
        Register domain-specific actions with action engine.

        Args:
            action_engine: ActionEngine instance
        """
        pass

    def evaluate_outcome(self,
                        action: Dict[str, Any],
                        outcome: Any,
                        context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate action outcome in domain context.

        Args:
            action: Action that was taken
            outcome: Resulting outcome
            context: Additional context

        Returns:
            Evaluation dict with metrics
        """
        # Default evaluation
        return {
            "success": outcome.get("status") == "success",
            "domain": self.name,
            "evaluation": "default"
        }

    def get_domain_metrics(self) -> Dict[str, Any]:
        """
        Get domain-specific performance metrics.

        Returns:
            Metrics dict
        """
        return {
            "domain": self.name,
            "status": "active"
        }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name='{self.name}'>"
