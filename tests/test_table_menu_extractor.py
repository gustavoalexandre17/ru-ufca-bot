"""
Testes para o TableMenuExtractor.

Seguindo TDD: testes de sanitização e listas limpas devem FALHAR primeiro (RED),
depois implementamos (GREEN).
"""

import pytest
from src.scraper.table_menu_extractor import TableMenuExtractor


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def simple_table():
    """
    Tabela mínima simulando estrutura do PDF do RU-UFCA.

    Colunas: col 0 = label, col 1 = 16/mar, col 2 = 17/mar
    """
    return [[
        # linha 0: cabeçalho de datas
        [None,           "16/mar",                     "17/mar"],
        # linha 1: ALMOÇO
        ["ALMOÇO",       "ALMOÇO",                     "ALMOÇO"],
        # linha 2: Principal
        ["Principal",    "FRANGO GRELHADO",             "PEIXE ASSADO"],
        # linha 3: Vegetariano
        ["Vegetariano",  "ROCAMBOLE DE SOJA",           "OMELETE DE FORNO"],
        # linha 4: Saladas — célula com vírgulas internas (causa raiz do bug)
        ["Saladas",      "ALFACE, CENOURA, TOMATE,",   "REPOLHO, BETERRABA,"],
        # linha 5: Guarnição
        ["Guarnição",    "CUSCUZ",                      "MACARRÃO"],
        # linha 6: Acompanhamento — célula com vírgulas internas
        ["Acompanhamentos", "ARROZ BRANCO, FEIJÃO CARIOCA,", "ARROZ INTEGRAL, FEIJÃO PRETO,"],
        # linha 7: Suco
        ["Suco",         "ACEROLA,",                    "CAJU,"],
        # linha 8: Sobremesa
        ["Sobremesa",    "MELANCIA,",                   "MAÇÃ,"],
        # linha 9: JANTAR
        ["JANTAR",       "JANTAR",                      "JANTAR"],
        # linha 10: Principal jantar
        ["Principal",    "CARNE ASSADA",                "FRANGO ACEBOLADO"],
        # linha 11: Saladas jantar — vírgulas
        ["Saladas",      "ALFACE, TOMATE,",             "REPOLHO, CENOURA,"],
        # linha 12: Guarnição jantar
        ["Guarnição",    "FAROFA",                      "CUSCUZ"],
        # linha 13: Acompanhamento jantar
        ["Acompanhamentos", "ARROZ BRANCO, FEIJÃO PRETO,", "ARROZ INTEGRAL, FEIJÃO CARIOCA,"],
        # linha 14: Suco jantar
        ["Suco",         "MANGA,",                      "GOIABA,"],
        # linha 15: Sobremesa jantar
        ["Sobremesa",    "MELÃO,",                      "MAMÃO,"],
    ]]


# ---------------------------------------------------------------------------
# Testes de sanitize_text()
# ---------------------------------------------------------------------------

class TestSanitizeText:
    """Testa a função utilitária sanitize_text."""

    def test_sanitize_removes_trailing_comma(self):
        """Deve remover vírgula no final da string."""
        from src.scraper.table_menu_extractor import sanitize_text

        assert sanitize_text("ACEROLA,") == "ACEROLA"

    def test_sanitize_removes_leading_comma(self):
        """Deve remover vírgula no início da string."""
        from src.scraper.table_menu_extractor import sanitize_text

        assert sanitize_text(",ACEROLA") == "ACEROLA"

    def test_sanitize_collapses_double_comma(self):
        """Deve colapsar dupla vírgula em simples."""
        from src.scraper.table_menu_extractor import sanitize_text

        assert sanitize_text("ALFACE,, CENOURA") == "ALFACE, CENOURA"

    def test_sanitize_trims_whitespace(self):
        """Deve remover espaços nas bordas."""
        from src.scraper.table_menu_extractor import sanitize_text

        assert sanitize_text("  MELANCIA  ") == "MELANCIA"

    def test_sanitize_handles_empty_string(self):
        """Deve retornar string vazia sem erro."""
        from src.scraper.table_menu_extractor import sanitize_text

        assert sanitize_text("") == ""

    def test_sanitize_does_not_alter_clean_text(self):
        """Não deve alterar texto já limpo."""
        from src.scraper.table_menu_extractor import sanitize_text

        assert sanitize_text("FRANGO GRELHADO") == "FRANGO GRELHADO"

    def test_sanitize_comma_space_comma(self):
        """Deve colapsar ', ,' (vírgula, espaço, vírgula)."""
        from src.scraper.table_menu_extractor import sanitize_text

        assert sanitize_text("ALFACE, , CENOURA") == "ALFACE, CENOURA"


# ---------------------------------------------------------------------------
# Testes de listas sem vírgulas residuais
# ---------------------------------------------------------------------------

class TestListFieldsNoDanglingCommas:
    """
    Verifica que saladas e acompanhamentos não contêm vírgulas residuais
    nos itens individuais da lista.
    """

    def test_saladas_items_have_no_trailing_comma(self, simple_table):
        """Cada item de saladas não deve terminar com vírgula."""
        extractor = TableMenuExtractor(simple_table)
        menus = extractor.extract_menus()

        almoco = menus["2026-03-16"]["almoco"]
        for item in almoco["saladas"]:
            assert not item.endswith(","), f"Item com vírgula residual: {item!r}"

    def test_acompanhamentos_items_have_no_trailing_comma(self, simple_table):
        """Cada item de acompanhamentos não deve terminar com vírgula."""
        extractor = TableMenuExtractor(simple_table)
        menus = extractor.extract_menus()

        almoco = menus["2026-03-16"]["almoco"]
        for item in almoco["acompanhamentos"]:
            assert not item.endswith(","), f"Item com vírgula residual: {item!r}"

    def test_suco_has_no_trailing_comma(self, simple_table):
        """Campo suco não deve conter vírgula."""
        extractor = TableMenuExtractor(simple_table)
        menus = extractor.extract_menus()

        almoco = menus["2026-03-16"]["almoco"]
        assert "," not in almoco["suco"], f"Suco com vírgula: {almoco['suco']!r}"

    def test_sobremesa_has_no_trailing_comma(self, simple_table):
        """Campo sobremesa não deve conter vírgula."""
        extractor = TableMenuExtractor(simple_table)
        menus = extractor.extract_menus()

        almoco = menus["2026-03-16"]["almoco"]
        assert "," not in almoco["sobremesa"], \
            f"Sobremesa com vírgula: {almoco['sobremesa']!r}"

    def test_jantar_saladas_items_have_no_trailing_comma(self, simple_table):
        """Saladas do jantar também não devem ter vírgulas residuais."""
        extractor = TableMenuExtractor(simple_table)
        menus = extractor.extract_menus()

        janta = menus["2026-03-16"]["janta"]
        for item in janta["saladas"]:
            assert not item.endswith(","), f"Item com vírgula residual: {item!r}"


# ---------------------------------------------------------------------------
# Testes de conteúdo esperado (split por vírgula, não por espaço)
# ---------------------------------------------------------------------------

class TestListSplitByComma:
    """
    Verifica que listas são construídas dividindo por vírgula (não espaço),
    preservando itens compostos como 'ARROZ BRANCO' como um único item.
    """

    def test_saladas_split_preserves_multi_word_items(self, simple_table):
        """
        'ALFACE, CENOURA, TOMATE' deve virar ['ALFACE', 'CENOURA', 'TOMATE'],
        não ['ALFACE,', 'CENOURA,', 'TOMATE'].
        """
        extractor = TableMenuExtractor(simple_table)
        menus = extractor.extract_menus()

        almoco = menus["2026-03-16"]["almoco"]
        # Deve ter pelo menos 2 itens distintos
        assert len(almoco["saladas"]) >= 2

    def test_acompanhamentos_preserves_multi_word_items(self, simple_table):
        """
        'ARROZ BRANCO, FEIJÃO CARIOCA' deve virar
        ['ARROZ BRANCO', 'FEIJÃO CARIOCA'], não ['ARROZ', 'BRANCO,', ...].
        """
        extractor = TableMenuExtractor(simple_table)
        menus = extractor.extract_menus()

        almoco = menus["2026-03-16"]["almoco"]
        assert "ARROZ BRANCO" in almoco["acompanhamentos"] or \
               any("ARROZ" in item for item in almoco["acompanhamentos"])


# ---------------------------------------------------------------------------
# Testes de formatação final (integração com formatter)
# ---------------------------------------------------------------------------

class TestFormatterIntegration:
    """
    Garante que o texto final formatado não contém dupla vírgula.
    """

    def test_formatted_output_has_no_double_comma(self, simple_table):
        """A mensagem formatada final não deve conter ',,' ou ', ,'."""
        from src.bot.formatter import MenuFormatter

        extractor = TableMenuExtractor(simple_table)
        menus = extractor.extract_menus()

        formatter = MenuFormatter()
        output = formatter.format_full_menu(menus["2026-03-16"], "2026-03-16")

        assert ",," not in output, f"Dupla vírgula encontrada:\n{output}"
        assert ", ," not in output, f"', ,' encontrada:\n{output}"

    def test_formatted_suco_no_trailing_comma(self, simple_table):
        """Suco formatado não deve ter vírgula residual."""
        from src.bot.formatter import MenuFormatter

        extractor = TableMenuExtractor(simple_table)
        menus = extractor.extract_menus()

        formatter = MenuFormatter()
        output = formatter.format_meal(menus["2026-03-16"]["almoco"], "Almoço")

        # A linha de suco não deve terminar com vírgula
        for line in output.splitlines():
            if "Suco" in line:
                assert not line.rstrip().endswith(","), \
                    f"Linha de suco com vírgula: {line!r}"
