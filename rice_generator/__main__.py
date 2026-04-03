#!/usr/bin/env python3
"""Точка входа для rice-generator CLI."""

import sys
from pathlib import Path

# Добавляем родительскую директорию в path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rice_generator.cli import main

if __name__ == "__main__":
    sys.exit(main())
