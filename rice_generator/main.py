"""Главный модуль для генерации райсов."""

import json
from pathlib import Path

from .openrouter_client import OpenRouterClient
from .config_parser import ConfigParser, ConfigGenerator
from .separate_generator import SeparateGenerator
from .config import settings


class RiceGenerator:
    """Основной класс для генерации конфигов на основе скриншота."""

    def __init__(
        self,
        api_key: str | None = None,
        templates_dir: str | Path | None = None,
        model: str | None = None,
        separate: bool = True,
        hyprland_config: str | Path | None = None,
    ):
        """
        Инициализация генератора.

        Args:
            api_key: API ключ OpenRouter.
            templates_dir: Директория с шаблонами.
            model: Модель для анализа (по умолчанию из конфига).
            separate: Использовать раздельные запросы (рекомендуется).
            hyprland_config: Путь к пользовательскому hyprland.conf (по умолчанию: встроенный шаблон).
        """
        self.api_key = api_key
        self.templates_dir = Path(templates_dir) if templates_dir else None
        self.model = model
        self.separate = separate
        self.hyprland_config = Path(hyprland_config) if hyprland_config else None

        if self.templates_dir is None:
            self.templates_dir = Path(__file__).parent / "templates"

    def generate(
        self,
        screenshot_path: str | Path,
        output_dir: str | Path,
    ) -> dict[str, Path]:
        """
        Генерирует конфиги на основе скриншота.

        Args:
            screenshot_path: Путь к скриншоту.
            output_dir: Директория для сохранения результатов.

        Returns:
            Словарь с путями к сгенерированным файлам.
        """
        screenshot_path = Path(screenshot_path)
        output_dir = Path(output_dir)

        if not screenshot_path.exists():
            raise FileNotFoundError(f"Скриншот не найден: {screenshot_path}")

        # Загрузка шаблонов
        # Используем пользовательский hyprland.conf или встроенный шаблон
        if self.hyprland_config and self.hyprland_config.exists():
            print(f"📄 Используем ваш hyprland.conf: {self.hyprland_config}")
            hyprland_template = self.hyprland_config.read_text()
        else:
            hyprland_template = (self.templates_dir / "hyprland.conf").read_text()

        waybar_template = (self.templates_dir / "waybar.json").read_text()
        kitty_template = (self.templates_dir / "kitty.conf").read_text()

        if self.separate:
            print("📸 Анализ скриншота...")
            print(f"🤖 Модель: {self.model or settings.MODEL}")
            print("=" * 40)

            # Используем раздельные запросы
            generator = SeparateGenerator(self.api_key, self.model)

            # 1. Генерация Hyprland
            print("🔵 [1/4] Генерация Hyprland...")
            hyprland_conf = generator.generate_hyprland(
                screenshot_path=screenshot_path,
                template=hyprland_template,
            )

            # 2. Генерация Waybar
            print("🟡 [2/4] Генерация Waybar...")
            waybar_config, waybar_style = generator.generate_waybar(
                screenshot_path=screenshot_path,
                config_template=waybar_template,
                style_template=self._get_waybar_style_template(),
            )

            # 3. Генерация Kitty
            print("🟢 [3/4] Генерация Kitty...")
            kitty_conf = generator.generate_kitty(
                screenshot_path=screenshot_path,
                template=kitty_template,
            )

            print("=" * 40)
            print("📝 Обработка результатов...")

            # Создаём GeneratedConfig из результатов
            from .config_parser import GeneratedConfig

            config = GeneratedConfig(
                hyprland_conf=hyprland_conf,
                waybar_conf=waybar_style,
                waybar_config=waybar_config,
                kitty_conf=kitty_conf,
                color_scheme={},
                fonts={},
                gaps={},
                notes="Сгенерировано с раздельными запросами",
            )
        else:
            print("📸 Анализ скриншота...")
            print(f"🤖 Модель: {self.model or settings.MODEL}")
            print("🤖 Отправка запроса к нейросети...")

            # Загрузка шаблона Hyprland для старого метода
            hyprland_template = (self.templates_dir / "hyprland.conf").read_text()

            # Анализ скриншота через OpenRouter (старый метод)
            with OpenRouterClient(self.api_key, self.model) as client:
                response = client.analyze_screenshot(
                    screenshot_path=screenshot_path,
                    hyprland_template=hyprland_template,
                    waybar_template=waybar_template,
                    kitty_template=kitty_template,
                )

            print("📝 Обработка ответа...")

            # Парсинг ответа
            parser = ConfigParser(response)
            config = parser.parse()

        # Генерация файлов
        gen = ConfigGenerator(config, output_dir)
        paths = gen.generate_all()

        print(f"✅ Конфиги сгенерированы в: {output_dir.absolute()}")
        print(f"📄 Файлов создано: {len(paths)}")

        return paths

    def _get_waybar_style_template(self) -> str:
        """Возвращает шаблон style.css для Waybar."""
        style_path = self.templates_dir / "waybar_style.css"
        if style_path.exists():
            return style_path.read_text()

        # Шаблон по умолчанию
        return """* {
    font-family: "JetBrainsMono Nerd Font";
    font-size: 14px;
    min-height: 30px;
}

window#waybar {
    background: rgba(30, 30, 46, 0.9);
    color: #c0caf5;
}

#workspaces {
    background: #1a1b26;
}

#workspaces button {
    padding: 0 10px;
    color: #c0caf5;
}

#workspaces button.active {
    background: #7aa2f7;
    color: #1a1b26;
}

#clock {
    background: #7aa2f7;
    color: #1a1b26;
    padding: 0 10px;
}
"""
