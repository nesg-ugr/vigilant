import ollama


def send_message(model_name: str, prompt: str) -> str:
    """Send a single prompt and return the full text response."""
    response = ollama.chat(
        model=model_name,
        messages=[{'role': 'user', 'content': prompt}],
    )
    return response['message']['content']


def send_message_stream(model_name: str, prompt: str) -> None:
    """Send a prompt and stream the response directly to stdout."""
    print(f"--- Model ({model_name}) Response ---")
    stream = ollama.chat(
        model=model_name,
        messages=[{'role': 'user', 'content': prompt}],
        stream=True,
    )
    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)
    print("\n")