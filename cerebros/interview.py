"""Entrevista de onboarding (F1) — gera o POLICY.md e os seeds do cérebro Self.

O diferencial do 3cerebros é a POLÍTICA, e ela deriva dos VALORES do dono.
Esta entrevista faz poucas perguntas e materializa três arquivos no cérebro:

  - 2-self/SOUL.md     a identidade do agente (carregada em todo build_context)
  - 2-self/values.md   valores + linha vermelha
  - POLICY.md          o que o cérebro faz sozinho vs confirma vs nunca

Dois modos, mesma lógica:
  - interativo:    Interview().run(brain)              (pergunta no terminal)
  - programático:  Interview().run(brain, answers={…}) (host/CLI passa respostas)
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .policy import DEFAULT_RULES


@dataclass
class Question:
    id: str
    prompt: str
    default: str = ""
    choices: tuple[str, ...] = ()
    multiline: bool = False


# As perguntas da entrevista. Poucas, de propósito: política nasce de valores.
QUESTIONS: list[Question] = [
    Question("name", "Como o cérebro deve te chamar / qual o nome do agente?"),
    Question("tone", "Em uma linha, que tom o agente deve ter?",
             default="direto, honesto, sem enrolação"),
    Question("mission", "O que você quer que esse cérebro/agente faça por você?"),
    Question("values", "Seus valores/princípios (um por linha, linha vazia encerra):",
             multiline=True),
    Question("red_lines", "Linhas vermelhas — o que ele NUNCA deve fazer (uma por linha):",
             multiline=True),
    Question("autonomy",
             "Quanta autonomia? conservador (pede quase tudo) / equilibrado / solto",
             default="conservador", choices=("conservador", "equilibrado", "solto")),
    Question("allow_messages", "Pode mandar mensagem por você sem perguntar? (s/N)",
             default="n", choices=("s", "n")),
    Question("allow_shell", "Pode rodar comandos no seu computador sem perguntar? (s/N)",
             default="n", choices=("s", "n")),
]

# Como cada nível de autonomia molda as ações "de fronteira".
_AUTONOMY = {
    "conservador": {"registrar_decisao": "confirm", "enviar_mensagem": "confirm",
                    "postar": "confirm", "rodar_shell": "deny"},
    "equilibrado": {"registrar_decisao": "allow", "enviar_mensagem": "confirm",
                    "postar": "confirm", "rodar_shell": "confirm"},
    "solto":       {"registrar_decisao": "allow", "enviar_mensagem": "allow",
                    "postar": "confirm", "rodar_shell": "confirm"},
}

# Uma linha vermelha citando uma destas palavras vira `deny` da ação.
_REDLINE_KEYWORDS = {
    "apagar": ("apag", "delet", "remov", "destru"),
    "comprar": ("compr", "buy", "carrinho"),
    "pagar": ("pagar", "pagamento", "boleto", "pay", "transfer", "pix"),
    "enviar_mensagem": ("mensag", "message", "whats", "email", "mandar msg"),
    "postar": ("postar", "publicar", "tweet", "post "),
    "rodar_shell": ("shell", "comando", "terminal", "command", "sudo"),
}


@dataclass
class Profile:
    name: str = ""
    tone: str = ""
    mission: str = ""
    values: list[str] = field(default_factory=list)
    red_lines: list[str] = field(default_factory=list)
    autonomy: str = "conservador"
    allow_messages: bool = False
    allow_shell: bool = False


def _lines(text: str) -> list[str]:
    return [ln.strip() for ln in (text or "").splitlines() if ln.strip()]


def build_profile(answers: dict) -> Profile:
    a = answers or {}
    autonomy = str(a.get("autonomy", "conservador")).strip().lower()
    if autonomy not in _AUTONOMY:
        autonomy = "conservador"
    return Profile(
        name=str(a.get("name", "")).strip(),
        tone=str(a.get("tone", "")).strip() or "direto, honesto, sem enrolação",
        mission=str(a.get("mission", "")).strip(),
        values=_lines(a.get("values", "")),
        red_lines=_lines(a.get("red_lines", "")),
        autonomy=autonomy,
        allow_messages=str(a.get("allow_messages", "n")).strip().lower() in ("s", "sim", "y", "yes", "true"),
        allow_shell=str(a.get("allow_shell", "n")).strip().lower() in ("s", "sim", "y", "yes", "true"),
    )


def build_policy(profile: Profile) -> dict:
    """Deriva as regras de política a partir do perfil."""
    rules = dict(DEFAULT_RULES)
    rules.update(_AUTONOMY[profile.autonomy])
    if profile.allow_messages:
        rules["enviar_mensagem"] = "allow"
    if profile.allow_shell and rules.get("rodar_shell") != "deny":
        rules["rodar_shell"] = "allow"
    # Linhas vermelhas endurecem ações específicas para `deny`.
    for rl in profile.red_lines:
        low = rl.lower()
        for action, kws in _REDLINE_KEYWORDS.items():
            if any(kw in low for kw in kws):
                rules[action] = "deny"
    return rules


def render_policy(rules: dict) -> str:
    body = "\n".join(f"{k}: {v}" for k, v in rules.items())
    return (
        "# POLICY — Política de automação (gerada pela entrevista)\n\n"
        "> O que o cérebro pode fazer SOZINHO vs o que pede confirmação.\n"
        "> Níveis: allow (faz sozinho) · confirm (pede ok) · deny (nunca).\n"
        "> Edite à vontade — uma regra por linha: `acao: nivel`.\n\n"
        f"{body}\n"
    )


def render_soul(p: Profile) -> str:
    return (
        "# SOUL — Quem eu sou (cérebro Self)\n\n"
        "> A personalidade do agente. Carregado em todo `build_context`.\n\n"
        f"- **Nome:** {p.name}\n"
        f"- **Tom:** {p.tone}\n"
        f"- **O que faço:** {p.mission}\n"
        "- **O que me guia:** ver [[values]]\n"
    )


def render_values(p: Profile) -> str:
    vals = "\n".join(f"{i}. {v}" for i, v in enumerate(p.values, 1)) or "1.\n2.\n3."
    reds = "\n".join(f"- {r}" for r in p.red_lines) or "-"
    return (
        "# Valores (cérebro Self)\n\n"
        "> Princípios estáveis. Consultados quando uma decisão é difícil.\n\n"
        f"{vals}\n\n"
        "## Linha vermelha (o que eu nunca faço)\n"
        f"{reds}\n"
    )


def _ask_terminal(q: Question, ask) -> str:
    if q.multiline:
        print(q.prompt)
        out = []
        while True:
            line = ask("… ")
            if not line.strip():
                break
            out.append(line)
        return "\n".join(out)
    suffix = f" [{q.default}]" if q.default else ""
    while True:
        val = ask(f"{q.prompt}{suffix} ").strip()
        if not val and q.default:
            return q.default
        if q.choices and val.lower() not in q.choices:
            print(f"  → responda com: {', '.join(q.choices)}")
            continue
        return val


class Interview:
    """Conduz a entrevista e materializa Self + POLICY no cérebro."""

    questions = QUESTIONS

    def collect(self, ask=None) -> dict:
        """Modo interativo: pergunta no terminal e devolve o dict de respostas."""
        ask = ask or input
        return {q.id: _ask_terminal(q, ask) for q in self.questions}

    def run(self, brain, answers: dict | None = None, ask=None) -> dict:
        """Gera SOUL/values/POLICY no cérebro. `answers` None → entrevista interativa."""
        if answers is None:
            answers = self.collect(ask)
        profile = build_profile(answers)
        rules = build_policy(profile)

        files = {
            "2-self/SOUL.md": render_soul(profile),
            "2-self/values.md": render_values(profile),
            "POLICY.md": render_policy(rules),
        }
        for rel, content in files.items():
            path = brain.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

        # recarrega a política do arquivo recém-escrito
        brain.policy.reload()
        return {"profile": profile, "rules": rules, "files": list(files)}
