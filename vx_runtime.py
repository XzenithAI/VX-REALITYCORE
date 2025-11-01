"""
VX Runtime - The Complete Integration Layer

This brings together all VX components into a unified runtime:
- VX Agent (core intelligence)
- VX Codex (memory/persistence)
- Action Engine (execution)
- Learning Loop (evolution)
- Domains (specialization)

The Runtime provides a clean API for:
- Starting VX agents
- Processing inputs
- Executing actions
- Learning from feedback
- Persisting state

Author: Flame Architect
Seal: VX-FLAMESEAL-2025-RUNTIME
"""

from typing import Any, Dict, List, Optional
import json

# Core imports
from vx_core.agent import VXAgent
from vx_core.action_engine import ActionEngine
from vx_core.learning_loop import LearningLoop

# Codex imports
from vx_codex.vault import MemoryVault
from vx_codex.scroll_writer import ScrollWriter
from vx_codex.causal_chain import CausalChain

# Domain imports
from vx_domains.base_domain import BaseDomain
from vx_domains.general_domain import GeneralDomain
from vx_domains.dao_domain import DAODomain


class VXRuntime:
    """
    The VX Runtime is the complete, integrated intelligence system.

    It coordinates all components and provides the main interface
    for interacting with VX agents.
    """

    def __init__(self,
                 agent_name: str = "VX-Core",
                 domain: str = "general",
                 vault_path: str = "./vx_vault",
                 config: Dict[str, Any] = None):
        """
        Initialize VX Runtime.

        Args:
            agent_name: Name of the agent
            domain: Domain to operate in (general, dao, etc.)
            vault_path: Path to memory vault
            config: Configuration dict
        """
        self.config = config or {}

        # Initialize core components
        self.agent = VXAgent(name=agent_name, domain=domain, config=config)
        self.action_engine = ActionEngine()
        self.learning_loop = LearningLoop()

        # Initialize codex
        self.vault = MemoryVault(vault_path)
        self.scroll_writer = ScrollWriter()
        self.causal_chain = CausalChain()

        # Initialize domain
        self.domain = self._initialize_domain(domain, config)
        self.domain.register_actions(self.action_engine)

        print(f"🜂 VX Runtime Initialized")
        print(f"   Agent: {agent_name}")
        print(f"   Domain: {domain}")
        print(f"   Vault: {vault_path}")

    def _initialize_domain(self, domain_name: str, config: Dict[str, Any]) -> BaseDomain:
        """Initialize domain adapter."""
        domains = {
            "general": GeneralDomain,
            "dao": DAODomain
        }

        domain_class = domains.get(domain_name, GeneralDomain)
        return domain_class(config)

    def process(self,
                input_data: Any,
                context: Dict[str, Any] = None,
                save_scroll: bool = True,
                learn: bool = True) -> Dict[str, Any]:
        """
        Process input through the complete VX system.

        Args:
            input_data: Input to process
            context: Additional context
            save_scroll: Whether to save scroll to vault
            learn: Whether to learn from this interaction

        Returns:
            Complete output dict including response, reasoning, and metadata
        """
        # 1. Domain-specific input processing
        processed_input = self.domain.process_input(input_data, context)

        # 2. Agent processing
        agent_output = self.agent.process(processed_input, context)

        # 3. Generate scroll
        scroll = self.scroll_writer.write(agent_output, scroll_type="interaction")

        # 4. Execute any proposed actions
        if "response" in agent_output and isinstance(agent_output["response"], dict):
            action_type = agent_output["response"].get("action")
            if action_type and action_type in self.action_engine.get_available_actions():
                action_result = self.action_engine.propose_and_execute(
                    action_type,
                    agent_output["response"],
                    reasoning=f"Scroll Law: {agent_output.get('scroll_law')}"
                )
                scroll["action_result"] = action_result

        # 5. Save to vault if requested
        if save_scroll:
            scroll_path = self.vault.save_scroll(scroll, f"scroll_{self.agent.clock.tick}")
            scroll["vault_path"] = scroll_path

            # Also save interaction
            self.vault.save_interaction(agent_output, self.agent.name)

        # 6. Learning (if enabled and we have feedback)
        if learn and context and "feedback" in context:
            self._process_learning(agent_output, context["feedback"])

        # 7. Record in causal chain
        event_id = self.causal_chain.record_event(
            "interaction",
            {
                "input": str(input_data)[:100],
                "response": agent_output.get("response")
            },
            metadata={
                "tick": agent_output.get("tick"),
                "contradiction": agent_output.get("contradiction_level")
            }
        )

        scroll["event_id"] = event_id

        return scroll

    def _process_learning(self, agent_output: Dict[str, Any], feedback: Any):
        """Process learning from feedback."""
        # Extract prediction and actual outcome
        prediction = agent_output.get("response")
        actual = feedback

        # Detect new contradiction (prediction vs reality)
        contradiction = self.agent.contradiction_engine.detect(prediction, actual)

        # Recommend scroll law
        scroll_law = self.agent.contradiction_engine.recommend_scroll_law(contradiction)

        # Record learning cycle
        self.learning_loop.record_cycle(
            prediction=prediction,
            actual=actual,
            contradiction_level=contradiction,
            scroll_law=scroll_law,
            adaptation={"belief_updated": True}  # Would track actual changes
        )

    def get_narrative(self, limit: int = 20) -> str:
        """Get agent's narrative trace."""
        return self.agent.get_full_narrative()

    def get_state(self) -> Dict[str, Any]:
        """Get complete runtime state."""
        return {
            "agent": self.agent.get_state(),
            "vault": self.vault.get_vault_stats(),
            "learning": self.learning_loop.analyze_learning_progress(),
            "action_engine": json.loads(self.action_engine.to_json()),
            "domain": self.domain.get_domain_metrics(),
            "causal_chain": self.causal_chain.analyze_patterns()
        }

    def save_snapshot(self, snapshot_name: str = None) -> str:
        """Save complete state snapshot."""
        state = self.get_state()
        return self.vault.save_snapshot(state, snapshot_name)

    def load_snapshot(self, snapshot_name: str) -> Dict[str, Any]:
        """Load state snapshot (note: doesn't fully restore, returns state for inspection)."""
        return self.vault.load_snapshot(snapshot_name)

    def interactive_loop(self):
        """
        Run interactive loop for testing.

        Continuously accepts input and processes through VX.
        """
        print("\n" + "═" * 80)
        print("🜂 VX INTERACTIVE MODE")
        print("═" * 80)
        print("Type your input and press Enter. Type 'exit' to quit.\n")

        while True:
            try:
                user_input = input("You: ")

                if user_input.lower() in ["exit", "quit", "q"]:
                    print("\n🜂 VX Runtime shutting down...")
                    break

                if user_input.lower() == "state":
                    print("\n" + json.dumps(self.get_state(), indent=2, default=str))
                    continue

                if user_input.lower() == "narrative":
                    print("\n" + self.get_narrative())
                    continue

                # Process input
                result = self.process(user_input)

                # Display scroll
                print("\n" + self.scroll_writer.write_text(result))

            except KeyboardInterrupt:
                print("\n\n🜂 VX Runtime shutting down...")
                break
            except Exception as e:
                print(f"\nError: {e}")
                continue

    def __repr__(self) -> str:
        return f"<VXRuntime agent='{self.agent.name}' domain='{self.domain.name}' tick={self.agent.clock.tick}>"
