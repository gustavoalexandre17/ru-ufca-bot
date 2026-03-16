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


@pytest.fixture
def real_pdf_text():
    """
    Fixture: Texto extraído do PDF real (16 a 20 de março 2026).
    
    Este texto representa a estrutura real do cardápio do RU-UFCA.
    """
    return """MARMITEK ALIMENTAÇÃO E SERVIÇOS
RESTAURANTE UNIVERSITÁRIO - UFCA
CARDÁPIO SEMANAL - 01 A 31 DE MARÇO DE 2026
FERIADO
16/mar 17/mar 18/mar 19/mar 20/mar
ALMOÇO segunda-feira terça-feira quarta-feira quinta-feira sexta-feira
COZIDO NORDESTINO SUÍNO AO MOLHO BARBECUE FEIJOADA A BRASILEIRA PEIXE A DELICIA*
Principal
FRANGO AO MOLHO DE
FRANGO ASSADO FRANGO ACEBOLADO BIFE A PARMEGIANA*
MOSTARDA
MIX DE BRÓCOLIS E COUVE-
FALAFEL COM MOLHO TARRINE OMELETE DE FORNO HAMBURGUER DE SOJA
Vegetariano FLOR COM PALMITO
ACELGA, CENOURA, REPOLHO, ALFACE, TOMATE, CENOURA
ALFACE, CENOURA, TOMATE, MANGA VINAGRETE
ABACAXI E PEPINO
Saladas
BATATA DOCE COM
MAIONESE DE BETERRABA PURÊ DE BATATA ABOBORA COM CEBOLINHA
SALSINHA
CUSCUZ MACARRÃO ESPAGUETE FAROFA FAROFA
Guarnição
BAIÃO ARROZ BRANCO ARROZ BRANCO ARROZ BRANCO
Acompanhamento
ARROZ INTEGRAL ARROZ INTEGRAL ARROZ INTEGRAL ARROZ INTEGRAL
s
FEIJÃO PRETO FEIJÃO DE CARIOCA FEIJÃO CARIOCA FEIJÃO CARIOCA
Suco CAJU ACEROLA CAJÁ ACEROLA
MAÇÃ MELÃO LARANJA MELANCIA
Sobremesa
DOCE DOCE DOCE DOCE
16/mar 17/mar 18/mar 19/mar 20/mar
JANTAR segunda-feira terça-feira quarta-feira quinta-feira sexta-feira
ESCONDIDINHO DE CARNE DE
CHURRASCO MISTO FRANGO A PIZZAIOLO* PEIXE FRITO*
SOL*
Principal
FRANGO AO MOLHO
FRANGO AO MOLHO BRANCO FRANGO AO CREME DE MILHO SUINO AO CONFIT DE ERVAS
FERRUGEM
SOPAS CANJA DE GALINHA SOPA DE FEIJÃO SOPA DE FRANGO MUNGUNZÁ
ESCONDIDINHO DE SOJA COM GRÃO DE BICO REFOGADO
BRÓCOLIS REFOGADO OVO A PARMEGIANA
Vegetariano LEGUMES COM LEGUMES
CENOURA AO MOLHO
CHUCHU, CENOURA E VARGEM BATATA DOCE COM SALSINHA BATATA SAUTÉ
BRANCO*
Saladas
REPOLHO ROXO, REPOLHO ALFACE, TOMATE,
ALFACE, TOMATE, REPLHO ROXO E ACELGA, ALFACE, BETERRABA,
BRANCO, ALFACE, BETERRABA, REPOLHO E
MANGA TOMATE E MANGA
BETERRABA E ABACAXI MILHO
Guarnição FAROFA MACARRÃO PARAFUSO CUSCUZ FAROFA
ARROZ BRANCO ARROZ À GREGA ARROZ BRANCO ARROZ BRANCO
Acompanhamento
ARROZ INTEGRAL ARROZ INTEGRAL ARROZ INTEGRAL ARROZ INTEGRAL
s
FEIJÃO CARIOCA FEIJÃO DE CORDA FEIJÃO DE CORDA FEIJÃO DE CORDA
Suco MANGA GOIABA CAJU CAJÁ
MELANCIA MAMÃO MAÇÃ MELÃO
Sobremesa
DOCE DOCE DOCE DOCE
OBS: O cardápio pode sofrer alterações, dependendo da disponibilidade de produtos em estoque.
* Contém LEITE/LACTOSE"""
