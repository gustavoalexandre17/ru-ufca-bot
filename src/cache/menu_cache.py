"""
Módulo de cache de cardápios.

Implementado seguindo TDD (Test-Driven Development).
Testes definidos em tests/test_menu_cache.py.
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any, List, Union


class MenuCache:
    """
    Gerencia o cache de cardápios em arquivo JSON.
    
    Responsabilidades:
    - Salvar cardápios para datas específicas
    - Carregar cardápios do cache
    - Consultar cardápio por data
    """
    
    def __init__(self, cache_file: Union[str, Path]):
        """
        Inicializa o cache de cardápios.
        
        Args:
            cache_file: Caminho para o arquivo de cache JSON
        """
        self.cache_file = Path(cache_file)
        self._data: Dict[str, Any] = {}
        self._load_cache()
    
    def _load_cache(self) -> None:
        """Carrega o cache do arquivo JSON ou cria arquivo vazio."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self._data = json.load(f)
            except (json.JSONDecodeError, IOError):
                # JSON corrompido ou erro de leitura: criar cache vazio
                self._data = {}
                self._save_cache()
        else:
            # Arquivo não existe: criar vazio
            self._data = {}
            self._save_cache()
    
    def _save_cache(self) -> None:
        """Persiste o cache no arquivo JSON."""
        # Criar diretório pai se não existir
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)
    
    def save_menu(self, menu_date: str, menu_data: Dict[str, Any]) -> None:
        """
        Salva um cardápio para uma data específica.
        
        Args:
            menu_date: Data do cardápio (string ISO formato YYYY-MM-DD)
            menu_data: Dados do cardápio (dict com 'almoco' e 'janta')
        """
        self._data[menu_date] = menu_data
        self._save_cache()
    
    def get_menu(self, menu_date: str) -> Optional[Dict[str, Any]]:
        """
        Recupera o cardápio de uma data específica.
        
        Args:
            menu_date: Data do cardápio (string ISO formato YYYY-MM-DD)
            
        Returns:
            Dados do cardápio ou None se não encontrado
        """
        return self._data.get(menu_date)


class UserManager:
    """
    Gerencia usuários inscritos para notificações.
    
    Responsabilidades:
    - Adicionar/remover usuários
    - Verificar inscrição
    - Persistir em JSON
    """
    
    def __init__(self, users_file: Union[str, Path]):
        """
        Inicializa o gerenciador de usuários.
        
        Args:
            users_file: Caminho para o arquivo de usuários JSON
        """
        self.users_file = Path(users_file)
        self._data: Dict[str, List[int]] = {"chat_ids": [], "admin_ids": []}
        self._load_users()
    
    def _load_users(self) -> None:
        """Carrega usuários do arquivo JSON ou cria arquivo vazio."""
        if self.users_file.exists():
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    self._data = json.load(f)
                    # Garantir estrutura mínima
                    if "chat_ids" not in self._data:
                        self._data["chat_ids"] = []
                    if "admin_ids" not in self._data:
                        self._data["admin_ids"] = []
            except (json.JSONDecodeError, IOError):
                # JSON corrompido: criar estrutura vazia
                self._data = {"chat_ids": [], "admin_ids": []}
                self._save_users()
        else:
            # Arquivo não existe: criar vazio
            self._data = {"chat_ids": [], "admin_ids": []}
            self._save_users()
    
    def _save_users(self) -> None:
        """Persiste usuários no arquivo JSON."""
        # Criar diretório pai se não existir
        self.users_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)
    
    def add_user(self, chat_id: int) -> None:
        """
        Adiciona um usuário à lista de inscritos.
        
        Args:
            chat_id: ID do chat do Telegram
        """
        if chat_id not in self._data["chat_ids"]:
            self._data["chat_ids"].append(chat_id)
            self._save_users()
    
    def remove_user(self, chat_id: int) -> None:
        """
        Remove um usuário da lista de inscritos.
        
        Args:
            chat_id: ID do chat do Telegram
        """
        if chat_id in self._data["chat_ids"]:
            self._data["chat_ids"].remove(chat_id)
            self._save_users()
    
    def is_subscribed(self, chat_id: int) -> bool:
        """
        Verifica se um usuário está inscrito.
        
        Args:
            chat_id: ID do chat do Telegram
            
        Returns:
            True se inscrito, False caso contrário
        """
        return chat_id in self._data["chat_ids"]
