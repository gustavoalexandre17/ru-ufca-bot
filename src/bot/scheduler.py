"""
Scheduler de notificações automáticas.

Responsável por agendar e enviar notificações de cardápios para usuários inscritos.
"""

from datetime import datetime
import logging
from telegram.error import Forbidden, TelegramError

logger = logging.getLogger(__name__)


class NotificationScheduler:
    """
    Scheduler para notificações automáticas de cardápios.
    
    Envia broadcasts de cardápios para usuários inscritos nos horários configurados.
    """
    
    def __init__(self, bot, menu_cache, user_manager, formatter):
        """
        Inicializa o scheduler.
        
        Args:
            bot: Instância do Bot do Telegram
            menu_cache: Instância de MenuCache para acessar cardápios
            user_manager: Instância de UserManager para gerenciar inscrições
            formatter: Instância de MenuFormatter para formatar mensagens
        """
        self.bot = bot
        self.cache = menu_cache
        self.users = user_manager
        self.formatter = formatter
    
    async def _send_meal_notification(self, meal_key: str, meal_type: str, meal_name: str):
        """
        Método auxiliar para enviar notificação de uma refeição.
        
        Args:
            meal_key: Chave do cardápio ("almoco" ou "janta")
            meal_type: Nome da refeição para formatação ("Almoço" ou "Jantar")
            meal_name: Nome da refeição para log ("Lunch" ou "Dinner")
        """
        today = datetime.now().strftime("%Y-%m-%d")
        menu_data = self.cache.get_menu(today)
        
        # Não enviar se cardápio não disponível
        if not menu_data or meal_key not in menu_data:
            logger.info(f"{meal_name} menu not available for {today}, skipping notification")
            return
        
        # Formatar mensagem
        formatted_message = self.formatter.format_meal(menu_data[meal_key], meal_type)
        
        # Enviar para todos os usuários
        await self._broadcast_to_users(formatted_message)
    
    async def send_lunch_notification(self):
        """
        Envia notificação do cardápio do almoço para todos os usuários inscritos.
        
        Chamado automaticamente às 10:30 (America/Fortaleza).
        Não envia se cardápio não estiver disponível.
        """
        await self._send_meal_notification("almoco", "Almoço", "Lunch")
    
    async def send_dinner_notification(self):
        """
        Envia notificação do cardápio da janta para todos os usuários inscritos.
        
        Chamado automaticamente às 16:30 (America/Fortaleza).
        Não envia se cardápio não estiver disponível.
        """
        await self._send_meal_notification("janta", "Jantar", "Dinner")
    
    async def broadcast_message(self, message: str):
        """
        Envia uma mensagem customizada para todos os usuários inscritos.
        
        Args:
            message: Mensagem a ser enviada
        """
        await self._broadcast_to_users(message)
    
    async def _broadcast_to_users(self, message: str):
        """
        Método auxiliar para broadcast de mensagens.
        
        Envia mensagem para todos os usuários inscritos.
        Remove automaticamente usuários que bloquearam o bot.
        
        Args:
            message: Mensagem a ser enviada
        """
        user_ids = self.users.get_all_users()
        
        for user_id in user_ids:
            try:
                await self.bot.send_message(
                    chat_id=user_id,
                    text=message,
                    parse_mode="Markdown"
                )
                logger.debug(f"Notification sent to user {user_id}")
                
            except Forbidden:
                # Usuário bloqueou o bot, remover da lista
                self.users.remove_user(user_id)
                logger.info(f"User {user_id} blocked bot, removed from list")
                
            except TelegramError as e:
                # Outros erros do Telegram (rate limit, etc)
                logger.error(f"Failed to send notification to user {user_id}: {e}")
