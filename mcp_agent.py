import asyncio
from pathlib import Path

from langchain.agents import create_agent
from langchain.mcp import MCPAdapter
from langchain_ollama import ChatOllama


async def main():
    model = ChatOllama(
        model="qwen3:8b",
        temperature=0.2,
    )

    server_path = Path("math_mcp_server.py").resolve()

    async with MCPAdapter(server_path) as adapter:
        tools = await adapter.list_tools()

        print("Discovered tools:")
        for tool in tools:
            print(f"- {tool.name}")

        agent = create_agent(
            model=model,
            tools=tools,
            system_prompt=(
                "You are a concise math assistant. "
                "Use the available tools for calculations."
            ),
        )

        result = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": "What is 37 multiplied by 19?",
                    }
                ]
            }
        )

        print("\nAssistant:")
        print(result["messages"][-1].content)


asyncio.run(main())