#!/usr/bin/env python3
"""
Runner voor agent: canon-curator

Beschikbare intents:
- adviseer-grondslag-verbeteringen
- valideer-grondslag-consistentie
- valideer-terminologische-scherpte

Architectuur: One Agent, One Runner.
Deze runner delegeert execution-file generatie aan ecosysteem-coordinator.runner.py.
"""

from pathlib import Path
import argparse
import os
import subprocess
import sys


TARGET_AGENT = 'canon-curator'


def find_ecosysteem_coordinator_runner() -> Path:
    """Zoek de ecosysteem-coordinator runner."""
    this_file = Path(__file__).resolve()
    repo_root = this_file.parent.parent.parent.parent

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

    p_adviseer_grondslag_verbeteringen = subparsers.add_parser('adviseer-grondslag-verbeteringen', help='Intent: adviseer-grondslag-verbeteringen')
    p_adviseer_grondslag_verbeteringen.add_argument('--scope', required=True, help='Pad of selectie van grondslag-artefacten waarvoor verbeteradvies wordt gevraagd')
    p_adviseer_grondslag_verbeteringen.add_argument('--focus', required=False, help='Specifiek verbeterdomein om op te richten')

    p_valideer_grondslag_consistentie = subparsers.add_parser('valideer-grondslag-consistentie', help='Intent: valideer-grondslag-consistentie')
    p_valideer_grondslag_consistentie.add_argument('--scope', required=True, help='Pad of selectie van te toetsen grondslag-artefacten binnen de canon')

    p_valideer_terminologische_scherpte = subparsers.add_parser('valideer-terminologische-scherpte', help='Intent: valideer-terminologische-scherpte')
    p_valideer_terminologische_scherpte.add_argument('--scope', required=True, help='Pad of selectie van te toetsen grondslag-artefacten binnen de canon')
    p_valideer_terminologische_scherpte.add_argument('--termenlijst', required=False, help='Expliciete lijst van termen om specifiek te controleren')

    args = parser.parse_args()
    params = {
        key: value
        for key, value in vars(args).items()
        if key != "intent" and value is not None
    }
    return run_intent(args.intent, params)


if __name__ == "__main__":
    sys.exit(main())
