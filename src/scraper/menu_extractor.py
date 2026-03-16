"""Extrai e estrutura cardápios a partir do texto do PDF."""

import re
from typing import Dict, List, Any, Optional, Union
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
        Extrai os campos de uma refeição (almoço ou jantar) usando detecção de colunas.
        
        O PDF tem layout tabular onde cada dia da semana ocupa uma coluna vertical.
        Detectamos as colunas pela posição dos cabeçalhos de data (16/mar, 17/mar, etc.)
        e extraímos o texto de cada categoria dentro dos limites da coluna específica.
        
        Args:
            meal_type: "ALMOÇO" ou "JANTAR"
            date_str: Data no formato "16/mar"
        
        Returns:
            Dicionário com as categorias do cardápio
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
        
        # 1. Encontrar início da seção (ALMOÇO ou JANTAR)
        meal_start = None
        for i, line in enumerate(lines):
            if meal_type.upper() in line.upper():
                meal_start = i
                break
        
        if meal_start is None:
            return meal_data
        
        # 2. Detectar colunas pela posição das datas nos cabeçalhos
        date_line = None
        for i in range(max(0, meal_start - 5), meal_start + 5):
            if i < len(lines) and date_str in lines[i]:
                date_line = lines[i]
                break
        
        if not date_line:
            return meal_data
        
        # Encontrar posição inicial da coluna da data
        col_start = date_line.find(date_str)
        if col_start == -1:
            return meal_data
        
        # Estimar largura da coluna (distância até próxima data ou fim da linha)
        col_end = len(date_line)
        dates = self.extract_dates()
        
        try:
            current_idx = dates.index(date_str)
            if current_idx + 1 < len(dates):
                next_date = dates[current_idx + 1]
                next_pos = date_line.find(next_date)
                if next_pos > col_start:
                    col_end = next_pos
        except ValueError:
            pass
        
        # 3. Mapear labels de categorias para suas posições de linha
        labels: Dict[str, Optional[int]] = {
            'Principal': None,
            'Vegetariano': None,
            'Saladas': None,
            'Guarnição': None,
            'Acompanhamento': None,
            'Suco': None,
            'Sobremesa': None
        }
        
        for label in labels:
            for i in range(meal_start, min(meal_start + 50, len(lines))):
                if i < len(lines) and label in lines[i]:
                    labels[label] = i
                    break
        
        # 4. Função para extrair texto de uma categoria dentro da coluna específica
        def extract_category_text(start_label: str) -> str:
            """Extrai texto da categoria dentro dos limites da coluna."""
            label_idx = labels.get(start_label)
            if label_idx is None:
                return ""
            
            start_idx: int = label_idx
            
            # Encontrar próximo label para definir fim da categoria
            label_order = ['Principal', 'Vegetariano', 'Saladas', 'Guarnição', 
                          'Acompanhamento', 'Suco', 'Sobremesa']
            current_pos = label_order.index(start_label) if start_label in label_order else -1
            
            end_idx: Optional[int] = None
            for next_label in label_order[current_pos + 1:]:
                next_idx = labels.get(next_label)
                if next_idx is not None:
                    end_idx = next_idx
                    break
            
            if end_idx is None:
                end_idx = min(start_idx + 10, len(lines))
            
            # Extrair texto das linhas dentro da coluna
            words = []
            for i in range(start_idx, end_idx):
                if i >= len(lines):
                    break
                
                line = lines[i]
                
                # Se a linha tem tamanho suficiente, extrair a parte da coluna
                if len(line) > col_start:
                    # Pegar o segmento da linha correspondente à coluna
                    segment = line[col_start:min(col_end, len(line))]
                    
                    # Remover labels desta linha
                    for label in labels:
                        segment = segment.replace(label, '')
                    
                    # Adicionar palavras não vazias
                    segment_words = segment.strip().split()
                    words.extend(segment_words)
            
            return ' '.join(words)
        
        # 5. Extrair cada categoria usando detecção de coluna
        principal_text = extract_category_text('Principal')
        vegetariano_text = extract_category_text('Vegetariano')
        saladas_text = extract_category_text('Saladas')
        guarnição_text = extract_category_text('Guarnição')
        acomp_text = extract_category_text('Acompanhamento')
        suco_text = extract_category_text('Suco')
        sobremesa_text = extract_category_text('Sobremesa')
        
        # 6. Popular meal_data com texto completo (não mais fragmentado)
        meal_data["prato_principal"] = principal_text[:100].strip() if principal_text else "Não disponível"
        meal_data["vegetariano"] = vegetariano_text[:80].strip() if vegetariano_text else ""
        
        # Para acompanhamentos, juntar guarnição + acompanhamento
        guarnição_parts = guarnição_text.split()[:5] if guarnição_text else []
        acomp_parts = acomp_text.split()[:5] if acomp_text else []
        meal_data["acompanhamentos"] = guarnição_parts + acomp_parts
        
        # Saladas como lista de palavras (primeiras 4)
        saladas_words = saladas_text.split()[:4] if saladas_text else []
        meal_data["saladas"] = saladas_words
        
        # Suco e sobremesa (primeira palavra de cada)
        meal_data["suco"] = suco_text.split()[0].strip() if suco_text else ""
        meal_data["sobremesa"] = sobremesa_text.split()[0].strip() if sobremesa_text else ""
        
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
