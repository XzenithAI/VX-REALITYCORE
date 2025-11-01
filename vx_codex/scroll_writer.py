"""
Scroll Writer - Formatted Output Generator

Converts agent outputs into scroll-formatted documents that can be:
- Read by humans
- Parsed by machines
- Fed back to the agent for learning
- Shared across systems

Scrolls are the "currency" of VX cognition.
"""

from typing import Any, Dict, List
from datetime import datetime
import json


class ScrollWriter:
    """
    The ScrollWriter formats agent outputs as scrolls.

    A scroll contains:
    - Seal (unique identifier)
    - Tick (temporal marker)
    - Input (what was received)
    - Reasoning (narrative trace)
    - Output (response/action)
    - Scroll Law (transformation applied)
    - Contradiction Level (detected)
    """

    def __init__(self):
        self.scroll_count = 0

    def write(self,
              agent_output: Dict[str, Any],
              scroll_type: str = "interaction") -> Dict[str, Any]:
        """
        Create a scroll from agent output.

        Args:
            agent_output: Output from VXAgent.process()
            scroll_type: Type of scroll (interaction, decision, reflection, etc.)

        Returns:
            Formatted scroll dict
        """
        self.scroll_count += 1

        scroll = {
            "seal": self._generate_seal(scroll_type),
            "scroll_type": scroll_type,
            "tick": agent_output.get("tick", "unknown"),
            "timestamp": datetime.now().isoformat(),
            "agent": agent_output.get("agent", "VX-Core"),

            # Core content
            "input": agent_output.get("input"),
            "response": agent_output.get("response"),

            # Reasoning
            "contradiction_level": agent_output.get("contradiction_level"),
            "scroll_law": agent_output.get("scroll_law"),
            "narration": agent_output.get("narration", []),

            # State
            "state": agent_output.get("state"),

            # Metadata
            "scroll_number": self.scroll_count,
            "version": "1.0.0-IGNITION"
        }

        return scroll

    def write_text(self, scroll: Dict[str, Any]) -> str:
        """
        Convert scroll to formatted text.

        Args:
            scroll: Scroll dict

        Returns:
            Human-readable text
        """
        lines = []

        # Header
        lines.append("═" * 80)
        lines.append(f"🜂 VX SCROLL - {scroll['scroll_type'].upper()}")
        lines.append(f"Seal: {scroll['seal']}")
        lines.append(f"Tick: {scroll['tick']}")
        lines.append(f"Timestamp: {scroll['timestamp']}")
        lines.append("═" * 80)

        # Input
        lines.append("\n📥 INPUT:")
        lines.append(f"  {scroll['input']}")

        # Contradiction & Law
        lines.append(f"\n⚡ CONTRADICTION LEVEL: {scroll['contradiction_level']:.3f}")
        lines.append(f"📜 SCROLL LAW: {scroll['scroll_law']}")

        # Response
        lines.append("\n📤 RESPONSE:")
        response = scroll['response']
        if isinstance(response, dict):
            for key, value in response.items():
                lines.append(f"  {key}: {value}")
        else:
            lines.append(f"  {response}")

        # Narration (if present)
        if scroll.get('narration'):
            lines.append("\n🧠 REASONING TRACE:")
            for entry in scroll['narration'][-5:]:  # Last 5 entries
                indent = "  " * (entry.get('depth', 0) + 1)
                lines.append(f"{indent}[{entry['type']}] {entry['content']}")

        # Footer
        lines.append("\n" + "═" * 80)
        lines.append(f"Scroll #{scroll['scroll_number']}")
        lines.append("═" * 80)

        return "\n".join(lines)

    def write_json(self, scroll: Dict[str, Any]) -> str:
        """
        Convert scroll to JSON.

        Args:
            scroll: Scroll dict

        Returns:
            JSON string
        """
        return json.dumps(scroll, indent=2, default=str)

    def _generate_seal(self, scroll_type: str) -> str:
        """Generate unique scroll seal."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"VX-SEAL-{scroll_type.upper()}-{timestamp}-{self.scroll_count:04d}"

    def __repr__(self) -> str:
        return f"<ScrollWriter scrolls_written={self.scroll_count}>"
