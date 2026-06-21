"""Importador: export do Telegram (`result.json`).

Aceita tanto o export de um chat (`{"messages": [...]}`) quanto o export geral
(`{"chats": {"list": [{"messages": [...]}]}}`). `text` pode ser string ou uma
lista de entidades — normalizamos para texto puro.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


def _text(t) -> str:
    if isinstance(t, str):
        return t
    if isinstance(t, list):
        return "".join(x if isinstance(x, str) else x.get("text", "") for x in t)
    return ""


def _messages(obj) -> list:
    if isinstance(obj, dict):
        if "messages" in obj:
            return obj["messages"]
        if "chats" in obj:
            out = []
            for ch in obj["chats"].get("list", []):
                out.extend(ch.get("messages", []))
            return out
    return []


def load_items(path: str) -> Iterable[str]:
    data = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    for m in _messages(data):
        if not isinstance(m, dict) or m.get("type") != "message":
            continue
        txt = _text(m.get("text")).strip()
        if not txt:
            continue
        who = m.get("from") or m.get("actor") or "?"
        yield f"**{who}:** {txt}"
