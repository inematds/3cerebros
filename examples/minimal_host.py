"""Host mínimo: como QUALQUER sistema incorpora o 3cerebros em ~30 linhas.

Isto é o esqueleto do que o intelecto faz no `core.py`: monta o contexto a
partir do cérebro, chama o seu LLM, e deixa o cérebro observar/rotear sozinho.

    python examples/minimal_host.py
"""
from cerebros import Brain


def fake_llm(system: str, user: str) -> str:
    """Troque por OpenRouter/Ollama/Claude no seu host real."""
    return f"(resposta do LLM usando {len(system)} chars de contexto)"


def main():
    brain = Brain("/tmp/cerebro-demo")  # use ~/.cerebros no host real

    # simula uma conversa
    for msg in [
        "decidi migrar o projeto pra Postgres na sexta",
        "acho que simplicidade vale mais que features",
        "Fernet usa AES-128-CBC + HMAC-SHA256",
    ]:
        system = brain.build_context(query=msg, who="demo")   # 1. contexto = Self + memórias
        reply = fake_llm(system, msg)                          # 2. seu LLM responde
        sector = brain.observe("demo", msg, reply)             # 3. cérebro roteia + salva sozinho
        print(f"[{sector:12}] {msg}")

    print("\nstats:", brain.stats())
    print("recall 'projeto':", [h["content"] for h in brain.recall("projeto postgres")])
    print("policy enviar_mensagem:", brain.policy.check("enviar_mensagem"))
    brain.close()


if __name__ == "__main__":
    main()
