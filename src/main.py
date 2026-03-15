"""
Entry point da aplicação RU UFCA Bot.

Responsabilidades:
- Carregar configurações do ambiente (.env)
- Instanciar e conectar todos os módulos
- Registrar handlers no bot do Telegram
- Configurar APScheduler com os horários de notificação
- Iniciar o polling do bot
"""

import os
import logging
from datetime import time

from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler

from src.bot.formatter import MenuFormatter
from src.bot.handlers import BotHandlers
from src.bot.scheduler import NotificationScheduler
from src.cache.menu_cache import MenuCache, UserManager

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def create_bot() -> Application:
    """
    Monta e configura a aplicação do bot.

    Instancia todos os componentes, registra os handlers de comandos
    e retorna a Application pronta para executar.

    Returns:
        Application: Aplicação configurada do python-telegram-bot

    Raises:
        ValueError: Se TELEGRAM_BOT_TOKEN não estiver definido no ambiente
    """
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN não configurado nas variáveis de ambiente")

    # Instanciar componentes
    cache = MenuCache("data/menu_cache.json")
    users = UserManager("data/users.json")
    formatter = MenuFormatter()
    handlers = BotHandlers(cache, users, formatter)

    # Criar aplicação com job_queue habilitado
    app = Application.builder().token(token).build()

    # Instanciar scheduler (precisa do bot da aplicação)
    scheduler = NotificationScheduler(app.bot, cache, users, formatter)

    # Registrar handlers de comandos
    app.add_handler(CommandHandler("start", handlers.start_command))
    app.add_handler(CommandHandler("almoco", handlers.almoco_command))
    app.add_handler(CommandHandler("janta", handlers.janta_command))
    app.add_handler(CommandHandler("semana", handlers.semana_command))
    app.add_handler(CommandHandler("parar", handlers.parar_command))
    app.add_handler(CommandHandler("help", handlers.help_command))

    # Configurar jobs agendados
    setup_scheduler(app, scheduler)

    logger.info("Bot configurado com sucesso.")
    return app


def setup_scheduler(app: Application, scheduler: NotificationScheduler) -> None:
    """
    Configura os jobs periódicos de notificação no job_queue da aplicação.

    Args:
        app: Application do python-telegram-bot
        scheduler: Instância de NotificationScheduler
    """
    tz_name = os.environ.get("TIMEZONE", "America/Fortaleza")
    lunch_time_str = os.environ.get("LUNCH_NOTIFICATION_TIME", "10:30")
    dinner_time_str = os.environ.get("DINNER_NOTIFICATION_TIME", "16:30")

    lunch_h, lunch_m = map(int, lunch_time_str.split(":"))
    dinner_h, dinner_m = map(int, dinner_time_str.split(":"))

    # Job diário para notificação do almoço
    app.job_queue.run_daily(
        callback=lambda ctx: scheduler.send_lunch_notification(),
        time=time(lunch_h, lunch_m, tzinfo=_get_timezone(tz_name)),
        name="lunch_notification",
    )

    # Job diário para notificação da janta
    app.job_queue.run_daily(
        callback=lambda ctx: scheduler.send_dinner_notification(),
        time=time(dinner_h, dinner_m, tzinfo=_get_timezone(tz_name)),
        name="dinner_notification",
    )

    logger.info(
        f"Scheduler configurado: almoço {lunch_time_str}, janta {dinner_time_str} ({tz_name})"
    )


def _get_timezone(tz_name: str):
    """
    Retorna objeto de timezone a partir do nome.

    Args:
        tz_name: Nome do timezone (ex: 'America/Fortaleza')

    Returns:
        tzinfo compatível com datetime.time
    """
    try:
        import zoneinfo
        return zoneinfo.ZoneInfo(tz_name)
    except Exception:
        logger.warning(f"Timezone '{tz_name}' não encontrado, usando UTC")
        import datetime
        return datetime.timezone.utc


def main() -> None:
    """
    Ponto de entrada principal. Inicia o bot em modo polling.
    """
    logger.info("Iniciando RU UFCA Bot...")
    app = create_bot()
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
