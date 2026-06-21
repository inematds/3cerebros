"""O ponto de costura (seam) no `intelecto-testes/src/agent/core.py`.

ANTES (intelecto hoje):
    soul = load_soul(settings.soul_path)
    response = await provider.chat(messages=history, system=soul)

DEPOIS (incorporando o 3cerebros) — o `soul.md` vira o seed do cérebro Self:
    from cerebros import Brain
    brain = Brain(settings.cerebros_path)
    system = brain.build_context(query=text, who=remote_jid)
    response = await provider.chat(messages=history, system=system)
    brain.observe(who=remote_jid, user_msg=text, ai_reply=response)

E os stubs do intelecto viram cascas finas:
    src/memory/    → brain.remember / brain.recall
    src/knowledge/ → brain.note / brain.ingest
    src/scheduler/ → brain.run_jobs()  (no tick do cron)
    antes de ação externa (WhatsApp proativo, tool) → brain.policy.check(...)

Abaixo, uma simulação síncrona do mesmo fluxo (sem FastAPI/Evolution).
    python examples/intelecto_seam.py
"""
from cerebros import Brain


async def fake_provider_chat(messages, system):  # assinatura do intelecto
    return f"(resposta usando {len(system)} chars de Self+memórias)"


def handle_message_sync(brain, remote_jid, text):
    """O corpo do handler do intelecto, em versão síncrona pra demo."""
    system = brain.build_context(query=text, who=remote_jid)
    response = f"(resposta usando {len(system)} chars de Self+memórias)"

    # antes de QUALQUER ação externa, a política decide
    verdict = brain.policy.check("enviar_mensagem")
    sent = response if verdict == "allow" else f"[{verdict}] não enviado sem ok"

    brain.observe(who=remote_jid, user_msg=text, ai_reply=response)
    return sent


def main():
    brain = Brain("/tmp/cerebro-intelecto-demo")
    brain.interview(answers={"name": "Intelecto", "autonomy": "conservador"})

    for text in ["decidi usar Postgres no projeto", "acho que foco vem antes de escala"]:
        out = handle_message_sync(brain, "5511999@s.whatsapp.net", text)
        print(out)

    print("cron tick →", list(brain.run_jobs()["ran"]))
    print("stats:", brain.stats())
    brain.close()


if __name__ == "__main__":
    main()
