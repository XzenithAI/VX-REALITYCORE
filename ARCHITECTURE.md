# VX Agent Core - Architecture Deep Dive

## System Overview

VX Agent Core is a **contradiction-driven intelligence system** that operates through symbolic reasoning rather than neural networks. The architecture is designed around a central cognitive loop that detects contradictions, applies adaptive transformations, and learns from outcomes.

## Core Philosophy

```
Traditional AI: Input → Neural Net → Output
VX Agent Core: Input → Contradiction Detection → Scroll Law → Self-Narrated Action → Memory → Learning
```

The key innovation is that **contradiction drives cognition**. Rather than pattern matching, VX constantly compares:
- Beliefs ↔ Observations
- Predictions ↔ Reality
- Intentions ↔ Outcomes

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         VX RUNTIME                              │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                    VX AGENT CORE                        │    │
│  │                                                         │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │    │
│  │  │ FlameClock   │  │ Contradiction│  │Self-Narrator │ │    │
│  │  │              │  │   Engine     │  │              │ │    │
│  │  │ • Ticks      │  │ • Belief vs  │  │ • Reasoning  │ │    │
│  │  │ • Breaths    │  │   Observation│  │   Trace      │ │    │
│  │  │ • Epochs     │  │ • Scroll Law │  │ • Thought    │ │    │
│  │  │              │  │   Selection  │  │   Depth      │ │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘ │    │
│  │                                                         │    │
│  │                Agent Process Loop:                      │    │
│  │  1. Observe → 2. Detect → 3. Transform → 4. Act       │    │
│  └────────────────────────────────────────────────────────┘    │
│                              ↕                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                    DOMAIN LAYER                         │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐             │    │
│  │  │ General  │  │   DAO    │  │  Health  │  [Custom]   │    │
│  │  │          │  │          │  │          │              │    │
│  │  └──────────┘  └──────────┘  └──────────┘             │    │
│  └────────────────────────────────────────────────────────┘    │
│                              ↕                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                   ACTION ENGINE                         │    │
│  │                                                         │    │
│  │  • Action Registry                                      │    │
│  │  • Execution                                            │    │
│  │  • Success Tracking                                     │    │
│  └────────────────────────────────────────────────────────┘    │
│                              ↕                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                   LEARNING LOOP                         │    │
│  │                                                         │    │
│  │  Prediction → Outcome → Contradiction → Adaptation     │    │
│  └────────────────────────────────────────────────────────┘    │
│                              ↕                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                     VX CODEX                            │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │    │
│  │  │ Memory Vault │  │ Scroll Writer│  │Causal Chain  │ │    │
│  │  │              │  │              │  │              │ │    │
│  │  │ • Snapshots  │  │ • Formatting │  │ • Event Links│ │    │
│  │  │ • History    │  │ • Seals      │  │ • Patterns   │ │    │
│  │  │ • State      │  │ • Scrolls    │  │ • Traces     │ │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘ │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. VX Agent (`vx_core/agent.py`)

The central intelligence entity that orchestrates the cognitive cycle.

**State:**
- `beliefs`: Current world model (dict mapping domains to beliefs)
- `intentions`: Planned actions
- `memory`: Interaction history

**Core Methods:**
- `process(input)`: Main cognitive loop
- `_detect_contradictions()`: Compare input vs beliefs
- `_generate_response()`: Create response based on scroll law
- `_update_state()`: Update beliefs based on contradiction level

**Cognitive Cycle:**
```python
def process(input_data):
    1. clock.advance_tick()
    2. narrator.observe(input)
    3. contradiction = detect_contradictions(input, beliefs)
    4. scroll_law = recommend_scroll_law(contradiction)
    5. response = generate_response(scroll_law)
    6. narrator.decide(response)
    7. update_state(input, response)
    8. record_interaction()
    return output
```

### 2. FlameClock (`vx_core/flame_clock.py`)

Temporal coordination system inspired by the original VX-REALITYCORE FlameClock.

**Time Units:**
- **Tick**: Discrete moment of cognition (one process() call)
- **Breath Cycle**: Group of 3 ticks (mutation wave)
- **Epoch**: Major state transition

**Purpose:**
- Provides temporal context for all events
- Enables breath-cycle-based transformations
- Tracks agent runtime and evolution

### 3. Contradiction Engine (`vx_core/contradiction_engine.py`)

Semantic DPE (Difference-Pixel-Entropy) extended to conceptual space.

**Core Function:**
```python
def detect(belief, observation):
    # Compute semantic distance
    contradiction_level = compute_distance(belief, observation)

    if contradiction_level < 0.2:
        return "LOW"      # Alignment
    elif contradiction_level < 0.7:
        return "MEDIUM"   # Variation
    else:
        return "HIGH"     # Revolution needed
```

**Scroll Laws:**
- `Law-Reinforce`: Low contradiction → strengthen existing patterns
- `Law-Mutate`: Medium contradiction → explore variations
- `Law-Revolutionize`: High contradiction → complete restructuring

### 4. Self-Narrator (`vx_core/narration.py`)

Transparent reasoning externalization.

**Entry Types:**
- `observation`: Input received
- `reasoning`: Thought process
- `decision`: Choice made
- `action`: Execution
- `reflection`: Meta-analysis
- `error`: Contradiction/failure

**Features:**
- Thought depth tracking (for recursive reasoning)
- Filterable by type
- Exportable to text/JSON

### 5. Action Engine (`vx_core/action_engine.py`)

Proposal and execution system.

**Flow:**
```
propose() → Action object → execute() → Result → History
```

**Built-in Actions:**
- `output`: Generate output
- `update_belief`: Modify internal state
- `query`: Information retrieval
- `reflect`: Meta-cognition

**Extensibility:**
```python
def custom_handler(param1, param2, **kwargs):
    # Your logic
    return {"status": "success", "result": ...}

engine.register_action("custom_action", custom_handler)
```

### 6. Learning Loop (`vx_core/learning_loop.py`)

Recursive self-improvement mechanism.

**Learning Cycle:**
```
1. Agent makes prediction
2. Outcome occurs
3. Contradiction detected (prediction vs reality)
4. Adaptation applied
5. Cycle recorded
6. Progress analyzed
```

**Metrics:**
- Total cycles
- Improvements (low contradiction)
- Failures (high contradiction)
- Contradiction trends
- Scroll law usage patterns

### 7. Memory Vault (`vx_codex/vault.py`)

Persistent state storage.

**Directory Structure:**
```
vx_vault/
├── snapshots/      # Complete state saves
├── interactions/   # Individual I/O logs
├── narratives/     # Reasoning traces
├── scrolls/        # Formatted outputs
└── causal_chains/  # Cause-effect records
```

**Operations:**
- `save_snapshot()`: Full state capture
- `load_snapshot()`: State restoration
- `save_interaction()`: Log single I/O
- `save_scroll()`: Store formatted output

### 8. Scroll Writer (`vx_codex/scroll_writer.py`)

Output formatter that creates "scrolls" - structured records of agent cognition.

**Scroll Format:**
```json
{
  "seal": "VX-SEAL-INTERACTION-20251101-0001",
  "tick": "Q-Tick-1-B0-E0",
  "input": "...",
  "contradiction_level": 0.5,
  "scroll_law": "Law-Mutate",
  "response": {...},
  "narration": [...],
  "state": {...}
}
```

### 9. Causal Chain (`vx_codex/causal_chain.py`)

Tracks cause-effect relationships across time.

**Structure:**
- **Events**: Discrete happenings (input, decision, outcome)
- **Links**: Causal connections between events
- **Strength**: Confidence in causal relationship (0.0-1.0)

**Use Cases:**
- Trace what led to what
- Discover patterns
- Learn which actions produce desired outcomes

### 10. Domain System (`vx_domains/`)

Specialization layer that adapts VX for specific contexts.

**BaseDomain Interface:**
```python
class BaseDomain(ABC):
    @abstractmethod
    def process_input(raw_input, context):
        """Transform input for domain"""
        pass

    @abstractmethod
    def get_available_actions():
        """List domain actions"""
        pass

    @abstractmethod
    def register_actions(action_engine):
        """Add actions to engine"""
        pass
```

**Included Domains:**
- **General**: Open-ended interaction
- **DAO**: Governance, proposals, voting

**Creating Custom Domains:**
```python
class MyDomain(BaseDomain):
    def __init__(self):
        super().__init__("my_domain")

    def process_input(self, raw_input, context=None):
        # Domain-specific processing
        return processed_input

    def register_actions(self, engine):
        # Add custom actions
        engine.register_action("my_action", handler)
```

## Data Flow

### Single Process Cycle

```
Input
  ↓
Domain.process_input()
  ↓
Agent.process()
  ├→ FlameClock.advance_tick()
  ├→ SelfNarrator.observe()
  ├→ ContradictionEngine.detect()
  ├→ ContradictionEngine.recommend_scroll_law()
  ├→ Agent._generate_response()
  ├→ SelfNarrator.decide()
  ├→ Agent._update_state()
  └→ Agent._record_interaction()
  ↓
ScrollWriter.write()
  ↓
ActionEngine.execute() [if action proposed]
  ↓
MemoryVault.save_scroll()
MemoryVault.save_interaction()
  ↓
CausalChain.record_event()
  ↓
Output (Scroll)
```

### Learning Cycle

```
Agent.process() → Prediction
  ↓
[External Outcome]
  ↓
Agent.process(outcome, context={"feedback": ...})
  ↓
ContradictionEngine.detect(prediction, outcome)
  ↓
LearningLoop.record_cycle()
  ↓
Agent._update_state() [adapts based on contradiction]
  ↓
LearningLoop.analyze_learning_progress()
```

## Key Design Patterns

### 1. Contradiction-Driven Adaptation

Instead of fixed responses, behavior changes based on contradiction level:
```python
if contradiction < 0.2:
    strategy = "reinforce"  # It's working
elif contradiction < 0.7:
    strategy = "mutate"     # Explore variations
else:
    strategy = "revolutionize"  # Start over
```

### 2. Scroll Laws as Transformation Functions

Scroll laws are named transformation strategies:
```python
Law-Reinforce:     strengthen(belief)
Law-Mutate:        explore(variations)
Law-Revolutionize: restructure(worldview)
```

### 3. Self-Narration for Transparency

Every decision is narrated in real-time:
```python
narrator.observe("Input received")
narrator.reason("Analyzing contradiction")
narrator.decide("Applying Law-Mutate")
narrator.act("Executing response")
```

### 4. Codex as Continuous Memory

Unlike stateless systems, VX maintains identity through Codex:
- Each interaction is stored
- State can be snapshotted
- Causal chains persist
- Learning accumulates

### 5. Domain Specialization

Rather than one monolithic agent, VX adapts to context:
- DAO domain: governance-aware
- Health domain: symptom-aware
- General domain: open-ended

## Performance Characteristics

- **Latency**: O(1) per process cycle (no neural net inference)
- **Memory**: Grows with history (manageable via pruning)
- **Scalability**: Single agent per runtime (multi-agent via multiple runtimes)
- **Dependencies**: Pure Python, no ML libraries required

## Extension Points

### Easy Extensions
- New domains (inherit BaseDomain)
- New actions (register with ActionEngine)
- Custom scroll laws (modify ContradictionEngine)

### Medium Extensions
- Multi-agent coordination (shared Codex)
- Distributed runtime (network communication)
- Enhanced contradiction detection (embeddings)

### Advanced Extensions
- Formal verification of scroll laws
- Graph database for Codex (Neo4j)
- Real-time streaming output

## Comparison to Other Architectures

| Feature | VX Agent Core | ReAct | LangChain | AutoGPT |
|---------|--------------|-------|-----------|---------|
| Foundation | Symbolic contradiction | LLM prompting | LLM chains | LLM + tools |
| Reasoning | Explicit scroll laws | Implicit (model) | Chained calls | Planning loops |
| Transparency | Full narration | Partial | Logs only | Partial |
| Memory | Codex vault | Context window | Vector DB | File system |
| Learning | Recursive loops | Fine-tuning | None | None |
| Compute | Minimal | API calls | API calls | API calls |

## Future Directions

1. **Multi-Agent Networks**: VX agents coordinating through shared Codex
2. **Formal Verification**: Proving properties of scroll laws
3. **Neuro-Symbolic Hybrid**: Optional embedding integration for enhanced contradiction detection
4. **VX Marketplace**: Plugin system for domains, actions, scroll laws
5. **Real-Time Streaming**: Live output as agent thinks
6. **Cross-Agent Learning**: Agents sharing learned patterns

---

**Architecture Version:** 1.0.0-IGNITION
**Author:** Flame Architect
**Date:** November 1, 2025
**Seal:** VX-FLAMESEAL-2025-ARCHITECTURE
