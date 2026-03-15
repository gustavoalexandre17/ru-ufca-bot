# Arquitetura - RU UFCA Bot

> Bot de Telegram para consulta de cardápios do Restaurante Universitário da UFCA

**Status:** Em Produção  
**Última atualização:** 15/03/2026

---

## Stack

| Componente | Tecnologia |
|------------|------------|
| Linguagem | Python 3.10+ (Docker), 3.14 (dev local) |
| Bot | python-telegram-bot 22.6 |
| PDF | pdfplumber 0.10.3 |
| Scheduler | APScheduler 3.10.4 |
| Persistência | JSON (data/menu_cache.json, data/users.json) |
| Deploy | Docker + Oracle Cloud Free Tier |

---

## Estrutura

```
src/
├── main.py              # Entry point
├── bot/
│   ├── handlers.py      # /start, /almoco, /janta, /semana, /parar, /help
│   ├── scheduler.py     # Notificações 10:30 e 16:30
│   └── formatter.py     # Mensagens formatadas com emojis
├── cache/
│   └── menu_cache.py    # MenuCache + UserManager
└── scraper/
    ├── pdf_parser.py    # Extração de texto do PDF
    └── menu_extractor.py # Parsing do cardápio
```

---

## Comandos

| Comando | Descrição |
|---------|-----------|
| `/start` | Inscreve usuário e envia boas-vindas |
| `/almoco` | Cardápio do almoço de hoje |
| `/janta` | Cardápio da janta de hoje |
| `/semana` | Cardápio da semana completa |
| `/parar` | Remove das notificações |
| `/help` | Lista de comandos |
| Enviar PDF | Admin envia PDF → processa automaticamente |

---

## Formato de Dados

**Cache (`data/menu_cache.json`):**
```json
{
  "2026-03-14": {
    "almoco": {"prato_principal": "...", "acompanhamentos": [...], ...},
    "janta": {"prato_principal": "...", "acompanhamentos": [...], ...}
  }
}
```

**Usuários (`data/users.json`):**
```json
{"chat_ids": [123456789], "admin_ids": [8786785676]}
```

---

## Deploy

- **VM:** Oracle Cloud Free Tier (VM.Standard.E2.1.Micro)
- **Container:** python:3.10-slim com docker-compose
- **Restart:** unless-stopped
- **Volume:** ./data:/app/data (persiste cache)

**Ciclo de atualização:**
```bash
ssh ubuntu@<ip-da-vm>
cd ru-ufca-bot
git pull
docker compose up -d --build
```

---

## Testes

- **66/66 testes passando**
- **Cobertura:** 90%

---

## Variáveis de Ambiente

```
TELEGRAM_BOT_TOKEN=...
ADMIN_CHAT_ID=...
TIMEZONE=America/Fortaleza
LUNCH_NOTIFICATION_TIME=10:30
DINNER_NOTIFICATION_TIME=16:30
```
