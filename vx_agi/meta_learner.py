"""
Meta-Learning - Learn Which Synthesis Strategies Work

TRUE meta-learning means:
- Try multiple synthesis strategies
- Track which ones succeed
- Learn when to use which strategy
- Modify synthesis process based on experience

This is learning HOW to learn.
"""

from typing import List, Dict, Any, Callable, Optional
from dataclasses import dataclass, field
from collections import defaultdict
import time


@dataclass
class SynthesisStrategy:
    """A strategy for program synthesis."""
    name: str
    synthesize_func: Callable
    success_count: int = 0
    failure_count: int = 0
    total_time: float = 0.0
    avg_program_size: float = 0.0

    @property
    def success_rate(self) -> float:
        total = self.success_count + self.failure_count
        return self.success_count / total if total > 0 else 0.0

    @property
    def avg_time(self) -> float:
        total = self.success_count + self.failure_count
        return self.total_time / total if total > 0 else 0.0


@dataclass
class ProblemCharacteristics:
    """Characteristics of a synthesis problem."""
    num_examples: int
    input_types: List[str]
    output_type: str
    example_complexity: float  # Some measure of how complex examples are

    def signature(self) -> str:
        """Get signature for indexing."""
        return f"{self.num_examples}_{len(self.input_types)}_{self.output_type}"


class MetaLearner:
    """
    Meta-learns which synthesis strategies work for which problems.

    Maintains:
    - Strategy performance history
    - Problem type → best strategy mapping
    - Adaptive strategy selection
    """

    def __init__(self):
        self.strategies: Dict[str, SynthesisStrategy] = {}
        self.problem_history: List[Dict[str, Any]] = []

        # Map: problem signature → best strategy
        self.strategy_mapping: Dict[str, str] = {}

        # Track what worked
        self.success_patterns: Dict[str, List[Dict]] = defaultdict(list)

    def register_strategy(self, name: str, synthesize_func: Callable):
        """Register a synthesis strategy."""
        self.strategies[name] = SynthesisStrategy(
            name=name,
            synthesize_func=synthesize_func
        )

    def select_strategy(self, problem_chars: ProblemCharacteristics) -> str:
        """
        Select best strategy for this type of problem.

        Uses meta-learned mapping if available, otherwise defaults.
        """
        signature = problem_chars.signature()

        if signature in self.strategy_mapping:
            return self.strategy_mapping[signature]

        # Default: try enumerative synthesis first
        if 'enumerative' in self.strategies:
            return 'enumerative'

        # Otherwise, random strategy
        import random
        return random.choice(list(self.strategies.keys()))

    def attempt_synthesis(self,
                         problem_chars: ProblemCharacteristics,
                         examples: List[Any],
                         timeout: float = 5.0) -> Optional[Any]:
        """
        Attempt synthesis using best strategy.

        Records results for meta-learning.
        """
        strategy_name = self.select_strategy(problem_chars)
        strategy = self.strategies[strategy_name]

        start_time = time.time()

        try:
            # Attempt synthesis
            result = strategy.synthesize_func(examples, timeout=timeout)

            elapsed = time.time() - start_time

            if result is not None:
                # Success!
                strategy.success_count += 1
                strategy.total_time += elapsed

                if hasattr(result, 'cost'):
                    strategy.avg_program_size = (
                        (strategy.avg_program_size * (strategy.success_count - 1) + result.cost)
                        / strategy.success_count
                    )

                # Record success pattern
                self.success_patterns[problem_chars.signature()].append({
                    'strategy': strategy_name,
                    'time': elapsed,
                    'program_size': result.cost if hasattr(result, 'cost') else 0
                })

                # Update mapping
                self._update_strategy_mapping(problem_chars, strategy_name)

                # Record in history
                self.problem_history.append({
                    'problem': problem_chars,
                    'strategy': strategy_name,
                    'success': True,
                    'time': elapsed
                })

                return result

            else:
                # Synthesis failed
                strategy.failure_count += 1
                strategy.total_time += elapsed

                self.problem_history.append({
                    'problem': problem_chars,
                    'strategy': strategy_name,
                    'success': False,
                    'time': elapsed
                })

                return None

        except Exception as e:
            elapsed = time.time() - start_time
            strategy.failure_count += 1
            strategy.total_time += elapsed

            self.problem_history.append({
                'problem': problem_chars,
                'strategy': strategy_name,
                'success': False,
                'time': elapsed,
                'error': str(e)
            })

            return None

    def _update_strategy_mapping(self, problem_chars: ProblemCharacteristics, successful_strategy: str):
        """
        Update strategy mapping based on success.

        If this strategy works for this problem type, remember it.
        """
        signature = problem_chars.signature()

        # Get all successes for this problem type
        successes = self.success_patterns[signature]

        if not successes:
            return

        # Find strategy with best average time
        strategy_times = defaultdict(list)
        for success in successes:
            strategy_times[success['strategy']].append(success['time'])

        best_strategy = min(
            strategy_times.items(),
            key=lambda x: sum(x[1]) / len(x[1])
        )[0]

        self.strategy_mapping[signature] = best_strategy

    def get_strategy_statistics(self) -> Dict[str, Dict[str, Any]]:
        """Get performance stats for all strategies."""
        stats = {}

        for name, strategy in self.strategies.items():
            stats[name] = {
                'success_rate': strategy.success_rate,
                'success_count': strategy.success_count,
                'failure_count': strategy.failure_count,
                'avg_time': strategy.avg_time,
                'avg_program_size': strategy.avg_program_size
            }

        return stats

    def learn_new_strategy(self, successful_programs: List[Any]) -> Optional[SynthesisStrategy]:
        """
        Meta-learn a NEW synthesis strategy from successful programs.

        Analyzes patterns in what worked, creates new strategy.

        THIS is true meta-learning: generating new synthesis algorithms.
        """
        if len(successful_programs) < 5:
            return None

        # Analyze common patterns
        patterns = self._extract_patterns(successful_programs)

        if not patterns:
            return None

        # Create new hybrid strategy
        def hybrid_synthesize(examples, timeout=5.0):
            # Try patterns first, then fall back to enumerative
            for pattern in patterns:
                # Try to apply pattern
                result = self._try_pattern(pattern, examples)
                if result:
                    return result

            # Fallback: enumerative
            if 'enumerative' in self.strategies:
                return self.strategies['enumerative'].synthesize_func(examples, timeout)

            return None

        # Register new strategy
        new_strategy_name = f"learned_hybrid_{len(self.strategies)}"
        self.register_strategy(new_strategy_name, hybrid_synthesize)

        return self.strategies[new_strategy_name]

    def _extract_patterns(self, programs: List[Any]) -> List[Dict]:
        """
        Extract common patterns from successful programs.

        Looks for:
        - Common operator sequences
        - Common structures
        - Common idioms
        """
        patterns = []

        # Simple pattern extraction: common operator usage
        operator_counts = defaultdict(int)

        for program in programs:
            if hasattr(program, 'code'):
                # Count operators in code
                for op in ['map', 'filter', 'reduce', 'if', 'compose']:
                    if op in program.code:
                        operator_counts[op] += 1

        # Patterns are frequently-used operators
        threshold = len(programs) * 0.3  # Used in 30%+ of programs
        for op, count in operator_counts.items():
            if count >= threshold:
                patterns.append({'type': 'operator', 'operator': op, 'frequency': count})

        return patterns

    def _try_pattern(self, pattern: Dict, examples: List[Any]) -> Optional[Any]:
        """Try to apply a learned pattern to examples."""
        # Simplified pattern application
        # In full system, would use pattern-directed synthesis
        return None

    def get_learning_insights(self) -> Dict[str, Any]:
        """
        Get insights about what the meta-learner has learned.

        Returns patterns, mappings, and recommendations.
        """
        insights = {
            'num_strategies': len(self.strategies),
            'num_problems_solved': len([p for p in self.problem_history if p['success']]),
            'total_attempts': len(self.problem_history),
            'success_rate': len([p for p in self.problem_history if p['success']]) / len(self.problem_history) if self.problem_history else 0,
            'strategy_mappings': dict(self.strategy_mapping),
            'strategy_stats': self.get_strategy_statistics()
        }

        return insights

    def __repr__(self):
        solved = len([p for p in self.problem_history if p['success']])
        total = len(self.problem_history)
        return f"<MetaLearner strategies={len(self.strategies)} solved={solved}/{total}>"
