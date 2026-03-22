#!/usr/bin/env python3
"""
Runner voor agent: ecosysteem-beschrijver

Intents:
- beschrijf-agent-positionering: Genereer context diagram (Mermaid flowchart LR) voor een agent
- beschrijf-ecosysteem-artefacten: Inventariseer artefacten per agent in het ecosysteem
- beschrijf-ecosysteem-contracten: Inventariseer agent-contracten in het ecosysteem
- beschrijf-ecosysteem-value-streams-agents: Overzicht value streams en agents

Architectuur: One Agent, One Runner principe.
Cross-cutting functionaliteit (generate-instructions) is gedelegeerd naar
ecosysteem-coordinator.runner.py conform de doctrine.
"""
import argparse
import hashlib
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict


def find_ecosysteem_coordinator_runner() -> Path:
    """Zoek de ecosysteem-coordinator runner."""
    this_file = Path(__file__).resolve()
    repo_root = this_file.parent.parent.parent.parent

    candidate = repo_root / "artefacten" / "aeo" / "aeo.02.ecosysteem-coordinator" / "runner" / "ecosysteem-coordinator.runner.py"
    if candidate.exists():
        return candidate

    cwd_candidate = Path.cwd() / "artefacten" / "aeo" / "aeo.02.ecosysteem-coordinator" / "runner" / "ecosysteem-coordinator.runner.py"
    if cwd_candidate.exists():
        return cwd_candidate

    raise FileNotFoundError("ecosysteem-coordinator.runner.py niet gevonden")


def run_generate_instructions(agent_naam: str, intent: str, params: Dict[str, str]):
    """Roep ecosysteem-coordinator aan om instructies te genereren."""
    try:
        coordinator = find_ecosysteem_coordinator_runner()
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    hash_input = f"{timestamp}{agent_naam}".encode('utf-8')

    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    if not (repo_root / "artefacten").exists():
        repo_root = Path.cwd()

    exec_dir = repo_root / "prompt-instructions"
    exec_dir.mkdir(exist_ok=True)
    filename = exec_dir / f"{timestamp}-{agent_naam}.{intent}.md"

    cmd = [
        sys.executable, str(coordinator), "genereer-instructies",
        "--agent", agent_naam,
        "--intent", intent,
        "--execution-file", str(filename)
    ]

    for k, v in params.items():
        if v:
            cmd.extend(["-p", f"{k}={v}"])

    env = dict(os.environ)
    env['PYTHONIOENCODING'] = 'utf-8'

    print(f"🚀 Start {agent_naam} met intent '{intent}'...")
    print(f"   Via: ecosysteem-coordinator.runner.py genereer-instructies")
    print()

    result = subprocess.run(cmd, env=env)

    if result.returncode == 0:
        subprocess.run(["code", str(filename)], shell=True)
    else:
        print(f"❌ Fout opgetreden bij genereren instructies voor {intent}.", file=sys.stderr)
        sys.exit(result.returncode)


def main():
    parser = argparse.ArgumentParser(
        description="Runner voor ecosysteem-beschrijver"
    )
    subparsers = parser.add_subparsers(dest='intent', metavar='INTENT')
    subparsers.required = True

    # beschrijf-agent-positionering
    p_positionering = subparsers.add_parser(
        "beschrijf-agent-positionering",
        help="Genereer context diagram (Mermaid flowchart LR) voor een agent"
    )
    p_positionering.add_argument("--agent-naam", required=True, help="Naam van de agent (kebab-case)")
    p_positionering.add_argument("--boundary-file", required=False,
                                  help="Pad naar het boundary-document (optioneel, afgeleid uit agent-naam)")

    # beschrijf-ecosysteem-artefacten
    p_artefacten = subparsers.add_parser(
        "beschrijf-ecosysteem-artefacten",
        help="Inventariseer artefacten per agent in het ecosysteem"
    )
    p_artefacten.add_argument("--value-stream-fase", required=True,
                               help="Value stream fase als scope (bijv. aeo.02)")
    p_artefacten.add_argument("--agent-naam", required=False,
                               help="Beperk tot één agent (optioneel, default: alle agents)")
    p_artefacten.add_argument("--artefact-types", required=False,
                               help="Komma-gescheiden artefacttypen (optioneel)")

    # beschrijf-ecosysteem-contracten
    p_contracten = subparsers.add_parser(
        "beschrijf-ecosysteem-contracten",
        help="Inventariseer agent-contracten in het ecosysteem"
    )
    p_contracten.add_argument("--value-stream-fase", required=True,
                               help="Value stream fase als scope (bijv. aeo.02)")
    p_contracten.add_argument("--agent-naam", required=False,
                               help="Beperk tot één agent (optioneel, default: alle agents)")

    # beschrijf-ecosysteem-value-streams-agents
    p_vs_agents = subparsers.add_parser(
        "beschrijf-ecosysteem-value-streams-agents",
        help="Overzicht van value streams en agents"
    )
    p_vs_agents.add_argument("--value-stream-fase", required=True,
                              help="Scope van het overzicht (bijv. aeo.02 of alle)")
    p_vs_agents.add_argument("--value-stream", required=False,
                              help="Beperk tot één value stream (optioneel)")

    args = parser.parse_args()

    params_dict = vars(args).copy()
    del params_dict['intent']
    formatted_params = {k.replace('-', '_'): v for k, v in params_dict.items() if v is not None}

    run_generate_instructions("ecosysteem-beschrijver", args.intent, formatted_params)


if __name__ == "__main__":
    main()
