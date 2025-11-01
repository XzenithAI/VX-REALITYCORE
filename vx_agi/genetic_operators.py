"""
Genetic Programming - Evolve Operators Through Mutation & Crossover

TRUE evolution means:
- Population of operator programs
- Mutation (random code changes)
- Crossover (combine successful programs)
- Selection (fitness-based survival)
- Generations evolve better operators

Not incrementing a counter. ACTUAL genetic algorithms on code.
"""

from typing import List, Tuple, Callable, Any, Optional
from dataclasses import dataclass, field
import random
import copy


@dataclass
class GeneticOperator:
    """An operator in the genetic population."""
    ast: Tuple  # Program AST
    fitness: float = 0.0
    age: int = 0
    parent_ids: List[int] = field(default_factory=list)
    mutations: int = 0

    def __hash__(self):
        return hash(str(self.ast))


class GeneticEvolution:
    """
    Evolves operators through genetic programming.

    Population → Evaluate Fitness → Select → Mutate/Crossover → Next Generation
    """

    def __init__(self,
                 population_size: int = 100,
                 mutation_rate: float = 0.1,
                 crossover_rate: float = 0.7,
                 tournament_size: int = 5):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.tournament_size = tournament_size

        self.population: List[GeneticOperator] = []
        self.generation = 0
        self.best_ever: Optional[GeneticOperator] = None
        self.fitness_history = []

        # Available primitives for building programs
        self.primitives = [
            'add', 'sub', 'mul', 'div',
            'and', 'or', 'not',
            'eq', 'gt', 'lt',
            'if', 'identity',
            'map', 'filter', 'reduce',
            'head', 'tail', 'cons'
        ]

    def initialize_population(self, max_depth: int = 3):
        """
        Create initial random population.

        Half grown (full depth), half full (variable depth).
        """
        self.population = []

        for i in range(self.population_size):
            if i < self.population_size // 2:
                # Grow method: variable depth
                ast = self._generate_random_ast(max_depth, method='grow')
            else:
                # Full method: always reach max depth
                ast = self._generate_random_ast(max_depth, method='full')

            operator = GeneticOperator(ast=ast)
            self.population.append(operator)

    def _generate_random_ast(self, max_depth: int, method: str = 'grow') -> Tuple:
        """
        Generate random program AST.

        method='grow': Can terminate early
        method='full': Always goes to max depth
        """
        if max_depth == 0 or (method == 'grow' and random.random() < 0.3):
            # Terminal: variable or constant
            if random.random() < 0.5:
                return ('var', random.randint(0, 2))
            else:
                return ('const', random.choice([0, 1, 2, True, False]))
        else:
            # Non-terminal: random primitive
            primitive = random.choice(self.primitives)
            arity = self._get_arity(primitive)

            children = [
                self._generate_random_ast(max_depth - 1, method)
                for _ in range(arity)
            ]

            return ('apply', primitive, tuple(children))

    def _get_arity(self, primitive: str) -> int:
        """Get arity of primitive."""
        if primitive in ['add', 'sub', 'mul', 'div', 'and', 'or', 'eq', 'gt', 'lt', 'cons']:
            return 2
        elif primitive in ['not', 'identity', 'head', 'tail']:
            return 1
        elif primitive in ['if', 'reduce']:
            return 3
        elif primitive in ['map', 'filter']:
            return 2
        else:
            return 1

    def evaluate_fitness(self, fitness_function: Callable[[Tuple], float]):
        """
        Evaluate fitness of entire population.

        fitness_function: Takes AST, returns fitness score (higher = better)
        """
        for operator in self.population:
            try:
                operator.fitness = fitness_function(operator.ast)
            except:
                operator.fitness = 0.0

        # Update best ever
        best_current = max(self.population, key=lambda op: op.fitness)
        if self.best_ever is None or best_current.fitness > self.best_ever.fitness:
            self.best_ever = copy.deepcopy(best_current)

        # Track fitness statistics
        avg_fitness = sum(op.fitness for op in self.population) / len(self.population)
        self.fitness_history.append({
            'generation': self.generation,
            'avg_fitness': avg_fitness,
            'max_fitness': best_current.fitness,
            'best_ever': self.best_ever.fitness
        })

    def selection(self) -> GeneticOperator:
        """
        Tournament selection.

        Pick k random individuals, return best.
        """
        tournament = random.sample(self.population, self.tournament_size)
        return max(tournament, key=lambda op: op.fitness)

    def crossover(self, parent1: GeneticOperator, parent2: GeneticOperator) -> Tuple[GeneticOperator, GeneticOperator]:
        """
        Subtree crossover: swap random subtrees.

        Returns two children.
        """
        if random.random() > self.crossover_rate:
            # No crossover, return copies
            return copy.deepcopy(parent1), copy.deepcopy(parent2)

        # Deep copy ASTs
        ast1 = copy.deepcopy(parent1.ast)
        ast2 = copy.deepcopy(parent2.ast)

        # Get random subtrees
        subtrees1 = self._get_all_subtrees(ast1)
        subtrees2 = self._get_all_subtrees(ast2)

        if not subtrees1 or not subtrees2:
            return copy.deepcopy(parent1), copy.deepcopy(parent2)

        # Swap random subtrees
        point1 = random.choice(range(len(subtrees1)))
        point2 = random.choice(range(len(subtrees2)))

        # Create children by swapping
        child1_ast = self._replace_subtree(ast1, point1, subtrees2[point2])
        child2_ast = self._replace_subtree(ast2, point2, subtrees1[point1])

        child1 = GeneticOperator(
            ast=child1_ast,
            parent_ids=[id(parent1), id(parent2)]
        )
        child2 = GeneticOperator(
            ast=child2_ast,
            parent_ids=[id(parent2), id(parent1)]
        )

        return child1, child2

    def mutate(self, operator: GeneticOperator) -> GeneticOperator:
        """
        Mutation: randomly modify AST.

        Types of mutation:
        1. Point mutation: change a node
        2. Subtree mutation: replace subtree with random tree
        3. Hoist mutation: replace tree with random subtree
        """
        if random.random() > self.mutation_rate:
            return copy.deepcopy(operator)

        mutated_ast = copy.deepcopy(operator.ast)

        mutation_type = random.choice(['point', 'subtree', 'hoist'])

        if mutation_type == 'point':
            # Change a random node
            mutated_ast = self._point_mutation(mutated_ast)

        elif mutation_type == 'subtree':
            # Replace random subtree
            subtrees = self._get_all_subtrees(mutated_ast)
            if subtrees:
                point = random.choice(range(len(subtrees)))
                new_subtree = self._generate_random_ast(max_depth=2)
                mutated_ast = self._replace_subtree(mutated_ast, point, new_subtree)

        elif mutation_type == 'hoist':
            # Replace with random subtree (simplification)
            subtrees = self._get_all_subtrees(mutated_ast)
            if len(subtrees) > 1:
                mutated_ast = random.choice(subtrees[1:])  # Don't pick root

        mutated = GeneticOperator(
            ast=mutated_ast,
            parent_ids=[id(operator)],
            mutations=operator.mutations + 1
        )

        return mutated

    def _get_all_subtrees(self, ast: Tuple) -> List[Tuple]:
        """Get all subtrees of AST (for crossover/mutation points)."""
        subtrees = [ast]

        if ast[0] == 'apply':
            children = ast[2]
            for child in children:
                subtrees.extend(self._get_all_subtrees(child))

        return subtrees

    def _replace_subtree(self, ast: Tuple, index: int, new_subtree: Tuple) -> Tuple:
        """Replace subtree at index with new_subtree."""
        subtrees = self._get_all_subtrees(ast)

        if index >= len(subtrees):
            return ast

        target = subtrees[index]

        def replace_in_ast(node):
            if node == target:
                return new_subtree
            elif node[0] == 'apply':
                return ('apply', node[1], tuple(replace_in_ast(child) for child in node[2]))
            else:
                return node

        return replace_in_ast(ast)

    def _point_mutation(self, ast: Tuple) -> Tuple:
        """Mutate a single node in AST."""
        if ast[0] == 'var':
            return ('var', random.randint(0, 2))
        elif ast[0] == 'const':
            return ('const', random.choice([0, 1, 2, True, False]))
        elif ast[0] == 'apply':
            # Change the operation
            new_primitive = random.choice(self.primitives)
            return ('apply', new_primitive, ast[2])
        else:
            return ast

    def evolve_generation(self, fitness_function: Callable[[Tuple], float]):
        """
        Run one generation of evolution.

        1. Evaluate fitness
        2. Select parents
        3. Create offspring through crossover/mutation
        4. Replace population
        """
        # Evaluate current population
        self.evaluate_fitness(fitness_function)

        # Create new population
        new_population = []

        # Elitism: keep best individual
        best = max(self.population, key=lambda op: op.fitness)
        new_population.append(copy.deepcopy(best))

        # Generate rest of population
        while len(new_population) < self.population_size:
            # Select parents
            parent1 = self.selection()
            parent2 = self.selection()

            # Crossover
            child1, child2 = self.crossover(parent1, parent2)

            # Mutation
            child1 = self.mutate(child1)
            child2 = self.mutate(child2)

            # Age children
            child1.age = 0
            child2.age = 0

            new_population.append(child1)
            if len(new_population) < self.population_size:
                new_population.append(child2)

        # Age existing population
        for op in self.population:
            op.age += 1

        # Replace population
        self.population = new_population
        self.generation += 1

    def run_evolution(self,
                     fitness_function: Callable[[Tuple], float],
                     generations: int = 50) -> GeneticOperator:
        """
        Run evolution for multiple generations.

        Returns best operator found.
        """
        for _ in range(generations):
            self.evolve_generation(fitness_function)

        return self.best_ever

    def get_best(self) -> GeneticOperator:
        """Get best operator in current population."""
        return max(self.population, key=lambda op: op.fitness)

    def get_statistics(self) -> dict:
        """Get evolution statistics."""
        current_best = self.get_best()

        return {
            'generation': self.generation,
            'population_size': len(self.population),
            'best_fitness': current_best.fitness,
            'best_ever_fitness': self.best_ever.fitness if self.best_ever else 0.0,
            'avg_fitness': sum(op.fitness for op in self.population) / len(self.population),
            'fitness_history': self.fitness_history
        }

    def __repr__(self):
        return f"<GeneticEvolution gen={self.generation} pop={len(self.population)} best={self.best_ever.fitness if self.best_ever else 0:.3f}>"
