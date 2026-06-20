"""Brain — a API pública do 3cerebros.

O contrato mínimo que qualquer host (intelecto, openpcbot, cerebro-inema, um
agente de terceiros) precisa conhecer pra incorporar o cérebro:

    brain = Brain("~/.cerebros")
    system = brain.build_context(query, who)   # Self + memórias relevantes
    brain.observe(who, user_msg, ai_reply)     # triagem + save autônomo
    brain.policy.check(action)                 # allow | confirm | deny
    brain.run_jobs()                           # manutenção (cron chama)
    brain.ingest(source)                       # importar export (F3)
"""
from __future__ import annotations

from pathlib import Path

from .distill import distill, slug
from .format import SECTORS, ensure_brain
from .memory import Memory
from .policy import Policy
from .triage import triage

DEFAULT_PATH = "~/.cerebros"


class Brain:
    def __init__(self, path: str | Path = DEFAULT_PATH, max_context: int = 8):
        self.root = ensure_brain(path)
        self.max_context = max_context
        self.memory = Memory(self.root / "memory.db")
        self.policy = Policy(self.root / "POLICY.md")

    # ---- leitura de arquivos do cérebro Self ----
    def _read(self, rel: str) -> str:
        f = self.root / rel
        return f.read_text(encoding="utf-8").strip() if f.exists() else ""

    # ---- API pública ----
    def build_context(self, query: str = "", who: str | None = None) -> str:
        """Monta o system prompt: identidade (Self) + memórias relevantes."""
        parts: list[str] = []
        soul = self._read("2-self/SOUL.md")
        if soul:
            parts.append(soul)
        values = self._read("2-self/values.md")
        if values:
            parts.append(values)
        mems = self.memory.search(query, limit=self.max_context) if query else []
        if mems:
            lines = [f"- [{m['sector']}] {m['content']}" for m in mems]
            parts.append("# Memórias relevantes\n" + "\n".join(lines))
        return "\n\n".join(parts).strip()

    def observe(self, who: str | None, user_msg: str, ai_reply: str | None = None) -> str:
        """Roteia a mensagem pro cérebro certo e salva (se a política permitir).

        Retorna o setor escolhido. `salvar_nota` é 'allow' por default → autônomo.
        """
        sector, category = triage(user_msg)
        if self.policy.check("salvar_nota") != "deny":
            self.memory.save(user_msg, sector=sector, category=category, who=who)
        return sector

    def remember(self, content: str, sector: str = "conhecimento", category: str = "fact",
                 who: str | None = None) -> int | None:
        """Salva uma memória explicitamente (setor à escolha)."""
        if sector not in SECTORS:
            raise ValueError(f"setor inválido: {sector!r} (use {SECTORS})")
        return self.memory.save(content, sector=sector, category=category, who=who)

    def recall(self, query: str, sector: str | None = None, limit: int = 10) -> list[dict]:
        """Busca memórias por relevância (BM25), opcionalmente filtrando por cérebro."""
        return self.memory.search(query, sector=sector, limit=limit)

    def note(self, content: str, llm=None) -> Path:
        """Destila um conteúdo cru em nota-wiki no cérebro Conhecimento."""
        d = distill(content, llm=llm)
        path = self.root / "3-conhecimento" / "notes" / f"{slug(d['title'])}.md"
        path.write_text(f"# {d['title']}\n\n{d['body']}\n", encoding="utf-8")
        self.memory.save(d["body"], sector="conhecimento", category="note")
        return path

    def ingest(self, source: str, path: str | None = None) -> int:
        """Importa itens de uma fonte externa pra inbox (F3)."""
        from . import ingest as _ingest

        n = 0
        for item in _ingest.load(source, path):
            (self.root / "0-inbox" / f"{source}-{n}.md").write_text(item, encoding="utf-8")
            n += 1
        return n

    def run_jobs(self) -> dict:
        """Manutenção autônoma (cron chama). F0: relata o que faria, sob política."""
        plan = {
            "triagem_inbox": self.policy.check("triagem"),
            "briefing_diario": self.policy.check("atualizar_daily"),
            "saude_cerebro": "allow",
        }
        return {"status": "F0-stub", "would_run": plan, "memorias": self.stats()}

    def stats(self) -> dict:
        return {s: self.memory.count(s) for s in SECTORS}

    def close(self) -> None:
        self.memory.close()
