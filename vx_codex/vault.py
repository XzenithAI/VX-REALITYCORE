"""
Memory Vault - Persistent Storage for VX Agent State

The Vault manages:
- Agent snapshots (complete state saves)
- Interaction logs
- Belief evolution
- Narrative traces
"""

import json
import os
from typing import Any, Dict, List, Optional
from datetime import datetime
from pathlib import Path


class MemoryVault:
    """
    The Memory Vault persists VX Agent state to disk.

    Organization:
    - snapshots/ - Full agent state captures
    - interactions/ - Individual interaction logs
    - narratives/ - Reasoning traces
    - scrolls/ - Transformed outputs
    """

    def __init__(self, vault_path: str = "./vx_vault"):
        """
        Initialize Memory Vault.

        Args:
            vault_path: Root directory for vault storage
        """
        self.vault_path = Path(vault_path)
        self._ensure_structure()

    def _ensure_structure(self):
        """Create vault directory structure."""
        subdirs = ['snapshots', 'interactions', 'narratives', 'scrolls', 'causal_chains']

        for subdir in subdirs:
            (self.vault_path / subdir).mkdir(parents=True, exist_ok=True)

    def save_snapshot(self,
                     agent_state: Dict[str, Any],
                     snapshot_name: Optional[str] = None) -> str:
        """
        Save complete agent state snapshot.

        Args:
            agent_state: Full agent state dict
            snapshot_name: Optional custom name

        Returns:
            Path to saved snapshot
        """
        if snapshot_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            snapshot_name = f"snapshot_{timestamp}.json"

        snapshot_path = self.vault_path / "snapshots" / snapshot_name

        with open(snapshot_path, 'w') as f:
            json.dump(agent_state, f, indent=2, default=str)

        return str(snapshot_path)

    def load_snapshot(self, snapshot_name: str) -> Dict[str, Any]:
        """
        Load agent state snapshot.

        Args:
            snapshot_name: Name of snapshot file

        Returns:
            Agent state dict
        """
        snapshot_path = self.vault_path / "snapshots" / snapshot_name

        with open(snapshot_path, 'r') as f:
            return json.load(f)

    def list_snapshots(self) -> List[str]:
        """List all available snapshots."""
        snapshots_dir = self.vault_path / "snapshots"
        return sorted([f.name for f in snapshots_dir.glob("*.json")])

    def save_interaction(self,
                        interaction_data: Dict[str, Any],
                        agent_name: str = "vx") -> str:
        """
        Save single interaction.

        Args:
            interaction_data: Interaction dict (input, response, etc.)
            agent_name: Agent identifier

        Returns:
            Path to saved interaction
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{agent_name}_{timestamp}.json"
        interaction_path = self.vault_path / "interactions" / filename

        with open(interaction_path, 'w') as f:
            json.dump(interaction_data, f, indent=2, default=str)

        return str(interaction_path)

    def save_narrative(self,
                      narrative_data: List[Dict[str, Any]],
                      agent_name: str = "vx",
                      narrative_name: Optional[str] = None) -> str:
        """
        Save narrative trace.

        Args:
            narrative_data: List of narrative entries
            agent_name: Agent identifier
            narrative_name: Optional custom name

        Returns:
            Path to saved narrative
        """
        if narrative_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            narrative_name = f"{agent_name}_narrative_{timestamp}.json"

        narrative_path = self.vault_path / "narratives" / narrative_name

        with open(narrative_path, 'w') as f:
            json.dump(narrative_data, f, indent=2, default=str)

        return str(narrative_path)

    def save_scroll(self,
                   scroll_data: Dict[str, Any],
                   scroll_name: str) -> str:
        """
        Save a scroll (transformed output).

        Args:
            scroll_data: Scroll content
            scroll_name: Scroll identifier

        Returns:
            Path to saved scroll
        """
        scroll_path = self.vault_path / "scrolls" / f"{scroll_name}.json"

        with open(scroll_path, 'w') as f:
            json.dump(scroll_data, f, indent=2, default=str)

        return str(scroll_path)

    def get_latest_snapshot(self) -> Optional[Dict[str, Any]]:
        """Get most recent snapshot."""
        snapshots = self.list_snapshots()
        if not snapshots:
            return None

        return self.load_snapshot(snapshots[-1])

    def get_vault_stats(self) -> Dict[str, Any]:
        """Get vault statistics."""
        stats = {}

        for subdir in ['snapshots', 'interactions', 'narratives', 'scrolls']:
            dir_path = self.vault_path / subdir
            file_count = len(list(dir_path.glob("*.json")))
            stats[subdir] = file_count

        stats['vault_path'] = str(self.vault_path)
        stats['total_files'] = sum(stats[k] for k in stats if k != 'vault_path')

        return stats

    def __repr__(self) -> str:
        stats = self.get_vault_stats()
        return f"<MemoryVault path='{stats['vault_path']}' files={stats['total_files']}>"
