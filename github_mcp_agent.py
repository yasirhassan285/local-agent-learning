import asyncio
import os

from fastmcp import Client
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver




async def main():
    token = os.environ["GITHUB_PAT"]

    client = Client(
        "https://api.githubcopilot.com/mcp/readonly",
        auth=token,
    )

    model = ChatOllama(
        model="qwen3:8b",
        temperature=0.2,
    )

    async with MCPAdapter(client) as adapter:
        tools = await adapter.list_tools()

        print("GitHub tools discovered:")

        for tool in tools:
            print(f"- {tool.name}")

        checkpointer = InMemorySaver()
        
        agent = create_agent(
            model=model,
            tools=tools,
            system_prompt=(
                "You are a concise GitHub repository assistant. "
                "Use GitHub tools when repository information is required. "
                "Do not invent repository state."
            ),
            checkpointer = checkpointer,
        )

        config = {
            "configurable":{
                "thread_id":"github-agent-1"
            }
        }

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
                },
                config,
            )

            print(
                f"\nAssistant: "
                f"{result['messages'][-1].content}\n"
            )


asyncio.run(main())