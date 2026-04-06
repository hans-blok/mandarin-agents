#!/usr/bin/env python3
"""
Agent Runner: thema-verwoorder
Automatisch gegenereerd door agent-engineer.

Intents:
- definieer-thematische-scope: Zet hypothese om naar thematische scope
- definieer-epic-structuur: Structureer epic binnen thematische context
- definieer-verbeter-voorstel: Genereer verbetervoorstellen voor thema
"""
import sys
import argparse
import subprocess
import os
from pathlib import Path


def run_generate_instructions(agent_naam: str, intent: str, params: dict):
    """Roep ecosysteem-coordinator aan voor instructie-generatie."""
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
        description="Runner voor agent: thema-verwoorder",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="intent", required=True, help="Beschikbare intents (commando's)")

    # 1. definieer-thematische-scope
    p_scope = subparsers.add_parser("definieer-thematische-scope", 
        help="Definieer thematische scope op basis van hypothese")
    p_scope.add_argument("--hypothese-bestand", required=True, 
        help="Bestandsnaam of code van het hypothese-document (bijv. HYP-20260327-01)")
    p_scope.add_argument("--auteur", required=True, 
        help="Naam van de auteur")
    p_scope.add_argument("--toelichting", default="", 
        help="Aanvullende toelichting (optioneel)")

    # 2. definieer-epic-structuur
    p_epic = subparsers.add_parser("definieer-epic-structuur", 
        help="Definieer epic structuur binnen thematische context")
    p_epic.add_argument("--hypothese-code", required=True, 
        help="Unieke hypothese-code (bijv. HYP-20260327-01)")
    p_epic.add_argument("--thema-code", required=True, 
        help="Unieke thema-code")
    p_epic.add_argument("--auteur", required=True, 
        help="Naam van de auteur")

    # 3. definieer-verbeter-voorstel
    p_verbeter = subparsers.add_parser("definieer-verbeter-voorstel", 
        help="Genereer verbetervoorstellen voor thema")
    p_verbeter.add_argument("--hypothese-code", required=True, 
        help="Unieke hypothese-code (bijv. HYP-20260327-01)")
    p_verbeter.add_argument("--thema-code", required=True, 
        help="Unieke thema-code")
    p_verbeter.add_argument("--auteur", required=True, 
        help="Naam van de auteur")
    p_verbeter.add_argument("--toelichting", default="", 
        help="Aanvullende context of richting (optioneel)")

    args = parser.parse_args()
    
    # Filter 'intent' argument uit de dictionary voor doorgifte aan de generator
    params_dict = vars(args).copy()
    del params_dict['intent']
    
    # Format de keys om '-' naar '_' te normaliseren
    formatted_params = {k.replace('-', '_'): v for k, v in params_dict.items()}

    run_generate_instructions("thema-verwoorder", args.intent, formatted_params)


if __name__ == "__main__":
    main()
