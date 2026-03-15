# Decisões de Arquitetura - RU UFCA Bot

> Documento de decisões arquiteturais para o bot de Telegram do Restaurante Universitário da UFCA

**Data:** 15 de março de 2026  
**Status:** Em Produção  
**Autor:** Gustavo Alexandre  
**Metodologia:** Test-Driven Development (TDD)

---

## 1. Visão Geral do Projeto

### Objetivo
Criar um bot de Telegram que forneça informações sobre o cardápio do Restaurante Universitário da UFCA, permitindo consultas sob demanda e enviando notificações automáticas nos horários das refeições.

### Características Principais
- Consultas sob demanda de cardápios (almoço/janta)
- Notificações automáticas agendadas
- Processamento de PDFs semanais com os cardápios
- Interface simples e intuitiva via Telegram

---

## 2. Decisões Tecnológicas

### 2.1. Linguagem: Python 3.10+ (produção), 3.14 (desenvolvimento local)

**Decisão:** Utilizar Python como linguagem principal do projeto.

**Contexto:**
- Necessidade de prototipagem rápida para MVP
- Facilidade de manutenção futura
- Rico ecossistema de bibliotecas

**Versões:**
- **Desenvolvimento local:** Python 3.14.3
- **Produção (Docker):** Python 3.10-slim

**Nota de compatibilidade:**
- `python-telegram-bot 22.6` exige Python 3.10+
- Ubuntu 20.04 da VM Oracle tem Python 3.8.10 (incompatível) → Docker resolve

**Alternativas Consideradas:**
- Node.js (Telegraf/Grammy)
- Go (Telegram Bot API)

**Justificativa:**
- **Prototipagem rápida:** Sintaxe simples e expressiva acelera desenvolvimento
- **Bibliotecas maduras:** Excelente suporte para Telegram bots e processamento de PDFs
- **Manutenibilidade:** Código legível facilita evolução do projeto
- **Experiência da equipe:** Familiaridade com Python

**Consequências:**
- ✅ Desenvolvimento rápido do MVP
- ✅ Fácil integração com bibliotecas de PDF e agendamento
- ⚠️ Performance inferior a Go (não crítico para este caso de uso)

---

### 2.2. Biblioteca Telegram: python-telegram-bot v22.6

**Decisão:** Utilizar `python-telegram-bot` como biblioteca principal para interação com a API do Telegram.

**Nota de compatibilidade:** A versão 20.7 é incompatível com Python 3.14. Atualizado para 22.6.

**Alternativas Consideradas:**

| Biblioteca | Prós | Contras | Avaliação |
|------------|------|---------|-----------|
| **python-telegram-bot** | Madura, documentação excelente, suporte a webhook e polling, comunidade grande | Sintaxe um pouco mais verbosa | ✅ **Escolhida** |
| aiogram | Moderna, asyncio-first, menos boilerplate | Comunidade menor, menos recursos de troubleshooting | ❌ |
| pyTelegramBotAPI (telebot) | Simples, boa para projetos pequenos | Menos features modernas, sem asyncio nativo | ❌ |

**Justificativa:**
- Estabilidade e maturidade comprovadas
- Documentação e exemplos abundantes
- Suporte asyncio nativo (importante para escalabilidade futura)
- Comunidade ativa facilita resolução de problemas

**Consequências:**
- ✅ Menos riscos de bugs e problemas de compatibilidade
- ✅ Facilidade para encontrar soluções e exemplos
- ⚠️ Curva de aprendizado um pouco maior devido às abstrações

---

### 2.3. Processamento de PDFs: pdfplumber

**Decisão:** Utilizar `pdfplumber` para extração de texto dos PDFs de cardápio.

**Alternativas Consideradas:**
- PyPDF2: Mais básico, dificuldade com tabelas
- pypdf: Fork moderno do PyPDF2
- pdfplumber: Especializado em extração estruturada

**Justificativa:**
- Melhor suporte para extração de tabelas (provável formato dos cardápios)
- API mais intuitiva para parsing estruturado
- Boa documentação e exemplos práticos

**Consequências:**
- ✅ Extração mais precisa de dados tabulares
- ✅ Menos necessidade de pós-processamento
- ⚠️ Dependência adicional (pillow, pdfminer.six)

---

### 2.4. Agendamento de Tarefas: APScheduler

**Decisão:** Utilizar `APScheduler` para gerenciar notificações automáticas.

**Justificativa:**
- Integração nativa com Python e asyncio
- Suporte a CronTrigger para horários específicos
- Persistência de jobs (não perde agendamentos em reinicializações)
- Timezone-aware (importante para horários locais de Fortaleza)

**Horários Definidos:**
- **10:30 (America/Fortaleza):** Notificação do cardápio do almoço
- **16:30 (America/Fortaleza):** Notificação do cardápio da janta
- **Domingo 18:00:** Verificação de cardápio da semana seguinte (notifica admin se ausente)

**Consequências:**
- ✅ Gerenciamento confiável de horários
- ✅ Configuração simples via código
- ⚠️ Bot precisa estar rodando continuamente (consideração para deploy)

---

## 3. Arquitetura do Sistema

### 3.1. Estrutura de Diretórios

```
ru-ufca-bot/
├── src/
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── handlers.py          # Comandos do bot (/start, /almoco, etc)
│   │   ├── scheduler.py         # Lógica de notificações agendadas
│   │   └── formatter.py         # Formatação de mensagens com emojis
│   ├── scraper/
│   │   ├── __init__.py
│   │   ├── pdf_parser.py        # Extração de texto do PDF
│   │   └── menu_extractor.py    # Parsing e estruturação do cardápio
│   ├── cache/
│   │   ├── __init__.py
│   │   └── menu_cache.py        # Gerenciamento de cache JSON (MenuCache + UserManager)
│   └── main.py                  # Entry point da aplicação
├── data/
│   ├── menu_cache.json          # Cache de cardápios da semana
│   └── users.json               # Lista de chat_ids inscritos
├── tests/
│   ├── __init__.py
│   ├── test_pdf_parser.py
│   ├── test_menu_extractor.py
│   ├── test_menu_cache.py
│   ├── test_formatter.py
│   ├── test_handlers.py
│   └── test_scheduler.py
├── .env.example                 # Template de variáveis de ambiente
├── .gitignore
├── .dockerignore
├── requirements.txt
├── requirements-dev.txt
├── docker-compose.yml           # Orquestração do container
├── Dockerfile                  # Imagem Python 3.10-slim
├── pytest.ini
├── README.md
├── ARCHITECTURE.md              # Este documento
└── LICENSE
```

**Princípios:**
- **Separação de responsabilidades:** Cada módulo tem função clara e única
- **Testabilidade:** Estrutura facilita testes unitários
- **Escalabilidade:** Fácil adicionar novos scrapers ou handlers

---

### 3.2. Fluxo de Dados

#### A. Obtenção do Cardápio (Upload Manual - MVP)

```
Admin → Envia documento PDF (Telegram)
    ↓
Bot recebe arquivo PDF
    ↓
pdf_parser.py extrai texto
    ↓
menu_extractor.py identifica estrutura
    ↓
Salva em data/menu_cache.json
    ↓
Confirma sucesso ao admin
```

**Nota:** O upload é feito enviando o arquivo PDF diretamente para o bot (não via comando /upload).

**Estratégia de Parsing:**
1. Extração de texto completo com `pdfplumber`
2. Detecção de padrões de dias da semana (regex)
3. Identificação de seções (Almoço/Janta)
4. Classificação de itens (prato principal, acompanhamentos, saladas, sobremesa)
5. Estruturação em JSON

**Tratamento de Falhas:**
- Se parsing falhar: Notifica admin com texto bruto extraído
- Admin pode usar comando futuro `/corrigir` para ajuste manual

---

#### B. Consulta Sob Demanda

```
Usuário → /almoco ou /janta
    ↓
menu_cache.py busca cardápio de hoje
    ↓
Formata mensagem (lista organizada)
    ↓
Envia resposta ao usuário
```

**Cenários:**
- ✅ **Cardápio disponível:** Envia formatado
- ⚠️ **Cardápio indisponível:** "Cardápio ainda não disponível. Aguarde upload do admin."

---

#### C. Notificações Automáticas

```
APScheduler (10:30 ou 16:30)
    ↓
scheduler.py verifica data/menus.json
    ↓
Se cardápio disponível:
    ↓
Itera sobre users.json (chat_ids)
    ↓
Envia broadcast formatado
```

**Comportamento:**
- Não envia notificação se cardápio ausente
- Registra logs de broadcast (quantidade de usuários alcançados)
- Tratamento de erros: Usuário bloqueou bot → Remove da lista

---

### 3.3. Formato de Dados

#### Cache de Cardápios (`data/menus.json`)

```json
{
  "2026-03-14": {
    "almoco": {
      "prato_principal": "Frango Grelhado",
      "acompanhamentos": [
        "Arroz Branco",
        "Feijão Carioca",
        "Farofa"
      ],
      "saladas": [
        "Alface",
        "Tomate"
      ],
      "sobremesa": "Melancia"
    },
    "janta": {
      "prato_principal": "Peixe Assado",
      "acompanhamentos": [
        "Arroz Integral",
        "Feijão Preto",
        "Purê de Batata"
      ],
      "saladas": [
        "Repolho",
        "Cenoura"
      ],
      "sobremesa": "Suco de Caju"
    }
  },
  "2026-03-15": { ... }
}
```

**Decisões de Design:**
- **Chave:** Data ISO (YYYY-MM-DD) para ordenação natural
- **Estrutura:** Separação clara de categorias facilita formatação
- **Flexibilidade:** Arrays permitem múltiplos itens por categoria

---

#### Usuários Inscritos (`data/users.json`)

```json
{
  "chat_ids": [123456789, 987654321],
  "admin_ids": [123456789]
}
```

**Decisões:**
- **Auto-inscrição:** Usuário é adicionado automaticamente ao usar `/start`
- **Opt-out:** Comando `/parar` remove da lista
- **Admin:** Controle de acesso para comandos privilegiados

---

### 3.4. Comandos do Bot

| Comando | Acesso | Descrição |
|---------|--------|-----------|
| `/start` | Todos | Boas-vindas + auto-inscrição para notificações |
| `/almoco` | Todos | Exibe cardápio do almoço de hoje |
| `/janta` | Todos | Exibe cardápio da janta de hoje |
| `/semana` | Todos | Exibe cardápio completo da semana |
| `/parar` | Todos | Remove das notificações automáticas |
| `/help` | Todos | Lista de comandos disponíveis |
| Enviar PDF | Admin | Enviando documento PDF, o bot processa automaticamente |

**Upload de Cardápio:**
- Admin envia o arquivo PDF diretamente para o bot
- Bot detecta formato PDF, processa e salva no cache
- Não há comando explícito; é identificado pelo tipo de arquivo

**Comandos Futuros (Pós-MVP):**
- `/corrigir` - Admin ajusta cardápio manualmente
- `/stats` - Admin vê estatísticas de uso
- `/proximo` - Exibe próximo cardápio (útil à noite para ver o almoço do dia seguinte)

---

### 3.5. Formato de Mensagens

**Decisão:** Lista organizada com categorização clara.

**Exemplo:**

```
🍽️ CARDÁPIO DO ALMOÇO - 14/03 (Sex)

🍖 Prato Principal:
   • Frango Grelhado

🍚 Acompanhamentos:
   • Arroz Branco
   • Feijão Carioca
   • Farofa

🥗 Saladas:
   • Alface
   • Tomate

🍉 Sobremesa:
   • Melancia

Bom apetite! 😋
```

**Justificativa:**
- **Clareza:** Categorias bem definidas facilitam leitura rápida
- **Escaneabilidade:** Bullets e emojis tornam informação digestível
- **Consistência:** Formato padronizado em todas as mensagens
- **Formato de data curto:** "14/03 (Sex)" - conciso e informativo

---

## 4. Estratégia de Persistência (MVP)

### 4.1. Armazenamento Simples

**Decisão:** Utilizar arquivos JSON locais para cache, sem banco de dados.

**Justificativa (YAGNI - You Aren't Gonna Need It):**
- Volume de dados baixo (1 semana de cardápios = ~14 registros)
- Sem necessidade de consultas complexas
- Simplicidade de deploy e manutenção
- Fácil inspeção e debug

**Arquivos:**
- `data/menu_cache.json` - Cardápios da semana
- `data/users.json` - Chat IDs dos usuários inscritos

**Limitações Conhecidas:**
- Sem histórico de cardápios antigos
- Concorrência pode causar race conditions (mitigado: apenas 1 processo)
- Sem backup automático (mitigação: Git + volume Docker persistente)

**Migração Futura:**
Se necessário, facilmente migrável para:
- **SQLite** (sem servidor adicional)
- **PostgreSQL** (se precisar de features avançadas)
- **Redis** (se precisar de cache distribuído)

---

## 5. Estratégia de Implementação

### 5.1. Fases de Desenvolvimento

#### Fase 1: MVP com Upload Manual ✅ APROVADA

**Escopo:**
- Upload manual de PDF via Telegram (comando `/upload`)
- Admin controla qual PDF é processado
- Sistema de parsing otimista com fallback para revisão manual

**Justificativa:**
- **Problema identificado:** PDFs do RU UFCA não seguem padrão de nomenclatura ou URL consistente
- **Solução pragmática:** Controle manual elimina incerteza de scraping automático
- **Validação rápida:** Permite testar valor do bot antes de automatizar
- **Menos riscos:** Não depende de site externo ou mudanças de estrutura

**Sequência de Implementação:**
1. Setup do projeto (estrutura, dependências)
2. Bot básico com comandos de consulta (`/start`, `/almoco`, `/janta`)
3. Sistema de cache JSON
4. Parser de PDF com regex patterns
5. Comando `/upload` para admin
6. Sistema de notificações agendadas
7. Testes com PDF real do RU

---

#### Fase 2: Scraping Automático (Futuro)

**Escopo:**
- Monitoramento da página de cardápios da UFCA
- Detecção automática de novos PDFs
- Notificação ao admin para aprovação
- Fallback para upload manual se detecção falhar

**Gatilho para Implementação:**
- Bot em uso regular há 2+ semanas
- Feedback positivo dos usuários
- Admin sente necessidade de automatização

**Abordagem Sugerida:**
```python
# Verificação semanal (domingo à noite)
1. Acessa página institucional do RU
2. Identifica link de PDF mais recente por:
   - Data de modificação do arquivo
   - Heurística de nome (ex: contém data futura)
   - Hash do arquivo (evita reprocessamento)
3. Baixa PDF e tenta parsing
4. Se sucesso: Notifica admin "Novo cardápio detectado, deseja publicar?"
5. Admin confirma ou rejeita
```

**Requisitos Técnicos:**
- Beautiful Soup ou Scrapy para parsing HTML
- Lógica de detecção robusta (não assumir estrutura fixa)
- Cache de hashes para evitar duplicatas

---

### 5.2. Deploy: Docker na Oracle Cloud Free Tier

**Decisão:** Container Docker em VM Oracle Cloud Free Tier (VM.Standard.E2.1.Micro).

**Infraestrutura:**
- **VM:** Oracle Cloud Free Tier — `VM.Standard.E2.1.Micro` (x86)
- **OS:** Ubuntu 20.04 (focal)
- **Docker:** Instalado na VM, container `python:3.10-slim`
- **IP:** `164.152.45.38`
- **Usuário:** `ubuntu`

**Configuração de Deploy:**
```yaml
# docker-compose.yml
services:
  bot:
    build: .
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./data:/app/data
```

**Ciclo de Atualização:**
```bash
# Na máquina local, após commit + push
ssh -i ~/Downloads/ssh-key-2026-03-15.key ubuntu@164.152.45.38
cd ru-ufca-bot
git pull
docker compose up -d --build
docker compose logs -f
```

**Variáveis de Ambiente em Produção:**
- `TELEGRAM_BOT_TOKEN` — Token do bot
- `ADMIN_CHAT_ID` — ID do admin
- `ENVIRONMENT=production`
- `TIMEZONE=America/Fortaleza`
- `LUNCH_NOTIFICATION_TIME=10:30`
- `DINNER_NOTIFICATION_TIME=16:30`

**Monitoramento:**
- `docker compose logs --tail=50` para ver logs
- Container com `restart: unless-stopped` reinicia automaticamente
- Volume `./data:/app/data` persiste cache entre rebuilds

**Nota Técnica:**
- Ubuntu 20.04 tem Python 3.8.10 (incompatível com python-telegram-bot 22.6)
- Solução: Docker com imagem oficial `python:3.10-slim` elimina o problema de versão

---

## 6. Tratamento de Erros e Edge Cases

### 6.1. Parsing de PDF Falha

**Cenário:** Formato do PDF mudou ou texto não é extraível.

**Estratégia:**
```python
try:
    menu = extract_menu_from_pdf(pdf_file)
except ParsingException as e:
    # Envia texto bruto ao admin
    send_to_admin(
        "⚠️ Parsing falhou. Revise o texto extraído:\n\n" + raw_text
    )
    # Aguarda correção manual
```

**Futuro:** Comando `/corrigir` permite admin inserir cardápio manualmente.

---

### 6.2. Sem Cardápio Disponível

**Cenário:** Usuário consulta cardápio mas não há dados.

**Resposta:**
```
📭 Cardápio ainda não disponível.

O cardápio da semana será publicado em breve. 
Você receberá notificação automática quando estiver disponível!
```

**Comportamento do Scheduler:**
- Não envia notificações se cardápio ausente
- No domingo às 18h: Verifica cardápio da semana seguinte
- Se ausente: Notifica admin "Lembre-se de fazer upload do cardápio!"

---

### 6.3. Usuário Bloqueia o Bot

**Cenário:** Bot tenta enviar mensagem mas usuário bloqueou.

**Tratamento:**
```python
try:
    bot.send_message(chat_id, text)
except telegram.error.Forbidden:
    # Remove da lista de usuários
    remove_user_from_list(chat_id)
    logger.info(f"User {chat_id} blocked bot, removed from list")
```

---

### 6.4. Bot Offline Durante Horário de Notificação

**Cenário:** Bot reinicia ou está offline às 10:30 ou 16:30.

**Comportamento:**
- APScheduler persiste jobs (não perde agendamento)
- Ao voltar online, **não envia retroativamente** (evita spam)
- Usuários podem consultar manualmente com `/almoco` ou `/janta`

**Mitigação em Produção:**
- Health checks do Railway/Render
- Auto-restart em caso de crash
- Monitoramento de uptime

---

## 7. Segurança e Privacidade

### 7.1. Proteção do Token

**Prática:** Token do bot em variável de ambiente, nunca commitado.

```bash
# .env
TELEGRAM_BOT_TOKEN=123456:ABCdefGHIjklMNOpqrsTUVwxyz

# .env.example (commitado)
TELEGRAM_BOT_TOKEN=your_token_here
```

**Gitignore:**
```
.env
data/users.json
data/menus.json
```

---

### 7.2. Controle de Acesso Admin

**Verificação em comandos privilegiados:**
```python
def upload_command(update, context):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        update.message.reply_text("⛔ Comando restrito a administradores.")
        return
    # Processa upload...
```

**Configuração:**
```python
# src/main.py
ADMIN_IDS = [123456789]  # Seu chat_id
```

**Como obter seu chat_id:**
1. Envie `/start` para @userinfobot
2. Bot responde com seu chat_id
3. Adicione ao código

---

### 7.3. Privacidade dos Usuários

**Dados Coletados:**
- ✅ Chat ID (necessário para enviar mensagens)
- ❌ Nomes, usernames, ou outros dados pessoais

**LGPD/GDPR:**
- Usuário pode se remover com `/parar` (opt-out transparente)
- Dados não são compartilhados com terceiros
- Sem analytics ou tracking

---

## 8. Testes

### 8.1. Estratégia de Testes

**Status atual (15/03/2026):**
- **66/66 testes passando**
- **Cobertura:** 90%

### 8.2. Testes Futuros

**Prioridades para MVP:**

1. **Testes Unitários:**
   - `test_pdf_parser.py` - Validar extração de texto
   - `test_menu_extractor.py` - Validar parsing de estrutura
   - `test_menu_cache.py` - Validar leitura/escrita JSON

2. **Testes de Integração:**
   - Bot responde corretamente a comandos
   - Scheduler executa nos horários corretos (mocks)

3. **Testes Manuais:**
   - Upload de PDF real
   - Comandos via interface do Telegram
   - Notificações agendadas em ambiente de staging

**Framework:** `pytest` + `pytest-asyncio`

**Cobertura Alvo:** >70% para lógica crítica (parser, cache)

---

### 8.2. PDF de Teste

**Disponibilidade:** Admin possui PDF real do RU UFCA.

**Uso:**
- Desenvolver parser com base no formato real
- Criar test fixtures com texto extraído
- Validar estrutura de dados gerada

**Localização:** `tests/fixtures/cardapio_exemplo.pdf`

---

## 9. Dependências do Projeto

### 9.1. Requirements.txt (Produção)

```
python-telegram-bot[job-queue]==22.6
pdfplumber==0.10.3
APScheduler==3.10.4
python-dotenv==1.0.0
pytz==2024.1
```

### 9.2. Requirements-dev.txt

```
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
```

**Justificativas:**
- `python-telegram-bot[job-queue]==22.6`: Versão que suporta Python 3.10+; job-queue para APScheduler
- `pdfplumber`: Parsing de PDFs
- `APScheduler`: Agendamento de tarefas
- `python-dotenv`: Gerenciamento de .env
- `pytz`: Timezone de Fortaleza

---

## 10. Riscos e Mitigações

### 10.1. Formato de PDF Muda

**Risco:** UFCA altera layout do PDF, quebra parser.

**Probabilidade:** Média  
**Impacto:** Alto (bot para de funcionar)

**Mitigação:**
- Parser defensivo (try/except com fallback)
- Notificação automática ao admin se parsing falhar
- Admin pode corrigir manualmente
- Testes com PDFs históricos (se disponíveis)

---

### 10.2. Bot Fica Offline

**Risco:** Servidor local desliga, bot não envia notificações.

**Probabilidade:** Média (desenvolvimento local)  
**Impacto:** Médio (usuários não recebem avisos)

**Mitigação:**
- Documentar processo de restart rápido
- Monitorar uptime manualmente
- Futuro: Migrar para cloud com auto-restart

---

### 10.3. Spam ou Abuso

**Risco:** Usuários spamam comandos, sobrecarregam bot.

**Probabilidade:** Baixa (público universitário)  
**Impacto:** Baixo (API do Telegram tem rate limiting)

**Mitigação:**
- Rate limiting por usuário (se necessário)
- Logs de uso para detectar padrões suspeitos
- Blocklist de usuários abusivos (futuro)

---

### 10.4. Falta de Adoção

**Risco:** Usuários preferem site oficial ou não descobrem bot.

**Probabilidade:** Média  
**Impacto:** Baixo (projeto experimental)

**Mitigação:**
- Divulgação em grupos de estudantes
- QR code em cartazes físicos no RU
- Tornar bot útil e confiável (notificações pontuais)

---

## 11. Métricas de Sucesso (Pós-MVP)

**KPIs sugeridos:**
- Número de usuários ativos (usaram bot nos últimos 7 dias)
- Taxa de retenção semanal
- Comandos mais utilizados
- Uptime do bot (% de disponibilidade)

**Implementação Futura:**
- Logs estruturados (JSON)
- Dashboard simples com estatísticas
- Comando `/stats` para admin

---

## 12. Roadmap de Funcionalidades Futuras

**Possibilidades pós-MVP (não priorizadas):**

- [ ] **Preferências alimentares:** Notificar apenas se houver opção vegetariana
- [ ] **Histórico:** Comando `/historico` para ver cardápios passados
- [ ] **Avaliações:** Usuários podem avaliar refeições (⭐1-5)
- [ ] **Alergênicos:** Destacar ingredientes comuns de alergia
- [ ] **Multilíngua:** Suporte a inglês para alunos estrangeiros
- [ ] **Bot Web:** Interface web para consulta sem Telegram
- [ ] **Integração RU:** API oficial (se UFCA disponibilizar)
- [ ] **Notificações personalizadas:** Usuário escolhe horários
- [ ] **Grupos:** Bot responde em grupos públicos

---

## 13. Referências

**Documentação:**
- [python-telegram-bot docs](https://docs.python-telegram-bot.org/)
- [pdfplumber docs](https://github.com/jsvine/pdfplumber)
- [APScheduler docs](https://apscheduler.readthedocs.io/)

**Inspirações:**
- Bots de cardápio de outras universidades
- @EpicRobotsBot (exemplo de notificações agendadas)

---

## 14. Metodologia de Desenvolvimento: TDD

### 14.1. Estratégia Test-Driven Development

**Decisão:** Adotar TDD (Test-Driven Development) como metodologia principal de desenvolvimento.

**Justificativa:**
- **Qualidade de código:** Testes escritos antes garantem cobertura desde o início
- **Documentação viva:** Testes servem como especificação executável
- **Confiança em refatorações:** Testes pegam regressões imediatamente
- **Design mais limpo:** TDD força pensar na API antes da implementação

**Ciclo TDD (Red-Green-Refactor):**

```
1. 🔴 RED: Escrever teste que FALHA
   - Escrever o teste ANTES do código
   - Executar: teste deve falhar (código não existe ainda)
   - Confirma que o teste está funcionando

2. 🟢 GREEN: Fazer o teste PASSAR
   - Escrever código APENAS para fazer o teste passar
   - Solução mínima e funcional
   - Executar: teste deve passar

3. 🔵 REFACTOR: Melhorar o código
   - Limpar código mantendo testes passando
   - Remover duplicação
   - Melhorar nomenclatura
   - Executar: testes continuam passando
```

### 14.2. Ordem de Implementação TDD

**Sequência escolhida (do mais simples ao mais complexo):**

1. **Cache Layer** (`menu_cache.py`)
   - Sem dependências externas
   - Lógica de I/O simples (JSON)
   - Base para outros módulos
   - **Testes:** 12-15 testes unitários

2. **PDF Parser** (`pdf_parser.py`)
   - Extração de texto com pdfplumber
   - Tratamento de erros
   - **Testes:** 5-7 testes unitários

3. **Menu Extractor** (`menu_extractor.py`)
   - Parsing de estrutura de dados
   - Regex e normalização
   - **Testes:** 8-10 testes unitários

4. **Message Formatter** (`formatter.py`)
   - Formatação de mensagens
   - Templates com emojis
   - **Testes:** 4-6 testes unitários

5. **Bot Handlers** (`handlers.py`)
   - Comandos do Telegram
   - Integração com cache
   - **Testes:** 10-15 testes com mocks

6. **Scheduler** (`scheduler.py`)
   - Notificações agendadas
   - Broadcast de mensagens
   - **Testes:** 6-8 testes com mocks

### 14.3. Ferramentas de Teste

**Framework Principal:** `pytest`

**Bibliotecas Auxiliares:**
- `pytest-asyncio`: Testes assíncronos
- `pytest-cov`: Cobertura de código
- `pytest-mock`: Helpers de mocking
- `unittest.mock`: Mocks para dependências externas

**Configuração (pytest.ini):**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts = -v --tb=short --cov=src --cov-report=term-missing
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
```

### 14.4. Meta de Cobertura

**Cobertura Alvo:** 60-70% (Pragmático)

**Prioridades:**
- ✅ Cobertura alta (>80%): Lógica crítica (parsing, cache)
- ✅ Cobertura média (60-70%): Handlers, formatação
- ⚠️ Cobertura baixa permitida: Código de setup, configuração

**Comandos úteis:**
```bash
# Rodar todos os testes
pytest

# Rodar com cobertura detalhada
pytest --cov=src --cov-report=html

# Rodar apenas testes unitários
pytest -m unit

# Rodar testes em modo verbose
pytest -v
```

### 14.5. Estratégia de Mocking

**Para APIs externas (Telegram):**
- Usar `unittest.mock.Mock` para objetos do Telegram
- Mockar apenas interfaces externas, não lógica interna
- Criar fixtures reutilizáveis para mocks comuns

**Exemplo de mock:**
```python
@pytest.fixture
def mock_telegram_update():
    update = Mock()
    update.effective_user.id = 123456789
    update.message.reply_text = Mock()
    return update
```

### 14.6. Estrutura de Testes

**Organização de diretório tests/:**
```
tests/
├── conftest.py              # Fixtures compartilhadas
├── fixtures/
│   └── cardapio_exemplo.pdf # PDF de teste
├── test_menu_cache.py       # Cache layer
├── test_pdf_parser.py       # PDF parsing
├── test_menu_extractor.py   # Menu extraction
├── test_formatter.py        # Message formatting
├── test_handlers.py         # Bot handlers
└── test_scheduler.py        # Scheduling
```

### 14.7. Boas Práticas Adotadas

1. **AAA Pattern (Arrange-Act-Assert):**
   ```python
   def test_example():
       # Arrange: Preparar dados
       data = create_test_data()
       
       # Act: Executar ação
       result = function_under_test(data)
       
       # Assert: Verificar resultado
       assert result == expected_value
   ```

2. **Testes isolados:**
   - Cada teste independente (sem estado compartilhado)
   - Usar fixtures para setup/teardown
   - Arquivos temporários via `tmp_path`

3. **Nomenclatura clara:**
   - `test_<action>_<expected_result>`
   - Exemplo: `test_save_menu_creates_file_if_not_exists`

4. **Um assert por conceito:**
   - Preferir múltiplos asserts relacionados
   - Evitar testar múltiplas funcionalidades em um teste

---

## 15. Changelog

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-03-14 | Criação do documento inicial | Gustavo Alexandre |
| 2026-03-14 | Adição de seção TDD e metodologia | Gustavo Alexandre |
| 2026-03-14 | Status mudado para "Em Desenvolvimento" | Gustavo Alexandre |
| 2026-03-15 | Status mudado para "Em Produção" | Gustavo Alexandre |
| 2026-03-15 | Adicionada seção de deploy Docker + Oracle Cloud | Gustavo Alexandre |
| 2026-03-15 | Atualizada versão do python-telegram-bot para 22.6 | Gustavo Alexandre |
| 2026-03-15 | Atualizada estrutura de diretórios e comandos do bot | Gustavo Alexandre |
| 2026-03-15 | Simplificados comentários e docstrings (refactor) | Gustavo Alexandre |

---

## 16. Próximos Passos

1. ✅ Revisar e validar documento de arquitetura
2. ✅ Obter PDF de exemplo para análise do formato
3. ✅ Adicionar metodologia TDD ao documento
4. ✅ Setup inicial do projeto (estrutura de diretórios e arquivos)
5. ✅ Implementar Cache Layer (TDD)
6. ✅ Implementar PDF Parser (TDD)
7. ✅ Implementar Menu Extractor (TDD)
8. ✅ Implementar Bot Handlers (TDD)
9. ✅ Implementar Scheduler (TDD)
10. ✅ Testes de integração completos
11. ✅ Deploy em produção (Docker + Oracle Cloud)
12. ⏳ Refatorar comentários e docstrings (concluído)
13. ⏳ Atualizar documento de arquitetura (concluído)

---

**Dúvidas ou sugestões?** Este documento é vivo e deve ser atualizado conforme o projeto evolui.
