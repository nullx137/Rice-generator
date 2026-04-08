#!/usr/bin/env python3
"""CLI интерфейс для rice-generator."""

import argparse
import sys
from pathlib import Path

from .main import RiceGenerator
from .config import settings


def main():
    """Точка входа CLI."""
    parser = argparse.ArgumentParser(
        prog="rice-generator",
        description="Генерация конфигов для Hyprland, Waybar и Kitty на основе скриншота",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  %(prog)s screenshot.png -o ./output
  %(prog)s ~/Pictures/rice.png --api-key your_key
  %(prog)s screenshot.png -o ./my-rice --templates ./custom-templates
  %(prog)s screenshot.png --model google/gemini-2.0-flash-001
  %(prog)s screenshot.png -H ~/.config/hypr/hyprland.conf  # использовать свой конфиг

Переменные окружения:
  OPENROUTER_API_KEY    API ключ для OpenRouter (обязательно)
  RICE_MODEL            Модель для анализа (по умолчанию: google/gemini-2.0-flash-exp:free)
  REQUEST_TIMEOUT       Таймаут запроса в секундах (по умолчанию: 120)
  MAX_TOKENS            Максимум токенов в ответе (по умолчанию: 4096)
        """,
    )

    parser.add_argument(
        "screenshot",
        type=str,
        help="Путь к скриншоту для анализа",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="./generated_configs",
        help="Директория для сохранения конфигов (по умолчанию: ./generated_configs)",
    )

    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="API ключ OpenRouter (можно через OPENROUTER_API_KEY)",
    )

    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default=None,
        help="Модель для анализа (по умолчанию: из конфига)",
    )

    parser.add_argument(
        "-t",
        "--templates",
        type=str,
        default=None,
        help="Директория с шаблонами (по умолчанию: встроенные шаблоны)",
    )

    parser.add_argument(
        "-H",
        "--hyprland-config",
        type=str,
        default=None,
        help="Путь к вашему hyprland.conf (по умолчанию: встроенный шаблон)",
    )

    parser.add_argument(
        "--list-models",
        action="store_true",
        help="Показать список доступных моделей",
    )

    parser.add_argument(
        "--validate",
        choices=["auto", "yes", "no"],
        default="auto",
        help="Режим проверки: auto (авто), yes (всегда), no (выключено)",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Включить подробный вывод",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )

    args = parser.parse_args()

    # Показ списка моделей
    if args.list_models:
        print("Доступные модели:")
        print("-" * 60)
        for model in settings.list_available_models():
            recommended = " (рекомендуется)" if model.get("recommended") else ""
            print(f"  • {model['id']}{recommended}")
            print(f"    {model['name']} ({model['provider']})")
        print("-" * 60)
        print(f"\nТекущая модель: {settings.MODEL}")
        print("\nИспользуйте --model для выбора модели")
        return 0

    # Проверка наличия API ключа
    api_key = args.api_key or Path.cwd() / ".env"
    if not api_key:
        api_key = None

    try:
        print("🚀 Rice Generator v0.1.0")
        print("=" * 40)

        generator = RiceGenerator(
            api_key=args.api_key,
            templates_dir=args.templates,
            model=args.model,
            hyprland_config=args.hyprland_config,
        )

        paths = generator.generate(
            screenshot_path=args.screenshot,
            output_dir=args.output,
        )

        # Проверка конфигов
        validate_mode = args.validate
        if validate_mode == "yes":
            print("\n🔍 Запуск ИИ-проверки конфигов...")
            from .validator import AIValidator
            ai_validator = AIValidator(api_key=args.api_key, model=args.model)
            results = ai_validator.validate_and_fix(
                screenshot_path=args.screenshot,
                output_dir=args.output,
                max_iterations=2,
            )
            if results:
                print(f"\n✅ Исправлено файлов: {len(results)}")
            else:
                print("\n✅ Все конфиги соответствуют скриншоту!")
        elif validate_mode == "no":
            pass  # Проверка выключена
        else:  # auto
            # Авто-режим: без проверки (быстрая генерация)
            pass

        print("=" * 40)
        print("📁 Сгенерированные файлы:")
        for name, path in paths.items():
            print(f"   • {name}: {path}")

        print("\n▶️  Для применения конфигов выполните:")
        print(f"   cd {args.output}")
        print("   chmod +x installer.sh")
        print("   ./installer.sh")

        return 0

    except FileNotFoundError as e:
        print(f"❌ Ошибка: {e}", file=sys.stderr)
        return 1

    except ValueError as e:
        print(f"❌ Ошибка обработки: {e}", file=sys.stderr)
        return 2

    except Exception as e:
        if args.verbose:
            import traceback

            traceback.print_exc()
        else:
            print(f"❌ Произошла ошибка: {e}", file=sys.stderr)
            print("   Используйте --verbose для подробностей", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
