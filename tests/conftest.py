"""
Configuração e fixtures compartilhadas do pytest.

Este arquivo contém fixtures que podem ser usadas em todos os testes.
"""

import pytest
import os


@pytest.fixture
def sample_menu():
    """
    Fixture: Cardápio de exemplo para testes.
    
    Retorna estrutura de dados padrão de um cardápio completo.
    """
    return {
        "almoco": {
            "prato_principal": "Frango Grelhado",
            "vegetariano": "Rocambole de Soja",
            "acompanhamentos": ["Arroz Branco", "Feijão Carioca", "Farofa"],
            "saladas": ["Alface", "Tomate", "Beterraba"],
            "sobremesa": "Melancia",
            "suco": "Acerola"
        },
        "janta": {
            "prato_principal": "Peixe Assado",
            "vegetariano": "Torta de Legumes",
            "acompanhamentos": ["Arroz Integral", "Feijão Preto", "Purê de Batata"],
            "saladas": ["Repolho", "Cenoura"],
            "sobremesa": "Suco de Caju",
            "suco": "Cajá"
        }
    }


@pytest.fixture
def pdf_fixture_path():
    """
    Fixture: Caminho do PDF de teste.
    
    Retorna caminho absoluto do PDF de exemplo na pasta fixtures.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "fixtures", "CARDAPIO-UFCA-MARÇO-SEGUNDA-SEMANA-2026.pdf")
