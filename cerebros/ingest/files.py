"""Importador: arquivos/pasta de `.md`/`.txt` soltos.

Aponta pra um arquivo único ou uma pasta (varre recursivo). Cada arquivo com
texto vira um item.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

EXTS = {".md", ".markdown", ".txt"}


def load_items(path: str) -> Iterable[str]:
    p = Path(path).expanduser()
    if p.is_file():
        targets = [p]
    else:
        targets = sorted(f for f in p.rglob("*") if f.suffix.lower() in EXTS)
    for f in targets:
        txt = f.read_text(encoding="utf-8", errors="replace").strip()
        if txt:
            yield txt
