"""
Agent Runner: agent-curator

Beheert agent-lifecycle: cureert boundaries, publiceert overzichten, 
archiveert en tracked agent-evolutie.

Input: Command-line argumenten (--scope volledig|incrementeel)
Output: agents-publicatie.json, markdown archief in docs/resultaten/

Intents:
- publiceer-agents-overzicht: Genereert JSON + markdown met alle agents
- archiveer-agent-versie: Slaat agent-snapshot op in archief
- cureer-boundary: Analyseert en valideert agent-boundary

Datum: 2026-02-06
Versie: 1.0
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

def scan_agent_folders() -> List[Dict]:
    """
    Scant artefacten/ voor agent-folders en verzamelt metadata.
    
    Returns:
        List van dictionaries met agent-info (naam, value_stream, fase, etc.)
    """
    # Gebruik relatief pad vanaf current working directory
    artefacten_path = Path("artefacten")
    
    if not artefacten_path.exists():
        print(f"[ERROR] artefacten/ folder not found")
        print(f"[DEBUG] Looking in: {artefacten_path.absolute()}")
        return []
    
    agents = []
    
    print(f"[INFO] Scanning agent folders in artefacten/...")
    
    # Scan alle value stream folders (aeo, fnd, kvl, etc.)
    for vs_folder in artefacten_path.iterdir():
        if not vs_folder.is_dir():
            continue
        
        # Scan agent folders binnen value stream (bijv. fnd.02.presentatie-architect)
        for agent_folder in vs_folder.iterdir():
            if not agent_folder.is_dir():
                continue
            
            # Parse folder naam: {vs}.{fase}.{agent-naam}
            parts = agent_folder.name.split('.', 2)
            if len(parts) < 3:
                continue
            
            value_stream = parts[0]
            fase = parts[1]
            agent_naam = parts[2]
            
            # Zoek charter
            charter_path = agent_folder / f"{agent_naam}.charter.md"
            charter_exists = charter_path.exists()
            
            # Zoek contracten
            contract_files = list(agent_folder.glob(f"{agent_naam}.*.agent.md"))
            intents = [f.stem.replace(f"{agent_naam}.", "").replace(".agent", "") 
                      for f in contract_files]
            
            # Zoek runner
            runner_path = agent_folder / f"{agent_naam}.runner.py"
            runner_exists = runner_path.exists()
            
            agents.append({
                "naam": agent_naam,
                "value_stream": value_stream,
                "fase": fase,
                "folder": str(agent_folder),
                "charter": charter_exists,
                "intents": intents,
                "runner": runner_exists,
                "contracten": len(contract_files)
            })
            
            print(f"  ✓ {agent_naam} ({value_stream}.{fase}) - {len(intents)} intents")
    
    return agents


def publiceer_agents_json(agents: List[Dict], output_path: Path) -> None:
    """
    Schrijft agents-publicatie.json voor fetch_agents.py consumptie.
    
    Args:
        agents: List van agent-dictionaries
        output_path: Pad naar output JSON bestand
    """
    publicatie = {
        "metadata": {
            "gegenereerd_op": datetime.now().isoformat(),
            "aantal_agents": len(agents),
            "versie": "1.0"
        },
        "agents": agents
    }
    
    output_path.write_text(json.dumps(publicatie, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[INFO] JSON gepubliceerd: {output_path}")


def publiceer_agents_markdown(agents: List[Dict], output_path: Path) -> None:
    """
    Schrijft markdown archief met agent-overzicht en digest.
    
    Args:
        agents: List van agent-dictionaries
        output_path: Pad naar output markdown bestand
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Groepeer agents per value stream
    by_value_stream = {}
    for agent in agents:
        vs = agent["value_stream"]
        by_value_stream.setdefault(vs, []).append(agent)
    
    # Genereer markdown
    lines = [
        f"# Agents Publicatie - {timestamp}",
        "",
        "**Samenvatting**:",
        f"- Totaal aantal agents: {len(agents)}",
        f"- Value streams: {', '.join(sorted(by_value_stream.keys()))}",
        "",
        "---",
        ""
    ]
    
    # Per value stream
    for vs in sorted(by_value_stream.keys()):
        vs_agents = by_value_stream[vs]
        lines.append(f"## Value Stream: {vs.upper()}")
        lines.append("")
        
        for agent in sorted(vs_agents, key=lambda a: (a["fase"], a["naam"])):
            lines.append(f"### {agent['naam']} (fase {agent['fase']})")
            lines.append("")
            lines.append(f"**Locatie**: `{agent['folder']}`")
            lines.append(f"**Charter**: {'✓' if agent['charter'] else '✗'}")
            lines.append(f"**Runner**: {'✓' if agent['runner'] else '✗'}")
            lines.append(f"**Contracten**: {agent['contracten']}")
            lines.append("")
            
            if agent["intents"]:
                lines.append("**Intents**:")
                for intent in agent["intents"]:
                    lines.append(f"- `{intent}`")
                lines.append("")
            
            lines.append("---")
            lines.append("")
    
    # Herkomstverantwoording
    lines.extend([
        "## Herkomstverantwoording",
        "",
        f"- Gegenereerd door: agent-curator",
        f"- Datum: {timestamp}",
        f"- Bron: artefacten/ (workspace scan)",
        "- Versie: 1.0"
    ])
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[INFO] Markdown archief: {output_path}")


def handle_publiceer_agents_overzicht(scope: str = "volledig") -> int:
    """
    Intent: publiceer-agents-overzicht
    
    Genereert agents-publicatie.json en markdown archief.
    
    Args:
        scope: "volledig" of "incrementeel" (voor nu alleen volledig)
    
    Returns:
        0 bij succes, 1 bij fout
    """
    print("\nAgent Curator — Publiceer Agents Overzicht")
    print("=" * 60)
    print()
    
    # Scan agents
    agents = scan_agent_folders()
    
    if not agents:
        print("[ERROR] No agents found")
        return 1
    
    print(f"\n[INFO] Gevonden {len(agents)} agents")
    
    # Publiceer JSON (root, voor fetch_agents.py)
    json_path = Path("agents-publicatie.json")
    publiceer_agents_json(agents, json_path)
    
    # Publiceer markdown archief
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    md_path = Path(f"docs/resultaten/agent-publicaties/agents-publicatie-{timestamp}.md")
    publiceer_agents_markdown(agents, md_path)
    
    print(f"\n[SUCCESS] Publicatie voltooid!")
    print(f"  - JSON: {json_path}")
    print(f"  - Archief: {md_path}")
    
    return 0


def main() -> int:
    """
    Main entry point voor agent-curator runner.
    
    Returns:
        0 bij succes, 1 bij fout
    """
    parser = argparse.ArgumentParser(description="Agent Curator - Publiceer agents overzicht")
    parser.add_argument("--scope", choices=["volledig", "incrementeel"], default="volledig",
                       help="Publicatie scope (volledig = alle agents, incrementeel = alleen changes)")
    
    args = parser.parse_args()
    
    try:
        return handle_publiceer_agents_overzicht(args.scope)
    except Exception as e:
        print(f"\n[ERROR] Fout bij publiceren: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())