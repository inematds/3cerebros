---
name: cerebro-triagem
description: Use quando o usuário jogar um pensamento, nota ou decisão solta e quiser guardar no segundo cérebro (3cerebros). Captura e roteia pro cérebro certo — Projeto / Self / Conhecimento — via a CLI `cerebros`. Acione com "guarda isso no cérebro", "anota no 3cerebros", "joga no inbox", "triagem".
---

# Cérebro — Triagem

Roteia qualquer captura pro cérebro certo e indexa pra busca. Opera o cérebro em
`~/.cerebros/` (ou `$CEREBROS_PATH`).

## Quando usar
O usuário soltou um pensamento/fato/decisão e quer guardar — sem dizer onde.

## Como fazer
1. **Captura direta** (um item): roteia e salva sozinho —
   ```bash
   cerebros observe "decidi migrar o projeto pra Postgres na sexta" --who nei
   ```
   Retorna o `setor` escolhido (`projeto` | `self` | `conhecimento`).

2. **Lote pela inbox**: se houver vários `.md` em `~/.cerebros/0-inbox/`, processa todos —
   ```bash
   cerebros jobs
   ```
   `run_jobs` roteia cada arquivo, indexa e move pro cérebro certo — **sob a política**
   (`triagem`). Se a política for `confirm`, ele lista o que faria sem mover.

3. **Conferir**: `cerebros stats` (contagem por cérebro) e `cerebros recall "termo"`.

## Regras
- Nada nasce classificado: cai no `0-inbox/`, a triagem decide.
- **Self** = identidade/opinião/dúvida · **Projeto** = o que rolou/decisão/prazo ·
  **Conhecimento** = fato/aprendizado.
- Respeite a política: nunca force uma ação `deny`/`confirm` sem o ok do dono.
