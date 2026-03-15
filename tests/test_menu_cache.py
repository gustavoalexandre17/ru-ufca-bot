"""
Testes para o módulo de cache de cardápios.

Seguindo TDD: Estes testes devem FALHAR primeiro (RED), depois implementamos (GREEN).
"""

import pytest
import json
from datetime import date
from pathlib import Path


class TestMenuCache:
    """
    Testes para a classe MenuCache que gerencia o cache de cardápios em JSON.
    
    Responsabilidades:
    - Salvar cardápios em data/menus.json
    - Carregar cardápios do cache
    - Consultar cardápio por data
    """
    
    @pytest.fixture
    def cache_file(self, tmp_path):
        """Cria um arquivo de cache temporário para testes isolados."""
        return tmp_path / "menus.json"
    
    @pytest.fixture
    def sample_menu_data(self):
        """Dados de exemplo de um cardápio completo."""
        return {
            "almoco": {
                "prato_principal": "Frango Grelhado",
                "acompanhamentos": ["Arroz Branco", "Feijão Carioca"],
                "sobremesa": "Melancia"
            },
            "janta": {
                "prato_principal": "Peixe Assado",
                "acompanhamentos": ["Arroz Integral", "Feijão Preto"],
                "sobremesa": "Banana"
            }
        }
    
    def test_init_creates_empty_cache_file_if_not_exists(self, cache_file):
        """
        Teste: Ao inicializar, deve criar arquivo de cache vazio se não existir.
        
        Arrange: Arquivo não existe
        Act: Criar MenuCache
        Assert: Arquivo criado com estrutura JSON vazia
        """
        from src.cache.menu_cache import MenuCache
        
        assert not cache_file.exists()
        cache = MenuCache(cache_file)
        assert cache_file.exists()
        
        with open(cache_file) as f:
            data = json.load(f)
        assert data == {}
    
    def test_save_menu_creates_new_entry(self, cache_file, sample_menu_data):
        """
        Teste: Deve salvar novo cardápio para uma data.
        
        Arrange: Cache vazio
        Act: Salvar cardápio
        Assert: Cardápio salvo corretamente
        """
        from src.cache.menu_cache import MenuCache
        
        cache = MenuCache(cache_file)
        cache.save_menu("2026-03-14", sample_menu_data)
        
        saved_menu = cache.get_menu("2026-03-14")
        assert saved_menu == sample_menu_data
    
    def test_get_menu_returns_none_if_not_found(self, cache_file):
        """
        Teste: Deve retornar None se cardápio não existe.
        
        Arrange: Cache vazio
        Act: Buscar data inexistente
        Assert: Retorna None
        """
        from src.cache.menu_cache import MenuCache
        
        cache = MenuCache(cache_file)
        result = cache.get_menu("2099-12-31")
        
        assert result is None

    def test_get_weekly_menu_returns_only_current_week(self, cache_file, sample_menu_data):
        """
        Teste: get_weekly_menu deve retornar apenas dias da semana corrente.

        Arrange: Cache com dias da semana atual e de semanas anteriores
        Act: Chamar get_weekly_menu
        Assert: Apenas dias da semana atual são retornados
        """
        from src.cache.menu_cache import MenuCache
        from datetime import date, timedelta

        cache = MenuCache(cache_file)

        # Descobrir segunda-feira da semana atual
        today = date.today()
        monday = today - timedelta(days=today.weekday())

        # Salvar 3 dias da semana atual
        for i in range(3):
            d = (monday + timedelta(days=i)).isoformat()
            cache.save_menu(d, sample_menu_data)

        # Salvar 1 dia de semana passada
        last_week = (monday - timedelta(days=3)).isoformat()
        cache.save_menu(last_week, sample_menu_data)

        result = cache.get_weekly_menu()

        assert len(result) == 3
        assert last_week not in result
        for i in range(3):
            assert (monday + timedelta(days=i)).isoformat() in result

    def test_get_weekly_menu_returns_empty_when_no_data_for_current_week(self, cache_file, sample_menu_data):
        """
        Teste: get_weekly_menu deve retornar {} se não há dados da semana atual.

        Arrange: Cache com dados apenas de semana passada
        Act: Chamar get_weekly_menu
        Assert: Retorna dicionário vazio
        """
        from src.cache.menu_cache import MenuCache
        from datetime import date, timedelta

        cache = MenuCache(cache_file)

        today = date.today()
        monday = today - timedelta(days=today.weekday())
        last_week_day = (monday - timedelta(days=3)).isoformat()
        cache.save_menu(last_week_day, sample_menu_data)

        result = cache.get_weekly_menu()

        assert result == {}


class TestUserManager:
    """
    Testes para a classe UserManager que gerencia usuários inscritos.
    
    Responsabilidades:
    - Adicionar usuários (chat_ids)
    - Remover usuários
    - Verificar inscrição
    """
    
    @pytest.fixture
    def users_file(self, tmp_path):
        """Cria um arquivo de usuários temporário para testes isolados."""
        return tmp_path / "users.json"
    
    def test_init_creates_empty_users_file_if_not_exists(self, users_file):
        """
        Teste: Deve criar arquivo vazio se não existir.
        
        Arrange: Arquivo não existe
        Act: Criar UserManager
        Assert: Arquivo criado com estrutura inicial
        """
        from src.cache.menu_cache import UserManager
        
        assert not users_file.exists()
        manager = UserManager(users_file)
        assert users_file.exists()
        
        with open(users_file) as f:
            data = json.load(f)
        assert data == {"chat_ids": [], "admin_ids": []}
    
    def test_add_user_adds_new_chat_id(self, users_file):
        """
        Teste: Deve adicionar novo usuário.
        
        Arrange: Lista vazia
        Act: Adicionar usuário
        Assert: Usuário na lista
        """
        from src.cache.menu_cache import UserManager
        
        manager = UserManager(users_file)
        manager.add_user(123456789)
        
        assert manager.is_subscribed(123456789)
    
    def test_remove_user_removes_existing_user(self, users_file):
        """
        Teste: Deve remover usuário existente.
        
        Arrange: Usuário inscrito
        Act: Remover usuário
        Assert: Usuário não está mais na lista
        """
        from src.cache.menu_cache import UserManager
        
        manager = UserManager(users_file)
        manager.add_user(123456789)
        manager.remove_user(123456789)
        
        assert not manager.is_subscribed(123456789)
