"""F2: run_jobs roteia o inbox, indexa, escreve briefing — tudo sob política."""
import tempfile
from pathlib import Path

from cerebros import Brain


def test_run_jobs_triage_index_and_briefing():
    with tempfile.TemporaryDirectory() as tmp:
        brain = Brain(tmp)
        inbox = brain.root / "0-inbox"
        (inbox / "a.md").write_text("decidi migrar pra Postgres no projeto X", encoding="utf-8")
        (inbox / "b.md").write_text("acho que simplicidade vale mais que features", encoding="utf-8")
        (inbox / "c.md").write_text("Fernet usa AES-128-CBC e HMAC-SHA256", encoding="utf-8")

        report = brain.run_jobs()
        ran = report["ran"]

        # triagem rodou (política triagem=allow) e moveu os 3 arquivos
        assert len(ran["triagem_inbox"]["processed"]) == 3
        assert not (inbox / "a.md").exists()
        # indexados e buscáveis
        assert any("Postgres" in h["content"] for h in brain.recall("Postgres projeto"))
        # briefing do dia escrito
        dailies = list((brain.root / "1-projeto" / "daily").glob("*.md"))
        assert len(dailies) == 1
        # saúde: inbox zerada
        assert ran["saude_cerebro"]["inbox_pendente"] == 0
        brain.close()


def test_run_jobs_respects_confirm_policy():
    with tempfile.TemporaryDirectory() as tmp:
        brain = Brain(tmp)
        brain.policy.rules["triagem"] = "confirm"
        (brain.root / "0-inbox" / "a.md").write_text("decidi algo no projeto", encoding="utf-8")

        report = brain.run_jobs()
        # não rodou: virou pendente e o arquivo continua na inbox
        assert "triagem_inbox" in report["pending"]
        assert (brain.root / "0-inbox" / "a.md").exists()
        brain.close()


def test_act_gates_by_policy():
    with tempfile.TemporaryDirectory() as tmp:
        brain = Brain(tmp)
        calls = []
        r = brain.act("salvar_nota", do=lambda: calls.append("did") or "ok")  # allow
        assert r["verdict"] == "allow" and r["result"] == "ok" and calls == ["did"]
        r = brain.act("apagar", do=lambda: calls.append("deleted"))           # deny
        assert r["verdict"] == "deny" and calls == ["did"]                    # não rodou
        r = brain.act("enviar_mensagem", do=lambda: 1, on_confirm=lambda: "pediu ok")
        assert r["verdict"] == "confirm" and r["result"] == "pediu ok"
        brain.close()
