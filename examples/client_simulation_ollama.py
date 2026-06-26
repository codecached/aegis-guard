import ollama  # Free, open-source engine
from pydantic import BaseModel, Field

from aegisagent.schema import schema_gate
from aegisagent.workflow import Workflow


# 1. Define the Real Business Schema
class FreightInvoice(BaseModel):
    carrier_name: str = Field(description="Name of the shipping company")
    invoice_number: str
    fuel_surcharge: float
    base_rate: float
    total_amount: float


# 2. Automated Agent Node Intercepting a Free Open-Source Local Model
@schema_gate(response_schema=FreightInvoice)
def live_email_parser_agent(email_body: str, session) -> str:
    print("\n[AegisAgent] Dispatching raw payload to Local Open-Source Engine (Llama 3.2)...")

    # Generate text on your own computer without using cloud credits
    response = ollama.chat(
        model="llama3.2:1b",
        messages=[
            {
                "role": "user",
                "content": f"Extract the invoice details into JSON format. Respond ONLY with valid JSON containing carrier_name, invoice_number, fuel_surcharge, base_rate, total_amount fields. Text: {email_body}",
            }
        ],
    )

    # Intercept token metrics directly from your local hardware execution
    prompt_tokens = response.get("prompt_eval_count", 1000)
    completion_tokens = response.get("eval_count", 500)

    # Pass the real token volumes directly into AegisAgent's deterministic pricing calculator
    session.record_llm_call(
        model="gpt-4o",  # We match token count against a production pricing tier for simulation
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
    )

    return response["message"]["content"]


def business_logic_audit_node(invoice: FreightInvoice, session) -> FreightInvoice:
    print(f"\n[Deterministic Engine] Auditing Invoice ID: {invoice.invoice_number}")
    expected = invoice.base_rate + invoice.fuel_surcharge

    if invoice.total_amount != expected:
        print(f"[REJECTED] Invoice math failure. Expected total calculation matches: {expected}")
    else:
        print("[APPROVED] Financial validation checks passed perfectly.")

    return invoice


# 3. Execution Wrapper Loop
if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING FREE OPEN-SOURCE LOCAL DEVELOPMENT CLIENT SIMULATION")
    print("=" * 60)

    # Set up a strict framework protection envelope
    # Set a tiny budget ($0.02) to trigger an intentional defensive crash demonstration
    pipeline = Workflow(max_cost_usd=0.02, max_iterations=3)
    pipeline.add_step(live_email_parser_agent)
    pipeline.add_step(business_logic_audit_node)

    mock_email = "Invoice FDX-882 received from FedEx. Base fee is 500 dollars plus 60 fuel charge. Total is 560."

    try:
        pipeline.execute(initial_input=mock_email)
    except SystemExit:
        print("\n[PROTECTION ACTIVE] Execution halted cleanly by circuit breaker. Zero dollars wasted.")
