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
        """Extrai os campos de uma refeição (almoço ou jantar) do texto."""
        meal_data = {
            "prato_principal": "",
            "vegetariano": "",
            "acompanhamentos": [],
            "saladas": [],
            "suco": "",
            "sobremesa": ""
        }
        
        meal_pattern = rf'{meal_type}.*?(?={meal_type}|JANTAR|$)'
        meal_match = re.search(meal_pattern, self.text, re.DOTALL | re.IGNORECASE)
        
        if meal_match:
            section = meal_match.group(0)
            
            principal_match = re.search(r'Principal\s+(.*?)(?=\n|Vegetariano|$)', section, re.DOTALL)
            if principal_match:
                first_line = principal_match.group(1).strip().split('\n')[0].strip()
                meal_data["prato_principal"] = first_line if first_line else "Não especificado"
            
            acomp_match = re.search(r'Acompanhamentos?\s+(.*?)(?=\n\n|Suco|Sobremesa|$)', section, re.DOTALL)
            if acomp_match:
                lines = [line.strip() for line in acomp_match.group(1).strip().split('\n') if line.strip()]
                meal_data["acompanhamentos"] = lines[:3]
        
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
