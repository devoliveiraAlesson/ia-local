"""Ponto de entrada da aplicação FastAPI."""

import structlog
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from webhook.handler import router as webhook_router
from agent.rag import ensure_collection

log = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    s = get_settings()
    log.info("bot_starting", chatwoot_url=s.chatwoot_url, model=s.gemini_model)
    await ensure_collection()
    log.info("qdrant_ready")
    yield
    log.info("bot_stopping")


app = FastAPI(
    title="Chatwoot Gemini Bot",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhook_router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/")
async def root():
    return {
        "service": "Chatwoot Gemini Bot",
        "docs": "/docs",
        "webhook": "/api/v1/webhook",
        "health": "/health",
    }
