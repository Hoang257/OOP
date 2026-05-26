"""
Точка входа ЛР-7.

Перед импортами добавляем корень репозитория OOP в sys.path — иначе не найдётся пакет src.
"""

from __future__ import annotations

import sys
from pathlib import Path


def _setup_path() -> None:
    # .../OOP/src/lib/lab07/main.py -> parents[3] == OOP
    root = Path(__file__).resolve().parents[3]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))


def main() -> None:
    _setup_path()
    from cli import run_cli

    run_cli()


if __name__ == "__main__":
    main()
