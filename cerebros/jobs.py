"""Autonomia (F2): tarefas de manutenção que o cron dispara via brain.run_jobs().

Cada job é governado pela POLÍTICA — nada sai do lugar sem o nível certo.
Jobs:
  - triagem_inbox  : roteia os arquivos de 0-inbox/ pro cérebro certo + indexa
  - briefing_diario: escreve 1-projeto/daily/<data>.md com o resumo recente
  - saude_cerebro  : conta memórias, mede o inbox parado e o tamanho do db
"""
from __future__ import annotations

import datetime as _dt

from .distill import slug
from .format import SECTOR_DIR
from .triage import triage

INBOX_SKIP = {"README.md"}


def _today() -> str:
    return _dt.date.today().isoformat()


def _unique(path):
    """Evita sobrescrever: nota.md → nota-1.md → nota-2.md …"""
    if not path.exists():
        return path
    i = 1
    while True:
        cand = path.with_name(f"{path.stem}-{i}{path.suffix}")
        if not cand.exists():
            return cand
        i += 1


def triagem_inbox(brain, do: bool = True) -> dict:
    """Roteia cada arquivo do inbox pro cérebro certo, indexa e move o .md."""
    inbox = brain.root / "0-inbox"
    processed, pending = [], []
    for f in sorted(inbox.glob("*.md")):
        if f.name in INBOX_SKIP:
            continue
        text = f.read_text(encoding="utf-8").strip()
        if not text:
            continue
        sector, category = triage(text)
        if not do:
            pending.append({"file": f.name, "sector": sector})
            continue
        brain.memory.save(text, sector=sector, category=category, who="inbox")
        dest_dir = brain.root / SECTOR_DIR[sector]
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = _unique(dest_dir / f"{slug(text.splitlines()[0])}.md")
        f.rename(dest)
        processed.append({"file": f.name, "sector": sector,
                          "to": str(dest.relative_to(brain.root))})
    return {"processed": processed, "pending": pending}


def briefing_diario(brain, limit: int = 12) -> dict:
    """Escreve o briefing do dia a partir das memórias mais recentes."""
    recents = brain.memory.recent(limit=limit)
    lines = [f"# Briefing {_today()}", "",
             f"_{len(recents)} memórias recentes:_", ""]
    lines += [f"- [{m['sector']}] {m['content']}" for m in recents]
    path = brain.root / "1-projeto" / "daily" / f"{_today()}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"file": str(path.relative_to(brain.root)), "memorias": len(recents)}


def saude_cerebro(brain) -> dict:
    """Métricas rápidas do cérebro (sempre permitido — só lê)."""
    inbox = [f for f in (brain.root / "0-inbox").glob("*.md")
             if f.name not in INBOX_SKIP]
    db = brain.root / "memory.db"
    return {
        "setores": brain.stats(),
        "inbox_pendente": len(inbox),
        "db_kb": round(db.stat().st_size / 1024, 1) if db.exists() else 0,
    }


def run(brain) -> dict:
    """Roda todos os jobs, cada um sob seu nível de política."""
    report: dict = {"ran": {}, "pending": {}, "skipped": {}}

    v = brain.policy.check("triagem")
    if v == "allow":
        report["ran"]["triagem_inbox"] = triagem_inbox(brain, do=True)
    elif v == "confirm":
        report["pending"]["triagem_inbox"] = triagem_inbox(brain, do=False)
    else:
        report["skipped"]["triagem_inbox"] = v

    v = brain.policy.check("atualizar_daily")
    if v == "allow":
        report["ran"]["briefing_diario"] = briefing_diario(brain)
    elif v == "confirm":
        report["pending"]["briefing_diario"] = "aguardando ok"
    else:
        report["skipped"]["briefing_diario"] = v

    # saúde só lê → sempre roda
    report["ran"]["saude_cerebro"] = saude_cerebro(brain)
    return report
