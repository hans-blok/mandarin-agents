#!/usr/bin/env python3
"""
Runner voor agent: capability-architect

Definieert servicelimieten van agents:
- definieer-agent-boundary: Definieert de servicegrens van een agent op basis van naam,
  value stream fase en korte beschrijving.

Architectuur: One Agent, One Runner principe.
Roept ecosysteem-coordinator aan voor het genereren van execution-ready instructies.
"""
from datetime import datetime
from pathlib import Path
import argparse
import hashlib
import os
import subprocess
import sys


AGENT_NAAM = "capability-architect"
VALUE_STREAM = "aeo"
FASE = "01"


def get_workspace_root() -> Path:
    """Detecteer workspace root relatief aan dit script, met fallback naar cwd."""
    candidate = Path(__file__).resolve().parent.parent.parent.parent.parent
    if (candidate / "artefacten").exists():
        return candidate
    return Path.cwd()


def find_ecosysteem_coordinator_runner() -> Path:
    """Zoek de ecosysteem-coordinator runner."""
    root = get_workspace_root()
    candidate = (
        root
        / "artefacten"
        / "fnd"
        / "fnd.01.ecosysteem-coordinator"
        / "runner"
        / "ecosysteem-coordinator.runner.py"
    )
    if candidate.exists():
        return candidate
    raise FileNotFoundError(
        f"ecosysteem-coordinator.runner.py niet gevonden (gezocht in: {candidate})"
    )


def run_generate_instructions(intent: str, params: dict) -> int:
    """
    Roep ecosysteem-coordinator aan om een execution-file te genereren
    voor de gegeven intent en parameters.

    Workflow:
    1. Bepaal output bestandsnaam voor het execution-file.
    2. Bouw de CLI-aanroep voor ecosysteem-coordinator genereer-instructies.
    3. Voer uit en open het gegenereerde execution-file in VS Code.
    """
    try:
        coordinator = find_ecosysteem_coordinator_runner()
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    # Genereer unieke bestandsnaam voor het execution-file
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    hash_input = f"{timestamp}{AGENT_NAAM}{intent}".encode("utf-8")
    hash_str = hashlib.md5(hash_input).hexdigest()[:4].lower()

    root = get_workspace_root()
    exec_dir = root / "executions"
    exec_dir.mkdir(exist_ok=True)
    exec_file = exec_dir / f"{timestamp}-{AGENT_NAAM}.{intent}.md"

    # Bouw CLI-commando
    cmd = [
        sys.executable,
        str(coordinator),
        "genereer-instructies",
        "--agent", AGENT_NAAM,
        "--intent", intent,
        "--execution-file", str(exec_file),
    ]
    for key, value in params.items():
        if value is not None:
            cmd.extend(["-p", f"{key}={value}"])

    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"

    print(f"Capability-architect: genereer instructies voor '{intent}'...")
    print(f"  Via: ecosysteem-coordinator genereer-instructies")
    print()

    result = subprocess.run(cmd, env=env)

    if result.returncode == 0:
        print(f"Execution-file aangemaakt: {exec_file}")
        subprocess.run(["code", str(exec_file)], shell=True)
    else:
        print(
            f"ERROR: Instructiegeneratie mislukt voor intent '{intent}'.",
            file=sys.stderr,
        )

    return result.returncode


# ==============================================================================
# INTENT HANDLERS
# ==============================================================================

def definieer_agent_boundary_main(args: argparse.Namespace) -> int:
    """
    Intent: definieer-agent-boundary

    Definieert de servicegrens van een agent op basis van naam,
    value stream fase en korte beschrijving.

    Verplichte parameters: agent_naam, value_stream_fase, korte_beschrijving
    """
    params = {
        "agent_naam": args.agent_naam,
        "value_stream_fase": args.value_stream_fase,
        "korte_beschrijving": args.korte_beschrijving,
    }

    return run_generate_instructions("definieer-agent-boundary", params)


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(
        description=f"Runner voor agent: {AGENT_NAAM}",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(
        dest="intent", required=True, help="Beschikbare intents"
    )

    # definieer-agent-boundary
    p_boundary = subparsers.add_parser(
        "definieer-agent-boundary",
        help=(
            "Definieert de servicegrens van een agent op basis van naam, "
            "value stream fase en korte beschrijving"
        ),
    )
    p_boundary.add_argument(
        "--agent-naam",
        required=True,
        help="Naam van de agent waarvoor de boundary wordt gedefinieerd (kebab-case)",
    )
    p_boundary.add_argument(
        "--value-stream-fase",
        required=True,
        help='Value stream en fase code (bijv. "aeo.02", "fnd.01")',
    )
    p_boundary.add_argument(
        "--korte-beschrijving",
        required=True,
        help="Korte beschrijving van het doel van de agent (1-3 zinnen)",
    )

    args = parser.parse_args()

    if args.intent == "definieer-agent-boundary":
        return definieer_agent_boundary_main(args)

    # Onbekende intent (kan niet voorkomen door subparsers required=True)
    print(f"ERROR: Onbekende intent '{args.intent}'", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
