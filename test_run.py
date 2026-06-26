import time

from pydantic import BaseModel

from aegisagent.budget import AgentSession
from aegisagent.schema import schema_gate
from aegisagent.workflow import Workflow


class CargoInvoice(BaseModel):
    id: str
    charge: float


# Node 1: A successful schema step (Probabilistic -> Deterministic coercion)
@schema_gate(response_schema=CargoInvoice)
def extraction_node(raw_input: str, session: AgentSession) -> str:
    print(f"-> Node processing raw payload... Content size: {len(raw_input)}")
    # Simulate an LLM call that consumes budget resources
    session.record_llm_call(model="gpt-4o", prompt_tokens=1000, completion_tokens=500)

    # Returns raw text containing a valid JSON segment
    return '```json {"id": "INV-100", "charge": 450.00} ```'


# Node 2: A faulty loop node that forces a runaway budget overflow crash
def processing_loop_node(validated_invoice: CargoInvoice, session: AgentSession):
    print(f"-> Verification Node processing invoice ID: {validated_invoice.id}")

    # Simulating a runaway background processing loop
    while True:
        session.increment_iteration()
        session.record_llm_call(
            model="gpt-4o", prompt_tokens=2000, completion_tokens=1000
        )
        time.sleep(0.2)


if __name__ == "__main__":
    # Create an integrated workflow with a tight $0.04 resource ceiling
    flow = Workflow(max_cost_usd=0.04, max_iterations=5)

    flow.add_step(extraction_node)
    flow.add_step(processing_loop_node)

    try:
        raw_email = "The shipping charge for items is listed inside."
        flow.execute(initial_input=raw_email)
    except SystemExit:
        print("\nWorkflow runtime halted cleanly. Inspecting workspace...")
