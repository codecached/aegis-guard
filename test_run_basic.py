from pydantic import BaseModel, Field

from aegisagent.schema import SchemaValidationError, schema_gate


# Define a strict financial schema requirement
class CorporateInvoice(BaseModel):
    invoice_id: str
    total_amount: float = Field(description="Must be a valid numerical dollar float")


# 1. Simulate a SUCCESSFUL schema extraction task
@schema_gate(response_schema=CorporateInvoice)
def successful_agent_task():
    # Simulates an AI that wraps its structured answer inside natural conversational text
    return """Sure, I found that data for you! 
    ```json
    {
        "invoice_id": "INV-2026-XYZ",
        "total_amount": 1450.75
    }
    ```
    Let me know if you need anything else!"""


# 2. Simulate a FAILING schema extraction task (Missing fields/Wrong types)
@schema_gate(response_schema=CorporateInvoice)
def chaotic_failing_agent_task():
    # Simulates a malfunctioning AI that hallucinates string descriptions instead of structured data
    return "The invoice id is unknown, and the billing amount is currently empty or pending."


if __name__ == "__main__":
    print("--- SCENARIO 1: SUCCESSFUL SCHEMA INTERCEPTION ---")
    data = successful_agent_task()
    print(f"Success! Validated Object: {data}")
    print(f"Accessing typed attributes: ID={data.invoice_id}, Amount=${data.total_amount}\n")

    print("--- SCENARIO 2: FAILING SCHEMA INTERCEPTION ---")
    try:
        chaotic_failing_agent_task()
    except SchemaValidationError as ex:
        print(f"Python caught expected deterministic block: {ex}")
