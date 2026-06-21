"""CLI do 3cerebros — opera o cérebro em ~/.cerebros (ou --brain / $CEREBROS_PATH).

    cerebros init [--auto]            # entrevista → SOUL/values/POLICY
    cerebros context "query" [--who]  # system prompt (Self + memórias)
    cerebros observe "msg" [--who]    # triagem + save autônomo → setor
    cerebros remember "texto" [--sector --category]
    cerebros recall "query" [--sector --limit]
    cerebros note "texto cru"         # destila em nota no Conhecimento
    cerebros ingest <fonte> --path X  # chatgpt_export|telegram|email|files → inbox
    cerebros jobs                     # run_jobs (autonomia, sob política)
    cerebros policy [acao]            # verdito de uma ação, ou lista as regras
    cerebros stats                    # memórias por cérebro
    cerebros mcp                      # sobe o MCP server (precisa de cerebros[mcp])
"""
from __future__ import annotations

import argparse
import json
import os

from .brain import Brain, DEFAULT_PATH


def _brain(args) -> Brain:
    path = args.brain or os.environ.get("CEREBROS_PATH") or DEFAULT_PATH
    return Brain(path)


def _out(obj) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2, default=str))


def cmd_init(args):
    brain = _brain(args)
    try:
        from .interview import Interview
        res = Interview().run(brain, answers={} if args.auto else None)
        _out({"ok": True, "files": res["files"], "rules": res["rules"]})
    finally:
        brain.close()


def cmd_context(args):
    brain = _brain(args)
    try:
        print(brain.build_context(args.query, args.who))
    finally:
        brain.close()


def cmd_observe(args):
    brain = _brain(args)
    try:
        _out({"sector": brain.observe(args.who, args.msg)})
    finally:
        brain.close()


def cmd_remember(args):
    brain = _brain(args)
    try:
        rid = brain.remember(args.text, sector=args.sector, category=args.category)
        _out({"saved": rid, "sector": args.sector})
    finally:
        brain.close()


def cmd_recall(args):
    brain = _brain(args)
    try:
        _out(brain.recall(args.query, sector=args.sector, limit=args.limit))
    finally:
        brain.close()


def cmd_note(args):
    brain = _brain(args)
    try:
        print(brain.note(args.text))
    finally:
        brain.close()


def cmd_ingest(args):
    brain = _brain(args)
    try:
        _out({"ingested": brain.ingest(args.source, args.path)})
    finally:
        brain.close()


def cmd_jobs(args):
    brain = _brain(args)
    try:
        _out(brain.run_jobs())
    finally:
        brain.close()


def cmd_policy(args):
    brain = _brain(args)
    try:
        if args.action:
            print(brain.policy.check(args.action))
        else:
            _out(brain.policy.rules)
    finally:
        brain.close()


def cmd_stats(args):
    brain = _brain(args)
    try:
        _out(brain.stats())
    finally:
        brain.close()


def cmd_mcp(args):
    path = args.brain or os.environ.get("CEREBROS_PATH") or DEFAULT_PATH
    from .mcp.server import main as mcp_main
    mcp_main(path)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="cerebros",
                                description="3cerebros — cérebro de IA embutível")
    p.add_argument("--brain", help="caminho do cérebro (default ~/.cerebros)")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("init", help="entrevista de onboarding")
    sp.add_argument("--auto", action="store_true", help="usa defaults, sem perguntar")
    sp.set_defaults(fn=cmd_init)

    sp = sub.add_parser("context", help="monta o system prompt")
    sp.add_argument("query", nargs="?", default="")
    sp.add_argument("--who")
    sp.set_defaults(fn=cmd_context)

    sp = sub.add_parser("observe", help="triagem + save autônomo")
    sp.add_argument("msg")
    sp.add_argument("--who")
    sp.set_defaults(fn=cmd_observe)

    sp = sub.add_parser("remember", help="salva uma memória explícita")
    sp.add_argument("text")
    sp.add_argument("--sector", default="conhecimento")
    sp.add_argument("--category", default="fact")
    sp.set_defaults(fn=cmd_remember)

    sp = sub.add_parser("recall", help="busca por relevância (BM25)")
    sp.add_argument("query")
    sp.add_argument("--sector")
    sp.add_argument("--limit", type=int, default=10)
    sp.set_defaults(fn=cmd_recall)

    sp = sub.add_parser("note", help="destila um texto cru em nota")
    sp.add_argument("text")
    sp.set_defaults(fn=cmd_note)

    sp = sub.add_parser("ingest", help="importa uma fonte externa pra inbox")
    sp.add_argument("source")
    sp.add_argument("--path", required=True)
    sp.set_defaults(fn=cmd_ingest)

    sp = sub.add_parser("jobs", help="roda a manutenção autônoma (sob política)")
    sp.set_defaults(fn=cmd_jobs)

    sp = sub.add_parser("policy", help="verdito de uma ação ou lista as regras")
    sp.add_argument("action", nargs="?")
    sp.set_defaults(fn=cmd_policy)

    sp = sub.add_parser("stats", help="memórias por cérebro")
    sp.set_defaults(fn=cmd_stats)

    sp = sub.add_parser("mcp", help="sobe o MCP server")
    sp.set_defaults(fn=cmd_mcp)

    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    args.fn(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
