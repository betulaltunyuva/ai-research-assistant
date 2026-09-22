import requests
from settings import (
    MODEL_NAME,
    OLLAMA_BASE_URL
)


def check_ollama(model_name: str):
    try:
        response = requests.get(
            f"{OLLAMA_BASE_URL}/api/tags",
            timeout=3
        )

        response.raise_for_status()

        data = response.json()

        installed_models = [
            model.get("name", "")
            for model in data.get("models", [])
        ]

        model_found = any(
            model_name == name
            or name.startswith(model_name + ":")
            for name in installed_models
        )

        if not model_found:
            return (
                False,
                f"'{model_name}' modeli bilgisayarda bulunamadı."
            )

        return True, "Ollama hazır."

    except requests.exceptions.ConnectionError:
        return (
            False,
            "Ollama çalışmıyor. Ollama uygulamasını açıp tekrar deneyin."
        )

    except Exception as e:
        return (
            False,
            f"Ollama kontrol edilirken hata oluştu: {e}"
        )