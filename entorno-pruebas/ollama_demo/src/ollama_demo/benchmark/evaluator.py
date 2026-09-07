import time
import ollama


def benchmark_prompt(
    model_name: str, prompt: str, system_prompt: str | None = None
) -> dict:
    """Run a prompt against a model and measure response metrics."""
    messages = []
    if system_prompt:
        messages.append({'role': 'system', 'content': system_prompt})
    messages.append({'role': 'user', 'content': prompt})

    start_time = time.perf_counter()

    # Call Ollama API
    response = ollama.chat(
        model=model_name,
        messages=messages,
    )

    end_time = time.perf_counter()

    # Extract performance metrics returned directly by Ollama API (in nanoseconds)
    total_duration_sec = (end_time - start_time)
    eval_count = response.get('eval_count', 0)  # Total tokens generated
    eval_duration_ns = response.get('eval_duration', 0)

    tokens_per_second = (
        (eval_count / (eval_duration_ns / 1e9)) if eval_duration_ns > 0 else 0.0
    )

    return {
        'model': model_name,
        'total_time_sec': round(total_duration_sec, 2),
        'eval_tokens': eval_count,
        'tokens_per_second': round(tokens_per_second, 2),
        'response_content': response['message']['content'],
    }


def compare_models(
    models: list[str], prompt: str, system_prompt: str | None = None
) -> list[dict]:
    """Execute the same benchmark prompt across multiple local models."""
    results = []
    print(f"\n==========================================")
    print(f"RUNNING BENCHMARK ACROSS MODELS")
    print(f"==========================================\n")

    for model in models:
        print(f"Benchmarking model: '{model}'...")
        try:
            metrics = benchmark_prompt(model, prompt, system_prompt)
            results.append(metrics)
            print(f" -> Completed in {metrics['total_time_sec']}s "
                  f"({metrics['tokens_per_second']} tok/s)")
        except Exception as e:
            print(f" -> Failed to run model '{model}': {e}")

    return results