"""Gate sequential blind releases on separately validated, immutable score saves.

This protects against a shell continuing to the next read after a failed write.
It never opens private-selection.json or supplies the hidden culprit to a reader.
"""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(version, trial, action, stage):
    assert version >= 1 and trial.isalnum() and 1 <= stage <= 8
    folder = ROOT / f"build/story-pass{version}" / trial
    journal_path = folder / "release-journal.json"
    journal = json.loads(journal_path.read_text(encoding="utf-8")) if journal_path.exists() else {"releases": []}
    first = (folder / "checkpoint_01.txt").read_text(encoding="utf-8").splitlines()
    names = {line.split(" / ", 1)[0] for line in first[2::3] if " / " in line}
    assert names, "Missing attending names"
    entries = journal["releases"]
    if action == "read":
        assert stage == len(entries) + 1, "Release must be read once, in order"
        for previous in entries:
            score_path = folder / f"result_{previous['stage']:02}.json"
            assert previous.get("result_sha256") == digest(score_path), "Earlier result missing, unvalidated, or changed"
        path = folder / f"checkpoint_{stage:02}.txt"
        entries.append({"stage": stage, "input_sha256": digest(path), "read_at": datetime.now(timezone.utc).isoformat()})
        journal_path.write_text(json.dumps(journal, indent=2) + "\n", encoding="utf-8")
        print(path.read_text(encoding="utf-8"))
    else:
        assert entries and entries[-1]["stage"] == stage, "Validate the current release before continuing"
        assert "result_sha256" not in entries[-1], "A saved assessment cannot be overwritten"
        result_path = folder / f"result_{stage:02}.json"
        result = json.loads(result_path.read_text(encoding="utf-8-sig"))
        rows = result["scores"]
        assert len(rows) == len(names) and {row["name"] for row in rows} == names, "One score per exact attending name required"
        assert all(type(row["score"]) is int and 0 <= row["score"] <= 10 for row in rows), "Integer scores 0–10 required"
        entries[-1].update(result_sha256=digest(result_path), saved_at=datetime.now(timezone.utc).isoformat())
        journal_path.write_text(json.dumps(journal, indent=2) + "\n", encoding="utf-8")
        print(f"Validated {trial} stage {stage}; earlier scores remain frozen.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["read", "validate"])
    parser.add_argument("--version", required=True, type=int)
    parser.add_argument("--trial", required=True)
    parser.add_argument("--stage", required=True, type=int)
    args = parser.parse_args()
    run(args.version, args.trial, args.action, args.stage)
