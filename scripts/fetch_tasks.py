"""Fetch VS Code tasks for a value stream fase (optionally one agent) into a target workspace.

Bron: source/.vscode/tasks.json
Doel: target/.vscode/tasks.json (merge/replace by label)

Typical usage (from another workspace, e.g. mandarin-architectuur):
    python ..\\mandarin-agents\\scripts\\fetch_tasks.py fnd.02 --agent concept-curator --source ..\\mandarin-agents --target .

Behavior:
- Selects tasks where label starts with '<CODE>.<fase> -' (e.g. 'FND.02 -')
- Optional --agent narrows to a single agent
- Merges selected tasks into target .vscode/tasks.json
- Copies only required inputs referenced by selected tasks (${input:...})
- Replaces existing tasks with same label to keep idempotent updates
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
SIBLING_AGENTS = REPO_ROOT.parent / "mandarin-agents"

if REPO_ROOT.name != "mandarin-agents" and SIBLING_AGENTS.exists():
    DEFAULT_SOURCE = SIBLING_AGENTS.resolve()
else:
    DEFAULT_SOURCE = REPO_ROOT

DEFAULT_TARGET = REPO_ROOT


def parse_value_stream_fase(value: str) -> Tuple[str, str]:
    if "." not in value:
        raise ValueError("Gebruik formaat <code>.<fase>, bijvoorbeeld fnd.02")
    code, fase = value.split(".", 1)
    code = code.strip().lower()
    fase = fase.strip().zfill(2)
    if not code or not fase.isdigit():
        raise ValueError("Ongeldige value stream fase; verwacht zoiets als fnd.02")
    return code, fase


def strip_jsonc(content: str) -> str:
    """Best effort JSONC -> JSON for tasks.json files with comments."""
    content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)
    content = re.sub(r"(^|\s)//.*$", "", content, flags=re.MULTILINE)
    return content


def load_tasks_json(path: Path) -> Dict:
    if not path.exists():
        return {"version": "2.0.0", "tasks": [], "inputs": []}
    raw = path.read_text(encoding="utf-8")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return json.loads(strip_jsonc(raw))


def normalize_text(value: str) -> str:
    return re.sub(r"[-_]+", " ", value.lower()).strip()


def task_matches_agent(task: Dict, agent_slug: str | None) -> bool:
    if not agent_slug:
        return True

    slug = agent_slug.lower().strip()
    if not slug:
        return True

    label = normalize_text(task.get("label", ""))
    title_words = normalize_text(slug)
    if title_words and title_words in label:
        return True

    args = task.get("args", [])
    if isinstance(args, list):
        args_blob = "\n".join(str(a).lower() for a in args)
    else:
        args_blob = str(args).lower()

    if f"'{slug}'" in args_blob or f'"{slug}"' in args_blob:
        return True
    if f"agent_naam={slug}" in args_blob:
        return True

    return False


def select_tasks(source: Dict, code: str, fase: str, agent_slug: str | None) -> List[Dict]:
    prefix = f"{code.upper()}.{fase} -"
    selected: List[Dict] = []
    for task in source.get("tasks", []):
        label = str(task.get("label", ""))
        if not label.startswith(prefix):
            continue
        if not task_matches_agent(task, agent_slug):
            continue
        selected.append(task)
    return selected


def extract_input_ids(tasks: List[Dict]) -> Set[str]:
    blob = json.dumps(tasks, ensure_ascii=False)
    return set(re.findall(r"\$\{input:([^}]+)\}", blob))


def merge_tasks(target: Dict, selected_tasks: List[Dict]) -> Tuple[int, int]:
    existing = target.get("tasks", [])
    existing_by_label = {str(t.get("label", "")): t for t in existing}

    replaced = 0
    added = 0
    for task in selected_tasks:
        label = str(task.get("label", ""))
        if label in existing_by_label:
            replaced += 1
        else:
            added += 1
        existing_by_label[label] = task

    merged = list(existing_by_label.values())
    merged.sort(key=lambda t: str(t.get("label", "")))
    target["tasks"] = merged
    return added, replaced


def merge_inputs(target: Dict, source: Dict, required_input_ids: Set[str]) -> int:
    source_inputs = {str(i.get("id", "")): i for i in source.get("inputs", []) if i.get("id")}
    target_inputs = {str(i.get("id", "")): i for i in target.get("inputs", []) if i.get("id")}

    changed = 0
    for input_id in sorted(required_input_ids):
        src = source_inputs.get(input_id)
        if not src:
            continue
        if target_inputs.get(input_id) != src:
            target_inputs[input_id] = src
            changed += 1

    merged_inputs = list(target_inputs.values())
    merged_inputs.sort(key=lambda i: str(i.get("id", "")))
    target["inputs"] = merged_inputs
    return changed


def write_log(target_root: Path, code: str, fase: str, agent: str | None, selected_labels: List[str], added: int, replaced: int, inputs_merged: int) -> Path:
    logs_dir = target_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_path = logs_dir / f"fetch-tasks-{code}-{fase}-{ts}.log"
    lines = [
        f"timestamp: {ts}",
        f"value_stream_fase: {code}.{fase}",
        f"agent_filter: {agent or '(none)'}",
        f"selected_tasks: {len(selected_labels)}",
        f"added: {added}",
        f"replaced: {replaced}",
        f"inputs_merged: {inputs_merged}",
        "labels:",
    ]
    lines.extend([f"  - {lbl}" for lbl in selected_labels])
    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return log_path


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description="Fetch tasks per value-stream fase")
    parser.add_argument("value_stream_fase", help="Formaat <code>.<fase>, bijv. fnd.02")
    parser.add_argument("--agent", help="Optionele agent filter, bijv. concept-curator")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE, help="Pad naar mandarin-agents bron")
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET, help="Doel workspace")
    args = parser.parse_args(argv)

    code, fase = parse_value_stream_fase(args.value_stream_fase)
    source_root = args.source.expanduser().resolve()
    target_root = args.target.expanduser().resolve()

    source_tasks_path = source_root / ".vscode" / "tasks.json"
    if not source_tasks_path.exists():
        parser.error(f"Bron tasks.json niet gevonden: {source_tasks_path}")

    target_tasks_path = target_root / ".vscode" / "tasks.json"
    target_tasks_path.parent.mkdir(parents=True, exist_ok=True)

    source_tasks = load_tasks_json(source_tasks_path)
    target_tasks = load_tasks_json(target_tasks_path)

    selected = select_tasks(source_tasks, code, fase, args.agent)
    if not selected:
        print(f"Geen tasks gevonden voor {code}.{fase}" + (f" en agent {args.agent}" if args.agent else ""))
        return 0

    required_inputs = extract_input_ids(selected)
    added, replaced = merge_tasks(target_tasks, selected)
    inputs_merged = merge_inputs(target_tasks, source_tasks, required_inputs)

    target_tasks.setdefault("version", "2.0.0")
    target_tasks_path.write_text(json.dumps(target_tasks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    selected_labels = [str(t.get("label", "")) for t in selected]
    log_path = write_log(target_root, code, fase, args.agent, selected_labels, added, replaced, inputs_merged)

    print(f"Yes! Tasks opgehaald voor {code}.{fase}" + (f" (agent: {args.agent})" if args.agent else ""))
    print(f"Tasks geselecteerd: {len(selected)} | toegevoegd: {added} | vervangen: {replaced}")
    print(f"Inputs bijgewerkt/toegevoegd: {inputs_merged}")
    print(f"Target: {target_tasks_path}")
    print(f"Log: {log_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
