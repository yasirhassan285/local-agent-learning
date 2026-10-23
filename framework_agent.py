from langchain.agents import create_agent
from langchain_ollama import ChatOllama
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

from tools import (
    calculate,
    list_project_files,
    read_text_file,
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
    ],
    system_prompt=(
        "You are a concise programming assistant working with a local project. "
        "Use tools when current project information is required. "
        "Do not invent file contents or calculation results."
    ),
    checkpointer=checkpointer,
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

    print(f"\nAssistant: {result['messages'][-1].content}\n")