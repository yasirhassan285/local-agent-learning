from ollama import chat
from tools import APPROVAL_REQUIRED, TOOLS, TOOL_REGISTRY


def request_approval(tool_name:str, arguments: dict) ->bool:
    """Ask the user before executing the tool"""

    print("\n ____APPROVAL REQUIRED_____")
    print(f"Tool:{tool_name}")
    print("Arguments:")

    for name, value in arguments.items():
        print(f"{name}:{value}")
    while True:
        answer = input("\n Execute this tool?[y/n]:").strip().lower()

        if answer in {"y", "yes"}:
            return True

        if answer in {"n", "no"}:
            return False
        print("Please enter y or n")


messages = [
    {
        "role": "system",
        "content": (
            "You are a concise programming assistant working with a local project."
            "Use the available tools when information about the current project is required. "
            "Do not invent file contents, filenames, calculation results, or tool results."
            "If a tool fails or action is denied, explain that clearly rather than"
            "pretending the action succeeded"
        ),
    }
]

while True:
    user_input = input("You: ").strip()

    if not user_input:
        continue

    if user_input.lower() in {"exit", "quit"}:
        print("Salam.")
        break

    messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    MAX_TOOL_ROUNDS = 8

    if _ in range(MAX_TOOL_ROUNDS):
        
        response = chat(
            model="qwen3:8b",
            messages=messages,
            tools=TOOLS,
            options={
                "temperature":0.2,
            },
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

            if tool_name not in TOOL_REGISTRY:
                result = f"Error: unknown tool {tool_name}"

            elif not isinstance(arguments, dict):
                    result = "Tool error: arguments must be a dictionary"

            else:
                tool_function = TOOL_REGISTRY[tool_name]

                approved = True

                if tool_name in APPROVAL_REQUIRED:
                    approved = request_approval(tool_name, arguments)

                if not approved:
                    result ="Tool execution denied by the user"

                else:
                    try:
                        result = tool_function(**arguments)
                    except TypeError as error:
                        result = f"Tool argument error: {error}"
                    except Exception as error: 
                        result = f"Tool error: {error}"

            result=str(result)
            MAX_TOOL_RESULT_LENGTH = 10_000
            if len(result)>MAX_TOOL_RESULT_LENGTH:
                result =(
                    result[:MAX_TOOL_RESULT_LENGTH]
                    +
                    "\n...[tool result truncated]"
                )

            messages.append(
                {
                    "role": "tool",
                    "tool_name": tool_name,
                    "content": str(result),
                }
            )
    else:
        print("\n Assistant: Stopped because the tool call limit was reached")