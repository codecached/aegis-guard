"""
AegisAgent Core Framework
Developed by AI Knights (codecached)
Founding Architect: Srinivasan Panneer

Secure, Deterministic Safety Layer for Autonomous AI Agents.
Distributed under the MIT License. Copyright (c) 2026 AI Knights.
"""

import json
import re
from collections.abc import Callable
from functools import wraps
from typing import Any

from pydantic import BaseModel, ValidationError


class SchemaValidationError(Exception):
    """Custom exception raised when AI output cannot be coerced into the schema."""

    pass


def _extract_json_block(text: str) -> str:
    """Helper to extract a clean JSON substring from chaotic AI conversational text."""
    # Look for standard markdown code blocks containing json or raw braces
    json_match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if json_match:
        return json_match.group(1).strip()

    # Fallback: attempt to find the first open brace and last closing brace
    brace_match = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
    if brace_match:
        return brace_match.group(1).strip()

    return text.strip()


def schema_gate(response_schema: type[BaseModel]):
    """Decorator to enforce strict data contracts on probabilistic AI outputs."""

    def decorator(func: Callable[..., str]):
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> BaseModel:
            # 1. Execute the agent function to get the raw text output
            raw_ai_text = func(*args, **kwargs)

            # 2. Extract potential JSON content from the raw string
            cleaned_json_str = _extract_json_block(raw_ai_text)

            try:
                # 3. Parse string into a Python dictionary
                parsed_data = json.loads(cleaned_json_str)

                # 4. Enforce structural validation via Pydantic model parsing
                validated_object = response_schema.model_validate(parsed_data)
                return validated_object

            except (json.JSONDecodeError, ValidationError) as err:
                print("\n[AegisAgent - CRITICAL] Schema Gate Intercepted Failure!")
                print("-" * 60)
                print(f"Target Schema: {response_schema.__name__}")
                print(f"Raw AI Input Received:\n{raw_ai_text}")
                print(f"Validation Error Specifics:\n{err}")
                print("-" * 60)

                # Deterministically halt process flow instead of passing corrupted data downstream
                raise SchemaValidationError(
                    f"AI response failed validation for contract '{response_schema.__name__}'."
                )

        return wrapper

    return decorator
