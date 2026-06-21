<div align="center">

# 🧠🧠🧠 3cerebros

**Um cérebro de IA com 3 cérebros — isolado e embutível por qualquer agente.**

Projeto · Self · Conhecimento · `.md` + SQLite · zero dependências no núcleo

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

## Status: operacional (F1–F4, menos SDK TS)

Núcleo rodável **com tudo ligado**: entrevista que gera a política (F1),
autonomia sob política (F2), conectores de ingestão (F3), e CLI + MCP server +
Agent Skills (F4). Único pendente: o SDK TypeScript (qualquer host TS usa o **MCP
server** enquanto isso). Núcleo só stdlib; `mcp` é dependência **opcional**.

## Uso (Python)

```python
from cerebros import Brain

brain = Brain("~/.cerebros")                 # cria os 3 cérebros se não existirem

brain.interview(answers={...})               # F1: entrevista → SOUL/values/POLICY
system = brain.build_context(query, who)     # Self + memórias relevantes → system prompt
brain.observe(who, user_msg, ai_reply)       # triagem + save autônomo (sob política)
brain.recall("postgres", sector="projeto")   # busca por relevância (BM25)
brain.note("texto cru")                       # destila em nota no Conhecimento
brain.ingest("chatgpt_export", path="…")     # F3: importa fonte externa → inbox
brain.run_jobs()                              # F2: manutenção autônoma (cron chama)
brain.act("enviar_mensagem", do=enviar)      # gate de ação SOB a política
brain.policy.check("enviar_mensagem")         # 'allow' | 'confirm' | 'deny'
```

Veja [`examples/minimal_host.py`](examples/minimal_host.py) (host completo) e
[`examples/intelecto_seam.py`](examples/intelecto_seam.py) (ponto de costura no `core.py`).

## Uso (CLI)

```bash
pip install -e .                  # instala o comando `cerebros`
cerebros init                     # entrevista de onboarding (gera a política)
cerebros observe "decidi migrar pra Postgres na sexta" --who nei
cerebros ingest chatgpt_export --path conversations.json
cerebros jobs                     # roda a manutenção autônoma (sob política)
cerebros recall "postgres" --sector projeto
cerebros policy enviar_mensagem   # → allow | confirm | deny
cerebros mcp                      # sobe o MCP server (pip install 'cerebros[mcp]')
```

## Agent Skills (Claude Code / Codex / Gemini)

Em [`skills/`](skills): `cerebro-triagem` (capturar/rotear), `cerebro-nota`
(destilar conhecimento) e `cerebro-socratica` (pensar apoiado no Self). Operam o
mesmo cérebro em `~/.cerebros/` via a CLI.

## Como incorporar no seu sistema

| Host | Como |
|---|---|
| Python (intelecto, jarvis caseiro) | `pip install -e .` ou git submodule → `from cerebros import Brain` |
| Claude Code / Codex / Gemini | Agent Skills de [`skills/`](skills) + MCP |
| Qualquer runtime | subir o MCP server (`cerebros mcp`) |
| TypeScript (ex.: openpcbot) | falar com o **MCP server** (SDK ts ainda não — único pendente) |
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
- **F1 ✅** entrevista → `POLICY.md` do usuário + `brain.act()` (o diferencial)
- **F2 ✅** autonomia: `run_jobs()` real (triagem/briefing/saúde) via cron
- **F3 ✅** conectores: ChatGPT export, Telegram, email/mbox, arquivos → inbox
- **F4 ✅** empacotar: CLI `cerebros` + MCP server + Agent Skills
- **F4 (resta)** SDK TypeScript — hosts TS usam o MCP server enquanto isso

---

<div align="center">
Um projeto <a href="https://inema.club">INEMA.CLUB</a>
</div>
