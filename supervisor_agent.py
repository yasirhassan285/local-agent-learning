from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from langgraph_supervisor import create_supervisor

from tools import (
    calculate,
    list_project_files,
    read_text_file,
)


model = ChatOllama(
    model="qwen3:8b",
    temperature=0.2,
)

research_agent = create_agent(
    model=model,
    tools=[
        list_project_files,
        read_text_file,
    ],
    name="research_agent",
    system_prompt=(
        "You are a project research specialist. "
        "Inspect project files when needed. "
        "Do not perform arithmetic yourself."
    ),
)

math_agent = create_agent(
    model=model,
    tools=[
        calculate,
    ],
    name="math_agent",
    system_prompt=(
        "You are a math specialist. "
        "Use the calculator tool for arithmetic."
    ),
)

workflow = create_supervisor(
    [
        research_agent,
        math_agent,
    ],
    model=model,
    prompt=(
        "Your are the supervisor of the two specialist agents."
        "Use research_agent for tasks involving project files."
        "use math_agent for arithmetic."
        "Delegate to specialists rather than doing their work yourself."
    ),
)

checkpointer= InMemorySaver()

app = workflow.compile(
    checkpointer=checkpointer,
)

config = {
    "configurable": {
        "thread_id": "supervisor-1"
    }
}


while True:
    user_input = input("You: ").strip()

    if not user_input:
        continue

    if user_input.lower() in {"exit", "quit"}:
        break

    result = app.invoke(
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