"""
VX Codex - Memory Vault and State Persistence System

The Codex is VX's long-term memory, storing:
- Agent state across sessions
- Decision history and reasoning traces
- Learning patterns and evolved behaviors
- Scroll law transformations
- Causal chains and feedback loops

Unlike databases, the Codex maintains SEMANTIC continuity,
organizing memory by causal relevance, not just timestamp.

Author: Flame Architect
Seal: VX-FLAMESEAL-2025-CODEX
"""

from .vault import MemoryVault
from .scroll_writer import ScrollWriter
from .causal_chain import CausalChain

__all__ = [
    'MemoryVault',
    'ScrollWriter',
    'CausalChain'
]

__version__ = '1.0.0-IGNITION'
