import ollama


def pull_model(model_name: str) -> None:
    """Download a model with a real-time progress indicator."""
    print(f"Pulling model '{model_name}'...")
    for progress in ollama.pull(model_name, stream=True):
        status = progress.get('status', '')
        completed = progress.get('completed') or 0
        total = progress.get('total')

        if total and total > 0:
            percentage = (completed / total) * 100
            print(f"\r{status}: {percentage:.1f}%", end='', flush=True)
        else:
            print(f"\r{status}", end='', flush=True)
    print("\nDownload complete!\n")


def list_installed_models() -> list[str]:
    """Retrieve a list of available local model names."""
    response = ollama.list()
    return [model.model for model in response.models]


def is_model_available(model_name: str) -> bool:
    """Check if a specific model is installed locally."""
    available_models = list_installed_models()
    return any(model_name in m for m in available_models)