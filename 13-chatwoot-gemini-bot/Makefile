.PHONY: setup up down logs bot-logs ingest restart-bot shell

setup:
	chmod +x scripts/setup.sh && bash scripts/setup.sh

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

bot-logs:
	docker compose logs -f bot

ingest:
	docker compose exec bot python /scripts/ingest_kb.py

restart-bot:
	docker compose restart bot

shell-bot:
	docker compose exec bot bash

chatwoot-prepare:
	docker compose run --rm chatwoot_web bundle exec rails db:chatwoot_prepare
