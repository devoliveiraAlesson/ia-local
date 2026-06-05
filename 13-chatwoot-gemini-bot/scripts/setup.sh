#!/usr/bin/env bash
# Setup inicial — rode UMA VEZ após subir os containers
set -e

echo "═══════════════════════════════════════════"
echo "  Chatwoot Gemini Bot — Setup Inicial"
echo "═══════════════════════════════════════════"

# 1. Verifica se .env existe
if [ ! -f .env ]; then
  echo "[1/4] Criando .env a partir do exemplo..."
  cp .env.example .env
  echo "      → Edite o .env com suas credenciais antes de continuar."
  echo "      → Rode este script novamente após configurar."
  exit 1
fi

echo "[1/4] .env encontrado."

# 2. Sobe os containers base (sem o bot ainda)
echo "[2/4] Subindo Chatwoot, banco de dados e Qdrant..."
docker compose up -d chatwoot_db chatwoot_redis qdrant

echo "      Aguardando banco de dados..."
sleep 15

# 3. Prepara o banco do Chatwoot (apenas primeira vez)
echo "[3/4] Rodando migrações do Chatwoot..."
docker compose run --rm chatwoot_web bundle exec rails db:chatwoot_prepare

# 4. Sobe tudo
echo "[4/4] Subindo todos os serviços..."
docker compose up -d

echo ""
echo "═══════════════════════════════════════════"
echo "  Serviços disponíveis:"
echo "  → Chatwoot UI:  http://localhost:3000"
echo "  → Bot API:      http://localhost:8000"
echo "  → Bot Docs:     http://localhost:8000/docs"
echo "  → Qdrant UI:    http://localhost:6333/dashboard"
echo ""
echo "  Próximos passos:"
echo "  1. Acesse http://localhost:3000 e crie sua conta de superadmin"
echo "  2. Em Configurações > Integrações > API, gere um token"
echo "  3. Cole o token em CHATWOOT_API_TOKEN no .env"
echo "  4. Crie uma Inbox e copie o ID para BOT_INBOX_ID no .env"
echo "  5. Configure o webhook da Inbox para: http://bot:8000/api/v1/webhook"
echo "  6. Reinicie o bot: docker compose restart bot"
echo "  7. Indexe sua base de conhecimento: docker compose exec bot python /app/../scripts/ingest_kb.py"
echo "═══════════════════════════════════════════"
