"""Конфигурация проекта."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Загрузка переменных окружения из .env
load_dotenv()


class Settings:
    """Настройки приложения."""

    # === OpenRouter API ===
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

    # === Модель ===
    MODEL: str = os.getenv(
        "RICE_MODEL", "google/gemini-3-flash-preview"
    )

    # === Таймауты ===
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "120"))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))

    # === Лимиты токенов ===
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "16384"))

    # === Пути ===
    BASE_DIR: Path = Path(__file__).parent.parent
    TEMPLATES_DIR: Path = BASE_DIR / "rice_generator" / "templates"
    DEFAULT_OUTPUT_DIR: Path = BASE_DIR / "generated_configs"

    # === Прочее ===
    # HTTP Referer для OpenRouter (требование API)
    HTTP_REFERER: str = os.getenv(
        "HTTP_REFERER", "https://github.com/rice-generator"
    )
    APP_TITLE: str = os.getenv("APP_TITLE", "Rice Generator")

    # Включить подробное логирование
    VERBOSE: bool = os.getenv("VERBOSE", "false").lower() == "true"

    @classmethod
    def validate(cls) -> None:
        """
        Проверяет наличие обязательных настроек.

        Raises:
            ValueError: Если API ключ не указан.
        """
        if not cls.OPENROUTER_API_KEY:
            raise ValueError(
                "OPENROUTER_API_KEY не указан. "
                "Установите переменную окружения или создайте файл .env"
            )

    @classmethod
    def get_model_info(cls) -> dict:
        """
        Возвращает информацию о текущей модели.

        Returns:
            Словарь с информацией о модели.
        """
        model_mapping = {
            "google/gemini-3-flash-preview": {
                "name": "Gemini 3 Flash Preview",
                "provider": "Google",
                "multimodal": True,
                "max_tokens": 8192,
            },
            "google/gemini-2.0-flash-001": {
                "name": "Gemini 2.0 Flash",
                "provider": "Google",
                "multimodal": True,
                "max_tokens": 8192,
            },
            "google/gemini-2.0-flash-exp:free": {
                "name": "Gemini 2.0 Flash Exp (Free)",
                "provider": "Google",
                "multimodal": True,
                "max_tokens": 4096,
            },
            "openai/gpt-4-vision-preview": {
                "name": "GPT-4 Vision Preview",
                "provider": "OpenAI",
                "multimodal": True,
                "max_tokens": 4096,
            },
            "anthropic/claude-3-opus": {
                "name": "Claude 3 Opus",
                "provider": "Anthropic",
                "multimodal": True,
                "max_tokens": 4096,
            },
            "anthropic/claude-3.5-sonnet": {
                "name": "Claude 3.5 Sonnet",
                "provider": "Anthropic",
                "multimodal": True,
                "max_tokens": 8192,
            },
        }

        return model_mapping.get(
            cls.MODEL,
            {
                "name": cls.MODEL,
                "provider": "Unknown",
                "multimodal": True,
                "max_tokens": cls.MAX_TOKENS,
            },
        )

    @classmethod
    def list_available_models(cls) -> list[dict]:
        """
        Возвращает список доступных моделей.

        Returns:
            Список словарей с информацией о моделях.
        """
        return [
            {
                "id": "google/gemini-3-flash-preview",
                "name": "Gemini 3 Flash Preview",
                "provider": "Google",
                "recommended": True,
            },
            {
                "id": "google/gemini-2.0-flash-001",
                "name": "Gemini 2.0 Flash",
                "provider": "Google",
                "recommended": False,
            },
            {
                "id": "google/gemini-2.0-flash-exp:free",
                "name": "Gemini 2.0 Flash Exp (Free)",
                "provider": "Google",
                "recommended": False,
            },
            {
                "id": "anthropic/claude-3.5-sonnet",
                "name": "Claude 3.5 Sonnet",
                "provider": "Anthropic",
                "recommended": False,
            },
            {
                "id": "anthropic/claude-3-opus",
                "name": "Claude 3 Opus",
                "provider": "Anthropic",
                "recommended": False,
            },
            {
                "id": "openai/gpt-4-vision-preview",
                "name": "GPT-4 Vision Preview",
                "provider": "OpenAI",
                "recommended": False,
            },
        ]


# Глобальный экземпляр настроек
settings = Settings()
