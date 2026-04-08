"""Rice Generator - генерация конфигов для Hyprland, Waybar и Kitty на основе скриншотов."""

__version__ = "0.1.0"

from .main import RiceGenerator
from .config_parser import ConfigParser, ConfigGenerator, GeneratedConfig
from .openrouter_client import OpenRouterClient
from .separate_generator import SeparateGenerator
from .validator import AIValidator
from .config import settings

__all__ = [
    "RiceGenerator",
    "ConfigParser",
    "ConfigGenerator",
    "GeneratedConfig",
    "OpenRouterClient",
    "SeparateGenerator",
    "AIValidator",
    "settings",
]
