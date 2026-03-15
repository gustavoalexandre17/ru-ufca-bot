"""
Formatador de mensagens do bot.

Responsável por formatar cardápios em mensagens bonitas com emojis para Telegram.
"""

from datetime import datetime
from typing import Dict, Any


class MenuFormatter:
    """
    Formata cardápios em mensagens para o Telegram.
    
    Adiciona emojis apropriados e formata datas em português.
    """
    
    # Mapeamento de emojis por categoria
    EMOJIS = {
        "prato_principal": "🍗",
        "vegetariano": "🥗",
        "acompanhamentos": "🍚",
        "saladas": "🥬",
        "suco": "🍹",
        "sobremesa": "🍉",
        "meal": "🍽️"
    }
    
    # Mapeamento de dias da semana em português
    WEEKDAYS = {
        0: "Seg",  # Monday
        1: "Ter",  # Tuesday
        2: "Qua",  # Wednesday
        3: "Qui",  # Thursday
        4: "Sex",  # Friday
        5: "Sáb",  # Saturday
        6: "Dom"   # Sunday
    }
    
    # Mapeamento de campos do cardápio para labels em português
    FIELD_LABELS = {
        "prato_principal": "Principal",
        "vegetariano": "Vegetariano",
        "acompanhamentos": "Acompanhamentos",
        "saladas": "Saladas",
        "suco": "Suco",
        "sobremesa": "Sobremesa"
    }
    
    def _format_field(self, field_key: str, field_value: Any) -> str:
        """
        Formata um campo individual do cardápio.
        
        Args:
            field_key: Chave do campo (ex: "prato_principal")
            field_value: Valor do campo (string ou lista)
            
        Returns:
            str: Linha formatada com emoji e label
        """
        emoji = self.EMOJIS.get(field_key, "")
        label = self.FIELD_LABELS.get(field_key, field_key.replace("_", " ").title())
        
        # Converter listas em string separada por vírgulas
        if isinstance(field_value, list):
            value_str = ", ".join(field_value)
        else:
            value_str = str(field_value)
        
        return f"{emoji} *{label}:* {value_str}"
    
    def format_meal(self, menu_data: Dict[str, Any], meal_type: str) -> str:
        """
        Formata uma refeição (almoço ou jantar) em mensagem para Telegram.
        
        Args:
            menu_data: Dicionário com dados do cardápio
            meal_type: Tipo da refeição ("Almoço" ou "Jantar")
            
        Returns:
            str: Mensagem formatada com emojis
        """
        if not menu_data:
            return f"{self.EMOJIS['meal']} *{meal_type}*\n\nCardápio não disponível."
        
        lines = [f"{self.EMOJIS['meal']} *{meal_type.upper()}*\n"]
        
        # Ordem preferencial dos campos
        field_order = ["prato_principal", "vegetariano", "acompanhamentos", "saladas", "suco", "sobremesa"]
        
        # Formatar cada campo presente no menu_data
        for field_key in field_order:
            if field_key in menu_data:
                lines.append(self._format_field(field_key, menu_data[field_key]))
        
        return "\n".join(lines)
    
    def format_date(self, iso_date: str) -> str:
        """
        Formata data no padrão brasileiro com dia da semana.
        
        Args:
            iso_date: Data no formato ISO "YYYY-MM-DD"
            
        Returns:
            str: Data formatada "DD/MM (Dia)"
            
        Example:
            "2026-03-14" -> "14/03 (Sex)"
        """
        date_obj = datetime.fromisoformat(iso_date)
        day = date_obj.day
        month = date_obj.month
        weekday = self.WEEKDAYS[date_obj.weekday()]
        
        return f"{day:02d}/{month:02d} ({weekday})"
    
    def format_full_menu(self, menu_data: Dict[str, Any], iso_date: str) -> str:
        """
        Formata cardápio completo (almoço + jantar) para um dia.
        
        Args:
            menu_data: Dicionário com chaves "almoco" e "janta"
            iso_date: Data no formato ISO "YYYY-MM-DD"
            
        Returns:
            str: Mensagem formatada com ambas as refeições
        """
        formatted_date = self.format_date(iso_date)
        lines = [f"📅 *Cardápio de {formatted_date}*\n"]
        
        # Almoço
        if "almoco" in menu_data:
            almoco_msg = self.format_meal(menu_data["almoco"], "Almoço")
            lines.append(almoco_msg)
        
        lines.append("\n" + "─" * 30 + "\n")
        
        # Jantar
        if "janta" in menu_data:
            janta_msg = self.format_meal(menu_data["janta"], "Jantar")
            lines.append(janta_msg)
        
        return "\n".join(lines)
