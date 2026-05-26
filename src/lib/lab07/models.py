"""
Реэкспорт моделей ЛР1–ЛР3.

Код предметной области не меняем — только удобные импорты для app/cli.
"""

from src.lib.lab03.base import Athlete
from src.lib.lab03.model import Runner, Swimmer

__all__ = ["Athlete", "Runner", "Swimmer"]
