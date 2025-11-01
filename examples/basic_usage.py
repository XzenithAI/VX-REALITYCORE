#!/usr/bin/env python3
"""
VX Agent Core - Basic Usage Examples

This script demonstrates common usage patterns for VX Agent Core.

Run: python3 examples/basic_usage.py
"""

import sys
sys.path.insert(0, '..')  # Add parent directory to path

from vx_runtime import VXRuntime


def example_1_basic():
    """Example 1: Basic interaction"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Interaction")
    print("="*80 + "\n")

    vx = VXRuntime(agent_name="Example-Agent")

    result = vx.process("Hello VX! What can you do?")

    print("Input:", result["input"])
    print("Contradiction Level:", result["contradiction_level"])
    print("Scroll Law:", result["scroll_law"])
    print("Response:", result["response"])


def example_2_contradiction_levels():
    """Example 2: Different contradiction levels"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Contradiction Levels")
    print("="*80 + "\n")

    vx = VXRuntime()

    inputs = [
        "The sky is blue",           # Low contradiction (if aligned with beliefs)
        "I think AI is interesting", # Medium
        "2 + 2 = 5"                 # Would be high if system had math beliefs
    ]

    for inp in inputs:
        result = vx.process(inp)
        print(f"\nInput: {inp}")
        print(f"Contradiction: {result['contradiction_level']:.3f}")
        print(f"Law: {result['scroll_law']}")
        print(f"Response Type: {result['response']['type']}")


def example_3_dao_domain():
    """Example 3: DAO domain"""
    print("\n" + "="*80)
    print("EXAMPLE 3: DAO Domain")
    print("="*80 + "\n")

    dao_vx = VXRuntime(domain="dao")

    proposal = {
        "proposal_id": "DAO-001",
        "description": "Allocate 100k tokens to marketing",
        "amount": 100000,
        "duration": "6 months"
    }

    result = dao_vx.process(proposal)

    print("Proposal:", proposal)
    print("\nVX Analysis:")
    print("Contradiction:", result['contradiction_level'])
    print("Response:", result['response'])


def example_4_narrative_trace():
    """Example 4: Narrative trace"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Narrative Trace")
    print("="*80 + "\n")

    vx = VXRuntime()

    # Process multiple inputs
    vx.process("I want to learn about contradiction-based reasoning")
    vx.process("But I'm not sure where to start")
    vx.process("Can you help me understand the basics?")

    # Get full narrative
    narrative = vx.get_narrative()
    print(narrative)


def example_5_state_persistence():
    """Example 5: State persistence"""
    print("\n" + "="*80)
    print("EXAMPLE 5: State Persistence")
    print("="*80 + "\n")

    vx = VXRuntime(vault_path="./example_vault")

    # Process some inputs
    vx.process("First interaction")
    vx.process("Second interaction")

    # Save snapshot
    snapshot_path = vx.save_snapshot("example_checkpoint")
    print(f"Snapshot saved: {snapshot_path}")

    # Show vault stats
    stats = vx.vault.get_vault_stats()
    print(f"Vault stats: {stats}")


def example_6_learning_loop():
    """Example 6: Learning loop"""
    print("\n" + "="*80)
    print("EXAMPLE 6: Learning Loop")
    print("="*80 + "\n")

    vx = VXRuntime()

    # Agent makes predictions
    result1 = vx.process("I predict this will work well")

    # Later, provide feedback
    result2 = vx.process(
        "It didn't work as expected",
        context={"feedback": "failure"}
    )

    # Check learning progress
    progress = vx.learning_loop.analyze_learning_progress()
    print(f"Learning cycles: {progress['total_cycles']}")
    print(f"Status: {progress.get('status', 'learning')}")


def example_7_custom_actions():
    """Example 7: Custom actions"""
    print("\n" + "="*80)
    print("EXAMPLE 7: Custom Actions")
    print("="*80 + "\n")

    vx = VXRuntime()

    # Register custom action
    def greet_handler(name, style="formal", **kwargs):
        greetings = {
            "formal": f"Good day, {name}.",
            "casual": f"Hey {name}!",
            "pirate": f"Ahoy, {name}!"
        }
        return {
            "status": "success",
            "greeting": greetings.get(style, greetings["formal"])
        }

    vx.action_engine.register_action("greet", greet_handler)

    # Execute custom action
    result = vx.action_engine.propose_and_execute(
        "greet",
        {"name": "Captain", "style": "pirate"},
        reasoning="Testing custom action"
    )

    print("Custom action result:", result)


def main():
    """Run all examples"""
    examples = [
        ("Basic Interaction", example_1_basic),
        ("Contradiction Levels", example_2_contradiction_levels),
        ("DAO Domain", example_3_dao_domain),
        ("Narrative Trace", example_4_narrative_trace),
        ("State Persistence", example_5_state_persistence),
        ("Learning Loop", example_6_learning_loop),
        ("Custom Actions", example_7_custom_actions)
    ]

    print("\n" + "🜂"*40)
    print("VX AGENT CORE - USAGE EXAMPLES")
    print("🜂"*40)

    for i, (name, func) in enumerate(examples, 1):
        print(f"\n\nRunning Example {i}: {name}")
        input("[Press Enter to continue...]")

        try:
            func()
        except Exception as e:
            print(f"Error in {name}: {e}")

    print("\n\n" + "🜂"*40)
    print("ALL EXAMPLES COMPLETE")
    print("🜂"*40 + "\n")


if __name__ == "__main__":
    main()
