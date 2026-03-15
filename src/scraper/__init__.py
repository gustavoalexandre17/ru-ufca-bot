"""
Módulo de scraping e parsing.

Responsável por extrair e processar dados dos PDFs de cardápios.
"""

from .pdf_parser import PDFParser
# TODO: Descomentar após implementar MenuExtractor
# from .menu_extractor import MenuExtractor

__all__ = ["PDFParser"]  # "MenuExtractor" será adicionado depois
