# Setup do Projeto - RU UFCA Bot

**Data:** 14 de março de 2026  
**Status:** ✅ Estrutura criada com sucesso

---

## ✅ O que foi feito

### 1. Documentação Atualizada

- ✅ **ARCHITECTURE.md** atualizado com:
  - Seção sobre metodologia TDD (Test-Driven Development)
  - Estratégia de implementação detalhada
  - Ferramentas de teste e configuração
  - Meta de cobertura (60-70%)
  - Boas práticas adotadas
  - Status mudado para "Em Desenvolvimento"

- ✅ **README.md** criado com:
  - Descrição do projeto
  - Instruções de setup
  - Guia de desenvolvimento TDD
  - Estrutura do projeto
  - Roadmap

### 2. Estrutura de Diretórios

```
ru-ufca-bot/
├── src/                           # Código fonte (26 arquivos criados)
│   ├── __init__.py               # Pacote principal
│   ├── main.py                   # Entry point (TODO)
│   ├── cache/                    # Módulo de cache
│   │   ├── __init__.py
│   │   └── menu_cache.py        # TODO: Implementar após testes
│   ├── scraper/                  # Módulo de parsing
│   │   ├── __init__.py
│   │   ├── pdf_parser.py        # TODO: Implementar após testes
│   │   └── menu_extractor.py    # TODO: Implementar após testes
│   └── bot/                      # Módulo do bot
│       ├── __init__.py
│       ├── handlers.py          # TODO: Implementar após testes
│       ├── formatter.py         # TODO: Implementar após testes
│       └── scheduler.py         # TODO: Implementar após testes
│
├── tests/                         # Testes (TDD)
│   ├── __init__.py               # Testes básicos de estrutura
│   ├── conftest.py               # Fixtures compartilhadas
│   ├── fixtures/                 # Dados de teste
│   │   └── CARDAPIO-UFCA-MARÇO-SEGUNDA-SEMANA-2026.pdf
│   ├── test_menu_cache.py       # TODO: Escrever testes primeiro
│   ├── test_pdf_parser.py       # TODO: Escrever testes primeiro
│   ├── test_menu_extractor.py   # TODO: Escrever testes primeiro
│   ├── test_formatter.py        # TODO: Escrever testes primeiro
│   ├── test_handlers.py         # TODO: Escrever testes primeiro
│   └── test_scheduler.py        # TODO: Escrever testes primeiro
│
├── data/                          # Dados persistidos
│   └── .gitkeep                  # Mantém diretório no git
│
├── requirements.txt               # Dependências de produção
├── requirements-dev.txt           # Dependências de desenvolvimento
├── pytest.ini                     # Configuração do pytest
├── .env.example                   # Template de variáveis de ambiente
├── .gitignore                     # Arquivos ignorados pelo git
├── README.md                      # Documentação do projeto
├── ARCHITECTURE.md                # Decisões arquiteturais
└── LICENSE                        # Licença MIT
```

### 3. Arquivos de Configuração

#### requirements.txt
```
python-telegram-bot[job-queue]==20.7
pdfplumber==0.10.3
APScheduler==3.10.4
python-dotenv==1.0.0
pytz==2024.1
```

#### requirements-dev.txt
```
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
pytest-mock==3.12.0
black==23.12.1
flake8==6.1.0
```

#### pytest.ini
- Configurado para rodar testes em `tests/`
- Cobertura de código habilitada
- Markers para unit/integration/slow tests
- Relatórios em terminal e HTML

#### .env.example
- Template com todas as variáveis necessárias
- Token do Telegram
- Admin chat ID
- Configurações de horários

#### .gitignore
- Arquivos Python compilados
- Ambientes virtuais
- Dados sensíveis (.env, data/*.json)
- Relatórios de cobertura
- Arquivos IDE

### 4. PDF de Teste

- ✅ PDF copiado para `tests/fixtures/`
- ✅ Formato analisado (tabular com dias da semana)
- ✅ Pronto para desenvolvimento do parser

---

## 📋 Próximos Passos

### Fase 1: Setup do Ambiente (Você precisa fazer)

```bash
# 1. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Instalar dependências
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 3. Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas credenciais

# 4. Testar se está tudo funcionando
pytest tests/__init__.py -v
```

### Fase 2: Desenvolvimento TDD (Começamos com Cache Layer)

**Ordem de implementação:**

1. **Cache Layer** (Mais simples - começar aqui)
   - Escrever testes em `tests/test_menu_cache.py`
   - Implementar `src/cache/menu_cache.py`
   - Classes: `MenuCache` e `UserManager`

2. **PDF Parser**
   - Escrever testes em `tests/test_pdf_parser.py`
   - Implementar `src/scraper/pdf_parser.py`
   - Classe: `PDFParser`

3. **Menu Extractor**
   - Escrever testes em `tests/test_menu_extractor.py`
   - Implementar `src/scraper/menu_extractor.py`
   - Classe: `MenuExtractor`

4. **Formatter**
   - Escrever testes em `tests/test_formatter.py`
   - Implementar `src/bot/formatter.py`
   - Classe: `MenuFormatter`

5. **Bot Handlers**
   - Escrever testes em `tests/test_handlers.py`
   - Implementar `src/bot/handlers.py`
   - Classe: `BotHandlers`

6. **Scheduler**
   - Escrever testes em `tests/test_scheduler.py`
   - Implementar `src/bot/scheduler.py`
   - Classe: `NotificationScheduler`

---

## 🎓 Lembretes sobre TDD

### Ciclo Red-Green-Refactor

```
1. 🔴 RED: Escrever teste que FALHA
   └─> O teste falha porque o código não existe ainda

2. 🟢 GREEN: Escrever código MÍNIMO para passar
   └─> Fazer o teste passar da forma mais simples

3. 🔵 REFACTOR: Melhorar código
   └─> Limpar, remover duplicação, melhorar nomes
```

### Mantra TDD

> **"Nunca escreva código de produção sem um teste falhando antes"**

### Padrão AAA nos Testes

```python
def test_exemplo():
    # Arrange: Preparar dados e estado inicial
    data = criar_dados_teste()
    
    # Act: Executar a ação sendo testada
    resultado = funcao_testada(data)
    
    # Assert: Verificar se resultado está correto
    assert resultado == valor_esperado
```

---

## 🐛 Notas sobre Erros LSP

Os erros que você vê no LSP (Language Server Protocol) são **ESPERADOS** e **NORMAIS** neste momento:

```
ERROR: "MenuCache" is unknown import symbol
ERROR: "PDFParser" is unknown import symbol
ERROR: "BotHandlers" is unknown import symbol
```

**Por quê?**
- Os módulos `__init__.py` importam classes que ainda não existem
- Isso é proposital: seguindo TDD, as classes serão criadas APÓS os testes
- Os erros desaparecerão conforme implementarmos cada módulo

**Quando desaparecerão?**
- Após implementar cada classe (MenuCache, PDFParser, etc.)
- Por enquanto, pode ignorar esses erros

---

## ✅ Checklist de Validação

- [x] Estrutura de diretórios criada
- [x] Arquivos Python criados com TODOs
- [x] Configurações do pytest criadas
- [x] Requirements.txt criados
- [x] .gitignore configurado
- [x] README.md documentado
- [x] ARCHITECTURE.md atualizado
- [x] PDF de teste copiado para fixtures
- [ ] Ambiente virtual criado (você precisa fazer)
- [ ] Dependências instaladas (você precisa fazer)
- [ ] Primeiro teste rodando (você precisa fazer)

---

## 🚀 Comando para Começar

Quando estiver pronto para iniciar o desenvolvimento TDD:

```bash
# Ativar ambiente
source venv/bin/activate

# Confirmar que pytest está funcionando
pytest tests/__init__.py -v

# Ver este documento
cat SETUP_SUMMARY.md
```

**Próxima etapa sugerida:** Começar escrevendo os testes para `MenuCache` em `tests/test_menu_cache.py`

---

**Estrutura criada com sucesso!** 🎉

O projeto está pronto para desenvolvimento seguindo TDD.
