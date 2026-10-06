from pathlib import Path    
from ollama import chat

def list_project_files() -> str:
    """
    List files and directories in the current project directory.

    Returns:
        A newline-separated list of files and directories.
    """
    items = []

    for path in Path(".").iterdir():
        if path.name in {".venv", ".git"}:
            continue

        items.append(path.name)

    return "\n".join(sorted(items))

def read_text_file(filename: str) -> str:
    """
    Read a text file from the current project directory.

    Args:
        filename: Name of the file to read.

    Returns:
        The contents of the file.
    """
    path = Path(filename)

    if not path.exists():
        return f"Error: {filename} does not exist."

    if not path.is_file():
        return f"Error: {filename} is not a file."

    return path.read_text()

tools = [
    list_project_files,
    read_text_file,
]

tool_registry = {
    "list_project_files": list_project_files,
    "read_text_file": read_text_file,
}

messages = [
    {
        "role": "system",
        "content": (
            "You are a programming assistant. "
            "Use the available tools when needed. "
            "Do not invent file contents or project state."
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

    while True:
        response = chat(
            model="qwen3:8b",
            messages=messages,
            tools=tools,
        )

        messages.append(response.message)

        if not response.message.tool_calls:
            print(f"\nAssistant: {response.message.content}\n")
            break

        for tool_call in response.message.tool_calls:
            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments

            print(f"\nTool requested: {tool_name}")
            print(f"Arguments: {arguments}")

            if tool_name not in tool_registry:
                result = f"Error: unknown tool {tool_name}"
            else:
                tool_function = tool_registry[tool_name]

                try:
                    result = tool_function(**arguments)
                except Exception as error:
                    result = f"Tool error: {error}"

            print(f"Tool result:\n{result}\n")

            messages.append(
                {
                    "role": "tool",
                    "tool_name": tool_name,
                    "content": str(result),
                }
            )