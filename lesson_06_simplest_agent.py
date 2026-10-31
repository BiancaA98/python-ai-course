import os
import subprocess
import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ConfigDict, Field, ValidationError


# variabila statica
PROJECT_ROOT = Path(__file__).resolve().parent


class FileNameValidator(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(description="Name of the text file in this project.")


class FileSummaryValidator(BaseModel):
    """This validator can validate the output of an agent, the JSON returned by the summary agent."""

    model_config = ConfigDict(extra="forbid")

    title: str = Field(description="The generated title for the file")
    summary: str = Field(description="The summary for that file.")


class DocAnalysisRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    file_name: str = Field(description="Name of the text file in this project.")
    words: list[str] = Field(description="Words to count in the given file.")


class DocAnalysisReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    file_name: str
    word_count: int
    matches: dict[str, int]


def analyze_document(args: dict):
    try:
        request = DocAnalysisRequest.model_validate(args)
        file_name = request.file_name
        words = request.words

        # open a file. find how many times a word occurs in the file.
        p = (PROJECT_ROOT / file_name).resolve()
        p.relative_to(PROJECT_ROOT)

        if not p.is_file():
            return f"error: {file_name} is not a file!"

        text = p.read_text(encoding="utf-8")
        split_document = text.lower().replace(".", " ").split()
        matches = {}

        for word in words:
            count = split_document.count(word)
            matches[word] = count

        report = DocAnalysisReport(
            file_name=file_name,
            matches=matches,
            word_count=len(split_document)
        )

        return report.model_dump_json()
    except (ValidationError, ValueError, OSError) as error:
        return f"error: {error}"


# starts a new agent and summarizes a file
def summarize_file(client: OpenAI, args: dict) -> str:
    try:
        req = FileNameValidator.model_validate(args)
        path = (PROJECT_ROOT / req.name).resolve()
        path.relative_to(PROJECT_ROOT)
        if not path.is_file():
            return f"error: {req.name!r} is not a file in this project"
        text = path.read_text(encoding="utf-8")

        # starts our agent.
        response = client.chat.completions.create(
            model=os.getenv("OPEN_ROUTER_MODEL_NAME"),
            messages=[
                {"role": "system", "content": "Return ONLY JSON, that contains a title and a short summary. Summarise the file you received, and put it in the JSON response."},
                {"role": "user", "content": f"Please summarize this file for me: {text}"},
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "file_summary",
                    "schema": FileSummaryValidator.model_json_schema(),
                    "strict": True,
                },
            },
        ).choices[0].message
        validated_model_json = FileSummaryValidator.model_validate_json(response.content)
        return validated_model_json.model_dump_json()
    except (OSError, ValidationError, ValueError) as error:
        return f"error: {error}"


def run_tests() -> str:
    try:
        result = subprocess.run(
            ["uv", "run", "pytest"],
            cwd=Path.cwd(),
            capture_output=True,
            text=True,
            timeout=60
        )
        return (result.stdout or "No output.") + "" + (result.stderr or "")
    except Exception as e:
        print(e)

def complete(client: OpenAI, messages: list[dict], tools: list[dict]):
    response = client.chat.completions.create(
        messages=messages,
        model=os.getenv("OPEN_ROUTER_MODEL_NAME"),
        tools=tools,
        tool_choice="auto"
    ).choices[0].message
    return response

# avem agentul. trebuie sa-i dam instructiuni despre cum sa ruleze o unealta oferita de noi.

def main():
    load_dotenv()

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPEN_ROUTER_API_KEY")
    )

    # aici o sa definim lista de tools pentru agent.
    tools = [
        {
            "type": "function",
            "function": {
                "name": "run_tests",
                "description": "Run uv run pytest."
            }
        },
        {
            "type": "function",
            "function": {
                "name": "summarize_file",
                "description": "Reads and summarizes a text file in the current project, as JSON output.",
                "parameters": FileNameValidator.model_json_schema()
            }
        },
        {
            "type": "function",
            "function": {
                "name": "analyze_document",
                "description": "Counts words and requested word matches in a text file in the current project, as JSON output.",
                "parameters": DocAnalysisRequest.model_json_schema()
            }
        }
    ]

    messages = []
    # system prompt.
    messages.append({
        "role": "system",
        "content": "You are a helpful assistant. If the user asks to run some tests, please only run the run_tests tool that you have at your disposal. If instead, the user asks to summarize a file, use the provided summarize_file tool that you have. If the user asks to analyze a file or count words in a file, use the provided analyze_document tool that you have."
    })
    while True:
        inp = input("you> ")
        if inp == "quit":
            break
        messages.append({
            "role": "user",
            "content": inp
        })

        # ii cerem agentului sa ne raspunda la un mesaj.
        response = complete(client, messages, tools)
        messages.append(response.model_dump(exclude_none=True))

        if response.tool_calls:
            for tool_call in response.tool_calls:
                tool_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                if tool_name == "summarize_file":
                    output = summarize_file(client, args)
                elif tool_name == "run_tests":
                    output = run_tests()
                elif tool_name == "analyze_document":
                    output = analyze_document(args)
                else:
                    output = f"error: unknown tool {tool_name}"

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": output,
                })

            # without this response, the agent can't reply to the user with the proper tool output data.
            response = complete(client, messages, tools)
            messages.append(response.model_dump(exclude_none=True))

        print("agent> ", response)
        print(f"Message count: {len(messages)}")


if __name__ == "__main__":
    main()
    # print(run_tests())
    # load_dotenv()
    #
    # client = OpenAI(
    #     base_url="https://openrouter.ai/api/v1",
    #     api_key=os.getenv("OPEN_ROUTER_API_KEY")
    # )

    # print(summarize_file(client, args={"name": "lesson_06_simplest_agent.py"}))
