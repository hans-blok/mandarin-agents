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
    # Vind root van de workspace
    workspace_root = Path(__file__).resolve().parent.parent.parent.parent.parent
    if not (workspace_root / "artefacten").exists():
        # Fallback als we ergens anders draaien
        workspace_root = Path.cwd()
        
    generator = workspace_root / 'artefacten' / 'aeo' / 'aeo.02.agent-engineer' / 'runners' / 'agent-engineer.runner.py'
    
    # Maak output pad
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    hash_input = f"{timestamp}{agent_naam}".encode('utf-8')
    hash_str = hashlib.md5(hash_input).hexdigest()[:4].lower()
    
    exec_dir = workspace_root / "prompt-instructions"
    exec_dir.mkdir(exist_ok=True)
    filename = exec_dir / f"{timestamp}-{agent_naam}.{intent}.md"
    
    cmd = [
        sys.executable, str(generator), 'generate-instructions',
        "--agent", agent_naam,
        "--intent", intent,
        "--execution-file", str(filename)
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
        # Open in VS Code
        subprocess.run(["code", str(filename)], shell=True)
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
    p_hyp = subparsers.add_parser("beschrijf-hypothese", help="beschrijf-hypothese")
    p_hyp.add_argument("--hypothese-document", required=True, help="Pad naar je document/tekst")

    # 2. beschrijf-aannames
    p_aan = subparsers.add_parser("beschrijf-aannames", help="beschrijf-aannames")
    p_aan.add_argument("--hypothese", required=True, help="De beschreven hypothese")

    # 3. beschrijf-toetsbaarheid
    p_toets = subparsers.add_parser("beschrijf-toetsbaarheid", help="beschrijf-toetsbaarheid")
    p_toets.add_argument("--aannames", required=True, help="De te toetsen aannames")

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
