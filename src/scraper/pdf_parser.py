"""
Parser de PDFs de cardápios.

Implementado seguindo TDD (Test-Driven Development).
Testes definidos em tests/test_pdf_parser.py.
"""

import pdfplumber
from pathlib import Path
from typing import Union


class PDFParser:
    """
    Extrai texto de arquivos PDF usando pdfplumber.
    
    Responsabilidades:
    - Abrir e validar arquivos PDF
    - Extrair texto completo do PDF
    - Contar número de páginas
    """
    
    def __init__(self, pdf_path: Union[str, Path]):
        """
        Inicializa o parser de PDF.
        
        Args:
            pdf_path: Caminho para o arquivo PDF
            
        Raises:
            FileNotFoundError: Se o arquivo não existir
        """
        self.pdf_path = Path(pdf_path)
        
        # Validar se arquivo existe
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {self.pdf_path}")
        
        # Tentar abrir o PDF para validar
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                self._page_count = len(pdf.pages)
        except Exception as e:
            raise Exception(f"Erro ao abrir PDF: {e}")
    
    def extract_text(self) -> str:
        """
        Extrai todo o texto do PDF.
        
        Returns:
            String com o texto completo do PDF
            
        Raises:
            Exception: Se houver erro ao processar o PDF
        """
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                text_parts = []
                
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
                
                return "\n".join(text_parts)
                
        except Exception as e:
            raise Exception(f"Erro ao extrair texto do PDF: {e}")
    
    def get_page_count(self) -> int:
        """
        Retorna o número de páginas do PDF.
        
        Returns:
            Número de páginas
        """
        return self._page_count
