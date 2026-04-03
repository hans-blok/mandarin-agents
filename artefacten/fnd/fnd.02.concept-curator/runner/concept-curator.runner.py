#!/usr/bin/env python3
"""
Runner voor agent: concept-curator

Beschikbare intents:
- definieer-concept
- rapporteer-concept-status
- valideer-concept-coherentie
- verweef-concepten

Architectuur: One Agent, One Runner.
Deze runner delegeert execution-file generatie aan ecosysteem-coordinator.runner.py.
"""

from pathlib import Path
import argparse
import os
import subprocess
import sys


TARGET_AGENT = 'concept-curator'


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

    p_definieer_concept = subparsers.add_parser('definieer-concept', help='Intent: definieer-concept')
    p_definieer_concept.add_argument('--term', required=True, help='De naam van het te definiëren concept')
    p_definieer_concept.add_argument('--definitie', required=True, help='De voorgestelde definitie van het concept')
    p_definieer_concept.add_argument('--domein', required=True, help='Het domein waarbinnen het concept wordt gedefinieerd')
    p_definieer_concept.add_argument('--synoniemen', required=False, help='Lijst van alternatieve termen')
    p_definieer_concept.add_argument('--relaties', required=False, help='Lijst van gerelateerde concepten')
    p_definieer_concept.add_argument('--bron', required=False, help='Bronvermelding van de definitie')

    p_rapporteer_concept_status = subparsers.add_parser('rapporteer-concept-status', help='Intent: rapporteer-concept-status')
    p_rapporteer_concept_status.add_argument('--domein', required=True, help='Het te inventariseren concepten-domein')
    p_rapporteer_concept_status.add_argument('--formaat', required=False, help="Gewenst output-formaat ('markdown', 'json')")
    p_rapporteer_concept_status.add_argument('--status-filter', required=False, help="Filter op status ('concept', 'stable', 'deprecated', 'all')")

    p_valideer_concept_coherentie = subparsers.add_parser('valideer-concept-coherentie', help='Intent: valideer-concept-coherentie')
    p_valideer_concept_coherentie.add_argument('--artefact-bestand', required=True, help='Het te valideren document of bestand')
    p_valideer_concept_coherentie.add_argument('--domein', required=True, help='Het referentiekader waartegen gevalideerd wordt')
    p_valideer_concept_coherentie.add_argument('--striktheid', required=False, help="Niveau van validatie ('strict', 'normal', 'lenient')")

    p_verweef_concepten = subparsers.add_parser('verweef-concepten', help='Intent: verweef-concepten')
    p_verweef_concepten.add_argument('--concept-bestand', required=True, help='Pad naar het bestand waarin concepten verweven moeten worden')

    args = parser.parse_args()
    params = {
        key: value
        for key, value in vars(args).items()
        if key != "intent" and value is not None
    }
    return run_intent(args.intent, params)


if __name__ == "__main__":
    sys.exit(main())
