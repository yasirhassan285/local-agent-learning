
#import ollama function 'chat' to comminucate with our model
from ollama import chat

                              
messages = [    
    {
        "role": "system",
        "content": (
            "You are a programming tutor. "
            "Explain technical concepts clearly and concisely."
        ),
    }
]


while True:
	user_input = input("You: ").strip()
	if not user_input:						#avoids sending blank messages
		continue

	if user_input.lower() in {"exit", "quit"}:
		print("Goodbye")
		break

	messages.append(
		{
			"role": "user",
			"content": user_input,
		}
	)

	response = chat(
		model= "qwen3:8b",
		messages = messages,
	)

	assistant_message = response.message.content

	print(f"\n Assistant:{assistant_message}\n")

	messages.append(
		{
			"role":assistant_message
		}
	)