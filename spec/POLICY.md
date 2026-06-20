# POLICY — formato da política de automação

O diferencial do `3cerebros`: define **o que o cérebro pode fazer sozinho** vs o
que **pede confirmação** vs o que é **proibido**. É o que falta em todos os outros
segundos cérebros (ver pesquisa de gating).

## Níveis
- `allow`   — o cérebro faz sozinho (autônomo).
- `confirm` — o cérebro propõe e espera o ok do dono.
- `deny`    — bloqueado, nunca.

## Formato (uma regra por linha)
```
acao: nivel
```
Linhas que não casam são ignoradas (pode comentar à vontade). O arquivo vivo do
usuário fica em `<brain>/POLICY.md`.

## Default conservador (começa fechado, o dono solta depois)
```
salvar_nota: allow
arquivar: allow
atualizar_daily: allow
triagem: allow
registrar_decisao: confirm
mover_cerebro: confirm
enviar_mensagem: confirm
postar: confirm
rodar_shell: confirm
apagar: deny
comprar: deny
pagar: deny
```

## Como o host usa
Antes de qualquer ação externa/autônoma:
```python
verdict = brain.policy.check("enviar_mensagem")   # 'allow' | 'confirm' | 'deny'
if verdict == "allow":   do_it()
elif verdict == "confirm": ask_owner_then_do()
else: skip()
```

## Origem
A política deriva dos **valores** do dono (cérebro Self). A entrevista de
onboarding (F1) gera o `POLICY.md` inicial a partir dessas respostas.
Ação desconhecida → cai no `default` (conservador: `confirm`).
