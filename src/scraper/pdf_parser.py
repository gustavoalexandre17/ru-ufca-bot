"""Extrai texto de PDFs de cardápio usando pdfplumber."""

import pdfplumber
from pathlib import Path
from typing import Union, List, Optional


class PDFParser:
    """Wrapper fino sobre pdfplumber para extrair texto de PDFs."""
    
    def __init__(self, pdf_path: Union[str, Path]):
        """
        Abre e valida o PDF.
        
        Raises:
            FileNotFoundError: se o arquivo não existir.
        """
        self.pdf_path = Path(pdf_path)
        
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {self.pdf_path}")
        
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                self._page_count = len(pdf.pages)
        except Exception as e:
            raise Exception(f"Erro ao abrir PDF: {e}")
    
    def extract_text(self) -> str:
        """Retorna o texto completo do PDF, página por página."""
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
    
    def extract_tables(self) -> List[List[List[Optional[str]]]]:
        """
        Extrai tabelas do PDF preservando estrutura de linhas/colunas.
        
        Returns:
            Lista de tabelas (uma por página), onde cada tabela é uma lista de linhas,
            e cada linha é uma lista de células (strings ou None).
        """
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                all_tables = []
                
                for page in pdf.pages:
                    tables = page.extract_tables()
                    if tables:
                        all_tables.extend(tables)
                
                return all_tables
                
        except Exception as e:
            raise Exception(f"Erro ao extrair tabelas do PDF: {e}")
    
    def get_page_count(self) -> int:
        """Retorna o número de páginas do PDF."""
        return self._page_count
