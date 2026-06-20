# FORMAT — o formato do cérebro (a "constituição")

Esta é a spec aberta do `3cerebros`. Qualquer ferramenta que respeite este
formato lê/escreve o mesmo cérebro. É o que torna o repo **embutível por qualquer um**.

## Layout (pasta, default `~/.cerebros/`)
```
<brain>/
├── 0-inbox/                 captura crua (não classificada) → triagem roteia
├── 1-projeto/               CÉREBRO 1 — episódico (o que rolou)
│   ├── daily/  projects/  decisions/log.md  archive/
├── 2-self/                  CÉREBRO 2 — identidade (quem eu sou)
│   ├── SOUL.md  values.md  questions/  thinking/  journal/
├── 3-conhecimento/          CÉREBRO 3 — referência (o que aprendi)
│   ├── sources/  notes/  topics/
├── CLAUDE.md                roteador (mapa dos 3 cérebros)
├── POLICY.md                política de automação (ver spec/POLICY.md)
└── memory.db               SQLite FTS5 (busca full-text por relevância)
```

## Setores (1 por cérebro)
`projeto` · `self` · `conhecimento`. Toda memória e toda nota pertence a um setor.

## Schema da memória (`memory.db`)
Tabela FTS5 única:
```sql
CREATE VIRTUAL TABLE memories USING fts5(
  content,
  sector   UNINDEXED,   -- projeto | self | conhecimento
  category UNINDEXED,    -- fact | note | decision | reflection | conversation ...
  who      UNINDEXED,    -- origem (ex.: id do usuário/chat)
  created_at UNINDEXED   -- epoch
);
-- busca: WHERE memories MATCH ? ORDER BY bm25(memories)
```

## Regras
- **Nada nasce classificado:** entra em `0-inbox/`, a triagem roteia.
- **Self é estável**, Projeto é datado/append-only, Conhecimento só acumula.
- **`[[wikilinks]]`** conectam notas entre cérebros (separação na pasta = ordem;
  links cruzados = o cérebro pensando junto).
- **A memória (db) e os arquivos (.md) são as duas faces:** o db é o índice
  consultável; os .md são a fonte legível (Obsidian/VSCode/cat).

## Como um host consome
- **Python:** `from cerebros import Brain; Brain("~/.cerebros")`.
- **Outro runtime:** MCP server (F4) sobre o `Brain`.
- **Claude Code/Codex:** Agent Skills (F4) que operam esta pasta.
- **Só o formato:** apontar qualquer ferramenta pra `<brain>/`.
