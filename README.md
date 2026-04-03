# 🚀 Rice Generator

Генерация конфигов для **Hyprland**, **Waybar** и **Kitty** на основе скриншотов с использованием мультимодальной ИИ-модели.

![Preview](screenshot.png)

## ✨ Возможности

- 📸 **Анализ скриншотов** — распознавание цветовой схемы, шрифтов, компоновки
- 🎨 **Генерация конфигов** — создание конфигурационных файлов на основе анализа
- 🔧 **Autoinstaller** — автоматическая установка конфигов с бэкапом
- ↩️ **Uninstaller** — откат изменений и восстановление из бэкапа
- 🤖 **AI-powered** — использует Google Gemini 3 через OpenRouter
- 📝 **Свой конфиг Hyprland** — используйте свой конфиг как шаблон

## 📋 Требования

- Python 3.10+
- API ключ OpenRouter
- Установленные Hyprland, Waybar, Kitty (для применения конфигов)

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/yourusername/rice-generator.git
cd rice-generator
```

### 2. Установка зависимостей

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Настройка API ключа

```bash
cp .env.example .env
nano .env  # Вставьте свой API ключ
```

Получите API ключ на [openrouter.ai](https://openrouter.ai/)

### 4. Использование

```bash
# Базовое использование
python -m rice_generator screenshot.png -o ./my-rice

# Использовать свой конфиг Hyprland как шаблон
python -m rice_generator screenshot.png -H ~/.config/hypr/hyprland.conf -o ./my-rice

# С указанием API ключа и модели
python -m rice_generator screenshot.png --api-key your_key -m google/gemini-3-flash-preview -o ./output
```

## 📖 Команды CLI

```
usage: rice-generator [-h] [-o OUTPUT] [--api-key API_KEY] [-m MODEL] [-t TEMPLATES] [-H HYPRLAND_CONFIG] [-v] [--version]

positional arguments:
  screenshot            Путь к скриншоту для анализа

options:
  -h, --help            Показать справку
  -o OUTPUT, --output OUTPUT
                        Директория для сохранения конфигов (по умолчанию: ./generated_configs)
  --api-key API_KEY     API ключ OpenRouter
  -m MODEL, --model MODEL
                        Модель для анализа (по умолчанию: google/gemini-3-flash-preview)
  -t TEMPLATES, --templates TEMPLATES
                        Директория с шаблонами
  -H HYPRLAND_CONFIG, --hyprland-config HYPRLAND_CONFIG
                        Путь к вашему hyprland.conf (вместо встроенного шаблона)
  --list-models         Показать список доступных моделей
  -v, --verbose         Подробный вывод
  --version             Версия
```

## 📁 Структура проекта

```
rice-generator/
├── rice_generator/
│   ├── __init__.py           # Инициализация пакета
│   ├── __main__.py           # Точка входа CLI
│   ├── cli.py                # CLI интерфейс
│   ├── main.py               # Основной класс RiceGenerator
│   ├── openrouter_client.py  # Клиент OpenRouter API
│   ├── separate_generator.py # Генератор с раздельными запросами
│   ├── config_parser.py      # Парсер и генератор конфигов
│   ├── config.py             # Настройки проекта
│   └── templates/
│       ├── hyprland.conf     # Шаблон Hyprland
│       ├── waybar.json       # Шаблон Waybar (config)
│       ├── waybar_style.css  # Шаблон Waybar (style)
│       └── kitty.conf        # Шаблон Kitty
├── .env.example              # Пример конфигурации
├── .gitignore
├── requirements.txt
└── README.md
```

## 🔧 Как это работает

1. **Загрузка скриншота** — вы указываете путь к скриншоту вашего рабочего стола
2. **Анализ ИИ** — модель Google Gemini анализирует:
   - Цветовую схему (цвета фона, текста, акцентов)
   - Шрифты и размеры
   - Отступы (gaps, padding)
   - Расположение элементов (бар, иконки)
   - Прозрачность и закругления
3. **Генерация конфигов**:
   - **Hyprland** — модифицирует шаблон (заменяет gaps, цвета, opacity, rounding, shadow, blur)
   - **Waybar** — создаётся `config.json` и `style.css`
   - **Kitty** — создаётся `kitty.conf` с цветовой схемой
4. **Создание скриптов** — генерируются `autoinstaller.sh` и `uninstaller.sh`

## 📦 Выходные файлы

После генерации вы получите:

```
output/
├── hyprland.conf         # Конфиг Hyprland
├── waybar_config.json    # Конфиг Waybar
├── waybar_style.css      # Стили Waybar
├── kitty.conf            # Конфиг Kitty
├── color_scheme.json     # Информация о цветовой схеме
├── autoinstaller.sh      # Скрипт установки
└── uninstaller.sh        # Скрипт отката
```

## 🛠️ Применение конфигов

```bash
cd output/
chmod +x autoinstaller.sh
./autoinstaller.sh
```

Скрипт:
- Создаст бэкап текущих конфигов
- Установит новые конфиги
- Перезапустит Waybar

## ↩️ Откат изменений

```bash
./uninstaller.sh
```

Скрипт предложит восстановить конфиги из одного из бэкапов.

## 🎨 Использование своего конфига Hyprland

Если вы хотите модифицировать свой существующий конфиг:

```bash
python -m rice_generator screenshot.png -H ~/.config/hypr/hyprland.conf -o ./output
```

**Что изменит ИИ:**
- `gaps_in` / `gaps_out` — отступы
- `col.active_border` / `col.inactive_border` — цвета рамок
- `active_opacity` / `inactive_opacity` — прозрачность
- `rounding` — скругления
- `shadow.*` — тени
- `blur.*` — блюр
- `border_size` — толщина рамок

**Что останется без изменений:**
- binds (горячие клавиши)
- input настройки
- monitor настройки
- windowrules

## 🔑 Получение API ключа

1. Зарегистрируйтесь на [openrouter.ai](https://openrouter.ai/)
2. Перейдите в раздел API Keys
3. Создайте новый ключ
4. Скопируйте и вставьте в `.env`

## 🤖 Доступные модели

```bash
python -m rice_generator --list-models
```

| Модель | Провайдер | Рекомендуемая |
|--------|-----------|---------------|
| google/gemini-3-flash-preview | Google | ✅ Да |
| google/gemini-2.0-flash-001 | Google | |
| anthropic/claude-3.5-sonnet | Anthropic | |

## ⚙️ Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `OPENROUTER_API_KEY` | API ключ OpenRouter | (обязательно) |
| `RICE_MODEL` | Модель для анализа | `google/gemini-3-flash-preview` |
| `REQUEST_TIMEOUT` | Таймаут запроса (сек) | `120` |
| `MAX_TOKENS` | Лимит токенов | `16384` |
| `VERBOSE` | Подробный вывод | `false` |

## 📝 Примеры

### Генерация с выводом в кастомную директорию

```bash
python -m rice_generator ~/Pictures/my-rice.png -o ~/.config/rice-themes/blue
```

### Использование своих шаблонов

```bash
python -m rice_generator screenshot.png \
    --templates ./my-templates \
    --output ./my-rice
```

### Свой конфиг Hyprland + подробный режим

```bash
python -m rice_generator screenshot.png \
    -H ~/.config/hypr/hyprland.conf \
    -v
```

## ⚠️ Ограничения

- Точность зависит от качества скриншота
- Некоторые элементы могут быть распознаны неверно
- Требуется ручная проверка конфигов перед применением
- Модель может не распознать кастомные шрифты

## 🤝 Вклад

1. Fork репозиторий
2. Создайте ветку (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request




