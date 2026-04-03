#!/usr/bin/env python3
"""
Runner voor agent: core-framework-architect

Beschikbare intents:
- structureer-actieve-structuur
- structureer-gedrag
- structureer-passieve-structuur
- structureer-totaal-view

Architectuur: One Agent, One Runner.
Deze runner delegeert execution-file generatie aan ecosysteem-coordinator.runner.py.
"""

from pathlib import Path
import argparse
import os
import subprocess
import sys


TARGET_AGENT = 'core-framework-architect'


def find_ecosysteem_coordinator_runner() -> Path:
    """Zoek de ecosysteem-coordinator runner."""
    this_file = Path(__file__).resolve()
    repo_root = this_file.parent.parent.parent.parent.parent

    candidate = repo_root / "artefacten" / "fnd" / "fnd.01.ecosysteem-coordinator" / "runner" / "ecosysteem-coordinator.runner.py"
    if candidate.exists():
        return candidate

    cwd_candidate = Path.cwd() / "artefacten" / "fnd" / "fnd.01.ecosysteem-coordinator" / "runner" / "ecosysteem-coordinator.runner.py"
    if cwd_candidate.exists():
        return cwd_candidate

    raise FileNotFoundError("ecosysteem-coordinator.runner.py niet gevonden")


def run_intent(intent: str, params: dict[str, str]) -> int:
    """Delegeer intent-uitvoering naar de ecosysteem-coordinator."""
    coordinator = find_ecosysteem_coordinator_runner()
    cmd = [
        sys.executable,
        str(coordinator),
        "genereer-instructies",
        "--agent",
        TARGET_AGENT,
        "--intent",
        intent,
    ]

    for key, value in params.items():
        if value is None or value == "":
            continue
        cmd.extend(["-p", f"{key}={value}"])

    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(cmd, env=env).returncode


def main() -> int:
    parser = argparse.ArgumentParser(
        description=f"Runner voor agent: {TARGET_AGENT}",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="intent", required=True, help="Beschikbare intents")

    p_structureer_actieve_structuur = subparsers.add_parser('structureer-actieve-structuur', help='Intent: structureer-actieve-structuur')
    p_structureer_actieve_structuur.add_argument('--archimate-laag', required=True, help='Te modelleren ArchiMate-laag')
    p_structureer_actieve_structuur.add_argument('--bestand', required=True, help='Pad naar het bronbestand dat als input dient voor modellering')

    p_structureer_gedrag = subparsers.add_parser('structureer-gedrag', help='Intent: structureer-gedrag')
    p_structureer_gedrag.add_argument('--archimate-laag', required=True, help='Te modelleren ArchiMate-laag')
    p_structureer_gedrag.add_argument('--bestand', required=True, help='Pad naar het bronbestand dat als input dient voor modellering')

    p_structureer_passieve_structuur = subparsers.add_parser('structureer-passieve-structuur', help='Intent: structureer-passieve-structuur')
    p_structureer_passieve_structuur.add_argument('--archimate-laag', required=True, help='Te modelleren ArchiMate-laag')
    p_structureer_passieve_structuur.add_argument('--bestand', required=True, help='Pad naar het bronbestand dat als input dient voor modellering')

    p_structureer_totaal_view = subparsers.add_parser('structureer-totaal-view', help='Intent: structureer-totaal-view')
    p_structureer_totaal_view.add_argument('--archimate-laag', required=True, help='Te modelleren ArchiMate-laag')
    p_structureer_totaal_view.add_argument('--bestand', required=True, help='Pad naar het bronbestand dat als input dient voor modellering')

    args = parser.parse_args()
    params = {
        key: value
        for key, value in vars(args).items()
        if key != "intent" and value is not None
    }
    return run_intent(args.intent, params)


if __name__ == "__main__":
    sys.exit(main())
