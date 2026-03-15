"""
Testes para o parser de PDFs.

Seguindo TDD: Estes testes devem FALHAR primeiro (RED), depois implementamos (GREEN).
"""

import pytest
from pathlib import Path


class TestPDFParser:
    """
    Testes para a classe PDFParser.
    
    Responsabilidades:
    - Extrair texto de PDFs usando pdfplumber
    - Validar se PDF é válido
    - Lidar com erros de arquivo
    """
    
    @pytest.fixture
    def sample_pdf_path(self):
        """Caminho para o PDF de teste."""
        return Path(__file__).parent / "fixtures" / "CARDAPIO-UFCA-MARÇO-SEGUNDA-SEMANA-2026.pdf"
    
    @pytest.fixture
    def invalid_pdf_path(self, tmp_path):
        """Caminho para arquivo que não é PDF."""
        fake_pdf = tmp_path / "fake.pdf"
        fake_pdf.write_text("Isso não é um PDF válido")
        return fake_pdf
    
    def test_init_accepts_valid_pdf_path(self, sample_pdf_path):
        """
        Teste: Deve aceitar caminho de PDF válido na inicialização.
        
        Arrange: PDF válido existe
        Act: Criar PDFParser
        Assert: Não lança exceção
        """
        from src.scraper.pdf_parser import PDFParser
        
        parser = PDFParser(sample_pdf_path)
        assert parser is not None
    
    def test_extract_text_returns_string_from_valid_pdf(self, sample_pdf_path):
        """
        Teste: Deve extrair texto de PDF válido.
        
        Arrange: PDF válido
        Act: Chamar extract_text()
        Assert: Retorna string não-vazia
        """
        from src.scraper.pdf_parser import PDFParser
        
        parser = PDFParser(sample_pdf_path)
        text = parser.extract_text()
        
        assert isinstance(text, str)
        assert len(text) > 0
    
    def test_extract_text_contains_expected_keywords(self, sample_pdf_path):
        """
        Teste: Texto extraído deve conter palavras-chave esperadas do cardápio.
        
        Arrange: PDF de cardápio
        Act: Extrair texto
        Assert: Contém palavras relacionadas a comida/dias da semana
        """
        from src.scraper.pdf_parser import PDFParser
        
        parser = PDFParser(sample_pdf_path)
        text = parser.extract_text()
        
        # Verificar palavras-chave que devem estar no cardápio
        text_lower = text.lower()
        assert "segunda" in text_lower or "terça" in text_lower or "quarta" in text_lower
    
    def test_extract_text_raises_error_on_nonexistent_file(self):
        """
        Teste: Deve lançar erro ao tentar abrir arquivo inexistente.
        
        Arrange: Caminho para arquivo que não existe
        Act: Tentar criar PDFParser
        Assert: Lança FileNotFoundError
        """
        from src.scraper.pdf_parser import PDFParser
        
        with pytest.raises(FileNotFoundError):
            parser = PDFParser("/caminho/inexistente/arquivo.pdf")
    
    def test_extract_text_raises_error_on_invalid_pdf(self, invalid_pdf_path):
        """
        Teste: Deve lançar erro ao tentar processar arquivo inválido.
        
        Arrange: Arquivo que não é PDF válido
        Act: Tentar extrair texto
        Assert: Lança exceção apropriada
        """
        from src.scraper.pdf_parser import PDFParser
        
        with pytest.raises(Exception):  # pdfplumber lançará alguma exceção
            parser = PDFParser(invalid_pdf_path)
            parser.extract_text()
    
    def test_get_page_count_returns_positive_number(self, sample_pdf_path):
        """
        Teste: Deve retornar número de páginas do PDF.
        
        Arrange: PDF válido
        Act: Chamar get_page_count()
        Assert: Retorna número > 0
        """
        from src.scraper.pdf_parser import PDFParser
        
        parser = PDFParser(sample_pdf_path)
        page_count = parser.get_page_count()
        
        assert isinstance(page_count, int)
        assert page_count > 0
