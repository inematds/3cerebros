"""Importador: export do ChatGPT (`conversations.json`).

O export é uma lista de conversas; cada uma tem um `mapping` (árvore de nós).
Reconstruímos cada conversa em ordem cronológica como um item de texto.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


def _parts_text(parts) -> str:
    out = []
    for p in parts or []:
        if isinstance(p, str):
            out.append(p)
        elif isinstance(p, dict):
            t = p.get("text") or p.get("content")
            if isinstance(t, str):
                out.append(t)
    return " ".join(x for x in out if x).strip()


def load_items(path: str) -> Iterable[str]:
    data = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    convos = data if isinstance(data, list) else data.get("conversations", [data])
    for c in convos:
        if not isinstance(c, dict):
            continue
        title = c.get("title") or "conversa"
        mapping = c.get("mapping") or {}
        msgs = []
        for node in mapping.values():
            m = (node or {}).get("message")
            if not m:
                continue
            role = (m.get("author") or {}).get("role")
            if role not in ("user", "assistant"):
                continue
            txt = _parts_text((m.get("content") or {}).get("parts"))
            if txt:
                msgs.append((m.get("create_time") or 0, role, txt))
        if not msgs:
            continue
        msgs.sort(key=lambda x: x[0] or 0)
        body = "\n".join(f"**{r}:** {t}" for _, r, t in msgs)
        yield f"# {title}\n\n{body}"
