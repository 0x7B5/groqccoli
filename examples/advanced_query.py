from groqccoli import Client

groq_client = Client()
chat = groq_client.create_chat(
    "What is the meaning of life?",
    model_id="llama2-70b-4096",
    max_tokens=4096,
    temperature=0.5,
    max_input_tokens=2048,
)

print(chat)
