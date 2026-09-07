from datetime import datetime
from pathlib import Path

from src.ollama_demo.benchmark.evaluator import compare_models
from src.ollama_demo.core.model_manager import is_model_available, pull_model
from src.ollama_demo.datasets.security_prompts import (
    PROMPT_PCAP_ANALYSIS,
    SYS_CYBERSECURITY_ANALYST,
)

MODELS_TO_TEST = [
    'qwen2.5-coder:7b',   # Especialista en código, logs y análisis técnico
    'deepseek-r1:8b',     # Razonamiento profundo paso a paso
    'llama3.1:8b'         # Modelo generalista fuerte en contexto teórico y marcos de seguridad
]

def prepare_environment() -> None:
    """Ensure all required benchmark models are pulled locally."""
    for model in MODELS_TO_TEST:
        if not is_model_available(model):
            print(f"Model '{model}' is missing.")
            pull_model(model)
        else:
            print(f"Model '{model}' is ready.")


def display_results(results: list[dict]) -> None:
    """Print benchmark comparison results in a formatted summary."""
    print("\n" + "=" * 65)
    print("BENCHMARK SUMMARY RESULTS")
    print("=" * 65)
    print(f"{'Model':<20} | {'Time (s)':<10} | {'Tokens':<8} | {'Speed (tok/s)':<12}")
    print("-" * 65)

    for res in results:
        print(
            f"{res['model']:<20} | "
            f"{res['total_time_sec']:<10} | "
            f"{res['eval_tokens']:<8} | "
            f"{res['tokens_per_second']:<12}"
        )
    print("=" * 65 + "\n")

    if results:
        print(f"--- Sample Analysis Output ({results[0]['model']}) ---")
        print(results[0]['response_content'])


def save_results_to_file(results: list[dict], test_name: str = "ollama_demo") -> None:
    """Save benchmark outputs and metrics to a text file in the 'resultados' directory."""
    # Calcula la ruta: sube 2 niveles desde main.py hasta 'entorno-pruebas'
    project_root = Path(__file__).resolve().parents[1]
    output_dir = project_root / "resultados"
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = output_dir / f"{test_name}.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(file_path, mode="a", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write(f"EJECUCIÓN DE PRUEBA: {timestamp}\n")
        f.write("=" * 80 + "\n\n")

        # Tabla resumen dentro del TXT
        f.write("--- MÉTRICAS DE RENDIMIENTO ---\n")
        f.write(f"{'Model':<20} | {'Time (s)':<10} | {'Tokens':<8} | {'Speed (tok/s)':<12}\n")
        f.write("-" * 60 + "\n")
        for res in results:
            f.write(
                f"{res['model']:<20} | "
                f"{res['total_time_sec']:<10} | "
                f"{res['eval_tokens']:<8} | "
                f"{res['tokens_per_second']:<12}\n"
            )
        f.write("\n" + "-" * 80 + "\n\n")

        # Respuestas detalladas de los modelos
        f.write("--- RESPUESTAS DETALLADAS ---\n\n")
        for res in results:
            f.write(f"=== MODELO: {res['model']} ===\n")
            f.write(f"{res['response_content']}\n\n")
            f.write("-" * 40 + "\n\n")

        f.write("=" * 80 + "\n\n\n")

    print(f"Resultados guardados exitosamente en: {file_path}")


def main() -> None:
    prepare_environment()

    results = compare_models(
        models=MODELS_TO_TEST,
        prompt=PROMPT_PCAP_ANALYSIS,
        system_prompt=SYS_CYBERSECURITY_ANALYST,
    )

    display_results(results)
    save_results_to_file(results, test_name="ollama_demo")


if __name__ == '__main__':
    main()