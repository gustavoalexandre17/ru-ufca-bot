"""Extrai e estrutura cardápios a partir do texto do PDF."""

import re
from typing import Dict, List, Any
from datetime import datetime


class MenuExtractor:
    """Parseia o texto do PDF e organiza os cardápios por data (almoço/janta)."""
    
    def __init__(self, text: str):
        self.text = text
        self._menus: Dict[str, Any] = {}
    
    def extract_dates(self) -> List[str]:
        """Extrai datas no formato "9/mar", "10/abr", etc., sem repetições."""
        pattern = r'\b(\d{1,2})/([a-z]{3})\b'
        matches = re.findall(pattern, self.text, re.IGNORECASE)
        
        dates = [f"{day}/{month}" for day, month in matches]
        
        # Deduplica mantendo a ordem de aparição
        seen = set()
        unique_dates = []
        for date in dates:
            if date not in seen:
                seen.add(date)
                unique_dates.append(date)
        
        return unique_dates
    
    def extract_menus(self) -> Dict[str, Dict[str, Any]]:
        """
        Retorna cardápios organizados por data ISO.
        
        Formato: {"2026-03-09": {"almoco": {...}, "janta": {...}}}
        """
        if not self.text.strip():
            return {}
        
        dates = self.extract_dates()
        if not dates:
            return {}
        
        menus = {}
        
        # Ano detectado pelo cabeçalho do PDF; padrão 2026
        year_match = re.search(r'\b(20\d{2})\b', self.text)
        year = int(year_match.group(1)) if year_match else 2026
        
        for date_str in dates[:5]:  # Semana útil: até 5 dias
            iso_date = self.normalize_date(date_str, year)
            menus[iso_date] = {
                "almoco": self._extract_meal_section("ALMOÇO", date_str),
                "janta": self._extract_meal_section("JANTAR", date_str)
            }
        
        return menus
    
    def _extract_meal_section(self, meal_type: str, date_str: str) -> Dict[str, Any]:
        """
        Extrai os campos de uma refeição (almoço ou jantar) do texto usando a primeira palavra de cada coluna.
        
        LIMITAÇÃO: O PDF não possui delimitadores fixos entre colunas, então este método
        extrai apenas palavras parciais (ex: "COZIDO" ao invés de "COZIDO NORDESTINO").
        Para extrair valores completos seria necessário usar OCR com coordenadas ou
        um parser PDF mais sofisticado com análise de layout.
        
        Args:
            meal_type: "ALMOÇO" ou "JANTAR"
            date_str: Data no formato "16/mar"
        
        Returns:
            Dicionário com as categorias do cardápio (valores podem ser parciais)
        """
        meal_data = {
            "prato_principal": "",
            "vegetariano": "",
            "acompanhamentos": [],
            "saladas": [],
            "suco": "",
            "sobremesa": ""
        }
        
        lines = self.text.split('\n')
        
        meal_start = None
        for i, line in enumerate(lines):
            if meal_type.upper() in line.upper():
                meal_start = i
                break
        
        if meal_start is None:
            return meal_data
        
        date_line_idx = None
        for i in range(max(0, meal_start - 3), min(len(lines), meal_start + 3)):
            if date_str in lines[i]:
                date_line_idx = i
                break
        
        if date_line_idx is None:
            return meal_data
        
        dates = self.extract_dates()
        col_idx = 0
        for i, d in enumerate(dates[:5]):
            if d == date_str:
                col_idx = i
                break
        
        categories = [
            ('Principal', 'prato_principal'),
            ('Vegetariano', 'vegetariano'),
            ('Saladas', 'saladas'),
            ('Guarnição', 'acompanhamentos'),
            ('Acompanhamento', 'acompanhamentos'),
            ('Suco', 'suco'),
            ('Sobremesa', 'sobremesa')
        ]
        
        for category_name, data_key in categories:
            for i in range(meal_start, min(meal_start + 50, len(lines))):
                line = lines[i]
                
                if category_name in line:
                    words = line.split()
                    
                    category_idx = None
                    for j, word in enumerate(words):
                        if category_name in word:
                            category_idx = j
                            break
                    
                    if category_idx is not None and category_idx + col_idx + 1 < len(words):
                        value = words[category_idx + col_idx + 1]
                        
                        if data_key in ['saladas', 'acompanhamentos']:
                            meal_data[data_key] = [value] if value else []
                        else:
                            meal_data[data_key] = value
                    elif i > 0:
                        prev_line = lines[i - 1]
                        words = prev_line.split()
                        
                        if col_idx < len(words):
                            value = words[col_idx]
                            
                            if data_key in ['saladas', 'acompanhamentos']:
                                meal_data[data_key] = [value] if value else []
                            else:
                                meal_data[data_key] = value
                    break
        
        return meal_data
    
    def normalize_date(self, date_str: str, year: int) -> str:
        """Converte "9/mar" para "2026-03-09". Retorna "{year}-01-01" em caso de falha."""
        months_pt = {
            'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4,
            'mai': 5, 'jun': 6, 'jul': 7, 'ago': 8,
            'set': 9, 'out': 10, 'nov': 11, 'dez': 12
        }
        
        match = re.match(r'(\d{1,2})/([a-z]{3})', date_str, re.IGNORECASE)
        if not match:
            return f"{year}-01-01"
        
        day = int(match.group(1))
        month = months_pt.get(match.group(2).lower(), 1)
        
        try:
            return datetime(year, month, day).strftime('%Y-%m-%d')
        except ValueError:
            return f"{year}-01-01"
