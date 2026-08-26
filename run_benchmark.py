#!/usr/bin/env python3
"""LUMEN Bench alpha validator and deterministic smoke-test scorer.

This script does not replace expert ratings. It checks submission structure and
whether responses mention case-specific semantic anchors.
"""
import argparse, json, re, sys
from pathlib import Path

REQ = ["id", "analysis", "intent", "recommendations", "continuity_flags", "questions", "confidence"]


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def tokens(text):
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def response_text(p):
    parts = [str(p.get("analysis", "")), str(p.get("intent", ""))]
    for item in p.get("recommendations", []):
        if isinstance(item, dict):
            parts += [str(item.get("action", "")), str(item.get("reason", ""))]
        else:
            parts.append(str(item))
    parts += [str(x) for x in p.get("continuity_flags", [])]
    parts += [str(x) for x in p.get("questions", [])]
    return " ".join(parts)


def validate_benchmark(data):
    errors = []
    if not isinstance(data.get("tasks"), list) or not data["tasks"]:
        return ["benchmark.tasks must be a non-empty list"]
    seen = set()
    for i, task in enumerate(data["tasks"]):
        label = task.get("id", f"index {i}")
        if label in seen:
            errors.append(f"duplicate task id: {label}")
        seen.add(label)
        for key in ["id", "capability", "task_type", "prompt", "evidence", "required_concepts", "active_dimensions"]:
            if key not in task:
                errors.append(f"{label}: missing {key}")
    if data.get("task_count") != len(data["tasks"]):
        errors.append("task_count does not match tasks length")
    return errors


def validate_predictions(preds, valid_ids):
    errors = []
    if not isinstance(preds, list):
        return ["predictions file must be a JSON list"]
    seen = set()
    for i, p in enumerate(preds):
        if not isinstance(p, dict):
            errors.append(f"prediction {i} must be an object")
            continue
        missing = [k for k in REQ if k not in p]
        if missing:
            errors.append(f"prediction {i}: missing {', '.join(missing)}")
        pid = p.get("id")
        if pid not in valid_ids:
            errors.append(f"prediction {i}: unknown id {pid!r}")
        if pid in seen:
            errors.append(f"duplicate prediction id: {pid}")
        seen.add(pid)
        if not isinstance(p.get("recommendations", []), list):
            errors.append(f"{pid}: recommendations must be a list")
        c = p.get("confidence")
        if not isinstance(c, (int, float)) or not 0 <= c <= 1:
            errors.append(f"{pid}: confidence must be between 0 and 1")
    return errors

def concept_match(concept, text_tokens):
    words = [w for w in tokens(concept) if len(w) > 2]
    if not words:
        return 0.0
    return sum(w in text_tokens for w in words) / len(words)


def score(benchmark, preds):
    by_id = {p["id"]: p for p in preds}
    rows = []
    for task in benchmark["tasks"]:
        p = by_id.get(task["id"])
        if not p:
            rows.append({"id": task["id"], "capability": task["capability"], "status": "missing", "smoke_score": 0.0})
            continue
        text = response_text(p)
        tt = tokens(text)
        anchors = task.get("required_concepts", [])
        matches = [concept_match(c, tt) for c in anchors]
        anchor_recall = sum(m >= 0.5 for m in matches) / max(1, len(matches))
        nonempty = sum(bool(p.get(k)) for k in ["analysis", "intent", "recommendations"]) / 3
        ordered = p.get("recommendations", [])
        priorities = [x.get("priority") for x in ordered if isinstance(x, dict)]
        priority_ok = bool(priorities) and all(isinstance(x, int) for x in priorities) and priorities == sorted(priorities)
        smoke = 100 * (0.70 * anchor_recall + 0.20 * nonempty + 0.10 * priority_ok)
        rows.append({
            "id": task["id"], "capability": task["capability"], "status": "scored",
            "semantic_anchor_recall": round(anchor_recall, 3),
            "structure_completeness": round(nonempty, 3),
            "priority_structure": int(priority_ok), "smoke_score": round(smoke, 1)
        })
    scored = [r for r in rows if r["status"] == "scored"]
    overall = sum(r["smoke_score"] for r in rows) / len(rows)
    caps = {}
    for r in rows:
        caps.setdefault(r["capability"], []).append(r["smoke_score"])
    return {
        "benchmark": benchmark.get("name"), "version": benchmark.get("version"),
        "warning": "Smoke-test metric only. Do not publish as an expert LUMEN Bench score.",
        "coverage": {"submitted": len(scored), "total": len(rows)},
        "smoke_score": round(overall, 1),
        "per_capability": {k: round(sum(v) / len(v), 1) for k, v in caps.items()},
        "cases": rows,
    }


def main():
    ap = argparse.ArgumentParser(description="Validate or smoke-test LUMEN Bench submissions")
    sub = ap.add_subparsers(dest="cmd", required=True)
    va = sub.add_parser("validate")
    va.add_argument("--benchmark", required=True)
    va.add_argument("--rubric", required=False)
    sc = sub.add_parser("score")
    sc.add_argument("--benchmark", required=True)
    sc.add_argument("--predictions", required=True)
    sc.add_argument("--out")
    args = ap.parse_args()
    benchmark = load_json(args.benchmark)
    errors = validate_benchmark(benchmark)
    if args.cmd == "validate":
        if args.rubric and not Path(args.rubric).is_file():
            errors.append(f"rubric not found: {args.rubric}")
        if errors:
            print("INVALID\n" + "\n".join(f"- {e}" for e in errors)); return 1
        print(f"VALID: {benchmark['name']} {benchmark['version']} ({len(benchmark['tasks'])} tasks)"); return 0
    preds = load_json(args.predictions)
    errors += validate_predictions(preds, {t["id"] for t in benchmark["tasks"]})
    if errors:
        print("INVALID\n" + "\n".join(f"- {e}" for e in errors)); return 1
    result = score(benchmark, preds)
    text = json.dumps(result, indent=2) + "\n"
    if args.out: Path(args.out).write_text(text, encoding="utf-8")
    else: print(text, end="")
    return 0

if __name__ == "__main__":
    sys.exit(main())
