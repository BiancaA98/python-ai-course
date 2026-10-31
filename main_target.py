import json
import os
import subprocess
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError


class RunTests(BaseModel):
    """Run the project's pytest suite."""

    tests: list[str] = Field(
        default_factory=list,
        description="Optional pytest test paths or node IDs, for example tests/test_validations.py::test_name.",
    )


def run_tests(args: dict) -> str:
    try:
        request = RunTests.model_validate(args)
        if any(not test or test.startswith("-") for test in request.tests):
            return "error: tests must be pytest paths or node IDs, not options"

        result = subprocess.run(
            ["uv", "run", "pytest", *request.tests],
            cwd=Path.cwd(),
            capture_output=True,
            text=True,
            timeout=60,
        )
        return (result.stdout or "") + (result.stderr or "")
    except (ValidationError, subprocess.TimeoutExpired, FileNotFoundError) as error:
        return f"error: {error}"


def complete(client: OpenAI, messages: list[dict], tools: list[dict]):
    return client.chat.completions.create(
        model=os.environ["OPEN_ROUTER_MODEL_NAME"],
        messages=messages,
        tools=tools,
        tool_choice="auto",
    ).choices[0].message


def main() -> None:
    load_dotenv()
    if not os.getenv("OPEN_ROUTER_API_KEY") or not os.getenv("OPEN_ROUTER_MODEL_NAME"):
        raise RuntimeError("Set OPEN_ROUTER_API_KEY and OPEN_ROUTER_MODEL_NAME in .env")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ["OPEN_ROUTER_API_KEY"],
    )
    messages = [{"role": "system", "content": "Use run_tests when asked to run tests."}]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "run_tests",
                "description": "Run uv run pytest, optionally for specific pytest paths or node IDs.",
                "parameters": RunTests.model_json_schema(),
            },
        }
    ]

    while True:
        messages.append({"role": "user", "content": input("you> ")})
        response = complete(client, messages, tools)
        messages.append(response.model_dump(exclude_none=True))

        for tool_call in response.tool_calls or []:
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": run_tests(json.loads(tool_call.function.arguments)),
                }
            )

        if response.tool_calls:
            response = complete(client, messages, tools)
            messages.append(response.model_dump(exclude_none=True))

        print("agent>", response.content)


if __name__ == "__main__":
    main()
