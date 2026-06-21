"""Memória do cérebro: SQLite FTS5 + ranking BM25, setor por cérebro.

Sem embeddings, sem API externa, sem custo. Busca full-text com relevância.
Cada memória pertence a um setor (projeto / self / conhecimento).
"""
from __future__ import annotations

import re
import sqlite3
import time
from pathlib import Path


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())


def _fts_query(q: str) -> str:
    """Converte texto livre em uma query FTS5 segura (evita erro de sintaxe)."""
    terms = re.findall(r"\w+", q, flags=re.UNICODE)
    return " OR ".join(terms)


class Memory:
    def __init__(self, db_path: str | Path):
        self.db = sqlite3.connect(str(db_path))
        self.db.row_factory = sqlite3.Row
        self._init()

    def _init(self) -> None:
        self.db.execute(
            """CREATE VIRTUAL TABLE IF NOT EXISTS memories USING fts5(
                   content,
                   sector UNINDEXED,
                   category UNINDEXED,
                   who UNINDEXED,
                   created_at UNINDEXED
               )"""
        )
        self.db.commit()

    def save(
        self,
        content: str,
        sector: str = "conhecimento",
        category: str = "fact",
        who: str | None = None,
    ) -> int | None:
        """Salva uma memória. Dedup simples: ignora conteúdo idêntico no mesmo setor."""
        content = (content or "").strip()
        if not content:
            return None
        norm = _norm(content)
        for row in self.db.execute(
            "SELECT rowid, content FROM memories WHERE sector = ?", (sector,)
        ):
            if _norm(row["content"]) == norm:
                return row["rowid"]
        cur = self.db.execute(
            "INSERT INTO memories(content, sector, category, who, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (content, sector, category, who, int(time.time())),
        )
        self.db.commit()
        return cur.lastrowid

    def search(
        self, query: str, sector: str | None = None, limit: int = 10
    ) -> list[dict]:
        """Busca full-text com ranking BM25. Filtra por setor se informado."""
        q = _fts_query(query or "")
        if not q:
            return []
        sql = (
            "SELECT content, sector, category, who, created_at, "
            "bm25(memories) AS rank FROM memories WHERE memories MATCH ?"
        )
        args: list = [q]
        if sector:
            sql += " AND sector = ?"
            args.append(sector)
        sql += " ORDER BY rank LIMIT ?"
        args.append(limit)
        try:
            return [dict(r) for r in self.db.execute(sql, args)]
        except sqlite3.OperationalError:
            return []

    def recent(self, limit: int = 10, sector: str | None = None) -> list[dict]:
        """Memórias mais recentes (por created_at), opcionalmente de um setor."""
        sql = "SELECT content, sector, category, who, created_at FROM memories"
        args: list = []
        if sector:
            sql += " WHERE sector = ?"
            args.append(sector)
        sql += " ORDER BY created_at DESC, rowid DESC LIMIT ?"
        args.append(limit)
        return [dict(r) for r in self.db.execute(sql, args)]

    def count(self, sector: str | None = None) -> int:
        if sector:
            row = self.db.execute(
                "SELECT count(*) AS n FROM memories WHERE sector = ?", (sector,)
            ).fetchone()
        else:
            row = self.db.execute("SELECT count(*) AS n FROM memories").fetchone()
        return int(row["n"])

    def close(self) -> None:
        self.db.close()
