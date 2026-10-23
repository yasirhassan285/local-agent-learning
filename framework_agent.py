from langchain.agents import create_agent
from langchain_ollama import ChatOllama
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.types import Command

from tools import (
    calculate,
    list_project_files,
    read_text_file,
    create_text_file,
)


model = ChatOllama(
    model="qwen3:8b",
    temperature=0.2,
)


connection = sqlite3.connect(
    "checkpoints.sqlite",
    check_same_thread=False,
)

checkpointer=SqliteSaver(connection)


agent = create_agent(
    model=model,
    tools=[
        calculate,
        list_project_files,
        read_text_file,
        create_text_file,
    ],
    system_prompt=(
        "You are a concise programming assistant working with a local project. "
        "Use tools when current project information is required. "
        "Do not invent file contents or calculation results."
    ),
    checkpointer=checkpointer,
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "create_text_file":True,
            }
        )
    ],
)

config = {
    "configurable": {
        "thread_id": "conversation-1"
    }
}


while True:
    user_input = input("You: ").strip()

    if not user_input:
        continue

    if user_input.lower() in {"exit", "quit"}:
        break

    result = agent.invoke(
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

    if "__interrupt__" in result:
        interrupt = result["__interrupt__"][0]

        print("\n--- APPROVAL REQUIRED ---")
        print(interrupt.value)

        decision = input("Approve? [y/n]: ").strip().lower()

        if decision in {"y", "yes"}:
            resume_value = {
                "decisions": [
                    {
                        "type": "approve"
                    }
                ]
            }
        else:
            resume_value = {
                "decisions": [
                    {
                        "type": "reject",
                        "message": "User rejected the action."
                    }
                ]
            }

        result = agent.invoke(
            Command(resume=resume_value),
            config,
        )

    print(f"\nAssistant: {result['messages'][-1].content}\n")