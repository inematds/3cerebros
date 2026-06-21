---
name: cerebro-nota
description: Use quando o usuário quiser transformar um texto cru (artigo, transcrição, ideia longa) numa nota-átomo de conhecimento no segundo cérebro (3cerebros). Destila o essencial e salva no cérebro Conhecimento via a CLI `cerebros`. Acione com "destila isso", "vira nota", "resume pro cérebro", "nota de conhecimento".
---

# Cérebro — Nota

Destila um texto cru numa nota curta e a guarda no cérebro **Conhecimento**
(`~/.cerebros/3-conhecimento/notes/`), indexada pra busca.

## Quando usar
O usuário deu um conteúdo longo e quer só a ideia essencial guardada e reencontrável.

## Como fazer
1. Destila e salva —
   ```bash
   cerebros note "BM25 é um ranking de relevância usado em busca full-text; pondera frequência do termo e tamanho do documento."
   ```
   Cria `3-conhecimento/notes/<slug>.md` (título + 2–4 frases) e indexa a nota.

2. **Com LLM melhor** (host): a destilação fica mais rica se o host passar um `llm`
   pra `Brain.note(content, llm=...)`. Pela CLI, a destilação é determinística (boa o
   suficiente pra capturar e reencontrar).

3. **Reencontrar**: `cerebros recall "BM25" --sector conhecimento`.

## Regras
- Uma nota = uma ideia (átomo). Se o texto tem várias, faça várias `note`.
- Conhecimento só acumula — não apaga. Conecte ideias com `[[wikilinks]]` no `.md`.
