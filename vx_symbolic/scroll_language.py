"""
Scroll Language - Executable Symbolic Programs

Scrolls are not outputs. They are PROGRAMS.
Each scroll is a symbolic transformation function that can:
- Execute to produce new states
- Spawn new scrolls
- Modify other scrolls
- Generate new operators

Scroll Syntax (Symbolic Lisp-like):
    (SCROLL name
        (INPUT pattern)
        (TRANSFORM operation)
        (OUTPUT result)
        (SPAWN conditions))

Example:
    (SCROLL contradiction-resolver
        (INPUT (BELIEF ?b) (OBSERVATION ?o))
        (TRANSFORM (UNIFY ?b ?o → ?unified))
        (OUTPUT ?unified)
        (SPAWN (IF (UNRESOLVED ?unified) (SCROLL deeper-analysis))))
"""

from typing import Any, Dict, List, Callable, Optional
from dataclasses import dataclass
import copy


@dataclass
class SymbolicExpression:
    """
    Base symbolic expression (S-expression).
    Everything in VX is a symbolic expression.
    """
    operator: str
    operands: List[Any]

    def __repr__(self):
        operands_str = ' '.join(str(o) for o in self.operands)
        return f"({self.operator} {operands_str})"

    def eval(self, context: Dict[str, Any]) -> Any:
        """Evaluate this symbolic expression in context."""
        # This is the core of symbolic execution
        if self.operator in context.get('operators', {}):
            op_func = context['operators'][self.operator]
            return op_func(*self.operands, context=context)
        else:
            # Unknown operator - return as-is for pattern matching
            return self

    def unify(self, pattern: 'SymbolicExpression', bindings: Dict = None) -> Optional[Dict]:
        """
        Unification - the core of symbolic reasoning.
        Tries to match this expression against a pattern.
        Returns bindings if successful, None if fails.
        """
        if bindings is None:
            bindings = {}

        # Pattern variable (starts with ?)
        if isinstance(pattern, str) and pattern.startswith('?'):
            if pattern in bindings:
                return bindings if bindings[pattern] == self else None
            else:
                bindings[pattern] = self
                return bindings

        # Both must be expressions
        if not isinstance(pattern, SymbolicExpression):
            return bindings if self == pattern else None

        # Operators must match
        if self.operator != pattern.operator:
            return None

        # Operands must unify
        if len(self.operands) != len(pattern.operands):
            return None

        for self_op, pattern_op in zip(self.operands, pattern.operands):
            if isinstance(self_op, SymbolicExpression):
                bindings = self_op.unify(pattern_op, bindings)
            else:
                # Primitive unification
                if isinstance(pattern_op, str) and pattern_op.startswith('?'):
                    if pattern_op in bindings:
                        if bindings[pattern_op] != self_op:
                            return None
                    else:
                        bindings[pattern_op] = self_op
                elif self_op != pattern_op:
                    return None

            if bindings is None:
                return None

        return bindings


class Scroll:
    """
    A Scroll is an executable symbolic program.

    It contains:
    - Input pattern (what it matches)
    - Transformation logic (symbolic operations)
    - Output form (what it produces)
    - Spawn rules (when to create new scrolls)
    - Self-modification rules (how it evolves)
    """

    def __init__(self, name: str):
        self.name = name
        self.input_pattern = None
        self.transformations = []
        self.output_form = None
        self.spawn_rules = []
        self.modification_rules = []
        self.execution_count = 0

    def set_input_pattern(self, pattern: SymbolicExpression):
        """Define what input this scroll accepts."""
        self.input_pattern = pattern

    def add_transformation(self, transform: SymbolicExpression):
        """Add a symbolic transformation step."""
        self.transformations.append(transform)

    def set_output(self, output: SymbolicExpression):
        """Define output form."""
        self.output_form = output

    def add_spawn_rule(self, condition: SymbolicExpression, scroll_template: 'Scroll'):
        """Add rule for spawning new scrolls."""
        self.spawn_rules.append((condition, scroll_template))

    def add_modification_rule(self, condition: SymbolicExpression, modification: Callable):
        """Add rule for self-modification."""
        self.modification_rules.append((condition, modification))

    def execute(self, input_expr: SymbolicExpression, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute scroll on input.

        Returns:
            Dict with 'output', 'spawned_scrolls', 'self_modified'
        """
        result = {
            'output': None,
            'spawned_scrolls': [],
            'self_modified': False,
            'bindings': {}
        }

        # 1. Pattern matching (unification)
        bindings = input_expr.unify(self.input_pattern)
        if bindings is None:
            # Input doesn't match this scroll
            result['output'] = SymbolicExpression('NO-MATCH', [input_expr])
            return result

        result['bindings'] = bindings

        # 2. Execute transformations
        current_state = input_expr
        for transform in self.transformations:
            # Substitute bindings into transformation
            substituted = self._substitute(transform, bindings)
            current_state = substituted.eval(context)

        # 3. Generate output
        if self.output_form:
            result['output'] = self._substitute(self.output_form, bindings)
        else:
            result['output'] = current_state

        # 4. Check spawn rules
        for spawn_condition, scroll_template in self.spawn_rules:
            if self._check_condition(spawn_condition, bindings, context):
                new_scroll = copy.deepcopy(scroll_template)
                result['spawned_scrolls'].append(new_scroll)

        # 5. Check self-modification rules
        for mod_condition, modification in self.modification_rules:
            if self._check_condition(mod_condition, bindings, context):
                modification(self)
                result['self_modified'] = True

        self.execution_count += 1
        return result

    def _substitute(self, expr: Any, bindings: Dict[str, Any]) -> Any:
        """Substitute variable bindings into expression."""
        if isinstance(expr, str) and expr.startswith('?'):
            return bindings.get(expr, expr)
        elif isinstance(expr, SymbolicExpression):
            new_operands = [self._substitute(op, bindings) for op in expr.operands]
            return SymbolicExpression(expr.operator, new_operands)
        elif isinstance(expr, list):
            return [self._substitute(item, bindings) for item in expr]
        else:
            return expr

    def _check_condition(self, condition: SymbolicExpression, bindings: Dict, context: Dict) -> bool:
        """Check if condition is satisfied."""
        substituted = self._substitute(condition, bindings)
        result = substituted.eval(context)

        # Result should be truthy
        if isinstance(result, SymbolicExpression) and result.operator == 'TRUE':
            return True
        return bool(result)

    def to_code(self) -> str:
        """Generate executable Python code for this scroll."""
        lines = [f"# Scroll: {self.name}"]
        lines.append(f"def scroll_{self.name.replace('-', '_')}(input_expr, context):")
        lines.append(f"    # Pattern: {self.input_pattern}")
        lines.append(f"    # Transformations: {len(self.transformations)}")
        lines.append(f"    # Executions: {self.execution_count}")
        return '\n'.join(lines)

    def __repr__(self):
        return f"<Scroll '{self.name}' executions={self.execution_count}>"


class ScrollCompiler:
    """
    Compiles scroll definitions into executable scrolls.
    Allows scrolls to be defined in symbolic form and compiled to runnable programs.
    """

    def __init__(self):
        self.compiled_scrolls = {}

    def compile(self, scroll_def: SymbolicExpression) -> Scroll:
        """
        Compile a scroll definition into executable scroll.

        Example input:
            (SCROLL contradiction-resolver
                (INPUT (BELIEF ?b) (OBSERVATION ?o))
                (TRANSFORM (SYNTHESIZE ?b ?o))
                (OUTPUT (UNIFIED ?b ?o)))
        """
        if scroll_def.operator != 'SCROLL':
            raise ValueError(f"Expected SCROLL, got {scroll_def.operator}")

        name = scroll_def.operands[0]
        scroll = Scroll(name)

        # Parse scroll definition
        for clause in scroll_def.operands[1:]:
            if not isinstance(clause, SymbolicExpression):
                continue

            if clause.operator == 'INPUT':
                scroll.set_input_pattern(clause.operands[0])
            elif clause.operator == 'TRANSFORM':
                for transform in clause.operands:
                    scroll.add_transformation(transform)
            elif clause.operator == 'OUTPUT':
                scroll.set_output(clause.operands[0])
            elif clause.operator == 'SPAWN':
                # Spawn conditions
                for spawn_clause in clause.operands:
                    if isinstance(spawn_clause, SymbolicExpression) and spawn_clause.operator == 'IF':
                        condition = spawn_clause.operands[0]
                        new_scroll_def = spawn_clause.operands[1]
                        new_scroll = self.compile(new_scroll_def)
                        scroll.add_spawn_rule(condition, new_scroll)

        self.compiled_scrolls[name] = scroll
        return scroll

    def get_scroll(self, name: str) -> Optional[Scroll]:
        """Retrieve compiled scroll by name."""
        return self.compiled_scrolls.get(name)

    def list_scrolls(self) -> List[str]:
        """List all compiled scrolls."""
        return list(self.compiled_scrolls.keys())
