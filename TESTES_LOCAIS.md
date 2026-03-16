# Testes Locais

## Setup

```bash
# Criar ambiente virtual (se não existir)
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Rodar testes
pytest
```

## Testar Bot Localmente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env com seu token de bot
# (obtenha em @BotFather)

# Rodar o bot
python -m src.main
```

## Deploy para Produção

```bash
# No servidor de produção:
cd ru-ufca-bot
git pull
docker compose up -d --build
```

## Fluxo Simples

1. Faz as alterações localmente
2. Rode `pytest` para verificar se tudo passa
3. Teste manualmente (envie commands no Telegram se quiser)
4. Commit e push: `git add . && git commit -m "mensagem" && git push`
5. Deploy: `ssh ubuntu@164.152.45.38 "cd ru-ufca-bot && git pull && docker compose up -d --build"`
