# 🛡️ AegisAgent

**The Open-Source, Code-First Deterministic Safety & Budget Layer for Python AI Agents.**

[![Python 3.12](https://shields.io)](https://python.org)
[![Linter: Ruff](https://shields.io)](https://github.com)
[![License: MIT](https://shields.io)](https://opensource.org)

Probabilistic AI models (LLMs) are great at reasoning, but dangerous when deployed autonomously. Left unchecked, agents suffer from **infinite reasoning loops, runaway API token bills, and schema validation crashes**. 

**AegisAgent** is a lightweight, zero-overhead framework that wraps chaotic AI agents inside strict, deterministic financial and compliance guardrails directly at the code level.

---

## ⚡ Core Value Pillars

*   **Runaway Cost Prevention:** Instantly halts agent loops via strict pythonic circuit breakers the exact millisecond a monetary budget ceiling is breached.
*   **Compile-Time Schema Gates:** Intercepts chaotic unstructured text strings and safely coerces them into strict, predictable database entities using Pydantic validation.
*   **Deterministic Circuit Breakers:** Sets hard iteration depth limits to detect and kill infinite execution loops automatically.
*   **Immutable State Snapshots:** Automatically serializes and dumps the agent's complete memory history, prompts, and tokens to disk upon failure for human-in-the-loop auditing.

---

## 🚀 Quick Start

### 1. Installation
Install the framework within your isolated virtual environment:

```bash
pip install -e .
```

### 2. Local No-Cost Development Setup
AegisAgent supports offline development using free, open-source local models. Download and launch [Ollama](https://ollama.com), then pull a lightweight model:

```bash
ollama pull llama3.2:1b
```

---

## 💻 Code Implementation Example

This real-world example creates a **Logistics Freight Invoice Processor** workflow. It extracts unstructured email text, forces it through a strict data contract, and protects the company from infinite runtime loop bills.

Create a script or run `examples/client_simulation.py`:

```python
import ollama
from pydantic import BaseModel, Field
from aegisagent.schema import schema_gate
from aegisagent.workflow import Workflow

# 1. Define your strict enterprise business data contract
class FreightInvoice(BaseModel):
    carrier_name: str = Field(description="Name of the shipping company")
    invoice_number: str
    fuel_surcharge: float
    base_rate: float
    total_amount: float

# 2. Wrap your probabilistic agent inside a deterministic schema gate
@schema_gate(response_schema=FreightInvoice)
def live_email_parser_agent(email_body: str, session) -> str:
    # Generate text on your local machine with zero API cost
    response = ollama.chat(
        model="llama3.2:1b",
        messages=[{"role": "user", "content": f"Extract invoice details into JSON: {email_body}"}]
    )

    # Intercept dynamic token counts directly from hardware execution
    prompt_tokens = response.get("prompt_eval_count", 1000)
    completion_tokens = response.get("eval_count", 500)

    # Record usage metrics into AegisAgent's pricing engine matrix
    session.record_llm_call(
        model="gpt-4o",  # Evaluates token footprints against standard production tiers
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens
    )
    return response["message"]["content"]

# 3. Secure your business pipelines using unified workflow envelopes
if __name__ == "__main__":
    # Hard envelope: Halt instantly if execution exceeds $0.02 or 3 iterations
    pipeline = Workflow(max_cost_usd=0.02, max_iterations=3)
    pipeline.add_step(live_email_parser_agent)

    mock_email = "Invoice FDX-882 from FedEx. Base is 500 dollars plus 60 fuel. Total is 560."
    
    try:
        pipeline.execute(initial_input=mock_email)
    except SystemExit:
        print("\n[AEGIS] Runaway bill blocked. Zero enterprise budget wasted.")
```

---

## 📊 Automated Failure Audit Logs

When an agent triggers a cost or iteration circuit breaker, a JSON state snapshot is dumped automatically to the `/logs` directory:

```json
{
    "timestamp": "2026-06-26T07:59:00.123456Z",
    "termination_reason": "Budget exceeded! Max: $0.0200, Current: $0.0325",
    "session_metrics": {
        "total_cost_usd": 0.0325,
        "max_cost_limit": 0.02,
        "total_iterations": 2
    },
    "execution_history": [
        {
            "model": "gpt-4o",
            "prompt_tokens": 1500,
            "completion_tokens": 800,
            "calculated_cost": 0.0195
        }
    ]
}
```

---

## 🛠️ Workspace Architecture

```text
aegis-agent-core/
├── src/
│   └── aegisagent/        # Core framework code
│       ├── __init__.py
│       ├── budget.py      # Budget tracking and circuit breakers
│       ├── schema.py      # Pydantic schema enforcement gates
│       └── workflow.py    # Multi-step graph orchestration and state serializers
├── examples/              # Ready-to-run client simulation scenarios
├── logs/                  # Automated crash audit logs
├── pyproject.toml         # Ruff configurations & Python package definitions
└── requirements.txt       # Project dependencies
```

---

## 🤝 Contributing & Community

AegisAgent is a developer-first tool. We warmly welcome community contributions regarding:
*   Additional cloud provider pricing matrices (Anthropic, Cohere, Mistral).
*   Dynamic text repair layers inside failed schema gates.
*   Persistent graph adapters for complex routing.

License: [MIT](LICENSE)
