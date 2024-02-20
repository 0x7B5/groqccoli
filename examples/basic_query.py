from groqccoli import Client

groq_client = Client()
chat = groq_client.create_chat("What is the meaning of life?")
print(chat.content)
