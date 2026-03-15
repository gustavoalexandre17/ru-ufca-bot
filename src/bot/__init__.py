"""
Módulo do bot de Telegram.

Contém handlers de comandos, formatação de mensagens e scheduler de notificações.
"""

from .handlers import BotHandlers
from .formatter import MenuFormatter
# from .scheduler import NotificationScheduler  # TODO: Uncomment when implemented

__all__ = ["BotHandlers", "MenuFormatter"]  # TODO: Add NotificationScheduler when implemented
