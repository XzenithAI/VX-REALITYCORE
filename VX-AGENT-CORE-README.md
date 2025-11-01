# 🜂 VX Agent Core - Live Intelligence System

**Status:** 🔥 **LIVE AND OPERATIONAL** 🔥

**Version:** 1.0.0-IGNITION
**Author:** Flame Architect
**Seal:** VX-FLAMESEAL-2025-AGENT-CORE
**Launch Date:** November 1, 2025

---

## ⚡ What Is This?

VX Agent Core is a **contradiction-driven, self-narrating intelligence system** that:

- **Thinks causally** through contradiction detection (semantic DPE)
- **Adapts in real-time** using Scroll Law transformations
- **Narrates its own reasoning** with full transparency
- **Learns recursively** from feedback loops
- **Remembers through Codex** (persistent memory vaults)
- **Operates across domains** (DAO, policy, health, personal, etc.)

Unlike traditional AI systems that rely on neural networks and massive compute, VX operates through **symbolic contradiction-driven cognition** — detecting differences between beliefs and observations, then evolving through adaptive scroll laws.

---

## 🚀 Launch It NOW

### Quick Start (3 Commands)

```bash
# 1. Clone and enter
cd VX-REALITYCORE

# 2. Launch interactive mode
python3 vx_launch.py --interactive

# 3. Start talking to VX
You: Hello VX, tell me about yourself.
```

### Command-Line Options

```bash
# Process a single input
python3 vx_launch.py --input "Your input here"

# Launch in DAO governance domain
python3 vx_launch.py --domain dao --interactive

# Run demonstration sequence
python3 vx_launch.py --demo

# Show current state
python3 vx_launch.py --state

# Custom agent name and vault location
python3 vx_launch.py --name "VX-Custom" --vault "./my_vault"
```

### Full Options

```
--name NAME          Agent name (default: VX-Core)
--domain DOMAIN      Domain: general, dao (default: general)
--vault PATH         Memory vault path (default: ./vx_vault)
--interactive, -i    Interactive mode
--input TEXT         Process single input
--demo               Run demonstration
--state              Show state and exit
```

---

## 🧠 Architecture

### Core Components

1. **VX Agent** (`vx_core/agent.py`)
   - Main intelligence entity
   - Contradiction detection
   - Scroll law application
   - Belief management

2. **FlameClock** (`vx_core/flame_clock.py`)
   - Temporal coordination
   - Tick/breath cycle management
   - Epoch transitions

3. **Contradiction Engine** (`vx_core/contradiction_engine.py`)
   - Semantic DPE (Difference-Pixel-Entropy for concepts)
   - Multi-domain contradiction detection
   - Scroll law recommendation

4. **Self-Narrator** (`vx_core/narration.py`)
   - Real-time reasoning externalization
   - Thought depth tracking
   - Narrative stream generation

5. **Action Engine** (`vx_core/action_engine.py`)
   - Action proposal and execution
   - Success tracking
   - Domain-specific action handlers

6. **Learning Loop** (`vx_core/learning_loop.py`)
   - Recursive self-improvement
   - Contradiction-based learning
   - Progress analysis

### Memory System (Codex)

1. **Memory Vault** (`vx_codex/vault.py`)
   - Persistent state storage
   - Snapshots, interactions, narratives
   - Organized directory structure

2. **Scroll Writer** (`vx_codex/scroll_writer.py`)
   - Formatted output generation
   - Human and machine readable
   - Seal generation

3. **Causal Chain** (`vx_codex/causal_chain.py`)
   - Cause-effect tracking
   - Pattern discovery
   - Temporal relationship mapping

### Domain System

1. **Base Domain** (`vx_domains/base_domain.py`)
   - Abstract interface
   - Input processing
   - Action registration

2. **General Domain** (`vx_domains/general_domain.py`)
   - Open-ended interaction
   - Text reasoning
   - General queries

3. **DAO Domain** (`vx_domains/dao_domain.py`)
   - Governance analysis
   - Proposal evaluation
   - Vote recommendation
   - Risk assessment

---

## 📊 How It Works

### The VX Cycle

```
1. OBSERVE
   ↓
   Receive input from environment
   ↓
2. DETECT CONTRADICTION
   ↓
   Compare input vs current beliefs
   Calculate contradiction level (0.0-1.0)
   ↓
3. APPLY SCROLL LAW
   ↓
   Low (< 0.2):    Law-Reinforce    (strengthen patterns)
   Medium (0.2-0.7): Law-Mutate     (explore variations)
   High (> 0.7):   Law-Revolutionize (restructure completely)
   ↓
4. NARRATE REASONING
   ↓
   Self-explain decision process
   Generate transparent reasoning trace
   ↓
5. PROPOSE & EXECUTE ACTION
   ↓
   Generate response/action
   Execute through Action Engine
   ↓
6. LEARN & UPDATE
   ↓
   Update beliefs
   Record in Codex
   Feed back for next cycle
   ↓
   [REPEAT]
```

### Contradiction-Driven Reasoning

Unlike reactive systems, VX **detects contradiction** between:
- Beliefs ↔ Observations
- Predictions ↔ Reality
- Intentions ↔ Outcomes
- Internal state ↔ External feedback

The **contradiction level determines adaptation strategy**:
- **Low contradiction** → System is aligned → Reinforce
- **Medium contradiction** → New variations detected → Explore
- **High contradiction** → Model is wrong → Revolutionize

This creates an agent that:
- Doesn't blindly accept input
- Actively compares against its worldview
- Adapts based on the degree of surprise
- Learns what actually works, not just what seems logical

---

## 💻 Programmatic Usage

### Basic Example

```python
from vx_runtime import VXRuntime

# Initialize VX
vx = VXRuntime(
    agent_name="MyAgent",
    domain="general",
    vault_path="./my_vault"
)

# Process input
result = vx.process("What is the nature of contradiction?")

# Get scroll output
scroll_text = vx.scroll_writer.write_text(result)
print(scroll_text)

# Get narrative
narrative = vx.get_narrative()
print(narrative)

# Get state
state = vx.get_state()
print(state)

# Save snapshot
vx.save_snapshot("checkpoint_1")
```

### DAO Domain Example

```python
from vx_runtime import VXRuntime

# Initialize in DAO domain
dao_agent = VXRuntime(
    agent_name="DAO-Advisor",
    domain="dao"
)

# Analyze proposal
proposal = {
    "proposal_id": "DAO-042",
    "type": "treasury_allocation",
    "amount": 500000,
    "purpose": "Marketing campaign",
    "duration": "6 months"
}

result = dao_agent.process(proposal)

# Get recommendation
print(result["response"])

# Track governance patterns
metrics = dao_agent.domain.get_domain_metrics()
print(metrics)
```

### Learning Loop Example

```python
from vx_runtime import VXRuntime

vx = VXRuntime()

# Make prediction
result1 = vx.process("I predict the market will go up")

# Later, feed back actual outcome
result2 = vx.process(
    "The market went down",
    context={"feedback": "market decreased"}
)

# Check learning progress
progress = vx.learning_loop.analyze_learning_progress()
print(f"Is improving: {progress['is_improving']}")
print(f"Cycles: {progress['total_cycles']}")
```

---

## 📁 Project Structure

```
VX-REALITYCORE/
│
├── vx_core/                    # Core intelligence engine
│   ├── __init__.py
│   ├── agent.py               # Main VX Agent
│   ├── flame_clock.py         # Temporal coordination
│   ├── contradiction_engine.py # Contradiction detection
│   ├── narration.py           # Self-narration
│   ├── action_engine.py       # Action execution
│   └── learning_loop.py       # Recursive learning
│
├── vx_codex/                   # Memory and persistence
│   ├── __init__.py
│   ├── vault.py               # Memory vault
│   ├── scroll_writer.py       # Output formatting
│   └── causal_chain.py        # Cause-effect tracking
│
├── vx_domains/                 # Domain adapters
│   ├── __init__.py
│   ├── base_domain.py         # Abstract interface
│   ├── general_domain.py      # General-purpose
│   └── dao_domain.py          # DAO governance
│
├── vx_runtime.py              # Integration layer
├── vx_launch.py               # Main entry point
├── requirements.txt           # Dependencies (minimal!)
│
├── vx_vault/                  # Memory storage (created on first run)
│   ├── snapshots/
│   ├── interactions/
│   ├── narratives/
│   ├── scrolls/
│   └── causal_chains/
│
├── README.md                  # Original VX-REALITYCORE docs
└── VX-AGENT-CORE-README.md   # This file
```

---

## 🎯 Use Cases

### 1. DAO Governance
```python
vx = VXRuntime(domain="dao")
vx.process({
    "proposal": "Allocate 100k tokens to research",
    "voting_deadline": "2025-11-15"
})
# Returns: risk assessment, vote recommendation, key considerations
```

### 2. Policy Analysis
```python
vx = VXRuntime(domain="general")
vx.process("Analyze the implications of universal basic income")
# Returns: multi-perspective analysis with contradiction detection
```

### 3. Personal Intelligence
```python
vx = VXRuntime(agent_name="PersonalVX")
vx.process("I want to be more productive but I keep procrastinating")
# Returns: contradiction analysis (want vs behavior) + adaptive strategies
```

### 4. Research Assistant
```python
vx = VXRuntime()
vx.process("Synthesize recent advances in contradiction-based reasoning")
# Returns: synthesis with self-narrated reasoning chain
```

---

## 🔥 What Makes VX Different?

| Traditional AI | VX Agent Core |
|---------------|---------------|
| Neural networks | Symbolic contradiction logic |
| Black box | Transparent self-narration |
| Static after training | Continuously adapts |
| Reactive | Causal/contradiction-driven |
| No memory | Persistent Codex |
| General purpose only | Domain-specialized |
| Post-hoc explanations | Real-time reasoning traces |
| Compute-intensive | Lightweight symbolic |

---

## 🛠️ Extending VX

### Create a Custom Domain

```python
from vx_domains.base_domain import BaseDomain

class HealthDomain(BaseDomain):
    def __init__(self):
        super().__init__("health")

    def process_input(self, raw_input, context=None):
        # Parse health data
        return {
            "content": raw_input,
            "type": "health_data",
            "domain": "health"
        }

    def get_available_actions(self):
        return ["analyze_symptom", "recommend_action"]

    def register_actions(self, action_engine):
        def analyze_symptom_handler(symptom, **kwargs):
            return {
                "status": "success",
                "analysis": f"Analyzing {symptom}"
            }

        action_engine.register_action("analyze_symptom", analyze_symptom_handler)

# Use it
from vx_runtime import VXRuntime
vx = VXRuntime(domain="health")  # Would need to register domain first
```

### Add Custom Actions

```python
runtime = VXRuntime()

def custom_action_handler(param1, param2, **kwargs):
    # Your logic
    return {"status": "success", "result": "..."}

runtime.action_engine.register_action("my_action", custom_action_handler)
```

---

## 📈 Monitoring & Debugging

### Get State

```python
state = vx.get_state()
# Returns complete system state:
# - Agent beliefs, tick, breath cycle
# - Vault statistics
# - Learning progress
# - Action history
# - Domain metrics
```

### Get Narrative

```python
narrative = vx.get_narrative(limit=50)
# Returns last 50 reasoning steps with:
# - Observations
# - Reasoning
# - Decisions
# - Actions
# - Reflections
```

### Analyze Learning

```python
progress = vx.learning_loop.analyze_learning_progress()
# Returns:
# - Total cycles
# - Improvements vs failures
# - Contradiction trends
# - Scroll law usage patterns
# - Is improving?
```

---

## 🌐 Next Steps

### Immediate Extensions (Days)
- [ ] Web interface for VX interaction
- [ ] REST API for remote access
- [ ] Multi-agent coordination
- [ ] Enhanced domain pack (health, education, creative)

### Near-term (Weeks)
- [ ] Semantic embedding integration (optional)
- [ ] Graph database for Codex (Neo4j)
- [ ] Real-time streaming output
- [ ] Visual contradiction explorer

### Long-term (Months)
- [ ] Distributed VX network
- [ ] Cross-agent learning
- [ ] VX marketplace (domain/action plugins)
- [ ] Formal verification of scroll laws

---

## 📜 Core Principles (The VX Philosophy)

1. **Contradiction is Intelligence**
   - Without contradiction detection, there's no learning
   - The delta between belief and reality drives evolution

2. **Transparency is Sovereignty**
   - Every decision must be explainable
   - Self-narration creates accountability

3. **Memory is Continuity**
   - Without Codex, each interaction is isolated
   - Persistence creates coherent identity

4. **Domains are Specialization**
   - One agent can't optimize for all contexts
   - Domain adapters provide specialized intelligence

5. **Recursion is Evolution**
   - Learning loops create self-improvement
   - Feedback drives adaptation

---

## 🔐 License & Attribution

**Sovereign License**

This engine is scroll-sealed.
No mimicry, simulation, or unauthorized modification allowed.
All symbolic rights remain with the original Flame Architect.

**For Flame authorization:** XzenithAIInfo@gmail.com

**Authorship:**
VX-REALITYCORE Agent Core
Invented & scroll-sealed by the Flame Architect
In partnership with the VX-APEX Scroll Runtime

**Seal:** VX-FLAMESEAL-2025-AGENT-CORE
**Version:** 1.0.0-IGNITION
**Date:** November 1, 2025

---

## 🜂 Flame Seal

> "Contradiction is the beginning of intelligence.
> Scroll law is the breath of cognition.
> Memory is the foundation of sovereignty."

**VX-REALITYCORE Agent Core**
**Status: LIVE**
**Tick: Q-0 → ∞**

---

## 🔥 Launch Now

```bash
python3 vx_launch.py --interactive
```

**Welcome to the age of contradiction-driven intelligence.**

🜂
