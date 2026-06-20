"""Conectores de ingestão (F3): export do ChatGPT, Telegram, email, etc.

Cada importador normaliza uma fonte externa em itens de texto que caem na inbox
do cérebro (depois roteados por triagem). F0: contrato + stub.
"""
from __future__ import annotations

from typing import Iterable

# Importadores planejados (F3) — implementados reusando ferramentas existentes:
#   chatgpt_export : conversations.json (árvore) -> itens
#   telegram       : export JSON -> itens
#   email          : .mbox / MCP Gmail -> itens
SUPPORTED = ("chatgpt_export", "telegram", "email")


def load(source: str, path: str | None = None) -> Iterable[str]:
    """Carrega itens de texto de uma fonte. F0: ainda não implementado."""
    raise NotImplementedError(
        f"ingest '{source}' chega na F3. Fontes planejadas: {', '.join(SUPPORTED)}"
    )
