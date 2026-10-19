from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from tools import (
    calculate,
    list_project_files,
    read_text_file,
)


model = ChatOllama(
    model="qwen3:8b",
    temperature=0.2,
)


agent = create_agent(
    model=model,
    tools=[calculate,
           list_project_files,
            read_text_file,
            ],
    system_prompt=(
        "You are a concise programming assistant working with a local project. "
        "Use tools when current project information is required. "
        "Do not invent file contents or calculation results."
    ),
)


result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "calculate 847 divided by 17",
            }
        ]
    }
)


print(result["messages"][-1].content)