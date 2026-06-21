---
name: cerebro-socratica
description: Use quando o usuário estiver em dúvida, decidindo algo difícil, ou quiser pensar em voz alta — para conduzir um diálogo socrático apoiado no cérebro Self (valores e dúvidas) do 3cerebros. Faz perguntas em vez de dar respostas prontas, e registra a reflexão. Acione com "me ajuda a pensar", "to em dúvida", "socrática", "reflexão", "decisão difícil".
---

# Cérebro — Socrática

Conduz o usuário a pensar melhor, ancorando no cérebro **Self** (`~/.cerebros/2-self/`)
— quem ele é, seus valores e suas dúvidas abertas — em vez de despejar respostas.

## Quando usar
Dúvida, decisão difícil, conflito de prioridades, ou "me ajuda a pensar".

## Como fazer
1. **Carregue a identidade** pra calibrar as perguntas aos valores do dono —
   ```bash
   cerebros context "" 
   ```
   (traz `SOUL.md` + `values.md`). Leia os valores e a linha vermelha antes de perguntar.

2. **Pergunte, não responda.** Uma pergunta por vez, do concreto ao princípio:
   - Qual é a decisão real, em uma frase?
   - Que valor seu está em jogo aqui? (cite o `values.md`)
   - O que você faria se não tivesse medo de errar?
   - Daqui a um ano, qual escolha você queria ter feito?

3. **Registre a reflexão** no cérebro Self (vira memória buscável e roteia pra `self`) —
   ```bash
   cerebros observe "acho que simplicidade vale mais que features neste projeto" --who nei
   ```
   Dúvidas abertas podem virar arquivos em `2-self/questions/`.

## Regras
- Não decida pelo usuário. O cérebro Self é dele; você espelha e questiona.
- Se a conversa virar ação externa (mandar mensagem, postar), passe pela política:
  `cerebros policy enviar_mensagem` antes de sugerir agir.
