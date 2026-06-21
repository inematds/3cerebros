"""Importador: caixa de email `.mbox` (stdlib `mailbox`, sem dependência).

Cada mensagem vira um item `# assunto / de / corpo`. Decodifica headers MIME e
extrai o corpo `text/plain` (mesmo em multipart).
"""
from __future__ import annotations

import mailbox
from email.header import decode_header, make_header
from typing import Iterable


def _decode(s) -> str:
    try:
        return str(make_header(decode_header(s or "")))
    except Exception:
        return s or ""


def _body(msg) -> str:
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                if payload is None:
                    continue
                return payload.decode(part.get_content_charset() or "utf-8", "replace")
        return ""
    payload = msg.get_payload(decode=True)
    if payload is None:
        return msg.get_payload() or ""
    return payload.decode(msg.get_content_charset() or "utf-8", "replace")


def load_items(path: str) -> Iterable[str]:
    box = mailbox.mbox(path)
    try:
        for msg in box:
            subj = _decode(msg.get("subject"))
            frm = _decode(msg.get("from"))
            body = (_body(msg) or "").strip()
            if not (subj or body):
                continue
            yield f"# {subj}\n_de: {frm}_\n\n{body}"
    finally:
        box.close()
