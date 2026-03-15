# RU UFCA Bot

Bot de Telegram para consulta de cardápios do Restaurante Universitário da UFCA.

## 📋 Sobre o Projeto

Este bot permite que estudantes da UFCA consultem o cardápio do RU de forma rápida e prática, além de receber notificações automáticas nos horários das refeições.

### Funcionalidades

- 🍽️ Consulta de cardápio do almoço e janta
- 📅 Visualização do cardápio semanal completo
- 🔔 Notificações automáticas nos horários das refeições
- 📄 Processamento automático de PDFs com cardápios
- 👤 Sistema de inscrição/desinscrição de notificações

## 🏗️ Arquitetura

Este projeto segue:
- **Metodologia:** Test-Driven Development (TDD)
- **Cobertura de testes:** 60-70% (pragmático)
- **Linguagem:** Python 3.11+

Consulte [ARCHITECTURE.md](./ARCHITECTURE.md) para detalhes completos das decisões arquiteturais.

## 🚀 Setup do Projeto

### Pré-requisitos

- Python 3.11 ou superior
- pip

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/ru-ufca-bot.git
cd ru-ufca-bot
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Para desenvolvimento
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite .env com suas credenciais
```

5. Execute os testes:
```bash
pytest
```

## 🧪 Desenvolvimento com TDD

Este projeto segue a metodologia TDD (Test-Driven Development):

### Ciclo TDD

```
1. 🔴 RED: Escrever teste que falha
2. 🟢 GREEN: Implementar código para passar o teste
3. 🔵 REFACTOR: Melhorar código mantendo testes passando
```

### Comandos úteis

```bash
# Rodar todos os testes
pytest

# Rodar com cobertura
pytest --cov=src --cov-report=html

# Rodar apenas testes unitários
pytest -m unit

# Rodar em modo verbose
pytest -v
```

## 📁 Estrutura do Projeto

```
ru-ufca-bot/
├── src/                    # Código fonte
│   ├── cache/             # Gerenciamento de cache
│   ├── scraper/           # Parsing de PDFs
│   ├── bot/               # Handlers e scheduler
│   └── main.py            # Entry point
├── tests/                  # Testes (TDD)
│   ├── fixtures/          # Dados de teste
│   └── test_*.py          # Arquivos de teste
├── data/                   # Dados persistidos
├── requirements.txt        # Dependências
└── ARCHITECTURE.md         # Documentação de arquitetura
```

## 🎯 Roadmap

- [x] Documentação de arquitetura
- [x] Setup da estrutura do projeto
- [ ] Implementação do Cache Layer (TDD)
- [ ] Implementação do PDF Parser (TDD)
- [ ] Implementação dos Handlers (TDD)
- [ ] Deploy em produção

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👤 Autor

**Gustavo Alexandre**

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se livre para abrir issues e pull requests.

---

Desenvolvido com ❤️ para a comunidade UFCA
