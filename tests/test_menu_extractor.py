"""
Testes para o extrator de cardápios.

Seguindo TDD: Estes testes devem FALHAR primeiro (RED), depois implementamos (GREEN).
"""

import pytest
from datetime import date


class TestMenuExtractor:
    """
    Testes para a classe MenuExtractor.
    
    Responsabilidades:
    - Parsear texto extraído do PDF
    - Identificar datas e dias da semana
    - Extrair estrutura de cardápio (almoço/janta)
    - Organizar em categorias (principal, vegetariano, saladas, etc.)
    """
    
    @pytest.fixture
    def sample_text(self):
        """Texto de exemplo simplificado de um cardápio."""
        return """
RESTAURANTE UNIVERSITÁRIO - UFCA
CARDÁPIO SEMANAL - 01 A 31 DE MARÇO DE 2026
9/mar 10/mar
ALMOÇO segunda-feira terça-feira
FRANGO GRELHADO PEIXE ASSADO
Principal
LASANHA DE SOJA OMELETE
Vegetariano
ARROZ BRANCO ARROZ BRANCO
Acompanhamentos
FEIJÃO CARIOCA FEIJÃO PRETO
ACEROLA MANGA
Suco
MELANCIA BANANA
Sobremesa

9/mar 10/mar
JANTAR segunda-feira terça-feira
CARNE ASSADA FRANGO ACEBOLADO
Principal
ARROZ BRANCO ARROZ INTEGRAL
Acompanhamentos
FEIJÃO CARIOCA FEIJÃO PRETO
"""
    
    def test_init_accepts_text(self):
        """
        Teste: Deve aceitar texto na inicialização.
        
        Arrange: Texto válido
        Act: Criar MenuExtractor
        Assert: Não lança exceção
        """
        from src.scraper.menu_extractor import MenuExtractor
        
        extractor = MenuExtractor("Texto qualquer")
        assert extractor is not None
    
    def test_extract_dates_returns_list_of_dates(self, sample_text):
        """
        Teste: Deve extrair datas do texto.
        
        Arrange: Texto com datas no formato "9/mar"
        Act: Chamar extract_dates()
        Assert: Retorna lista de strings com datas
        """
        from src.scraper.menu_extractor import MenuExtractor
        
        extractor = MenuExtractor(sample_text)
        dates = extractor.extract_dates()
        
        assert isinstance(dates, list)
        assert len(dates) > 0
        assert "9/mar" in dates or "10/mar" in dates
    
    def test_extract_menus_returns_dict_structure(self, sample_text):
        """
        Teste: Deve extrair cardápios organizados por data.
        
        Arrange: Texto com estrutura de cardápio
        Act: Chamar extract_menus()
        Assert: Retorna dict com datas como chaves
        """
        from src.scraper.menu_extractor import MenuExtractor
        
        extractor = MenuExtractor(sample_text)
        menus = extractor.extract_menus()
        
        assert isinstance(menus, dict)
        assert len(menus) > 0
    
    def test_extract_menus_contains_almoco_and_jantar(self, sample_text):
        """
        Teste: Cada data deve ter 'almoco' e 'jantar'.
        
        Arrange: Texto com ALMOÇO e JANTAR
        Act: Extrair cardápios
        Assert: Dicts contêm chaves 'almoco' e 'jantar'
        """
        from src.scraper.menu_extractor import MenuExtractor
        
        extractor = MenuExtractor(sample_text)
        menus = extractor.extract_menus()
        
        # Pegar primeira data
        first_date = list(menus.keys())[0]
        menu_day = menus[first_date]
        
        assert "almoco" in menu_day
        assert "janta" in menu_day
    
    def test_extract_menus_contains_expected_categories(self, sample_text):
        """
        Teste: Almoço/Janta devem ter categorias esperadas.
        
        Arrange: Texto estruturado
        Act: Extrair cardápios
        Assert: Contém prato_principal, acompanhamentos, etc.
        """
        from src.scraper.menu_extractor import MenuExtractor
        
        extractor = MenuExtractor(sample_text)
        menus = extractor.extract_menus()
        
        first_date = list(menus.keys())[0]
        almoco = menus[first_date]["almoco"]
        
        # Verificar que tem pelo menos algumas categorias
        assert "prato_principal" in almoco or "acompanhamentos" in almoco
    
    def test_extract_menus_handles_empty_text(self):
        """
        Teste: Deve lidar com texto vazio sem quebrar.
        
        Arrange: Texto vazio
        Act: Tentar extrair cardápios
        Assert: Retorna dict vazio ou lança exceção apropriada
        """
        from src.scraper.menu_extractor import MenuExtractor
        
        extractor = MenuExtractor("")
        menus = extractor.extract_menus()
        
        assert isinstance(menus, dict)
        assert len(menus) == 0
    
    def test_normalize_date_converts_to_iso_format(self):
        """
        Teste: Deve normalizar data do formato "9/mar" para ISO "2026-03-09".
        
        Arrange: Data no formato "9/mar" e ano 2026
        Act: Chamar normalize_date()
        Assert: Retorna "2026-03-09"
        """
        from src.scraper.menu_extractor import MenuExtractor
        
        extractor = MenuExtractor("")
        iso_date = extractor.normalize_date("9/mar", 2026)
        
        assert isinstance(iso_date, str)
        assert iso_date == "2026-03-09"
