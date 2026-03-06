"""fetch_mandarin_agents.py - Haalt prompts, agents en tasks op voor een value stream fase.

Kopieert vanuit mandarin-agents (bron) naar een doel-workspace:
  - artefacten/<code>/<code>.<fase>.<agent>/prompts/*.prompt.md         -> .github/prompts/
  - artefacten/<code>/<code>.<fase>.<agent>/agent-contracten/*.agent.md -> .github/agents/
  - artefacten/<code>/<code>.<fase>.<agent>/tasks/*.tasks.json          -> .vscode/tasks.json

Agent-discovery is puur op mapstructuur -- geen agents-publicatie.json nodig.
Tasks worden op label gemerged in bestaand tasks.json; inputs worden meegekopieerd.

Gebruik:
    python scripts/fetch_mandarin_agents.py aeo.02
    python scripts/fetch_mandarin_agents.py aeo.02 --source ../mandarin-agents --target .
    python scripts/fetch_mandarin_agents.py aeo.02 --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
SIBLING_AGENTS = REPO_ROOT.parent / "mandarin-agents"

DEFAULT_SOURCE = (
    SIBLING_AGENTS.resolve()
    if (REPO_ROOT.name != "mandarin-agents" and SIBLING_AGENTS.exists())
    else REPO_ROOT
)
DEFAULT_TARGET = REPO_ROOT


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_vsf(value: str) -> Tuple[str, str]:
    """Parseer 'aeo.02' -> ('aeo', '02')."""
    if "." not in value:
        raise ValueError(f"Gebruik formaat <code>.<fase>, bijv. aeo.02 (gegeven: {value!r})")
    code, fase = value.split(".", 1)
    code = code.strip().lower()
    fase = fase.strip().zfill(2)
    if not code.isalpha() or not fase.isdigit():
        raise ValueError(f"Ongeldige value stream fase: {value!r}")
    return code, fase


def find_fase_dirs(artefacten_root: Path, code: str, fase: str) -> List[Path]:
    """Geeft alle mappen terug van de vorm artefacten/<code>/<code>.<fase>.<agent>/."""
    base = artefacten_root / code
    if not base.is_dir():
        return []
    prefix = f"{code}.{fase}."
    return sorted(p for p in base.iterdir() if p.is_dir() and p.name.startswith(prefix))


def strip_jsonc(content: str) -> str:
    """Verwijder JSONC-commentaar, string-aware (slaat string-literals over)."""
    result: list[str] = []
    i, n = 0, len(content)
    in_string = False
    while i < n:
        c = content[i]
        if in_string:
            if c == "\\" and i + 1 < n:
                result.append(c)
                result.append(content[i + 1])
                i += 2
                continue
            if c == '"':
                in_string = False
            result.append(c)
            i += 1
        else:
            if c == '"':
                in_string = True
                result.append(c)
                i += 1
            elif c == "/" and i + 1 < n and content[i + 1] == "/":
                while i < n and content[i] != "\n":
                    i += 1
            elif c == "/" and i + 1 < n and content[i + 1] == "*":
                i += 2
                while i < n - 1 and not (content[i] == "*" and content[i + 1] == "/"):
                    i += 1
                i += 2
            else:
                result.append(c)
                i += 1
    return "".join(result)


def load_tasks_json(path: Path) -> dict:
    if not path.exists():
        return {"version": "2.0.0", "tasks": [], "inputs": []}
    raw = path.read_text(encoding="utf-8")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return json.loads(strip_jsonc(raw))


# ---------------------------------------------------------------------------
# Stap 1: Prompts en agents-contracten kopiëren
# ---------------------------------------------------------------------------

def collect_files(fase_dirs: List[Path]) -> Tuple[List[Tuple[Path, str]], List[Tuple[Path, str]]]:
    """
    Zoek alle prompt- en agent-bestanden in de fase-mappen.
    Retourneert (prompts, contracts) als lijsten van (src_path, dest_name).
    """
    prompts: List[Tuple[Path, str]] = []
    contracts: List[Tuple[Path, str]] = []

    for fase_dir in fase_dirs:
        prompts_dir = fase_dir / "prompts"
        if prompts_dir.is_dir():
            for f in sorted(prompts_dir.glob("*.prompt.md")):
                prompts.append((f, f.name))

        contracts_dir = fase_dir / "agent-contracten"
        if contracts_dir.is_dir():
            for f in sorted(contracts_dir.glob("*.agent.md")):
                contracts.append((f, f.name))

    return prompts, contracts


def copy_files(
    items: List[Tuple[Path, str]],
    target_dir: Path,
    dry_run: bool,
    label: str,
) -> List[str]:
    """Kopieer bestanden naar target_dir; retourneert lijst van gekopieerde namen."""
    copied: List[str] = []
    if not items:
        return copied
    if not dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)

    for src, name in items:
        dest = target_dir / name
        copied.append(name)
        if dry_run:
            print(f"  [dry] {label}: {src.name}")
        else:
            shutil.copy2(src, dest)
            print(f"  OK {label}: {src.name}")

    return copied


# ---------------------------------------------------------------------------
# Stap 2: Tasks mergen
# ---------------------------------------------------------------------------

def collect_task_files(fase_dirs: List[Path]) -> List[Path]:
    """Zoek alle *.tasks.json bestanden in tasks/-submappen."""
    found: List[Path] = []
    for fase_dir in fase_dirs:
        tasks_dir = fase_dir / "tasks"
        if tasks_dir.is_dir():
            found.extend(sorted(tasks_dir.glob("*.tasks.json")))
    return found


def load_artefact_tasks(task_files: List[Path]) -> Tuple[List[dict], List[dict]]:
    """Laad alle tasks + inputs vanuit artefact task-bestanden."""
    all_tasks: List[dict] = []
    all_inputs: List[dict] = []
    seen_labels: Set[str] = set()

    for f in task_files:
        try:
            data = json.loads(strip_jsonc(f.read_text(encoding="utf-8")))
        except Exception as e:
            print(f"  WAARSCHUWING: Kan {f.name} niet lezen: {e}", file=sys.stderr)
            continue
        for task in data.get("tasks", []):
            label = task.get("label", "")
            if label in seen_labels:
                print(f"  WAARSCHUWING: Duplicate label '{label}' in {f.name} -- overgeslagen")
                continue
            seen_labels.add(label)
            all_tasks.append(task)
        all_inputs.extend(data.get("inputs", []))

    return all_tasks, all_inputs


def extract_input_ids(tasks: List[dict]) -> Set[str]:
    blob = json.dumps(tasks, ensure_ascii=False)
    return set(re.findall(r"\$\{input:([^}]+)\}", blob))


def merge_tasks_into_target(
    target: dict,
    new_tasks: List[dict],
    new_inputs: List[dict],
) -> Tuple[int, int, int]:
    """Merge nieuwe tasks en inputs in target dict. Retourneert (added, replaced, inputs_changed)."""
    existing_by_label: Dict[str, dict] = {
        str(t.get("label", "")): t for t in target.get("tasks", [])
    }
    added = replaced = 0

    for task in new_tasks:
        label = str(task.get("label", ""))
        if label in existing_by_label:
            replaced += 1
        else:
            added += 1
        existing_by_label[label] = task

    target["tasks"] = list(existing_by_label.values())

    required_ids = extract_input_ids(new_tasks)
    existing_inputs: Dict[str, dict] = {
        str(i.get("id", "")): i for i in target.get("inputs", []) if i.get("id")
    }
    source_inputs: Dict[str, dict] = {
        str(i.get("id", "")): i for i in new_inputs if i.get("id")
    }

    inputs_changed = 0
    for iid in required_ids:
        src = source_inputs.get(iid)
        if not src:
            continue
        if existing_inputs.get(iid) != src:
            existing_inputs[iid] = src
            inputs_changed += 1

    target["inputs"] = sorted(existing_inputs.values(), key=lambda i: str(i.get("id", "")))
    return added, replaced, inputs_changed


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Haal prompts, agents en tasks op voor een value stream fase."
    )
    parser.add_argument("value_stream_fase", help="Bijv. aeo.02, fnd.02, sfw.03")
    parser.add_argument(
        "--source", type=Path, default=DEFAULT_SOURCE,
        help=f"Pad naar mandarin-agents (default: {DEFAULT_SOURCE})",
    )
    parser.add_argument(
        "--target", type=Path, default=DEFAULT_TARGET,
        help=f"Doel workspace (default: {DEFAULT_TARGET})",
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Toon wat er zou worden gekopieerd zonder te schrijven")
    args = parser.parse_args(argv)

    try:
        code, fase = parse_vsf(args.value_stream_fase)
    except ValueError as e:
        parser.error(str(e))

    source_root = args.source.expanduser().resolve()
    target_root = args.target.expanduser().resolve()
    artefacten_root = source_root / "artefacten"

    if not artefacten_root.is_dir():
        parser.error(
            f"artefacten/ map ontbreekt in {source_root}. "
            "Voer git pull uit of geef --source."
        )

    print(f"\nFetch {code}.{fase}  |  bron: {source_root}  ->  doel: {target_root}\n")

    fase_dirs = find_fase_dirs(artefacten_root, code, fase)
    if not fase_dirs:
        print(f"WAARSCHUWING: Geen agent-mappen gevonden voor {code}.{fase} in {artefacten_root}")
        return 1

    agents_found = [d.name.split(".", 2)[2] for d in fase_dirs]
    print(f"Gevonden agents ({len(fase_dirs)}): {', '.join(agents_found)}\n")

    # Prompts en contracten kopiëren
    prompts, contracts = collect_files(fase_dirs)

    print(f"Prompts ({len(prompts)}):")
    copied_prompts = copy_files(prompts, target_root / ".github" / "prompts", args.dry_run, "prompt")
    if not prompts:
        print("  (geen)")

    print(f"\nAgents ({len(contracts)}):")
    copied_contracts = copy_files(contracts, target_root / ".github" / "agents", args.dry_run, "agent")
    if not contracts:
        print("  (geen)")

    # Tasks mergen
    task_files = collect_task_files(fase_dirs)
    print(f"\nTasks-bestanden ({len(task_files)}):")

    tasks_added = tasks_replaced = inputs_changed = 0
    if task_files:
        artefact_tasks, artefact_inputs = load_artefact_tasks(task_files)
        if artefact_tasks:
            target_tasks_path = target_root / ".vscode" / "tasks.json"
            target_tasks = load_tasks_json(target_tasks_path)
            tasks_added, tasks_replaced, inputs_changed = merge_tasks_into_target(
                target_tasks, artefact_tasks, artefact_inputs
            )
            if not args.dry_run:
                target_tasks_path.parent.mkdir(parents=True, exist_ok=True)
                target_tasks_path.write_text(
                    json.dumps(target_tasks, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
            for f in task_files:
                prefix = "[dry] " if args.dry_run else ""
                print(f"  OK {prefix}{f.parent.parent.name}/tasks/{f.name}")
    else:
        print("  (geen)")

    # Samenvatting
    mode = "[DRY-RUN] " if args.dry_run else ""
    print(f"\n{'-'*60}")
    print(f"{mode}Klaar voor {code}.{fase}")
    print(f"  Prompts gekopieerd : {len(copied_prompts)}")
    print(f"  Agents gekopieerd  : {len(copied_contracts)}")
    print(f"  Tasks toegevoegd   : {tasks_added}")
    print(f"  Tasks vervangen    : {tasks_replaced}")
    print(f"  Inputs bijgewerkt  : {inputs_changed}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))