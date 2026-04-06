#!/usr/bin/env python3
"""
Runner voor agent: handoff-steward

Beschikbare intents:
- realiseer-handoff-sluiting
- realiseer-initiele-handoff
- realiseer-overzicht-inspectie-handoffs

Architectuur: One Agent, One Runner.
Deze runner delegeert execution-file generatie aan ecosysteem-coordinator.runner.py.
"""

from pathlib import Path
import argparse
import os
import subprocess
import sys


TARGET_AGENT = 'handoff-steward'


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

    p_realiseer_handoff_sluiting = subparsers.add_parser('realiseer-handoff-sluiting', help='Intent: realiseer-handoff-sluiting')
    p_realiseer_handoff_sluiting.add_argument('--handoff-id', required=True, help='De handoff-identificatie van de te sluiten handoff')
    p_realiseer_handoff_sluiting.add_argument('--handoff-register', required=True, help='Pad naar het handoff-register dat wordt bijgewerkt')
    p_realiseer_handoff_sluiting.add_argument('--ontvangstbevestiging', required=False, help='Beschrijving of referentie van de bevestiging van ontvangst door de ontvangende agent')
    p_realiseer_handoff_sluiting.add_argument('--sluitings-datum', required=False, help='Datum van sluiting')

    p_realiseer_initiele_handoff = subparsers.add_parser('realiseer-initiele-handoff', help='Intent: realiseer-initiele-handoff')
    p_realiseer_initiele_handoff.add_argument('--execution-bestand', required=True, help='Pad naar het afgeronde execution-bestand van de overdragende agent')
    p_realiseer_initiele_handoff.add_argument('--ontvangende-agent', required=True, help='Identifier van de agent die het handoff-bestand ontvangt')
    p_realiseer_initiele_handoff.add_argument('--handoff-register', required=True, help='Pad naar het handoff-register')
    p_realiseer_initiele_handoff.add_argument('--overdrachtsnota', required=False, help='Vrije tekst met aanvullende instructie of context voor de ontvanger')
    p_realiseer_initiele_handoff.add_argument('--escalatie-indicatie', required=False, help='Geeft aan of de handoff een escalation van de overdragende agent naar een mens vereist')
    p_realiseer_initiele_handoff.add_argument('--escalatie-reden', required=False, help='Beschrijving van de situatie die escalatie vereist')
    p_realiseer_initiele_handoff.add_argument('--escalatie-urgentie', required=False, help='Ernst van de escalatie')

    p_realiseer_overzicht_inspectie_handoffs = subparsers.add_parser('realiseer-overzicht-inspectie-handoffs', help='Intent: realiseer-overzicht-inspectie-handoffs')
    p_realiseer_overzicht_inspectie_handoffs.add_argument('--handoff-register', required=True, help='Pad naar het handoff-register')
    p_realiseer_overzicht_inspectie_handoffs.add_argument('--filter-status', required=False, help='Filtert het overzicht op status')
    p_realiseer_overzicht_inspectie_handoffs.add_argument('--filter-maand', required=False, help='Filtert het overzicht op kalendermaand in formaat `JJMM`')
    p_realiseer_overzicht_inspectie_handoffs.add_argument('--output-bestand', required=False, help='Pad naar het bestand waar het overzicht wordt geschreven')

    args = parser.parse_args()
    params = {
        key: value
        for key, value in vars(args).items()
        if key != "intent" and value is not None
    }
    return run_intent(args.intent, params)


if __name__ == "__main__":
    sys.exit(main())
