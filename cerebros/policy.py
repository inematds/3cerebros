"""Política de automação — o diferencial do 3cerebros.

Define o que o cérebro pode fazer SOZINHO vs o que pede confirmação vs nunca.
Lê regras de um POLICY.md (formato `acao: nivel`). Default conservador.
Níveis: 'allow' (faz sozinho) · 'confirm' (pede ok) · 'deny' (bloqueado).
"""
from __future__ import annotations

import re
from pathlib import Path

LEVELS = ("allow", "confirm", "deny")

# Default conservador: na dúvida, pede confirmação; ações destrutivas, nega.
DEFAULT_RULES = {
    "salvar_nota": "allow",
    "arquivar": "allow",
    "atualizar_daily": "allow",
    "triagem": "allow",
    "registrar_decisao": "confirm",
    "mover_cerebro": "confirm",
    "enviar_mensagem": "confirm",
    "postar": "confirm",
    "rodar_shell": "confirm",
    "apagar": "deny",
    "comprar": "deny",
    "pagar": "deny",
}

_RULE_RE = re.compile(r"^\s*([a-z0-9_]+)\s*[:=]\s*(allow|confirm|deny)\s*$", re.I)


class Policy:
    def __init__(self, policy_path: str | Path | None = None, default: str = "confirm"):
        self.default = default if default in LEVELS else "confirm"
        self.rules = dict(DEFAULT_RULES)
        if policy_path and Path(policy_path).exists():
            self._load(Path(policy_path))

    def _load(self, path: Path) -> None:
        for line in path.read_text(encoding="utf-8").splitlines():
            m = _RULE_RE.match(line.lstrip("-* "))
            if m:
                self.rules[m.group(1).lower()] = m.group(2).lower()

    def check(self, action: str) -> str:
        """Retorna 'allow' | 'confirm' | 'deny' para uma ação."""
        return self.rules.get(action, self.default)

    def can_auto(self, action: str) -> bool:
        """Atalho: True só se a ação pode ser feita sem confirmação."""
        return self.check(action) == "allow"
