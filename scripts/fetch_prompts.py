"""Fetch prompt files for a value stream fase and copy them to a target workspace.

Bron: artefacten/<code>/<code>.<fase>.<agent>/mandarin.<agent>.*.prompt.md
Doel:  target/.github/prompts/

Typical usage (from another workspace):
    python ..\\mandarin-agents\\scripts\\fetch_prompts.py sfw.03 --source ..\\mandarin-agents --target .

Default source lookup: if this script lives in mandarin-canon, it auto-targets the
peer repo mandarin-agents (../mandarin-agents). Otherwise it uses the repo root it
is in. Override with --source as needed.

Default target: the repo root where this script lives (so calling from scripts/ still
copies into repo/.github/prompts). Override with --target to point elsewhere.

The script reads agents-publicatie.json, finds agents for the given value stream code
and fase, collects their prompt files from artefacten/, and copies them into
.github/prompts in the target workspace. A log file is written to logs/ with details
of the run. Use --dry-run to see what would happen.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
SIBLING_AGENTS = REPO_ROOT.parent / "mandarin-agents"

# Prefer sibling mandarin-agents when this script is placed in mandarin-canon; else use current repo.
if REPO_ROOT.name != "mandarin-agents" and SIBLING_AGENTS.exists():
    DEFAULT_SOURCE = SIBLING_AGENTS.resolve()
else:
    DEFAULT_SOURCE = REPO_ROOT

# Default target is the repo root where this script lives so running from scripts/ keeps
# .github/prompts under the repository, not under the current working directory.
DEFAULT_TARGET = REPO_ROOT


def parse_value_stream_fase(value: str) -> Tuple[str, str]:
    if "." not in value:
        raise ValueError("Gebruik formaat <code>.<fase>, bijvoorbeeld sfw.03")
    code, fase = value.split(".", 1)
    code = code.strip().lower()
    fase = fase.strip().zfill(2)
    if not code or not fase.isdigit():
        raise ValueError("Ongeldige value stream of fase; verwacht zoiets als sfw.03")
    return code, fase


def load_publicatie(source_root: Path) -> Dict:
    manifest_path = source_root / "agents-publicatie.json"
    if not manifest_path.is_file():
        hint = "Voer een git pull uit in de bron of geef --source naar mandarin-agents."
        raise FileNotFoundError(f"Niet gevonden: {manifest_path}. {hint}")
    with manifest_path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def find_agents(manifest: Dict, code: str, fase: str) -> List[str]:
    for vs in manifest.get("value_streams", []):
        if vs.get("code", "").lower() != code:
            continue
        for fase_entry in vs.get("fasen", []):
            if str(fase_entry.get("volgnummer", "")).zfill(2) == fase:
                return [agent.get("naam", "").strip() for agent in fase_entry.get("agents", []) if agent.get("naam")]
    raise ValueError(f"Geen agents gevonden voor {code}.{fase}")


def collect_prompt_files(artefacten_root: Path, code: str, fase: str, agents: Iterable[str]) -> Dict[str, List[Path]]:
    base = artefacten_root / code
    if not base.is_dir():
        raise FileNotFoundError(f"Artefacten map ontbreekt: {base}")

    mapping: Dict[str, List[Path]] = {}
    fase_marker = f"{code}.{fase}"
    fase_dirs = [p for p in base.iterdir() if p.is_dir() and p.name.startswith(fase_marker)]
    for agent in agents:
        # Pattern matcht mandarin.{agent}-*.prompt.md en mandarin.{agent}.*.prompt.md
        pattern = f"mandarin.{agent}*.prompt.md"
        hits: List[Path] = []
        for fase_dir in fase_dirs:
            hits.extend(fase_dir.glob(pattern))
        mapping[agent] = sorted(hits)
    return mapping


def copy_prompts(mapping: Dict[str, List[Path]], target_dir: Path, dry_run: bool) -> List[Path]:
    copied: List[Path] = []
    if not target_dir.exists() and not dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)
    for files in mapping.values():
        for src in files:
            dest = target_dir / src.name
            copied.append(dest)
            if dry_run:
                continue
            shutil.copy2(src, dest)
    return copied


def write_log(target_root: Path, code: str, fase: str, mapping: Dict[str, List[Path]], copied: List[Path], dry_run: bool, source_root: Path) -> Path:
    logs_dir = target_root / "logs"
    if not logs_dir.exists() and not dry_run:
        logs_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_path = logs_dir / f"fetch-prompts-{code}-{fase}-{timestamp}.log"
    lines = [
        f"timestamp: {timestamp}",
        f"value_stream: {code}",
        f"fase: {fase}",
        f"source: {source_root}",
        f"target: {target_root}",
        f"dry_run: {dry_run}",
        "agents: " + ", ".join(sorted(mapping.keys())),
    ]
    lines.append("files:")
    for agent, files in sorted(mapping.items()):
        if files:
            for f in files:
                lines.append(f"  {agent}: {f}")
        else:
            lines.append(f"  {agent}: GEEN PROMPTS GEVONDEN")
    if copied:
        lines.append("copied:")
        for dest in copied:
            lines.append(f"  {dest}")
    if dry_run:
        lines.append("actie: dry-run, niets gekopieerd")
    content = "\n".join(lines) + "\n"
    if not dry_run:
        log_path.write_text(content, encoding="utf-8")
    return log_path


def build_message(code: str, fase: str, copied: List[Path], missing: List[str], dry_run: bool) -> str:
    if dry_run:
        base = f"Dry-run klaar voor {code}.{fase}." if copied or missing else f"Geen prompts gevonden voor {code}.{fase}."
    else:
        base = f"Yes! Prompts voor {code}.{fase} zijn klaargezet." if copied else f"Geen prompts gekopieerd voor {code}.{fase}."
    parts = [base]
    if copied:
        parts.append(f"Gekopieerd: {len(copied)} files.")
    if missing:
        parts.append(f"Ontbrekend voor agents: {', '.join(sorted(missing))}.")
    if not dry_run:
        parts.append("Succes met de volgende stap!")
    return " ".join(parts)


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description="Fetch prompt files voor een value stream fase")
    parser.add_argument("value_stream_fase", help="Formaat <code>.<fase> bijvoorbeeld sfw.03")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE, help="Pad naar mandarin-agents bron (met agents-publicatie.json)")
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET, help="Doel workspace waarin .github/prompts staat")
    parser.add_argument("--dry-run", action="store_true", help="Toon wat er zou gebeuren zonder te kopiëren")
    args = parser.parse_args(argv)

    code, fase = parse_value_stream_fase(args.value_stream_fase)
    source_root = args.source.expanduser().resolve()
    target_root = args.target.expanduser().resolve()
    manifest_path = source_root / "agents-publicatie.json"
    artefacten_root = source_root / "artefacten"
    if not manifest_path.is_file():
        parser.error(f"agents-publicatie.json ontbreekt in {source_root}. Tip: git pull in mandarin-agents of geef --source.")
    if not artefacten_root.is_dir():
        parser.error(f"Artefacten map ontbreekt: {artefacten_root}. Tip: git pull in mandarin-agents of geef --source.")

    manifest = load_publicatie(source_root)
    agents = find_agents(manifest, code, fase)
    mapping = collect_prompt_files(artefacten_root, code, fase, agents)
    copied = copy_prompts(mapping, target_root / ".github" / "prompts", args.dry_run)
    missing = [agent for agent, files in mapping.items() if not files]
    log_path = write_log(target_root, code, fase, mapping, copied, args.dry_run, source_root)

    message = build_message(code, fase, copied, missing, args.dry_run)
    print(message)
    if not args.dry_run:
        print(f"Log: {log_path}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main(sys.argv[1:]))
