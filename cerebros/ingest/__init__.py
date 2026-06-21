"""Conectores de ingestão (F3): export do ChatGPT, Telegram, email, arquivos.

Cada importador normaliza uma fonte externa em itens de texto. `Brain.ingest`
joga cada item na inbox; o `run_jobs` (F2) roteia depois por triagem.

Tudo stdlib — sem dependência. O host só aponta o `path` da fonte.
"""
from __future__ import annotations

from typing import Iterable

from . import chatgpt, files
from . import email as _email
from . import telegram

# Fontes suportadas (e seus apelidos).
SUPPORTED = ("chatgpt_export", "telegram", "email", "files")

_LOADERS = {
    "chatgpt_export": chatgpt.load_items,
    "chatgpt": chatgpt.load_items,
    "telegram": telegram.load_items,
    "email": _email.load_items,
    "mbox": _email.load_items,
    "files": files.load_items,
    "markdown": files.load_items,
    "text": files.load_items,
    "directory": files.load_items,
}


def load(source: str, path: str | None = None) -> Iterable[str]:
    """Carrega itens de texto de uma fonte externa."""
    key = (source or "").lower()
    if key not in _LOADERS:
        raise ValueError(
            f"fonte {source!r} não suportada. Use: {', '.join(SUPPORTED)}"
        )
    if not path:
        raise ValueError(f"ingest {source!r} precisa de path= (arquivo/pasta da fonte)")
    yield from _LOADERS[key](path)
