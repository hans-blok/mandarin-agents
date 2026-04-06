#!/usr/bin/env python3
"""
Agent Runner: hypothese-vormer
Automatisch gegenereerd door agent-engineer (concept fase).
"""
import sys
import argparse
import subprocess
import os
from pathlib import Path
from datetime import datetime
import hashlib

def run_generate_instructions(agent_naam: str, intent: str, params: dict):
    # Vind root van mandarin-agents (waar dit script staat)
    script_root = Path(__file__).resolve().parent.parent.parent.parent.parent
    
    # Gebruik ecosysteem-coordinator runner voor genereer-instructies
    generator = script_root / 'artefacten' / 'fnd' / 'fnd.01.ecosysteem-coordinator' / 'runner' / 'ecosysteem-coordinator.runner.py'
    
    if not generator.exists():
        print(f"❌ Generator niet gevonden: {generator}", file=sys.stderr)
        sys.exit(1)
    
    cmd = [
        sys.executable, str(generator), 'genereer-instructies',
        "--agent", agent_naam,
        "--intent", intent,
    ]
    
    for k, v in params.items():
        if v:  # Filter lege optionals eruit
            cmd.extend(["-p", f"{k}={v}"])
            
    # Subprocess Environment
    env = dict(os.environ)
    env['PYTHONIOENCODING'] = 'utf-8'
    
    print(f"🚀 Start {agent_naam} met intent '{intent}'...")
    result = subprocess.run(cmd, env=env)
    
    if result.returncode == 0:
        print(f"\n\033[1mInstructies gegenereerd. Bekijk executions/ folder.\033[0m")
    else:
        print(f"❌ Fout opgetreden bij genereren instructies voor {intent}.", file=sys.stderr)
        sys.exit(result.returncode)

def main():
    parser = argparse.ArgumentParser(
        description="Runner voor agent: hypothese-vormer",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="intent", required=True, help="Beschikbare intents (commando's)")

    # 1. beschrijf-hypothese
    p_hyp = subparsers.add_parser("beschrijf-hypothese", help="Formuleer een hypothese op basis van een probleem en idee")
    p_hyp.add_argument("--probleem", required=True, help="Het probleem dat je wilt oplossen")
    p_hyp.add_argument("--idee-voor-de-oplossing", required=True, help="Je idee voor de oplossing")
    p_hyp.add_argument("--auteur", required=True, help="Naam van de auteur")
    p_hyp.add_argument("--bronnen", default="", help="Bronnen (optioneel)")
    p_hyp.add_argument("--context", default="", help="Context informatie (optioneel)")
    p_hyp.add_argument("--betrokkenen", default="", help="Betrokkenen (optioneel)")

    # 2. beschrijf-aannames
    p_aan = subparsers.add_parser("beschrijf-aannames", help="Beschrijf de aannames in een hypothese")
    p_aan.add_argument("--hypothese-titel", required=True, help="Titel van de hypothese")

    # 3. beschrijf-toetsbaarheid
    p_toets = subparsers.add_parser("beschrijf-toetsbaarheid", help="Beschrijf hoe de hypothese getoetst kan worden")
    p_toets.add_argument("--hypothese-statement", required=True, help="De hypothese statement")
    p_toets.add_argument("--auteur", required=True, help="Naam van de auteur")
    p_toets.add_argument("--hypothese-bestand", default="", help="Pad naar hypothese bestand (optioneel)")
    p_toets.add_argument("--toetsingscontext", default="", help="Context voor toetsing (optioneel)")
    p_toets.add_argument("--beschikbare-metrics", default="", help="Beschikbare metrics (optioneel)")
    p_toets.add_argument("--acceptatie-drempel", default="", help="Acceptatie drempel (optioneel)")

    args = parser.parse_args()
    
    # Filter 'intent' argument uit de dictionary voor doorgifte aan de generator
    params_dict = vars(args).copy()
    del params_dict['intent']
    
    # Format de keys om '-' terug naar '_' te normaliseren als nodig, al is het nu netjes in CLI params
    # We vertalen het exact zoals aangenomen wordt in parameters
    formatted_params = {k.replace('-', '_'): v for k, v in params_dict.items()}

    run_generate_instructions("hypothese-vormer", args.intent, formatted_params)

if __name__ == "__main__":
    main()
