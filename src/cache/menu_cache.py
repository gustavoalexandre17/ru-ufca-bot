"""Cache de cardápios e gerenciamento de usuários inscritos."""

import json
from datetime import date, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List, Union


class MenuCache:
    """Persiste cardápios em JSON e os recupera por data."""
    
    def __init__(self, cache_file: Union[str, Path]):
        self.cache_file = Path(cache_file)
        self._data: Dict[str, Any] = {}
        self._load_cache()
    
    def _load_cache(self) -> None:
        """Carrega o arquivo de cache ou cria um vazio se não existir."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self._data = json.load(f)
            except (json.JSONDecodeError, IOError):
                # Arquivo corrompido — começa do zero
                self._data = {}
                self._save_cache()
        else:
            self._data = {}
            self._save_cache()
    
    def _save_cache(self) -> None:
        """Persiste o estado atual no arquivo JSON."""
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)
    
    def save_menu(self, menu_date: str, menu_data: Dict[str, Any]) -> None:
        """Salva o cardápio de uma data (formato ISO YYYY-MM-DD)."""
        self._data[menu_date] = menu_data
        self._save_cache()
    
    def get_menu(self, menu_date: str) -> Optional[Dict[str, Any]]:
        """Retorna o cardápio de uma data ou None se não encontrado."""
        return self._data.get(menu_date)

    def get_weekly_menu(self) -> Dict[str, Any]:
        """Retorna os cardápios da semana corrente (seg–dom) que existem no cache."""
        today = date.today()
        monday = today - timedelta(days=today.weekday())
        week_dates = {
            (monday + timedelta(days=i)).isoformat()
            for i in range(7)
        }
        return {d: v for d, v in self._data.items() if d in week_dates}


class UserManager:
    """Gerencia a lista de usuários inscritos para notificações."""
    
    def __init__(self, users_file: Union[str, Path]):
        self.users_file = Path(users_file)
        self._data: Dict[str, List[int]] = {"chat_ids": [], "admin_ids": []}
        self._load_users()
    
    def _load_users(self) -> None:
        """Carrega o arquivo de usuários ou cria um vazio se não existir."""
        if self.users_file.exists():
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    self._data = json.load(f)
                    # Garante que as chaves esperadas existam
                    if "chat_ids" not in self._data:
                        self._data["chat_ids"] = []
                    if "admin_ids" not in self._data:
                        self._data["admin_ids"] = []
            except (json.JSONDecodeError, IOError):
                # Arquivo corrompido — começa do zero
                self._data = {"chat_ids": [], "admin_ids": []}
                self._save_users()
        else:
            self._data = {"chat_ids": [], "admin_ids": []}
            self._save_users()
    
    def _save_users(self) -> None:
        """Persiste a lista de usuários no arquivo JSON."""
        self.users_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)
    
    def add_user(self, chat_id: int) -> None:
        """Inscreve um usuário (idempotente)."""
        if chat_id not in self._data["chat_ids"]:
            self._data["chat_ids"].append(chat_id)
            self._save_users()
    
    def remove_user(self, chat_id: int) -> None:
        """Remove um usuário da lista (idempotente)."""
        if chat_id in self._data["chat_ids"]:
            self._data["chat_ids"].remove(chat_id)
            self._save_users()
    
    def is_subscribed(self, chat_id: int) -> bool:
        """Retorna True se o usuário estiver inscrito."""
        return chat_id in self._data["chat_ids"]

    def get_all_users(self) -> List[int]:
        """Retorna todos os chat_ids inscritos."""
        return self._data["chat_ids"]
