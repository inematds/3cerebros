"""F3: importadores normalizam fontes externas em itens; ingest enche a inbox."""
import json
import mailbox
import tempfile
from pathlib import Path

from cerebros import Brain, ingest


def test_ingest_chatgpt_export():
    with tempfile.TemporaryDirectory() as tmp:
        cj = Path(tmp) / "conversations.json"
        cj.write_text(json.dumps([{
            "title": "Sobre cérebros",
            "mapping": {
                "1": {"message": {"author": {"role": "user"},
                                  "content": {"parts": ["o que é um segundo cérebro?"]},
                                  "create_time": 1.0}},
                "2": {"message": {"author": {"role": "assistant"},
                                  "content": {"parts": ["é um sistema externo de memória"]},
                                  "create_time": 2.0}},
            },
        }]), encoding="utf-8")
        items = list(ingest.load("chatgpt_export", str(cj)))
        assert len(items) == 1
        assert "segundo cérebro" in items[0] and "memória" in items[0]


def test_ingest_files_dir():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "notas"
        d.mkdir()
        (d / "n1.md").write_text("nota um", encoding="utf-8")
        (d / "n2.txt").write_text("nota dois", encoding="utf-8")
        (d / "ignora.bin").write_text("x", encoding="utf-8")
        assert set(ingest.load("files", str(d))) == {"nota um", "nota dois"}


def test_ingest_telegram():
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "result.json"
        f.write_text(json.dumps({"messages": [
            {"type": "message", "from": "nei", "text": "primeira"},
            {"type": "message", "from": "bot",
             "text": ["segunda ", {"type": "bold", "text": "parte"}]},
            {"type": "service", "text": "ignorar"},
        ]}), encoding="utf-8")
        items = list(ingest.load("telegram", str(f)))
        assert len(items) == 2 and "segunda parte" in items[1]


def test_ingest_email_mbox():
    with tempfile.TemporaryDirectory() as tmp:
        path = str(Path(tmp) / "in.mbox")
        box = mailbox.mbox(path)
        msg = mailbox.mboxMessage()
        msg["subject"] = "Assunto X"
        msg["from"] = "a@b.com"
        msg.set_payload("corpo do email")
        box.add(msg)
        box.flush()
        box.close()
        items = list(ingest.load("email", path))
        assert items and "corpo do email" in items[0] and "Assunto X" in items[0]


def test_brain_ingest_fills_inbox():
    with tempfile.TemporaryDirectory() as tmp:
        cj = Path(tmp) / "c.json"
        cj.write_text(json.dumps([{"title": "t", "mapping": {
            "1": {"message": {"author": {"role": "user"},
                              "content": {"parts": ["oi"]}, "create_time": 1}}}}]),
            encoding="utf-8")
        brain = Brain(str(Path(tmp) / "brain"))
        n = brain.ingest("chatgpt_export", str(cj))
        assert n == 1
        assert list((brain.root / "0-inbox").glob("chatgpt_export-*.md"))
        brain.close()


def test_ingest_unknown_source_raises():
    try:
        list(ingest.load("nope", "x"))
    except ValueError as e:
        assert "não suportada" in str(e)
    else:
        raise AssertionError("deveria recusar fonte desconhecida")
