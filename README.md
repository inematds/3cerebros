<div align="center">

# 🧠🧠🧠 3cerebros

**Um cérebro de IA com 3 cérebros — isolado e embutível por qualquer agente.**

Projeto · Self · Conhecimento · `.md` + SQLite · zero dependências (F0)

</div>

---

## O que é

`3cerebros` é o **cérebro**, num repo isolado pra você **incorporar no seu sistema**
(jarvis, bot, agente CLI, o que for). Ele separa a memória em **3 cérebros com
necessidades opostas** — em vez de um monte só que incha:

| Cérebro | Guarda | Natureza |
|---|---|---|
| **1 · Projeto** | o que rolou, decisões, estado | episódico |
| **2 · Self** | quem você é, valores, dúvidas | identidade |
| **3 · Conhecimento** | fatos, o que aprendeu | referência |

Mais o diferencial que nenhum outro segundo cérebro tem: uma **política de
automação** (o que o cérebro pode fazer sozinho vs pedir confirmação).

> A pesquisa e o racional estão em [inematds/2cerebrox](https://github.com/inematds/2cerebrox).

## Status: F0 (esqueleto)

A F0 entrega o **núcleo rodável**: `Brain` com memória SQLite FTS5, triagem,
política e destilação. Conectores (F3), MCP/SDK-ts/Agent-Skills (F4) vêm depois.

## Uso (Python)

```python
from cerebros import Brain

brain = Brain("~/.cerebros")                 # cria os 3 cérebros se não existirem

system = brain.build_context(query, who)     # Self + memórias relevantes → system prompt
brain.observe(who, user_msg, ai_reply)       # triagem + save autônomo (sob política)
brain.recall("postgres", sector="projeto")   # busca por relevância (BM25)
brain.note("texto cru")                       # destila em nota no Conhecimento
brain.policy.check("enviar_mensagem")         # 'allow' | 'confirm' | 'deny'
brain.run_jobs()                              # manutenção (cron chama)
```

Veja [`examples/minimal_host.py`](examples/minimal_host.py) — um host completo em ~30 linhas.

## Como incorporar no seu sistema

| Host | Como |
|---|---|
| Python (intelecto, jarvis caseiro) | `pip install -e .` ou git submodule → `from cerebros import Brain` |
| TypeScript (ex.: openpcbot) | SDK ts (F4) ou o MCP server |
| Claude Code / Codex / Gemini | Agent Skills (F4) + MCP |
| Qualquer runtime | subir o MCP server (F4) |
| Só o formato | apontar a ferramenta pra `~/.cerebros/` — spec aberta |

## Formato e política

- [`spec/FORMAT.md`](spec/FORMAT.md) — a estrutura do cérebro (pasta + schema SQLite).
- [`spec/POLICY.md`](spec/POLICY.md) — o formato da política de automação.

## Rodar o teste

```bash
python -m pytest -q          # ou: python tests/test_smoke.py
```

## Roadmap

- **F0 ✅** núcleo: Brain, memória FTS5, triagem, política, destilação
- **F1** entrevista → `POLICY.md` do usuário (o diferencial)
- **F2** autonomia: `run_jobs()` real (triagem/briefing/saúde) via cron
- **F3** conectores: ChatGPT export, Telegram, email → inbox
- **F4** empacotar: MCP server + SDK ts + Agent Skills

---

<div align="center">
Um projeto <a href="https://inema.club">INEMA.CLUB</a>
</div>
