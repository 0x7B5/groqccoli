# Groqccoli 
An unoffical Python client for the Groq API. No API key needed.

## Installation 
You can install the package with pip and git 
```bash
pip install git+https://github.com/0x7B5/groqccoli
```

## Basic Usage 
You can import the groqccoli class and use the client like this (it uses mixtral-8x7b-32768 by default). 

```python
from groqccoli import Client

groq_client = Client()
chat = groq_client.create_chat("What is the meaning of life?")
print(chat.content)
```

## Advanced Usage 
If you want to pass additional parameters or use a different model (right now only mixtral-8x7b-32768 and llama2-70b-4096 are supported) you can. 

```python
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
```

### Streaming 
Groqccoli also supports streaming out of the box so you don't have to wait for the full response to process. 

```python
from groqccoli import Client
groq_client = Client()

while True:
    query = input("Query (type 'exit' to quit): ")

    with groq_client.create_streaming_chat(
        query,
        model_id="llama2-70b-4096",
    ) as response:
        for line in response:
            if line:
                print(line, end="")
    print()
```

### Proxies 
Probably a good idea to use proxies with groqccoli.

```python
from groqccoli import Client

groq_client = Client(proxies={"http": 127.0.0, "https": 127.0.0})
chat = groq_client.create_chat(
    "What is the meaning of life?",
    model_id="llama2-70b-4096")

print(chat)
```


See /examples for more code samples. 

## Authors

- **Vlad Munteanu**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details

## Questions

If you have any questions about this repository, or any others of mine, please
don't hesitate to contact me.