import asyncio

from langchain.agents import create_agent
from langchain.mcp import MCPAdapter
from langchain_ollama import ChatOllama

from tools import list_project_files


async def main():
    model = ChatOllama(
        model="qwen3:8b",
        temperature=0.2,
    )

    config = {
        "mcpServers": {
            "math": {
                "command": "python",
                "args": ["math_mcp_server.py"],
            },
            "text": {
                "command": "python",
                "args": ["text_mcp_server.py"],
            },
        }
    }

    async with MCPAdapter(config) as adapter:
        mcp_tools = await adapter.list_tools()

        tools = [
            list_project_files,
            *mcp_tools,
        ]

        print("Available tools:")

        for tool in tools:
            name = getattr(tool, "name", None) or getattr(tool, "__name__", "Unknown")
            print(f"- {name}")
            
        agent = create_agent(
            model=model,
            tools=tools,
            system_prompt=(
                "You are a concise assistant. "
                "Use tools when appropriate."
            ),
        )

        while True:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in {"exit", "quit"}:
                break

            result = await agent.ainvoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": user_input,
                        }
                    ]
                }
            )

            print(
                f"\nAssistant: "
                f"{result['messages'][-1].content}\n"
            )


asyncio.run(main())