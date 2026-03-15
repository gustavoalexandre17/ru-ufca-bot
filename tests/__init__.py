"""
Testes iniciais para validar estrutura do projeto.
"""

import pytest
import sys
import os


def test_pytest_is_working():
    """Teste simples para verificar que pytest está funcionando."""
    assert True


def test_python_version():
    """Verifica se está usando Python 3.11+"""
    assert sys.version_info >= (3, 11), "Projeto requer Python 3.11+"


def test_project_structure_exists():
    """Verifica se diretórios principais existem."""
    assert os.path.isdir("src"), "Diretório src/ não existe"
    assert os.path.isdir("tests"), "Diretório tests/ não existe"
    assert os.path.isdir("data"), "Diretório data/ não existe"


def test_requirements_files_exist():
    """Verifica se arquivos de requirements existem."""
    assert os.path.isfile("requirements.txt"), "requirements.txt não existe"
    assert os.path.isfile("requirements-dev.txt"), "requirements-dev.txt não existe"


def test_pdf_fixture_exists():
    """Verifica se o PDF de teste existe."""
    pdf_path = "tests/fixtures/CARDAPIO-UFCA-MARÇO-SEGUNDA-SEMANA-2026.pdf"
    assert os.path.isfile(pdf_path), f"PDF de teste não encontrado: {pdf_path}"
