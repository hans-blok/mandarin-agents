#!/usr/bin/env python3
"""
Agent Runner: documentatie-omvormer
Value Stream: fnd (Foundation)
Fase: 01

Automatisch gegenereerd door agent-engineer.
"""
import sys
import argparse
import subprocess
import os
from pathlib import Path
from datetime import datetime


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
        print(f"\n\033[1mInstructies gegenereerd. Bekijk prompt-instructions/ folder.\033[0m")
    else:
        print(f"❌ Fout opgetreden bij genereren instructies voor {intent}.", file=sys.stderr)
        sys.exit(result.returncode)


def main():
    parser = argparse.ArgumentParser(
        description="Runner voor agent: documentatie-omvormer",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="intent", required=True, help="Beschikbare intents (commando's)")

    # 1. genereer-publicatiestructuur
    p_pub = subparsers.add_parser(
        "genereer-publicatiestructuur", 
        help="Transformeer markdown naar MkDocs-compatibele mappenstructuur"
    )
    p_pub.add_argument(
        "--structuur-regels", 
        default="", 
        help="Expliciete regels voor mappenstructuur of volgorde (optioneel)"
    )
    p_pub.add_argument(
        "--exclude-patterns", 
        default="", 
        help="Patronen voor bestanden/mappen die moeten worden uitgesloten (optioneel)"
    )

    # 2. genereer-navigatiebestand
    p_nav = subparsers.add_parser(
        "genereer-navigatiebestand", 
        help="Genereer nav-sectie voor mkdocs.yml"
    )
    # Geen parameters voor deze intent

    # 3. genereer-correcte-links
    p_links = subparsers.add_parser(
        "genereer-correcte-links", 
        help="Valideer en rapporteer interne links"
    )
    p_links.add_argument(
        "--docs-folder", 
        required=True, 
        help="Pad naar de docs-map met te controleren documentatie"
    )
    p_links.add_argument(
        "--platform", 
        required=True, 
        choices=["github", "gitlab", "mkdocs"],
        help="Doelplatform voor linkvalidatie: github, gitlab, of mkdocs"
    )
    p_links.add_argument(
        "--base-url", 
        default="", 
        help="Basis-URL voor absolute links (optioneel)"
    )
    p_links.add_argument(
        "--exclude-patterns", 
        default="", 
        help="Patronen voor bestanden die moeten worden overgeslagen (optioneel)"
    )

    args = parser.parse_args()
    
    # Filter 'intent' argument uit de dictionary voor doorgifte aan de generator
    params_dict = vars(args).copy()
    del params_dict['intent']
    
    # Normaliseer parameter keys: CLI gebruikt '-', generator verwacht '_'
    formatted_params = {k.replace('-', '_'): v for k, v in params_dict.items()}

    run_generate_instructions("documentatie-omvormer", args.intent, formatted_params)


if __name__ == "__main__":
    main()
