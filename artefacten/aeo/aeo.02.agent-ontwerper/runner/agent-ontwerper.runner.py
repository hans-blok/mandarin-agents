#!/usr/bin/env python3
"""
Runner voor agent: agent-ontwerper

Ontwerpt agent-artefacten op basis van een bestaande agent-boundary:
- definieer-agent-charter:  Genereert een agent-charter op basis van boundary + template.
- definieer-agent-contract: Genereert een agent-contract voor een specifieke intent.
- definieer-agent-template: Genereert een output-template voor een agent.

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


AGENT_NAAM = "agent-ontwerper"
VALUE_STREAM = "aeo"
FASE = "02"


def get_workspace_root() -> Path:
    """Detecteer workspace root relatief aan dit script, met fallback naar cwd."""
    candidate = Path(__file__).resolve().parent.parent.parent.parent.parent
    if (candidate / "artefacten").exists():
        return candidate
    return Path.cwd()


def find_agent_folder(agent_naam: str) -> tuple[str, Path]:
    """
    Zoek de agent-folder in artefacten/*/.
    
    Returns:
        (value_stream_fase, folder_path) - bijv. ("fnd.01", Path("artefacten/fnd/fnd.01.documentatie-omvormer"))
    
    Raises:
        FileNotFoundError als agent niet gevonden wordt.
    """
    root = get_workspace_root()
    artefacten = root / "artefacten"
    
    for vs_folder in artefacten.iterdir():
        if not vs_folder.is_dir():
            continue
        for agent_folder in vs_folder.iterdir():
            if not agent_folder.is_dir():
                continue
            # Patroon: {vs}.{fase}.{agent-naam}
            parts = agent_folder.name.split(".")
            if len(parts) >= 3 and ".".join(parts[2:]) == agent_naam:
                value_stream_fase = f"{parts[0]}.{parts[1]}"
                return (value_stream_fase, agent_folder)
    
    raise FileNotFoundError(
        f"Agent-folder niet gevonden voor '{agent_naam}' in {artefacten}"
    )


def derive_boundary_file(agent_naam: str, value_stream_fase: str = None) -> str:
    """
    Leid het boundary bestandspad af uit agent_naam.
    
    Als value_stream_fase niet meegegeven wordt, wordt deze automatisch
    gedetecteerd uit de folder-structuur.
    """
    if value_stream_fase is None:
        value_stream_fase, _ = find_agent_folder(agent_naam)
    vs = value_stream_fase.split(".")[0]
    return f"artefacten/{vs}/{value_stream_fase}.{agent_naam}/{agent_naam}.agent-boundary.md"


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
    """
    try:
        coordinator = find_ecosysteem_coordinator_runner()
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    hash_input = f"{timestamp}{AGENT_NAAM}{intent}".encode("utf-8")
    hash_str = hashlib.md5(hash_input).hexdigest()[:4].lower()

    root = get_workspace_root()
    exec_dir = root / "prompt-instructions"
    exec_dir.mkdir(exist_ok=True)
    exec_file = exec_dir / f"{timestamp}-{AGENT_NAAM}.{intent}.md"

    cmd = [
        sys.executable,
        str(coordinator),
        "genereer-instructies",
        "--agent", AGENT_NAAM,
        "--intent", intent,
        "--execution-file", str(exec_file),
    ]
    for key, value in params.items():
        if value is not None and value != "":
            cmd.extend(["-p", f"{key}={value}"])

    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"

    print(f"Agent-ontwerper: genereer instructies voor '{intent}'...")
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

def definieer_agent_charter_main(args: argparse.Namespace) -> int:
    """
    Intent: definieer-agent-charter

    Genereert een agent-charter op basis van een agent-boundary document.

    Verplichte parameters: agent_naam
    Afgeleid:              boundary_file, value_stream_fase (uit folder-structuur)
    """
    value_stream_fase, _ = find_agent_folder(args.agent_naam)
    boundary_file = args.boundary_file or derive_boundary_file(args.agent_naam, value_stream_fase)

    print(f"  Discovery: boundary          = {boundary_file}")
    print(f"  Discovery: value_stream_fase = {value_stream_fase}")

    params = {
        "agent_naam": args.agent_naam,
        "boundary_file": boundary_file,
        "value_stream_fase": value_stream_fase,
    }
    return run_generate_instructions("definieer-agent-charter", params)


def definieer_agent_contract_main(args: argparse.Namespace) -> int:
    """
    Intent: definieer-agent-contract

    Genereert agent-contracten voor alle intents in de boundary.
    Convention over Configuration: template, intents en referenties worden
    automatisch afgeleid uit de folder-structuur en boundary.

    Verplichte parameters: agent_naam
    Afgeleid:              boundary_file, value_stream_fase (uit folder-structuur)
    """
    value_stream_fase, _ = find_agent_folder(args.agent_naam)
    boundary_file = args.boundary_file or derive_boundary_file(args.agent_naam, value_stream_fase)

    print(f"  Discovery: boundary          = {boundary_file}")
    print(f"  Discovery: value_stream_fase = {value_stream_fase}")

    params = {
        "agent_naam": args.agent_naam,
        "boundary_file": boundary_file,
        "value_stream_fase": value_stream_fase,
    }
    return run_generate_instructions("definieer-agent-contract", params)


def definieer_agent_template_main(args: argparse.Namespace) -> int:
    """
    Intent: definieer-agent-template

    Genereert output-templates voor alle intents in de boundary.
    Convention over Configuration: intents en inspiratiebestanden worden
    automatisch afgeleid uit de folder-structuur en boundary.

    Verplichte parameters: agent_naam
    Afgeleid:              boundary_file, value_stream_fase (uit folder-structuur)
    """
    value_stream_fase, _ = find_agent_folder(args.agent_naam)
    boundary_file = derive_boundary_file(args.agent_naam, value_stream_fase)

    print(f"  Discovery: boundary          = {boundary_file}")
    print(f"  Discovery: value_stream_fase = {value_stream_fase}")

    params = {
        "agent_naam": args.agent_naam,
        "boundary_file": boundary_file,
        "value_stream_fase": value_stream_fase,
    }
    return run_generate_instructions("definieer-agent-template", params)


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

    # ── definieer-agent-charter ──────────────────────────────────────────────
    p_charter = subparsers.add_parser(
        "definieer-agent-charter",
        help="Genereert een agent-charter op basis van een boundary document",
    )
    p_charter.add_argument(
        "--agent-naam", required=True,
        help="Naam van de agent waarvoor het charter wordt gedefinieerd (kebab-case)",
    )
    p_charter.add_argument(
        "--boundary-file", required=False, default=None,
        help="Pad naar het agent-boundary document (optioneel, wordt automatisch afgeleid)",
    )
    p_charter.add_argument(
        "--value-stream-fase", required=False, default=None,
        help=argparse.SUPPRESS,
    )

    # ── definieer-agent-contract ─────────────────────────────────────────────
    p_contract = subparsers.add_parser(
        "definieer-agent-contract",
        help="Genereert een agent-contract voor een specifieke intent",
    )
    p_contract.add_argument(
        "--agent-naam", required=True,
        help="Naam van de agent waarvoor contracten worden gedefinieerd (kebab-case)",
    )
    p_contract.add_argument(
        "--boundary-file", required=False, default=None,
        help=argparse.SUPPRESS,
    )
    p_contract.add_argument(
        "--value-stream-fase", required=False, default=None,
        help=argparse.SUPPRESS,
    )

    # ── definieer-agent-template ─────────────────────────────────────────────
    p_template = subparsers.add_parser(
        "definieer-agent-template",
        help="Genereert een output-template voor een agent",
    )
    p_template.add_argument(
        "--agent-naam", required=True,
        help="Naam van de agent waarvoor templates worden gedefinieerd (kebab-case)",
    )
    p_template.add_argument(
        "--value-stream-fase", required=False, default=None,
        help=argparse.SUPPRESS,
    )

    args = parser.parse_args()

    if args.intent == "definieer-agent-charter":
        return definieer_agent_charter_main(args)
    elif args.intent == "definieer-agent-contract":
        return definieer_agent_contract_main(args)
    elif args.intent == "definieer-agent-template":
        return definieer_agent_template_main(args)

    print(f"ERROR: Onbekende intent '{args.intent}'", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
