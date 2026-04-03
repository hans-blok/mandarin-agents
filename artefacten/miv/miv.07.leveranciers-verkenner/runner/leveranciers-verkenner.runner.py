#!/usr/bin/env python3
"""
Runner voor agent: leveranciers-verkenner

Beschikbare intents:
- beschrijf-leveranciersfit
- beschrijf-longlist
- beschrijf-uitsluitingsgronden

Architectuur: One Agent, One Runner.
Deze runner delegeert execution-file generatie aan ecosysteem-coordinator.runner.py.
"""

from pathlib import Path
import argparse
import os
import subprocess
import sys


TARGET_AGENT = 'leveranciers-verkenner'


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

    p_beschrijf_leveranciersfit = subparsers.add_parser('beschrijf-leveranciersfit', help='Intent: beschrijf-leveranciersfit')
    p_beschrijf_leveranciersfit.add_argument('--longlist-bron', required=True, help='Pad naar bestaand longlist-document of gelijkwaardige lijst van kandidaat-leveranciers die inhoudelijk in aanmerking komen')
    p_beschrijf_leveranciersfit.add_argument('--fit-aspecten', required=True, help='Beschrijving van de fit-aspecten, gebaseerd op het door de agent gelokaliseerde behoefteprofiel, die per leverancier moeten worden geduid, zoals managed services, compliance, GitLab-beheer, supportmodel en schaalbaarheid')
    p_beschrijf_leveranciersfit.add_argument('--output-naam', required=False, help='Logische naam voor het outputbestand')
    p_beschrijf_leveranciersfit.add_argument('--selectiecriteria-bron', required=False, help='Pad naar bestaand document met selectiecriteria voor aanvullende duiding')
    p_beschrijf_leveranciersfit.add_argument('--aanvullende-context', required=False, help='Extra operationele context of bekende beperkingen voor de fit-duiding')

    p_beschrijf_longlist = subparsers.add_parser('beschrijf-longlist', help='Intent: beschrijf-longlist')
    p_beschrijf_longlist.add_argument('--aanvullende-randvoorwaarden', required=False, help='Aanvullende context of uitsluitingen die niet expliciet in behoefteprofiel of selectiecriteria zijn opgenomen')

    p_beschrijf_uitsluitingsgronden = subparsers.add_parser('beschrijf-uitsluitingsgronden', help='Intent: beschrijf-uitsluitingsgronden')
    p_beschrijf_uitsluitingsgronden.add_argument('--selectiecriteria-bron', required=True, help='Pad naar bestaand document met selectiecriteria of harde randvoorwaarden voor leveranciersuitsluiting')
    p_beschrijf_uitsluitingsgronden.add_argument('--leveranciersbron', required=True, help='Pad naar longlist, bruto leverancierslijst of marktoverzicht waarin mogelijke leveranciers zijn opgenomen')
    p_beschrijf_uitsluitingsgronden.add_argument('--output-naam', required=False, help='Logische naam voor het outputbestand')
    p_beschrijf_uitsluitingsgronden.add_argument('--scope-afbakening', required=False, help='Aanvullende scopebeschrijving voor expliciete mismatch-detectie')
    p_beschrijf_uitsluitingsgronden.add_argument('--aanvullende-bronnen', required=False, help='Lijst van externe bronnen die de uitsluitingsgrond onderbouwen')

    args = parser.parse_args()
    params = {
        key: value
        for key, value in vars(args).items()
        if key != "intent" and value is not None
    }
    return run_intent(args.intent, params)


if __name__ == "__main__":
    sys.exit(main())
