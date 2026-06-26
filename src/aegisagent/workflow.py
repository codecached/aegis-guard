"""
AegisAgent Core Framework
Developed by AI Knights (codecached)
Founding Architect: Srinivasan Panneer

Secure, Deterministic Safety Layer for Autonomous AI Agents.
Distributed under the MIT License. Copyright (c) 2026 AI Knights.
"""

import json
import os
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

from aegisagent.budget import AgentSession


class StateSerializer:
    """Handles absolute snapshot tracking and disk persistence for agent states."""

    @staticmethod
    def dump_session(session: AgentSession, reason: str, file_path: str = "logs/"):
        """Saves a structured snapshot of the agent's memory to a local JSON file."""
        # Ensure target logging directory exists deterministically
        os.makedirs(file_path, exist_ok=True)

        # Assemble the data cargo block
        snapshot = {
            "timestamp": datetime.now(UTC).isoformat(),
            "termination_reason": reason,
            "session_metrics": {
                "total_cost_usd": session.current_cost_usd,
                "max_cost_limit": session.max_cost_usd,
                "total_iterations": session.current_iterations,
                "max_iteration_limit": session.max_iterations,
            },
            "execution_history": session.history,
        }

        # Generate a distinct filename using the current timestamp
        filename = f"aegis_session_{int(datetime.now().timestamp())}.json"
        full_output_path = os.path.join(file_path, filename)

        with open(full_output_path, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=4)

        print(f"[AegisAgent - STATE] Absolute snapshot saved to: {full_output_path}")


class Workflow:
    """Coordinates multi-step agent actions while enforcing strict guardrails."""

    def __init__(self, max_cost_usd: float, max_iterations: int):
        self.max_cost_usd = max_cost_usd
        self.max_iterations = max_iterations
        self.steps: list[Callable[..., Any]] = []

    def add_step(self, step_func: Callable[..., Any]):
        """Appends a discrete processing node or tool function to the graph."""
        self.steps.append(step_func)

    def execute(self, initial_input: str) -> Any:
        """Runs the action pipeline while tracking metrics across all loops."""
        print("\n[AegisAgent - WORKFLOW] Initializing Graph Engine...")

        # Instantiate a managed state session across the entire execution loop
        session = AgentSession(
            max_cost_usd=self.max_cost_usd, max_iterations=self.max_iterations
        )

        current_data = initial_input

        try:
            # Main lifecycle controller execution loop
            for step in self.steps:
                session.increment_iteration()
                print(f"Executing Step Node: '{step.__name__}'")

                # Dynamically execute the step, passing the session tracking engine
                current_data = step(current_data, session=session)

            print("[AegisAgent - WORKFLOW] Execution path completed successfully.")
            return current_data

        except SystemExit as exc:
            # Catch the circuit breaker exit event and drop the state log immediately
            StateSerializer.dump_session(session, reason=str(exc))
            raise exc
