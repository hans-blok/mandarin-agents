#!/usr/bin/env python3
"""
Runner voor agent: positionering-en-monetisatie-toetser

Beschikbare intents:
- signaleer-spanningsvelden
- stel-toetsingsrapport-op
- toets-strategische-compatibiliteit

Architectuur: One Agent, One Runner.
Deze runner delegeert execution-file generatie aan ecosysteem-coordinator.runner.py.
"""

from pathlib import Path
import argparse
import os
import subprocess
import sys


TARGET_AGENT = 'positionering-en-monetisatie-toetser'


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

    p_signaleer_spanningsvelden = subparsers.add_parser('signaleer-spanningsvelden', help='Intent: signaleer-spanningsvelden')
    p_signaleer_spanningsvelden.add_argument('--longlist-bron', required=True, help='Pad naar bestaand longlist-document met kandidaat-leveranciers')
    p_signaleer_spanningsvelden.add_argument('--spanningsveld-focus', required=True, help='Beschrijving van de spanningsveld-dimensies die moeten worden gesignaleerd')
    p_signaleer_spanningsvelden.add_argument('--strategische-kaders', required=False, help='Beschrijving van de geldende positioneringskaders als context voor spanningsveld-interpretatie')
    p_signaleer_spanningsvelden.add_argument('--te-analyseren-kandidaten', required=False, help='Subset van leveranciers uit de longlist die moeten worden geanalyseerd')
    p_signaleer_spanningsvelden.add_argument('--output-naam', required=False, help='Logische naam voor het outputbestand')
    p_signaleer_spanningsvelden.add_argument('--aanvullende-context', required=False, help='Extra technische of contractuele context over de leveranciers')

    p_stel_toetsingsrapport_op = subparsers.add_parser('stel-toetsingsrapport-op', help='Intent: stel-toetsingsrapport-op')
    p_stel_toetsingsrapport_op.add_argument('--toetsing-bron', required=True, help='Pad naar bestaand strategische-compatibiliteitstoetsing-document')
    p_stel_toetsingsrapport_op.add_argument('--spanningsvelden-bron', required=True, help='Pad naar bestaand spanningsvelden-overzicht')
    p_stel_toetsingsrapport_op.add_argument('--longlist-bron', required=False, help='Pad naar het originele longlist-document voor contextcompletiteit')
    p_stel_toetsingsrapport_op.add_argument('--output-naam', required=False, help='Logische naam voor het outputbestand')
    p_stel_toetsingsrapport_op.add_argument('--aanvullende-context', required=False, help='Extra context die in het rapport moet worden meegenomen')

    p_toets_strategische_compatibiliteit = subparsers.add_parser('toets-strategische-compatibiliteit', help='Intent: toets-strategische-compatibiliteit')
    p_toets_strategische_compatibiliteit.add_argument('--longlist-bron', required=True, help='Pad naar bestaand longlist-document met kandidaat-leveranciers')
    p_toets_strategische_compatibiliteit.add_argument('--strategische-kaders', required=True, help='Beschrijving van de geldende positioneringskaders en monetisatie-logica waarop getoetst wordt')
    p_toets_strategische_compatibiliteit.add_argument('--selectiecriteria-bron', required=False, help='Pad naar bestaand selectiecriteria-document als aanvullende context voor de toetsing')
    p_toets_strategische_compatibiliteit.add_argument('--te-toetsen-kandidaten', required=False, help='Subset van leveranciers uit de longlist die moeten worden getoetst')
    p_toets_strategische_compatibiliteit.add_argument('--output-naam', required=False, help='Logische naam voor het outputbestand')
    p_toets_strategische_compatibiliteit.add_argument('--aanvullende-context', required=False, help='Extra strategische context of bekende constraints die relevant zijn voor de toetsing')

    args = parser.parse_args()
    params = {
        key: value
        for key, value in vars(args).items()
        if key != "intent" and value is not None
    }
    return run_intent(args.intent, params)


if __name__ == "__main__":
    sys.exit(main())
