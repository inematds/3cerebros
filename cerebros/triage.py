"""Triagem: roteia um texto para o cérebro certo (projeto / self / conhecimento).

F0: heurística por palavras-chave (PT/EN), determinística e sem custo.
Futuro (F2): triagem por LLM quando ambíguo.
"""
from __future__ import annotations

import re

# Cérebro Self: identidade, opinião, dúvida, sentimento.
_SELF = [
    r"\bacho\b", r"\bacredito\b", r"\bpenso\b", r"\bsinto\b", r"\bvalor(es)?\b",
    r"\bd[úu]vida\b", r"\bser[áa] que\b", r"\bquero ser\b", r"\bme incomoda\b",
    r"\bi think\b", r"\bi believe\b", r"\bi feel\b", r"\bi value\b",
]
# Cérebro Projeto: o que rolou, decisão, trabalho, prazo.
_PROJETO = [
    r"\bdecid\w+\b", r"\bdecis[ãa]o\b", r"\bprojeto\b", r"\bcliente\b",
    r"\bdeploy\b", r"\bprazo\b", r"\breuni[ãa]o\b", r"\btarefa\b",
    r"\bpr[óo]xim\w+\b", r"\bentreg\w+\b", r"\bbug\b", r"\bsprint\b",
    r"\bdecided\b", r"\bdeadline\b", r"\bmeeting\b", r"\btask\b",
]

_SELF_RE = re.compile("|".join(_SELF), re.I)
_PROJETO_RE = re.compile("|".join(_PROJETO), re.I)


def triage(text: str) -> tuple[str, str]:
    """Retorna (setor, categoria) para um texto.

    setor ∈ {projeto, self, conhecimento}. Default = conhecimento (fato).
    """
    t = text or ""
    if _SELF_RE.search(t):
        return ("self", "reflection")
    if _PROJETO_RE.search(t):
        return ("projeto", "note")
    return ("conhecimento", "fact")
