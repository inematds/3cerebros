"""MCP server do 3cerebros (F4) — expõe o Brain como tools p/ qualquer runtime.

É o curinga da distribuição: qualquer agente que fale MCP (Claude Code, Codex,
Gemini CLI, terceiros) pluga no mesmo cérebro sem precisar de SDK.

Requer o SDK MCP (dependência opcional):
    pip install 'cerebros[mcp]'

Rodar:
    cerebros mcp                       # usa ~/.cerebros (ou $CEREBROS_PATH)
    python -m cerebros.mcp.server
"""
from __future__ import annotations

import os

from ..brain import DEFAULT_PATH, Brain


def build_server(path: str | None = None):
    """Cria o FastMCP com as tools do Brain. Lança erro claro se faltar o SDK."""
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as e:  # pragma: no cover - depende de extra opcional
        raise SystemExit(
            "SDK MCP não instalado. Rode: pip install 'cerebros[mcp]'"
        ) from e

    brain = Brain(path or os.environ.get("CEREBROS_PATH") or DEFAULT_PATH)
    mcp = FastMCP("3cerebros")

    @mcp.tool()
    def build_context(query: str = "", who: str = "") -> str:
        """System prompt: identidade (Self) + memórias relevantes."""
        return brain.build_context(query, who or None)

    @mcp.tool()
    def observe(user_msg: str, who: str = "", ai_reply: str = "") -> str:
        """Roteia uma mensagem pro cérebro certo e salva (autônomo, sob política). Retorna o setor."""
        return brain.observe(who or None, user_msg, ai_reply or None)

    @mcp.tool()
    def remember(content: str, sector: str = "conhecimento", category: str = "fact") -> str:
        """Salva uma memória explícita num setor (projeto|self|conhecimento)."""
        rid = brain.remember(content, sector=sector, category=category)
        return f"saved #{rid} em {sector}"

    @mcp.tool()
    def recall(query: str, sector: str = "", limit: int = 10) -> list:
        """Busca memórias por relevância (BM25)."""
        return brain.recall(query, sector=sector or None, limit=limit)

    @mcp.tool()
    def note(content: str) -> str:
        """Destila um texto cru numa nota do cérebro Conhecimento."""
        return str(brain.note(content))

    @mcp.tool()
    def ingest(source: str, path: str) -> str:
        """Importa uma fonte externa (chatgpt_export|telegram|email|files) pra inbox."""
        return f"ingeridos {brain.ingest(source, path)} itens"

    @mcp.tool()
    def run_jobs() -> dict:
        """Manutenção autônoma (triagem do inbox, briefing, saúde), sob política."""
        return brain.run_jobs()

    @mcp.tool()
    def policy_check(action: str) -> str:
        """Verdito da política p/ uma ação: allow | confirm | deny."""
        return brain.policy.check(action)

    @mcp.tool()
    def stats() -> dict:
        """Contagem de memórias por cérebro."""
        return brain.stats()

    return mcp


def main(path: str | None = None) -> None:
    build_server(path).run()


if __name__ == "__main__":
    main()
