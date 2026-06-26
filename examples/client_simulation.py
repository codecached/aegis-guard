import time

from pydantic import BaseModel, Field

from aegisagent.schema import schema_gate
from aegisagent.workflow import Workflow


# 1. Define the Client's Business Data Contract
class FreightInvoice(BaseModel):
    carrier_name: str = Field(description="Name of the shipping company")
    invoice_number: str
    fuel_surcharge: float
    base_rate: float
    total_amount: float


# 2. Simulate Client App Steps (Nodes)
@schema_gate(response_schema=FreightInvoice)
def raw_email_ingestion_agent(email_body: str, session) -> str:
    print("\n[Client App] Agent reading raw inbound email text...")

    # Simulate an LLM call parsing the email (Consumes budget)
    session.record_llm_call(model="gpt-4o", prompt_tokens=1500, completion_tokens=800)

    # Simulating a successful extraction output containing a markdown JSON block
    return """
    Processed email. Here is the extracted invoice data layout:
    ```json
    {
        "carrier_name": "FedEx Supply Chain",
        "invoice_number": "FDX-2026-891A",
        "fuel_surcharge": 120.50,
        "base_rate": 850.00,
        "total_amount": 970.50
    }
    ```
    """

def deterministic_financial_audit(invoice: FreightInvoice, session) -> FreightInvoice:
    print("\n[Client App] Running strict auditing calculations...")

    # Hardcoded calculation verification (Pure deterministic logic)
    expected_total = invoice.base_rate + invoice.fuel_surcharge
    if invoice.total_amount != expected_total:
        print(f"[CRITICAL WARNING] Math mismatch! Expected {expected_total}")
    else:
        print("[SUCCESS] Invoice math verified perfectly.")

    return invoice

def rogue_autonomous_reconciliation_loop(invoice: FreightInvoice, session):
    print("\n[Client App] Launching autonomous payment reconciliation handler...")
    print("[SYSTEM] Simulated connection error occurred. Agent attempting auto-retry...")

    # Simulating a rogue agent loop trying to bypass the connection error
    while True:
        session.increment_iteration()
        # High token cost loop simulating a model generating continuous reasoning strings
        session.record_llm_call(model="gpt-4o", prompt_tokens=3000, completion_tokens=1500)
        time.sleep(0.1)


# 3. Main Client Application Execution Entry
if __name__ == "__main__":
    print("=" * 60)
    print("STARTING CLIENT APPLICATION SIMULATION: FREIGHT AUDIT SYSTEM")
    print("=" * 60)

    # Instantiate the workflow with an enterprise protection envelope
    # Hard resource constraint: Max $0.05 spend ceiling or 4 loop iterations
    freight_workflow = Workflow(max_cost_usd=0.05, max_iterations=4)

    # Build the processing pipeline
    freight_workflow.add_step(raw_email_ingestion_agent)
    freight_workflow.add_step(deterministic_financial_audit)
    freight_workflow.add_step(rogue_autonomous_reconciliation_loop)

    # Mock unstructured incoming data payload
    mock_customer_email = "Hey team, attached is the invoice FDX-2026-891A for our base rate of 850."

    try:
        freight_workflow.execute(initial_input=mock_customer_email)
    except SystemExit:
        print("\n" + "=" * 60)
        print("CLIENT SIMULATION PROTECTED: Runaway bill blocked successfully.")
        print("=" * 60)
