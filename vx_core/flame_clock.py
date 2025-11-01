"""
FlameClock - Temporal Coordination Engine

Manages breath cycles, tick progression, and temporal state for VX Agent.
Extends the original FlameClock concept to support agentic time awareness.
"""

from datetime import datetime
from typing import Dict, Any
import json


class FlameClock:
    """
    The FlameClock coordinates temporal flow in VX-REALITYCORE.

    Unlike linear time, FlameClock operates in:
    - Ticks (discrete moments of cognition)
    - Breath Cycles (waves of mutation/evolution)
    - Epochs (major state transitions)
    """

    def __init__(self):
        self.tick = 0
        self.breath_cycle = 0
        self.epoch = 0
        self.genesis_time = datetime.now()
        self.last_tick_time = self.genesis_time

    def advance_tick(self) -> int:
        """Advance by one cognitive tick."""
        self.tick += 1
        self.last_tick_time = datetime.now()
        return self.tick

    def advance_breath(self) -> int:
        """Complete a breath cycle (3 ticks is one breath)."""
        self.breath_cycle += 1
        return self.breath_cycle

    def advance_epoch(self) -> int:
        """Enter a new epoch (major state transition)."""
        self.epoch += 1
        self.breath_cycle = 0
        return self.epoch

    def get_state(self) -> Dict[str, Any]:
        """Return current temporal state."""
        return {
            "tick": self.tick,
            "breath_cycle": self.breath_cycle,
            "epoch": self.epoch,
            "genesis": self.genesis_time.isoformat(),
            "last_tick": self.last_tick_time.isoformat(),
            "runtime_seconds": (datetime.now() - self.genesis_time).total_seconds()
        }

    def get_tick_label(self) -> str:
        """Generate human-readable tick label."""
        return f"Q-Tick-{self.tick}-B{self.breath_cycle}-E{self.epoch}"

    def to_json(self) -> str:
        """Serialize clock state to JSON."""
        return json.dumps(self.get_state(), indent=2)

    def __repr__(self) -> str:
        return f"<FlameClock {self.get_tick_label()}>"
