
#import ollama function 'chat' to comminucate with our model
from ollama import chat

#send request to local ollama service
response = chat(
	model ="qwen3:8b",	#select which local model should handle the request
	messages=[
		   {
		"role": "system", #Tell model what's it's role
		"content": (
			"you are a programming tutor"
			"Explain technical concepts clearly and concisely"
			   ),
		   },
		{
		"role":"user",   #what user wants to ask
		"content": (
			"Explain what a python virtual environment is"
			"in three sentences"
			 ),
		},
		],
		)

print(response.message.content)
