import ollama

response = ollama.chat(model='llama3',
                       keep_alive=-1,
                       messages=[
  {
    'role': 'user',
    'content': """
    show me the time not available
    1:00 available
    2:00 Booked
    3:00 available
    4:00 available
    5:00 available
""",
  },
])
print(response['message']['content'])