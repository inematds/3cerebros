"""Smoke test da F0: Brain cria estrutura, roteia, salva, busca, aplica política."""
import tempfile
from pathlib import Path

from cerebros import Brain


def test_f0_end_to_end():
    with tempfile.TemporaryDirectory() as tmp:
        brain = Brain(tmp)

        # estrutura dos 3 cérebros criada
        for d in ("0-inbox", "1-projeto", "2-self", "3-conhecimento"):
            assert (Path(tmp) / d).is_dir()
        assert (Path(tmp) / "2-self" / "SOUL.md").exists()
        assert (Path(tmp) / "POLICY.md").exists()

        # observe roteia pro cérebro certo
        assert brain.observe("u", "decidi usar Gemini no projeto X") == "projeto"
        assert brain.observe("u", "acho que foco vem antes de escala") == "self"
        assert brain.observe("u", "SQLite FTS5 usa ranking BM25") == "conhecimento"

        # busca por relevância encontra a memória certa
        hits = brain.recall("Gemini projeto")
        assert any("Gemini" in h["content"] for h in hits)

        # filtro por cérebro
        assert all(h["sector"] == "self" for h in brain.recall("foco escala", sector="self"))

        # build_context traz Self + memórias
        ctx = brain.build_context("Gemini")
        assert "Gemini" in ctx

        # política: conservadora por default
        assert brain.policy.check("salvar_nota") == "allow"
        assert brain.policy.check("enviar_mensagem") == "confirm"
        assert brain.policy.check("apagar") == "deny"
        assert brain.policy.check("acao_desconhecida") == "confirm"  # default

        # note() destila no cérebro Conhecimento
        p = brain.note("BM25 é um ranking de relevância usado em busca full-text.")
        assert p.exists() and p.suffix == ".md"

        # stats e dedup
        s = brain.stats()
        assert s["projeto"] >= 1 and s["self"] >= 1 and s["conhecimento"] >= 1
        brain.observe("u", "decidi usar Gemini no projeto X")  # idêntica → dedup
        assert brain.stats()["projeto"] == s["projeto"]

        brain.close()
        print("OK F0:", s)


if __name__ == "__main__":
    test_f0_end_to_end()
