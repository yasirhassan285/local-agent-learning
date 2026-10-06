from pathlib import Path

from ollama import chat


def list_project_files() -> str:
    """
    List the files and directories in the current project directory.

    Returns:
        A newline-separated list of files and directories.
    """
    items = []

    for path in Path(".").iterdir():
        if path.name in {".venv", ".git"}:
            continue

        items.append(path.name)

    return "\n".join(sorted(items))


messages = [
    {
        "role": "system",
        "content": (
            "You are a programming assistant. "
            "Use the available tools when they are needed to answer accurately."
        ),
    }
]


while True:
    user_input = input("You: ").strip()

    if not user_input:
        continue

    if user_input.lower() in {"exit", "quit"}:
        print("Goodbye.")
        break

    messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    response = chat(
        model="qwen3:8b",
        messages=messages,
        tools=[list_project_files],
    )

    print("\nDEBUG:")
    print("Content:", response.message.content)
    print("Tool calls:", response.message.tool_calls)
    print()

    messages.append(response.message)

    if response.message.tool_calls:
        tool_call = response.message.tool_calls[0]

        if tool_call.function.name == "list_project_files":
            result = list_project_files()

            print("Tool executed: list_project_files")
            print("Tool result:")
            print(result)
            print()

            messages.append(
                {
                    "role": "tool",
                    "tool_name": "list_project_files",
                    "content": result,
                }
            )

            final_response = chat(
                model="qwen3:8b",
                messages=messages,
                tools=[list_project_files],
            )

            print(f"Assistant: {final_response.message.content}\n")

            messages.append(final_response.message)

    else:
        print(f"Assistant: {response.message.content}\n")