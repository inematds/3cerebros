"""Destilação: raw -> nota-átomo do cérebro Conhecimento.

F0: destilação trivial (passa o conteúdo, gera título por heurística). A versão
real (F2) usa o LLM do host pra destilar em nota-wiki com [[wikilinks]].
"""
from __future__ import annotations

import re


def slug(text: str, maxlen: int = 60) -> str:
    s = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    s = re.sub(r"\s+", "-", s)
    return s[:maxlen] or "nota"


def distill(content: str, llm=None) -> dict:
    """Retorna {'title', 'body'} de uma fonte crua.

    Se `llm` (callable que recebe prompt e devolve texto) for dado, usa-o pra
    destilar. Sem llm (F0), faz uma destilação mínima determinística.
    """
    content = (content or "").strip()
    if llm:
        prompt = (
            "Destile o texto abaixo em UMA nota-átomo de conhecimento. "
            "Responda com a primeira linha = título curto, e o resto = 2-4 "
            "frases com a ideia essencial, com suas palavras.\n\n" + content
        )
        out = llm(prompt).strip()
        first, _, rest = out.partition("\n")
        return {"title": first.strip("# ").strip(), "body": rest.strip() or out}
    # F0: título = primeira linha/frase; corpo = o conteúdo.
    first = content.splitlines()[0] if content else "nota"
    title = first[:80]
    return {"title": title, "body": content}
