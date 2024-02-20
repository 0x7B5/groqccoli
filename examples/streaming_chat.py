from groqccoli import Client

groq_client = Client()

while True:

    query = input("Query (type 'exit' to quit): ")

    if query == "exit":
        break

    with groq_client.create_streaming_chat(
        query,
        model_id="llama2-70b-4096",
    ) as response:
        for line in response:
            if line:
                print(line, end="")
    print()
