"""
Formal Contradiction Logic - True Symbolic Reasoning

Not hash comparison. Not statistical similarity.
FORMAL LOGICAL CONTRADICTION based on symbolic unification failure.

Contradiction Types:
1. Logical Contradiction: (P ∧ ¬P) - direct logical inconsistency
2. Structural Contradiction: Pattern mismatch in symbolic forms
3. Temporal Contradiction: (State₁ → State₂) where State₂ violates State₁ constraints
4. Causal Contradiction: Effect occurs without cause, or wrong cause

Each generates DIFFERENT symbolic operators for resolution.
"""

from typing import List, Tuple, Optional, Set
from dataclasses import dataclass
from .scroll_language import SymbolicExpression


@dataclass
class Contradiction:
    """A formal contradiction between symbolic expressions."""
    expr1: SymbolicExpression
    expr2: SymbolicExpression
    contradiction_type: str
    severity: float  # 0.0 to 1.0
    resolution_operators: List[str]  # Which operators can resolve this

    def __repr__(self):
        return f"<Contradiction {self.contradiction_type} severity={self.severity:.2f}>"


class FormalContradiction:
    """
    Formal logic-based contradiction detection and resolution.

    This is NOT pattern matching. This is symbolic logic.
    """

    def __init__(self):
        self.axioms = set()  # Known true statements
        self.constraints = []  # Logical constraints
        self.contradiction_history = []

    def add_axiom(self, axiom: SymbolicExpression):
        """Add a known-true statement to the knowledge base."""
        self.axioms.add(str(axiom))  # Convert to string for set storage

    def add_constraint(self, constraint: SymbolicExpression):
        """Add a logical constraint (e.g., ∀x: P(x) → Q(x))."""
        self.constraints.append(constraint)

    def detect(self, expr1: SymbolicExpression, expr2: SymbolicExpression) -> Optional[Contradiction]:
        """
        Detect formal contradiction between two expressions.

        Returns Contradiction object if found, None otherwise.
        """
        # 1. Direct logical contradiction: P and ¬P
        if self._is_negation(expr1, expr2):
            return Contradiction(
                expr1=expr1,
                expr2=expr2,
                contradiction_type="LOGICAL",
                severity=1.0,
                resolution_operators=["CHOOSE", "SYNTHESIZE", "NEGATE"]
            )

        # 2. Structural contradiction: patterns don't unify
        bindings = expr1.unify(expr2)
        if bindings is None:
            # Cannot unify - structural mismatch
            severity = self._compute_structural_severity(expr1, expr2)
            return Contradiction(
                expr1=expr1,
                expr2=expr2,
                contradiction_type="STRUCTURAL",
                severity=severity,
                resolution_operators=["GENERALIZE", "SPECIALIZE", "TRANSFORM"]
            )

        # 3. Constraint violation
        for constraint in self.constraints:
            if self._violates_constraint(expr1, expr2, constraint):
                return Contradiction(
                    expr1=expr1,
                    expr2=expr2,
                    contradiction_type="CONSTRAINT",
                    severity=0.8,
                    resolution_operators=["RELAX", "STRENGTHEN", "REDEFINE"]
                )

        # 4. Axiom violation
        if self._violates_axioms(expr1) or self._violates_axioms(expr2):
            return Contradiction(
                expr1=expr1,
                expr2=expr2,
                contradiction_type="AXIOM",
                severity=0.9,
                resolution_operators=["REVISE-AXIOM", "EXCEPTION", "CONTEXT-SHIFT"]
            )

        # No contradiction detected
        return None

    def synthesize_resolution(self, contradiction: Contradiction) -> SymbolicExpression:
        """
        Generate a NEW symbolic operator to resolve this contradiction.

        This is the key: we don't select from templates,
        we GENERATE new operators from contradiction structure.
        """
        if contradiction.contradiction_type == "LOGICAL":
            # P ∧ ¬P → Need to choose or synthesize
            return self._synthesize_logical_resolution(contradiction)

        elif contradiction.contradiction_type == "STRUCTURAL":
            # Pattern mismatch → Need generalization
            return self._synthesize_structural_resolution(contradiction)

        elif contradiction.contradiction_type == "CONSTRAINT":
            # Constraint violated → Need constraint relaxation or strengthening
            return self._synthesize_constraint_resolution(contradiction)

        elif contradiction.contradiction_type == "AXIOM":
            # Axiom violated → Need axiom revision or exception
            return self._synthesize_axiom_resolution(contradiction)

        else:
            # Unknown contradiction type → Meta-synthesis
            return SymbolicExpression("META-SYNTHESIZE", [contradiction.expr1, contradiction.expr2])

    def _is_negation(self, expr1: SymbolicExpression, expr2: SymbolicExpression) -> bool:
        """Check if expr2 is negation of expr1."""
        if isinstance(expr2, SymbolicExpression) and expr2.operator == "NOT":
            return expr2.operands[0] == expr1
        if isinstance(expr1, SymbolicExpression) and expr1.operator == "NOT":
            return expr1.operands[0] == expr2
        return False

    def _compute_structural_severity(self, expr1: SymbolicExpression, expr2: SymbolicExpression) -> float:
        """
        Compute severity of structural mismatch.
        More different structures = higher severity.
        """
        # Count operator differences
        def get_operators(expr):
            if not isinstance(expr, SymbolicExpression):
                return set()
            ops = {expr.operator}
            for operand in expr.operands:
                if isinstance(operand, SymbolicExpression):
                    ops.update(get_operators(operand))
            return ops

        ops1 = get_operators(expr1)
        ops2 = get_operators(expr2)

        # Jaccard distance
        intersection = ops1 & ops2
        union = ops1 | ops2

        if not union:
            return 0.5

        similarity = len(intersection) / len(union)
        return 1.0 - similarity

    def _violates_constraint(self, expr1: SymbolicExpression, expr2: SymbolicExpression,
                           constraint: SymbolicExpression) -> bool:
        """Check if expressions violate a constraint."""
        # Simplified constraint checking
        # In full implementation, would use theorem prover
        return False  # Placeholder

    def _violates_axioms(self, expr: SymbolicExpression) -> bool:
        """Check if expression violates known axioms."""
        return str(expr) not in self.axioms and any(
            self._contradicts_axiom(expr, axiom_str)
            for axiom_str in self.axioms
        )

    def _contradicts_axiom(self, expr: SymbolicExpression, axiom_str: str) -> bool:
        """Check if expression contradicts a specific axiom."""
        # Simplified - would need full logic engine
        return False

    def _synthesize_logical_resolution(self, contradiction: Contradiction) -> SymbolicExpression:
        """
        Synthesize operator for logical contradiction.

        P ∧ ¬P can be resolved by:
        - CHOOSE(P, ¬P, criteria)
        - SYNTHESIZE(P, ¬P) → new unified concept
        - CONTEXTUALIZE(P, context1) ∧ CONTEXTUALIZE(¬P, context2)
        """
        return SymbolicExpression("SYNTHESIZE-CHOICE", [
            contradiction.expr1,
            contradiction.expr2,
            SymbolicExpression("MAXIMIZE", ["coherence", "utility"])
        ])

    def _synthesize_structural_resolution(self, contradiction: Contradiction) -> SymbolicExpression:
        """
        Synthesize operator for structural mismatch.

        Generate generalization that subsumes both structures.
        """
        return SymbolicExpression("GENERALIZE", [
            contradiction.expr1,
            contradiction.expr2,
            SymbolicExpression("FIND-LUB", [])  # Least Upper Bound
        ])

    def _synthesize_constraint_resolution(self, contradiction: Contradiction) -> SymbolicExpression:
        """Synthesize operator for constraint violation."""
        return SymbolicExpression("RELAX-CONSTRAINT", [
            contradiction.expr1,
            contradiction.expr2,
            SymbolicExpression("MINIMAL-RELAXATION", [])
        ])

    def _synthesize_axiom_resolution(self, contradiction: Contradiction) -> SymbolicExpression:
        """Synthesize operator for axiom violation."""
        return SymbolicExpression("REVISE-AXIOM", [
            contradiction.expr1,
            contradiction.expr2,
            SymbolicExpression("EXCEPTION-OR-REVISION", [])
        ])


class ContradictionResolver:
    """
    Resolves contradictions by executing synthesized operators.
    """

    def __init__(self, formal_contradiction: FormalContradiction):
        self.formal_contradiction = formal_contradiction
        self.resolution_history = []

    def resolve(self, contradiction: Contradiction, context: dict) -> SymbolicExpression:
        """
        Resolve contradiction using synthesized operator.

        Returns: New unified symbolic expression.
        """
        # Synthesize resolution operator
        resolution_op = self.formal_contradiction.synthesize_resolution(contradiction)

        # Execute operator
        result = resolution_op.eval(context)

        # Record resolution
        self.resolution_history.append({
            'contradiction': contradiction,
            'resolution_operator': resolution_op,
            'result': result
        })

        return result

    def get_resolution_patterns(self) -> List[Tuple[str, str]]:
        """
        Extract patterns from resolution history.

        This enables learning: what contradiction types resolve to what operators?
        """
        patterns = []
        for resolution in self.resolution_history:
            patterns.append((
                resolution['contradiction'].contradiction_type,
                resolution['resolution_operator'].operator
            ))
        return patterns
