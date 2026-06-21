"""F1: a entrevista gera SOUL/values/POLICY e a política reflete as respostas."""
import tempfile

from cerebros import Brain
from cerebros.interview import Interview, build_policy, build_profile


def test_interview_generates_self_and_policy():
    with tempfile.TemporaryDirectory() as tmp:
        brain = Brain(tmp)
        answers = {
            "name": "Jarvis",
            "tone": "seco e direto",
            "mission": "organizar minha vida e meu trabalho",
            "values": "honestidade\nsimplicidade",
            "red_lines": "nunca apagar nada sem perguntar\nnunca pagar contas",
            "autonomy": "equilibrado",
            "allow_messages": "n",
            "allow_shell": "n",
        }
        res = brain.interview(answers=answers)

        soul = (brain.root / "2-self" / "SOUL.md").read_text(encoding="utf-8")
        assert "Jarvis" in soul and "seco e direto" in soul
        values = (brain.root / "2-self" / "values.md").read_text(encoding="utf-8")
        assert "honestidade" in values and "apagar" in values
        assert (brain.root / "POLICY.md").exists()

        # autonomia 'equilibrado' solta registrar_decisao
        assert brain.policy.check("registrar_decisao") == "allow"
        # linhas vermelhas endurecem pra deny
        assert brain.policy.check("apagar") == "deny"
        assert brain.policy.check("pagar") == "deny"
        # não autorizou mensagens → segue confirm
        assert brain.policy.check("enviar_mensagem") == "confirm"
        assert "POLICY.md" in res["files"]
        brain.close()


def test_solto_allows_messages_and_defaults_are_conservative():
    p_solto = build_policy(build_profile({"autonomy": "solto", "allow_messages": "s"}))
    assert p_solto["enviar_mensagem"] == "allow"

    # default (respostas vazias) é conservador
    p_default = build_policy(build_profile({}))
    assert p_default["enviar_mensagem"] == "confirm"
    assert p_default["rodar_shell"] == "deny"
    assert p_default["apagar"] == "deny"


def test_interactive_mode_uses_ask_callback():
    answers_seq = iter([
        "Bot", "calmo", "me ajudar",
        "foco", "",            # values (linha vazia encerra)
        "",                    # red_lines (vazio)
        "conservador", "n", "n",
    ])
    with tempfile.TemporaryDirectory() as tmp:
        brain = Brain(tmp)
        Interview().run(brain, ask=lambda _prompt: next(answers_seq))
        assert "Bot" in (brain.root / "2-self" / "SOUL.md").read_text(encoding="utf-8")
        brain.close()
