"""Formato do cérebro: estrutura de pastas dos 3 cérebros + seeds.

A estrutura é a "constituição" do 3cerebros (ver spec/FORMAT.md). `ensure_brain`
materializa um cérebro vazio em qualquer caminho — sem depender de template externo,
pra ser embutível por qualquer host.
"""
from __future__ import annotations

from pathlib import Path

# Os 3 cérebros + a inbox de captura. Sub-pastas por cérebro.
DIRS = [
    "0-inbox",
    "1-projeto/daily",
    "1-projeto/projects",
    "1-projeto/decisions",
    "1-projeto/archive",
    "2-self/questions",
    "2-self/thinking",
    "2-self/journal",
    "3-conhecimento/sources",
    "3-conhecimento/notes",
    "3-conhecimento/topics",
]

# Setores válidos (1 por cérebro) — usados na memória e na triagem.
SECTORS = ("projeto", "self", "conhecimento")

# Onde a triagem (F2) arquiva o .md de cada setor, ao esvaziar a inbox.
SECTOR_DIR = {
    "projeto": "1-projeto/projects",
    "self": "2-self/journal",
    "conhecimento": "3-conhecimento/notes",
}

SEED_SOUL = """# SOUL — Quem eu sou (cérebro Self)

> A personalidade do agente. Se este cérebro alimenta um jarvis, este arquivo
> É a alma dele. Edite à vontade. Carregado em todo `build_context`.

- **Nome:**
- **Tom:** direto, honesto, sem enrolação.
- **O que faço:**
- **O que me guia:** ver [[values]]
"""

SEED_VALUES = """# Valores (cérebro Self)

> Princípios estáveis. Consultados quando uma decisão é difícil.

1.
2.
3.

## Linha vermelha (o que eu nunca faço)
-
"""

SEED_DECISIONS = """# Log de Decisões (cérebro Projeto)

> Append-only. Cada decisão: data + razão + contexto.

<!-- adicione decisões abaixo -->
"""

SEED_INBOX = """# 0-inbox — Captura

Jogue tudo aqui sem classificar. `brain.observe()` / `/triagem` roteia depois
pro cérebro certo (projeto / self / conhecimento).
"""

SEED_CLAUDE = """# CLAUDE.md — roteador do cérebro (3cerebros)

Três cérebros que não se misturam:
- `1-projeto/`      o que rolou, decisões, estado (episódico)
- `2-self/`         quem eu sou, valores, dúvidas (identidade)
- `3-conhecimento/` fatos, o que aprendi (referência)

Entrada: `0-inbox/` (captura) → triagem roteia. Política em `POLICY.md`.
Memória full-text em `memory.db` (SQLite FTS5).
"""

# Política seed — conservadora por padrão (o usuário solta depois).
SEED_POLICY = """# POLICY — Política de automação

> O que o cérebro pode fazer SOZINHO vs o que pede confirmação.
> Níveis: allow (faz sozinho) · confirm (pede ok) · deny (nunca).
> Formato de regra (uma por linha):  `acao: nivel`

salvar_nota: allow
arquivar: allow
atualizar_daily: allow
triagem: allow
registrar_decisao: confirm
mover_cerebro: confirm
enviar_mensagem: confirm
postar: confirm
rodar_shell: confirm
apagar: deny
comprar: deny
pagar: deny
"""

_SEEDS = {
    "2-self/SOUL.md": SEED_SOUL,
    "2-self/values.md": SEED_VALUES,
    "1-projeto/decisions/log.md": SEED_DECISIONS,
    "0-inbox/README.md": SEED_INBOX,
    "CLAUDE.md": SEED_CLAUDE,
    "POLICY.md": SEED_POLICY,
}


def ensure_brain(path: Path) -> Path:
    """Cria a estrutura dos 3 cérebros em `path` se ainda não existir.

    Idempotente: não sobrescreve seeds já editados. Retorna o caminho resolvido.
    """
    root = Path(path).expanduser()
    root.mkdir(parents=True, exist_ok=True)
    for d in DIRS:
        (root / d).mkdir(parents=True, exist_ok=True)
    for rel, content in _SEEDS.items():
        f = root / rel
        if not f.exists():
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(content, encoding="utf-8")
    return root
