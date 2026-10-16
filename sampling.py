from ollama import chat


prompt = """
You have these tools:

- read_text_file(filename)
- write_text_file(filename, content)
- calculate(operation, a, b)

The user asks:
"What Python packages are listed in requirements.txt?"

Briefly explain what action you would take first.
"""


temperatures = [
    0.0,
    0.2,
    0.8,
    1.5,
]


for temperature in temperatures:
    print(f"\n--- Temperature: {temperature} ---")

    response = chat(
        model="qwen3:8b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        options={
            "temperature": temperature,
        },
    )

    print(response.message.content)