import os
import openai

def chat_gpt(chat_data):

  openai.api_key = "sk-"+"yfCjXJoJXg"+"jUX2LqMB5M"+"T3BlbkFJh5"+"Y81yB0Rph"+"7qKUhJ9G9"

  start_sequence = "\nAI:"
  restart_sequence = "\nHuman: "

  response = openai.Completion.create(
    model="text-davinci-003",
    prompt="\nHuman:"+chat_data+"\nAI:",
    temperature=0.9,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
  )
  print(response["choices"][0]["text"])

  return response["choices"][0]["text"]
