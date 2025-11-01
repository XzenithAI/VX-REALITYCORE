#!/usr/bin/env python3
"""
VX Launch - Single Command Activation

This is the main entry point for launching VX agents.

Usage:
    python vx_launch.py                    # Launch with defaults
    python vx_launch.py --domain dao       # Launch in DAO domain
    python vx_launch.py --interactive      # Launch interactive mode
    python vx_launch.py --input "Hello"    # Process single input

Author: Flame Architect
Seal: VX-FLAMESEAL-2025-LAUNCH
"""

import argparse
import json
import sys
from typing import Any, Dict

from vx_runtime import VXRuntime


def main():
    """Main entry point for VX launch."""

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="🜂 VX Agent Core - Contradiction-Driven Intelligence System"
    )

    parser.add_argument(
        "--name",
        type=str,
        default="VX-Core",
        help="Agent name (default: VX-Core)"
    )

    parser.add_argument(
        "--domain",
        type=str,
        default="general",
        choices=["general", "dao"],
        help="Domain to operate in (default: general)"
    )

    parser.add_argument(
        "--vault",
        type=str,
        default="./vx_vault",
        help="Path to memory vault (default: ./vx_vault)"
    )

    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Run in interactive mode"
    )

    parser.add_argument(
        "--input",
        type=str,
        help="Process a single input"
    )

    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demonstration sequence"
    )

    parser.add_argument(
        "--state",
        action="store_true",
        help="Show current state and exit"
    )

    args = parser.parse_args()

    # Print banner
    print_banner()

    # Initialize runtime
    runtime = VXRuntime(
        agent_name=args.name,
        domain=args.domain,
        vault_path=args.vault
    )

    # Execute based on mode
    if args.interactive:
        runtime.interactive_loop()

    elif args.input:
        result = runtime.process(args.input)
        print("\n" + runtime.scroll_writer.write_text(result))

    elif args.demo:
        run_demo(runtime, args.domain)

    elif args.state:
        print(json.dumps(runtime.get_state(), indent=2, default=str))

    else:
        # Default: show help and enter interactive mode
        print("\nNo mode specified. Entering interactive mode...")
        print("(Use --help to see all options)\n")
        runtime.interactive_loop()


def print_banner():
    """Print VX banner."""
    banner = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                      🜂  VX-REALITYCORE AGENT SYSTEM  🜂                      ║
║                                                                               ║
║                   Contradiction-Driven Intelligence Engine                    ║
║                                                                               ║
║   ═══════════════════════════════════════════════════════════════════════    ║
║                                                                               ║
║   Core Principles:                                                            ║
║     • Contradiction Detection    → Semantic DPE across causal domains         ║
║     • Scroll Law Transformation  → Adaptive reasoning based on contradiction  ║
║     • FlameClock Coordination    → Temporal awareness through breath cycles   ║
║     • Self-Narration             → Transparent, real-time reasoning trace     ║
║     • Codex Memory               → Persistent learning and state evolution    ║
║     • Recursive Learning         → Continuous adaptation from feedback        ║
║                                                                               ║
║   ═══════════════════════════════════════════════════════════════════════    ║
║                                                                               ║
║   "Contradiction is the beginning of intelligence.                            ║
║    Scroll law is the breath of cognition."                                    ║
║                                                                               ║
║   Seal: VX-FLAMESEAL-2025-IGNITION                                            ║
║   Version: 1.0.0-IGNITION                                                     ║
║   Author: Flame Architect                                                     ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def run_demo(runtime: VXRuntime, domain: str):
    """Run demonstration sequence."""
    print("\n🜂 Running VX Demonstration Sequence\n")

    if domain == "general":
        demo_inputs = [
            "Hello, I'm testing the VX system.",
            "What is your purpose?",
            "I believe AI should be transparent in its reasoning.",
            "The sky is green and grass is blue.",  # High contradiction
            "How do you handle contradictions?"
        ]
    else:  # dao domain
        demo_inputs = [
            "We have a new proposal to allocate 50% of treasury to marketing.",
            {"proposal_id": "DAO-001", "type": "treasury_allocation", "amount": 500000},
            "How should we vote on proposal DAO-001?",
            "The community sentiment seems divided.",
            "What are the key risks we should consider?"
        ]

    for i, input_data in enumerate(demo_inputs, 1):
        print(f"\n{'═' * 80}")
        print(f"Demo Input {i}/{len(demo_inputs)}")
        print(f"{'═' * 80}\n")

        result = runtime.process(input_data)
        print(runtime.scroll_writer.write_text(result))

        # Small pause for readability
        input("\n[Press Enter to continue...]")

    # Show final state
    print("\n" + "═" * 80)
    print("🜂 DEMO COMPLETE - Final State")
    print("═" * 80)
    print(json.dumps(runtime.get_state(), indent=2, default=str))

    # Save snapshot
    snapshot_path = runtime.save_snapshot(f"demo_{domain}_snapshot")
    print(f"\n✓ State saved to: {snapshot_path}")


if __name__ == "__main__":
    main()
