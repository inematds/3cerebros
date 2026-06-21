"""F4: a CLI opera o cérebro ponta a ponta (init/observe/recall/policy/stats)."""
import io
import tempfile
from contextlib import redirect_stdout

from cerebros import cli


def _run(args) -> str:
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = cli.main(args)
    assert rc == 0
    return buf.getvalue()


def test_cli_end_to_end():
    with tempfile.TemporaryDirectory() as tmp:
        out = _run(["--brain", tmp, "init", "--auto"])
        assert "rules" in out and "POLICY.md" in out

        _run(["--brain", tmp, "observe", "decidi usar Postgres no projeto", "--who", "u"])
        assert "Postgres" in _run(["--brain", tmp, "recall", "Postgres"])

        assert "deny" in _run(["--brain", tmp, "policy", "apagar"])
        assert "projeto" in _run(["--brain", tmp, "stats"])

        note_path = _run(["--brain", tmp, "note", "BM25 ranqueia relevância em busca full-text"])
        assert ".md" in note_path


def test_cli_mcp_module_imports():
    # módulo importável sem o SDK MCP (import do SDK é lazy dentro de build_server)
    import cerebros.mcp.server as s
    assert hasattr(s, "build_server") and hasattr(s, "main")
