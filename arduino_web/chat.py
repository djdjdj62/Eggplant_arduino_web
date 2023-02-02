import os
import openai

def chat_gpt(chat_data):
  openai.api_key = "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"

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
  #print(response["choices"][0]["text"])
  return response["choices"][0]["text"]
