import functools
import sys
from dataclasses import dataclass, field
from collections.abc import Callable
from typing import Any


@dataclass
class AgentSession:
    """Tracks runtime metrics for a unique agent execution path."""

    max_cost_usd: float
    max_iterations: int
    current_cost_usd: float = 0.0
    current_iterations: int = 0
    history: list[dict[str, Any]] = field(default_factory=list)

    def record_llm_call(self, model: str, prompt_tokens: int, completion_tokens: int):
        """Calculates token costs deterministically and checks boundaries."""
        # Simple pricing matrix mapping: Cost per 1M tokens (Example pricing)
        pricing = {
            "gpt-4o": {"prompt": 5.00, "completion": 15.00},
            "gpt-3.5-turbo": {"prompt": 0.50, "completion": 1.50},
        }

        rates = pricing.get(model, {"prompt": 10.00, "completion": 30.00})
        cost = (prompt_tokens / 1_000_000 * rates["prompt"]) + (
            completion_tokens / 1_000_000 * rates["completion"]
        )

        self.current_cost_usd += cost
        self.history.append(
            {
                "model": model,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "calculated_cost": cost,
            }
        )

        if self.current_cost_usd > self.max_cost_usd:
            self._trigger_circuit_breaker(
                f"Budget exceeded! Max: ${self.max_cost_usd:.4f}, Current: ${self.current_cost_usd:.4f}"
            )

    def increment_iteration(self):
        """Tracks execution graph depth to stop infinite loops."""
        self.current_iterations += 1
        if self.current_iterations > self.max_iterations:
            self._trigger_circuit_breaker(
                f"Loop depth exceeded! Max iterations: {self.max_iterations}"
            )

    def _trigger_circuit_breaker(self, message: str):
        """Halts the execution pipeline deterministically."""
        print(f"\n[AegisAgent - CRITICAL] Circuit Breaker Tripped!")
        print("-" * 50)
        print(f"Reason: {message}")
        print(f"Total Iterations: {self.current_iterations}")
        print(f"Total Cost: ${self.current_cost_usd:.4f}")
        print("-" * 50)
        # Prevent any further downstream processing
        raise SystemExit("Execution halted by AegisAgent budget guardrails.")


def budget_breaker(max_cost_usd: float, max_iterations: int):
    """Decorator to enforce deterministic resource boundaries on agent loops."""

    def decorator(func: Callable[..., Any]):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Inject a managed tracking session into the execution
            session = AgentSession(
                max_cost_usd=max_cost_usd, max_iterations=max_iterations
            )

            # Look for an 'agent_session' keyword argument or pass it in
            kwargs["session"] = session
            return func(*args, **kwargs)

        return wrapper

    return decorator
