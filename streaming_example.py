from ollama import chat

stream=chat(
    model="qwen3:8b",
    messages=[
        {
            "role":"user",
            "content": "Explain recursion briefly",
        }
    ],
    stream=True,
)

for chunk in stream:
    print(chunk.message.content, end="", flush=True)
print()