from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from langgraph_swarm import create_handoff_tool, create_swarm

from tools import (
    calculate,
    list_project_files,
    read_text_file,
)

model= ChatOllama(
    model="qwen3:8b",
    temperature=0.2,
)

transfer_to_math = create_handoff_tool(
    agent_name="math_agent",
)

transfer_to_research = create_handoff_tool(
    agent_name ="research_agent",
)

research_agent = create_agent(
    model=model,
    tools=[
        list_project_files,
        read_text_file,
        transfer_to_math,
    ],
    name="research_agent",
    system_prompt=(
        "You are the research agent."
        "Your job is to inspect project and answer questions about them."
        "If the task primarily requires arithmetic, handoff to math_agent"
    ),
)

math_agent= create_agent(
    model=model,
    tools= [
        calculate,
        transfer_to_research,
    ],
    name= "math_agent",
    system_prompt=(
        "You are the math agent."
        "Your job is to perform calcualtions using the calculator tool."
        "If information must be obtained from the project files,"
        "hand off to research agent"
    ),
)

workflow = create_swarm(
    [
        research_agent,
        math_agent,
    ],
    default_active_agent ="research_agent",
)

checkpointer = InMemorySaver()

app = workflow.compile(
    checkpointer=checkpointer,
    )

config = {
    "configurable": {
        "thread_id": "multi-agent-1"
    }
}

while True:
    user_input = input("You: ").strip()

    if not user_input:
        continue

    if user_input.lower() in {"salam", "Allah Hafiz"}:
        break

    result = app.invoke(
        {
            "messages":[
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        },
        config
    )

    print(f"\n Assistant:{result['messages'][-1].content}\n")

