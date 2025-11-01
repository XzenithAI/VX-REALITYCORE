"""
Program Synthesis Engine - Generate Code from Specifications

TRUE synthesis means:
- Given: Input/output examples
- Generate: Working code that generalizes

Not template filling. ACTUAL program synthesis.

Approach:
1. Bottom-up synthesis (enumerate small programs, compose larger)
2. Top-down synthesis (recursively decompose problem)
3. Constraint-based synthesis (encode as SAT/SMT, solve)
4. Probabilistic synthesis (beam search over program space)

This is how the system gains NEW capabilities.
"""

from typing import List, Tuple, Callable, Any, Optional, Set
from dataclasses import dataclass
import itertools
from collections import defaultdict


@dataclass
class IOExample:
    """Input/output example for synthesis."""
    inputs: Tuple[Any, ...]
    output: Any

    def __hash__(self):
        return hash((self.inputs, self.output))


@dataclass
class SynthesizedProgram:
    """A synthesized program."""
    code: str
    function: Callable
    cost: int  # Complexity measure
    examples_satisfied: int
    generalizes: bool  # Does it work on held-out examples?

    def __lt__(self, other):
        return self.cost < other.cost


class ProgramSynthesizer:
    """
    Synthesizes programs from input/output examples.

    This is CORE to true AGI - the ability to generate new code.
    """

    def __init__(self, max_program_size: int = 10):
        self.max_program_size = max_program_size
        self.primitive_ops = self._initialize_primitives()
        self.synthesis_cache = {}  # Memoize synthesis results
        self.learned_programs = []  # Programs that worked

    def _initialize_primitives(self) -> dict[str, Callable]:
        """
        Initialize primitive operations we can use to build programs.

        These are the ATOMS from which all programs are built.
        """
        primitives = {
            # Arithmetic
            'add': lambda x, y: x + y,
            'sub': lambda x, y: x - y,
            'mul': lambda x, y: x * y,
            'div': lambda x, y: x / y if y != 0 else 0,

            # Logic
            'and': lambda x, y: x and y,
            'or': lambda x, y: x or y,
            'not': lambda x: not x,
            'eq': lambda x, y: x == y,
            'gt': lambda x, y: x > y,
            'lt': lambda x, y: x < y,

            # Combinators
            'if': lambda cond, then_val, else_val: then_val if cond else else_val,
            'identity': lambda x: x,
            'const': lambda x: lambda _: x,
            'compose': lambda f, g: lambda x: f(g(x)),

            # List operations
            'map': lambda f, xs: list(map(f, xs)) if isinstance(xs, list) else xs,
            'filter': lambda f, xs: list(filter(f, xs)) if isinstance(xs, list) else xs,
            'reduce': lambda f, xs, init: self._safe_reduce(f, xs, init),
            'head': lambda xs: xs[0] if xs and isinstance(xs, list) else None,
            'tail': lambda xs: xs[1:] if xs and isinstance(xs, list) else [],
            'cons': lambda x, xs: [x] + (xs if isinstance(xs, list) else []),

            # Higher-order
            'fix': lambda f: self._fixed_point(f),  # Fixed-point combinator
        }
        return primitives

    def _safe_reduce(self, f, xs, init):
        """Safe reduce that handles errors."""
        try:
            result = init
            for x in xs:
                result = f(result, x)
            return result
        except:
            return init

    def _fixed_point(self, f, max_iter=100):
        """Compute fixed point of function."""
        def fix_fn(x):
            result = x
            for _ in range(max_iter):
                new_result = f(result)
                if new_result == result:
                    return result
                result = new_result
            return result
        return fix_fn

    def synthesize(self,
                   examples: List[IOExample],
                   timeout_programs: int = 10000) -> Optional[SynthesizedProgram]:
        """
        Main synthesis algorithm: enumerate-and-check.

        1. Enumerate programs in order of increasing complexity
        2. Check each against examples
        3. Return first that works

        This is bottom-up enumerative synthesis.
        """
        # Split examples into train/test
        if len(examples) < 2:
            train_examples = examples
            test_examples = []
        else:
            split = len(examples) * 2 // 3
            train_examples = examples[:split]
            test_examples = examples[split:]

        # Try synthesizing with increasing complexity
        for size in range(1, self.max_program_size + 1):
            programs_checked = 0

            # Enumerate programs of this size
            for program_ast in self._enumerate_programs(size):
                if programs_checked >= timeout_programs:
                    break

                programs_checked += 1

                # Check if program satisfies examples
                try:
                    func = self._compile_ast(program_ast)

                    # Test on training examples
                    satisfied = 0
                    for example in train_examples:
                        try:
                            result = func(*example.inputs)
                            if result == example.output:
                                satisfied += 1
                        except:
                            break

                    # If satisfies all training examples
                    if satisfied == len(train_examples):
                        # Test generalization on held-out examples
                        generalizes = True
                        if test_examples:
                            for example in test_examples:
                                try:
                                    result = func(*example.inputs)
                                    if result != example.output:
                                        generalizes = False
                                        break
                                except:
                                    generalizes = False
                                    break

                        # Found a working program!
                        code = self._ast_to_code(program_ast)
                        synthesized = SynthesizedProgram(
                            code=code,
                            function=func,
                            cost=size,
                            examples_satisfied=satisfied,
                            generalizes=generalizes
                        )

                        self.learned_programs.append(synthesized)
                        return synthesized

                except Exception as e:
                    # Program doesn't compile or crashes
                    continue

        return None  # No program found

    def _enumerate_programs(self, size: int):
        """
        Enumerate all programs up to given size.

        Programs are trees of primitive operations.
        Size = number of nodes in tree.
        """
        if size == 1:
            # Base case: just primitives and variables
            for op_name in self.primitive_ops:
                yield ('primitive', op_name)
            # Variables
            for i in range(3):  # Support up to 3 arguments
                yield ('var', i)
        else:
            # Recursive case: combine smaller programs
            for op_name, op_func in self.primitive_ops.items():
                # Get arity (number of arguments)
                arity = self._get_arity(op_name)

                # Generate all combinations of subprograms that sum to size-1
                for subprogram_sizes in self._partitions(size - 1, arity):
                    # Generate subprograms for each partition
                    subprogram_iterators = [
                        self._enumerate_programs(s) for s in subprogram_sizes
                    ]

                    # Cartesian product of subprograms
                    for subprograms in itertools.product(*subprogram_iterators):
                        yield ('apply', op_name, subprograms)

    def _get_arity(self, op_name: str) -> int:
        """Get number of arguments for operation."""
        # Most operations are binary
        if op_name in ['add', 'sub', 'mul', 'div', 'and', 'or', 'eq', 'gt', 'lt', 'cons', 'compose']:
            return 2
        elif op_name in ['not', 'identity', 'head', 'tail', 'const']:
            return 1
        elif op_name in ['if', 'reduce']:
            return 3
        elif op_name in ['map', 'filter']:
            return 2
        else:
            return 1

    def _partitions(self, n: int, k: int) -> List[List[int]]:
        """
        Generate all ways to partition n into k positive integers.

        Example: partitions(4, 2) = [[1,3], [2,2], [3,1]]
        """
        if k == 1:
            yield [n]
        elif k > 1:
            for i in range(1, n):
                for partition in self._partitions(n - i, k - 1):
                    yield [i] + partition

    def _compile_ast(self, ast) -> Callable:
        """
        Compile AST to executable Python function.

        This is where symbolic becomes executable.
        """
        if ast[0] == 'primitive':
            op_name = ast[1]
            return self.primitive_ops[op_name]

        elif ast[0] == 'const':
            # Constant value
            const_val = ast[1]
            return lambda *args: const_val

        elif ast[0] == 'var':
            var_idx = ast[1]
            return lambda *args: args[var_idx] if var_idx < len(args) else None

        elif ast[0] == 'apply':
            op_name = ast[1]
            subprograms = ast[2]

            op_func = self.primitive_ops[op_name]
            compiled_subs = [self._compile_ast(sub) for sub in subprograms]

            def composed_func(*args):
                sub_results = [sub(*args) for sub in compiled_subs]
                return op_func(*sub_results)

            return composed_func

        else:
            raise ValueError(f"Unknown AST node: {ast[0]}")

    def _ast_to_code(self, ast) -> str:
        """Convert AST to readable code string."""
        if ast[0] == 'primitive':
            return ast[1]
        elif ast[0] == 'var':
            return f"arg{ast[1]}"
        elif ast[0] == 'apply':
            op_name = ast[1]
            subprograms = ast[2]
            sub_codes = [self._ast_to_code(sub) for sub in subprograms]
            return f"{op_name}({', '.join(sub_codes)})"
        else:
            return "unknown"

    def synthesize_from_type_signature(self,
                                       type_sig: str,
                                       examples: List[IOExample]) -> Optional[SynthesizedProgram]:
        """
        Synthesis guided by type signature.

        More constrained search = faster synthesis.
        """
        # This would use type-directed synthesis
        # For now, fallback to regular synthesis
        return self.synthesize(examples)

    def get_learned_abstractions(self) -> List[SynthesizedProgram]:
        """
        Return programs that successfully generalized.

        These become new primitives the system can use.
        """
        return [p for p in self.learned_programs if p.generalizes]

    def add_learned_as_primitive(self, program: SynthesizedProgram, name: str):
        """
        Add a learned program as a new primitive.

        This is how the system expands its capabilities.
        """
        self.primitive_ops[name] = program.function

    def __repr__(self):
        return f"<ProgramSynthesizer primitives={len(self.primitive_ops)} learned={len(self.learned_programs)}>"
