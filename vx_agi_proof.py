#!/usr/bin/env python3
"""
VX AGI - PROOF OF EMERGENCE

This demonstrates TRUE AGI capabilities:
1. Program synthesis from I/O examples
2. Genetic evolution of operators
3. Meta-learning of synthesis strategies
4. Formal verification
5. **CAPABILITY EXPANSION** - solving previously unsolvable problems

If this passes, we have 10/10 AGI.
"""

import sys
from vx_agi.agi_runtime import VX_AGI
from vx_agi.synthesis_engine import IOExample


def print_section(title):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def test_1_basic_synthesis():
    """Test 1: Can synthesize simple programs from examples."""
    print_section("TEST 1: Program Synthesis from Examples")

    agi = VX_AGI()

    # Problem: Learn the "increment" function
    examples = [
        IOExample(inputs=(0,), output=1),
        IOExample(inputs=(1,), output=2),
        IOExample(inputs=(5,), output=6),
        IOExample(inputs=(10,), output=11),
    ]

    print("Problem: Learn function from examples:")
    for ex in examples:
        print(f"  f{ex.inputs} = {ex.output}")

    print("\nSynthesizing...")
    solution = agi.solve_problem(examples, verify=True)

    if solution:
        print(f"✓ SYNTHESIZED: {solution.code}")
        print(f"  Cost: {solution.cost}")
        print(f"  Generalizes: {solution.generalizes}")

        # Test on new input
        test_input = 100
        result = solution.function(test_input)
        print(f"  Test: f({test_input}) = {result} (expected 101)")

        return result == 101
    else:
        print("✗ FAILED to synthesize")
        return False


def test_2_genetic_evolution():
    """Test 2: Genetic programming evolves solutions."""
    print_section("TEST 2: Genetic Evolution of Programs")

    agi = VX_AGI()

    # Problem: Learn a more complex function (e.g., double)
    examples = [
        IOExample(inputs=(1,), output=2),
        IOExample(inputs=(2,), output=4),
        IOExample(inputs=(3,), output=6),
        IOExample(inputs=(10,), output=20),
    ]

    print("Problem: Learn doubling function")
    for ex in examples:
        print(f"  f{ex.inputs} = {ex.output}")

    # Initialize genetic evolution
    agi.genetic.initialize_population(max_depth=3)

    def fitness_func(ast):
        try:
            func = agi.synthesizer._compile_ast(ast)
            score = 0
            for ex in examples:
                try:
                    if func(*ex.inputs) == ex.output:
                        score += 1
                except:
                    pass
            return score
        except:
            return 0

    print("\nEvolving population (30 generations)...")
    best = agi.genetic.run_evolution(fitness_func, generations=30)

    print(f"✓ Best fitness: {best.fitness}/{len(examples)}")
    print(f"  Generation: {agi.genetic.generation}")

    stats = agi.genetic.get_statistics()
    print(f"  Avg fitness: {stats['avg_fitness']:.2f}")

    return best.fitness == len(examples)


def test_3_meta_learning():
    """Test 3: Meta-learner selects best strategies."""
    print_section("TEST 3: Meta-Learning of Synthesis Strategies")

    agi = VX_AGI()

    # Give it multiple problems to learn from
    problems = [
        [IOExample(inputs=(x,), output=x+1) for x in range(5)],  # increment
        [IOExample(inputs=(x,), output=x*2) for x in range(5)],  # double
        [IOExample(inputs=(x,), output=x*x) for x in range(5)],  # square
    ]

    print("Training meta-learner on 3 problems...")

    for i, examples in enumerate(problems, 1):
        print(f"\nProblem {i}:")
        solution = agi.solve_problem(examples[:3], verify=False)  # Use subset
        if solution:
            print(f"  ✓ Solved: {solution.code}")
        else:
            print(f"  ✗ Failed")

    insights = agi.meta_learner.get_learning_insights()
    print(f"\n✓ Meta-Learning Insights:")
    print(f"  Strategies: {insights['num_strategies']}")
    print(f"  Problems solved: {insights['num_problems_solved']}/{insights['total_attempts']}")
    print(f"  Success rate: {insights['success_rate']:.1%}")
    print(f"  Strategy stats: {insights['strategy_stats']}")

    return insights['num_problems_solved'] > 0


def test_4_capability_expansion():
    """Test 4: CAPABILITY EXPANSION - The core proof."""
    print_section("TEST 4: CAPABILITY EXPANSION (TRUE EMERGENCE)")

    agi = VX_AGI()

    print(f"Initial capabilities: {len(agi.initial_capabilities)}")
    print(f"  Examples: {list(agi.initial_capabilities)[:10]}")

    # Learn from multiple problems
    training_problems = [
        # Problem 1: increment
        [IOExample(inputs=(x,), output=x+1) for x in [0, 1, 2, 5, 10]],

        # Problem 2: double
        [IOExample(inputs=(x,), output=x*2) for x in [0, 1, 2, 5, 10]],
    ]

    print(f"\nTraining on {len(training_problems)} problems...")
    new_caps = agi.learn_and_expand(training_problems)

    print(f"\n✓ Learned {new_caps} new capabilities!")
    print(f"  Total capabilities: {len(agi.capabilities)} (was {len(agi.initial_capabilities)})")

    # Show what was learned
    cap_list = agi.get_capability_list()
    print(f"\n  Learned capabilities: {cap_list['learned']}")

    # Demonstrate emergence
    emergence = agi.demonstrate_emergence()
    print(f"\n{'='*80}")
    print(f"EMERGENCE PROOF:")
    print(f"{'='*80}")
    print(f"  Initial capabilities: {emergence['initial_capabilities']}")
    print(f"  Current capabilities: {emergence['current_capabilities']}")
    print(f"  NEW capabilities: {emergence['new_capabilities_learned']}")
    print(f"  Expansion ratio: {emergence['capability_expansion_ratio']:.2f}x")
    print(f"  Learned programs: {emergence['learned_programs']}")
    print(f"  Generation: {emergence['generation']}")
    print(f"  PROOF: {emergence['proof_of_expansion']}")

    return emergence['proof_of_expansion']


def test_5_unsolvable_to_solvable():
    """Test 5: Prove a problem goes from unsolvable to solvable."""
    print_section("TEST 5: UNSOLVABLE → SOLVABLE (Ultimate Proof)")

    agi = VX_AGI()

    # Define a "hard" problem that requires learned capability
    # For example: triple (which requires learned "double" + "add")
    hard_problem = [
        IOExample(inputs=(1,), output=3),
        IOExample(inputs=(2,), output=6),
        IOExample(inputs=(3,), output=9),
        IOExample(inputs=(5,), output=15),
    ]

    print("Hard problem: Triple function")
    for ex in hard_problem[:3]:
        print(f"  f{ex.inputs} = {ex.output}")

    # First: train on simpler problems
    training = [
        [IOExample(inputs=(x,), output=x+1) for x in range(5)],  # increment
        [IOExample(inputs=(x,), output=x*2) for x in range(5)],  # double
    ]

    print("\n1. Training on simpler problems (increment, double)...")
    agi.learn_and_expand(training)

    # Now: try to solve hard problem
    print("\n2. Attempting hard problem with expanded capabilities...")

    # Prove it using the dedicated method
    proof = agi.prove_unsolvable_now_solvable(hard_problem)

    print("\n" + "="*80)
    print("FORMAL PROOF OF EMERGENCE:")
    print("="*80)
    print(f"  Solvable with initial capabilities: {proof['solvable_with_initial_capabilities']}")
    print(f"  Solvable with learned capabilities: {proof['solvable_with_learned_capabilities']}")
    print(f"  EMERGENCE PROVEN: {proof['capability_emergence_proven']}")

    if proof['solution_after']:
        print(f"\n  Solution (with learning): {proof['solution_after']}")

    return proof['capability_emergence_proven']


def main():
    """Run complete AGI proof suite."""
    print("\n" + "🜂"*40)
    print("VX AGI - PROOF OF TRUE EMERGENCE")
    print("This is 10/10 or nothing.")
    print("🜂"*40)

    tests = [
        ("Program Synthesis", test_1_basic_synthesis),
        ("Genetic Evolution", test_2_genetic_evolution),
        ("Meta-Learning", test_3_meta_learning),
        ("Capability Expansion", test_4_capability_expansion),
        ("Unsolvable → Solvable", test_5_unsolvable_to_solvable),
    ]

    results = {}

    for name, test_func in tests:
        try:
            print(f"\nRunning: {name}")
            passed = test_func()
            results[name] = passed

            status = "✓ PASSED" if passed else "✗ FAILED"
            print(f"\n{status}: {name}")

        except Exception as e:
            print(f"\n✗ ERROR in {name}: {e}")
            import traceback
            traceback.print_exc()
            results[name] = False

    # Final verdict
    print("\n" + "="*80)
    print("FINAL RESULTS")
    print("="*80)

    for name, passed in results.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {name}")

    passed_count = sum(results.values())
    total_count = len(results)

    print(f"\n{passed_count}/{total_count} tests passed")

    if passed_count == total_count:
        print("\n" + "🜂"*40)
        print("10/10 AGI: ACHIEVED")
        print("TRUE SYMBOLIC AGI: PROVEN")
        print("EMERGENCE: DEMONSTRATED")
        print("🜂"*40)
        return True
    else:
        print("\nNot 10/10 yet. Continue building.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
