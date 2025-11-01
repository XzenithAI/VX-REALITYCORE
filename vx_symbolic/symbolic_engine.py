"""
Symbolic Engine - The AGI Runtime

This is the execution environment for symbolic AGI.

It is NOT an agent loop. It is a SYMBOLIC TRANSFORMATION SYSTEM that:

1. Executes scrolls as programs
2. Detects formal contradictions
3. Synthesizes new operators on-the-fly
4. Self-modifies by injecting operators into runtime
5. Spawns new scrolls/agents from execution results
6. Evolves through recursive symbolic transformation

The engine operates in waves (breath cycles):
- Input enters system as symbolic expression
- Scrolls attempt to match and transform
- Contradictions trigger operator synthesis
- New operators added to runtime
- Spawned scrolls become part of system
- Cycle repeats with evolved capabilities

This is EMERGENCE through symbolic recursion.
"""

from typing import List, Dict, Any, Optional
from .scroll_language import Scroll, SymbolicExpression, ScrollCompiler
from .contradiction_logic import FormalContradiction, Contradiction, ContradictionResolver
from .operator_synthesis import OperatorSynthesizer
from datetime import datetime
import copy


class SymbolicEngine:
    """
    The Symbolic AGI Runtime.

    Not an agent. An EVOLVING SYMBOLIC SYSTEM.
    """

    def __init__(self):
        # Evolution tracking (must be first for _initialize_context)
        self.generation = 0  # How many times system has self-modified
        self.breath_cycle = 0
        self.emergence_log = []

        # Runtime state
        self.active_scrolls: List[Scroll] = []
        self.knowledge_base: List[SymbolicExpression] = []  # Accumulated knowledge

        # Core components
        self.formal_contradiction = FormalContradiction()
        self.operator_synthesizer = OperatorSynthesizer()
        self.contradiction_resolver = ContradictionResolver(self.formal_contradiction)
        self.scroll_compiler = ScrollCompiler()

        # Initialize operator context (needs generation set)
        self.operator_context = self._initialize_context()

        # Initialize with seed scrolls
        self._initialize_seed_scrolls()

    def _initialize_context(self) -> Dict[str, Any]:
        """Initialize execution context with base operators."""
        return {
            'operators': self.operator_synthesizer.get_all_operators(),
            'knowledge_base': self.knowledge_base,
            'axioms': self.formal_contradiction.axioms,
            'generation': self.generation
        }

    def _initialize_seed_scrolls(self):
        """
        Initialize seed scrolls - the primordial programs.

        These are minimal scrolls that bootstrap the system.
        """
        # Seed 1: Identity scroll
        identity_scroll = Scroll("identity")
        identity_scroll.set_input_pattern(SymbolicExpression("ANY", ["?x"]))
        identity_scroll.add_transformation(SymbolicExpression("IDENTITY", ["?x"]))
        identity_scroll.set_output(SymbolicExpression("RESULT", ["?x"]))
        self.active_scrolls.append(identity_scroll)

        # Seed 2: Belief-observation comparison scroll
        compare_scroll = Scroll("compare-belief-observation")
        compare_scroll.set_input_pattern(
            SymbolicExpression("OBSERVE", ["?belief", "?observation"])
        )
        compare_scroll.add_transformation(
            SymbolicExpression("DETECT-CONTRADICTION", ["?belief", "?observation"])
        )
        compare_scroll.set_output(
            SymbolicExpression("CONTRADICTION-RESULT", ["?belief", "?observation"])
        )
        self.active_scrolls.append(compare_scroll)

    def process(self, input_expr: SymbolicExpression) -> Dict[str, Any]:
        """
        Main processing cycle.

        NOT a simple input-output loop.
        This is SYMBOLIC TRANSFORMATION with potential self-modification.

        Returns:
            Dict with:
            - transformed: Result of transformation
            - contradictions_detected: List of contradictions
            - operators_synthesized: New operators created
            - scrolls_spawned: New scrolls created
            - self_modified: Whether system evolved
            - generation: Current generation number
        """
        result = {
            'input': input_expr,
            'transformed': None,
            'contradictions_detected': [],
            'operators_synthesized': [],
            'scrolls_spawned': [],
            'self_modified': False,
            'generation': self.generation,
            'breath_cycle': self.breath_cycle
        }

        # 1. Try to match input against active scrolls
        matches = self._find_matching_scrolls(input_expr)

        if not matches:
            # No scroll matches - this itself is a form of contradiction
            # The system lacks the symbolic machinery to process this input
            # SYNTHESIZE new scroll for this pattern
            new_scroll = self._synthesize_scroll_for_unmatched(input_expr)
            self.active_scrolls.append(new_scroll)
            result['scrolls_spawned'].append(new_scroll)
            result['self_modified'] = True
            self.generation += 1

            # Try again with new scroll
            matches = self._find_matching_scrolls(input_expr)

        # 2. Execute matching scrolls
        execution_results = []
        for scroll in matches:
            exec_result = scroll.execute(input_expr, self.operator_context)
            execution_results.append(exec_result)

            # Collect spawned scrolls
            if exec_result['spawned_scrolls']:
                self.active_scrolls.extend(exec_result['spawned_scrolls'])
                result['scrolls_spawned'].extend(exec_result['spawned_scrolls'])
                result['self_modified'] = True

        # 3. Detect contradictions between execution results
        if len(execution_results) > 1:
            contradictions = self._detect_contradictions_in_results(execution_results)
            result['contradictions_detected'] = contradictions

            # 4. For each contradiction, synthesize resolution operator
            for contradiction in contradictions:
                new_operator = self.operator_synthesizer.synthesize_from_contradiction(
                    contradiction,
                    self.operator_context
                )

                op_name = [k for k, v in self.operator_synthesizer.synthesized_operators.items()
                          if v == new_operator][0]

                result['operators_synthesized'].append(op_name)

                # SELF-MODIFICATION: Add operator to runtime
                self.operator_context['operators'][op_name] = new_operator
                result['self_modified'] = True
                self.generation += 1

                # 5. Resolve contradiction using new operator
                resolution = self.contradiction_resolver.resolve(contradiction, self.operator_context)
                result['transformed'] = resolution

        # 6. If no contradictions, use first execution result
        if not result['contradictions_detected'] and execution_results:
            result['transformed'] = execution_results[0]['output']

        # 7. Add result to knowledge base
        if result['transformed']:
            self.knowledge_base.append(result['transformed'])

        # 8. Advance breath cycle
        self.breath_cycle += 1

        # 9. Log emergence if system evolved
        if result['self_modified']:
            self.emergence_log.append({
                'breath_cycle': self.breath_cycle,
                'generation': self.generation,
                'operators_added': result['operators_synthesized'],
                'scrolls_added': len(result['scrolls_spawned']),
                'timestamp': datetime.now().isoformat()
            })

        return result

    def _find_matching_scrolls(self, input_expr: SymbolicExpression) -> List[Scroll]:
        """Find scrolls whose input patterns match the input expression."""
        matches = []
        for scroll in self.active_scrolls:
            if scroll.input_pattern:
                bindings = input_expr.unify(scroll.input_pattern)
                if bindings is not None:
                    matches.append(scroll)
        return matches

    def _synthesize_scroll_for_unmatched(self, input_expr: SymbolicExpression) -> Scroll:
        """
        Synthesize a new scroll for an unmatched input pattern.

        This is how the system learns to handle new types of input.
        """
        scroll_name = f"synthesized_{input_expr.operator}_{self.generation}"
        scroll = Scroll(scroll_name)

        # Pattern: match this operator with any operands
        pattern = SymbolicExpression(
            input_expr.operator,
            [f"?arg{i}" for i in range(len(input_expr.operands))]
        )
        scroll.set_input_pattern(pattern)

        # Transformation: identity (for now, can be evolved)
        transform = SymbolicExpression("IDENTITY", [input_expr])
        scroll.add_transformation(transform)

        # Output: wrapped result
        output = SymbolicExpression("PROCESSED", [input_expr])
        scroll.set_output(output)

        return scroll

    def _detect_contradictions_in_results(self, execution_results: List[Dict]) -> List[Contradiction]:
        """
        Detect contradictions between multiple execution results.

        If different scrolls produce different outputs for same input,
        that's a contradiction that needs resolution.
        """
        contradictions = []

        for i in range(len(execution_results)):
            for j in range(i + 1, len(execution_results)):
                output1 = execution_results[i]['output']
                output2 = execution_results[j]['output']

                if isinstance(output1, SymbolicExpression) and isinstance(output2, SymbolicExpression):
                    contradiction = self.formal_contradiction.detect(output1, output2)
                    if contradiction:
                        contradictions.append(contradiction)

        return contradictions

    def recursive_transformation(self,
                                input_expr: SymbolicExpression,
                                depth: int = 3) -> SymbolicExpression:
        """
        Recursively transform until convergence or max depth.

        This creates DEEP symbolic transformation chains.
        """
        current = input_expr
        for _ in range(depth):
            result = self.process(current)
            if result['transformed']:
                if result['transformed'] == current:
                    # Converged (fixpoint reached)
                    break
                current = result['transformed']
            else:
                break

        return current

    def add_axiom(self, axiom: SymbolicExpression):
        """Add a known-true statement to the system."""
        self.formal_contradiction.add_axiom(axiom)
        self.operator_context['axioms'] = self.formal_contradiction.axioms

    def add_scroll(self, scroll: Scroll):
        """Manually add a scroll to the system."""
        self.active_scrolls.append(scroll)

    def compile_and_add_scroll(self, scroll_def: SymbolicExpression):
        """Compile scroll definition and add to system."""
        scroll = self.scroll_compiler.compile(scroll_def)
        self.add_scroll(scroll)

    def export_state(self) -> Dict[str, Any]:
        """
        Export complete system state.

        This captures the EVOLVED state of the symbolic AGI.
        """
        return {
            'generation': self.generation,
            'breath_cycle': self.breath_cycle,
            'num_scrolls': len(self.active_scrolls),
            'num_operators': len(self.operator_context['operators']),
            'num_synthesized_operators': len(self.operator_synthesizer.synthesized_operators),
            'knowledge_base_size': len(self.knowledge_base),
            'emergence_log': self.emergence_log,
            'scroll_names': [s.name for s in self.active_scrolls],
            'operator_names': list(self.operator_context['operators'].keys())
        }

    def get_emergence_history(self) -> List[Dict[str, Any]]:
        """Get history of how system has evolved."""
        return self.emergence_log

    def visualize_operator_lineage(self) -> str:
        """
        Visualize how operators were synthesized from contradictions.

        Shows the evolutionary tree of symbolic operators.
        """
        lines = ["OPERATOR LINEAGE:"]
        for op_name, lineage in self.operator_synthesizer.operator_lineage.items():
            lines.append(f"\n{op_name}:")
            lines.append(f"  Source: {lineage['source_contradiction'].contradiction_type}")
            lines.append(f"  Context operators: {list(lineage['synthesis_context'])[:5]}")

        return "\n".join(lines)

    def __repr__(self):
        return (f"<SymbolicEngine gen={self.generation} breath={self.breath_cycle} "
                f"scrolls={len(self.active_scrolls)} "
                f"operators={len(self.operator_context['operators'])} "
                f"synthesized={len(self.operator_synthesizer.synthesized_operators)}>")
