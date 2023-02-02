import os
import openai

openai.api_key = "sk-"+"yfCjXJoJXgjUX2LqMB5MT3BlbkFJh5Y81yB0Rph7qKUhJ9G9"

aa = "聊天講一個笑話"

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

response = openai.Completion.create(
  model="text-davinci-003",
  prompt="\nHuman:"+aa[2:]+"\nAI:",
  temperature=0.9,
  max_tokens=100,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0.6,
  stop=[" Human:", " AI:"]
)
print(response["choices"][0]["text"])
