"""Host mínimo: como QUALQUER sistema incorpora o 3cerebros operacional.

É o esqueleto do que o intelecto faz no `core.py`: monta contexto a partir do
cérebro, chama o LLM, deixa o cérebro observar/rotear sozinho, roda manutenção
autônoma e gateia ações externas pela política.

    python examples/minimal_host.py
"""
from cerebros import Brain


def fake_llm(system: str, user: str) -> str:
    """Troque por OpenRouter/Ollama/Claude no seu host real."""
    return f"(resposta do LLM usando {len(system)} chars de contexto)"


def main():
    brain = Brain("/tmp/cerebro-demo")  # use ~/.cerebros no host real

    # 0. onboarding (F1): gera SOUL/values/POLICY a partir de respostas
    brain.interview(answers={
        "name": "Demo", "tone": "direto", "mission": "organizar tudo",
        "values": "simplicidade", "red_lines": "nunca apagar sozinho",
        "autonomy": "equilibrado", "allow_messages": "n", "allow_shell": "n",
    })

    # 1-3. o loop de conversa
    for msg in [
        "decidi migrar o projeto pra Postgres na sexta",
        "acho que simplicidade vale mais que features",
        "Fernet usa AES-128-CBC + HMAC-SHA256",
    ]:
        system = brain.build_context(query=msg, who="demo")   # 1. contexto = Self + memórias
        reply = fake_llm(system, msg)                          # 2. seu LLM responde
        sector = brain.observe("demo", msg, reply)             # 3. cérebro roteia + salva sozinho
        print(f"[{sector:12}] {msg}")

    # 4. manutenção autônoma (F2) — o cron do host chamaria isto
    jobs = brain.run_jobs()
    print("\njobs:", list(jobs["ran"]))

    # 5. ação externa SOB a política (F1) — o gate do diferencial
    gate = brain.act("enviar_mensagem",
                     do=lambda: "enviado!",
                     on_confirm=lambda: "pediria confirmação ao dono")
    print("enviar_mensagem:", gate["verdict"], "→", gate["result"])

    print("stats:", brain.stats())
    print("recall 'postgres':", [h["content"] for h in brain.recall("postgres projeto")])
    brain.close()


if __name__ == "__main__":
    main()
