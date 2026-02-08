"""
Agent Runner: agent-curator

Beheert agent-lifecycle: cureert boundaries, publiceert overzichten, 
archiveert en tracked agent-evolutie.

Input: Command-line argumenten (--scope volledig|incrementeel)
Output: agents-publicatie.json, markdown archief in docs/resultaten/

Intents:
- publiceer-agents-overzicht: Genereert JSON + markdown conform schema v2.0
- archiveer-agent-versie: Slaat agent-snapshot op in archief
- cureer-boundary: Analyseert en valideert agent-boundary

Conformiteit: agents-publicatie-schema.json v2.0
Datum: 2026-02-08
Versie: 2.0
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

def scan_agent_folders() -> Dict[str, Dict[str, List[Dict]]]:
    """
    Scant artefacten/ voor agent-folders en bouwt hierarchische structuur.
    
    Returns:
        Nested dict: {value_stream: {fase: [agents]}} conform schema v2.0
        
    Structure:
        {
            'aeo': {
                '01': [
                    {'naam': 'canon-curator', 'aantal_agent_files': 4, ...},
                    ...
                ],
                '02': [...]
            },
            'miv': {...}
        }
    """
    # Gebruik relatief pad vanaf current working directory
    artefacten_path = Path("artefacten")
    
    if not artefacten_path.exists():
        print(f"[ERROR] artefacten/ folder not found")
        print(f"[DEBUG] Looking in: {artefacten_path.absolute()}")
        return {}
    
    data: Dict[str, Dict[str, List[Dict]]] = {}
    
    print(f"[INFO] Scanning agent folders in artefacten/...")
    
    # Scan alle value stream folders (aeo, fnd, kvl, etc.)
    for vs_folder in artefacten_path.iterdir():
        if not vs_folder.is_dir():
            continue
        
        # Skip __pycache__ en andere non-value_stream folders
        if vs_folder.name.startswith('_'):
            continue
        
        value_stream = vs_folder.name
        
        # Scan agent folders binnen value stream (bijv. fnd.02.presentatie-architect)
        for agent_folder in vs_folder.iterdir():
            if not agent_folder.is_dir():
                continue
            
            # Parse folder naam: {vs}.{fase}.{agent-naam}
            parts = agent_folder.name.split('.', 2)
            if len(parts) < 3:
                continue
            
            vs_parsed, fase, agent_naam = parts
            
            # Valideer dat value_stream uit folder naam matcht
            if vs_parsed != value_stream:
                print(f"[WARNING] Mismatch value_stream in {agent_folder.name}")
                continue
            
            # Tel artifacts per type
            counts = _count_agent_artifacts(agent_folder, agent_naam)
            
            # Bouw agent record conform schema v2.0
            agent_record = {
                'naam': agent_naam,
                **counts
            }
            
            # Voeg toe aan data structuur
            if value_stream not in data:
                data[value_stream] = {}
            if fase not in data[value_stream]:
                data[value_stream][fase] = []
            
            data[value_stream][fase].append(agent_record)
            
            print(f"  ✓ {agent_naam} ({value_stream}.{fase}) - "
                  f"files:{counts['aantal_agent_files']} prompts:{counts['aantal_prompts']} "
                  f"templates:{counts['aantal_templates']} charters:{counts['aantal_charters']}")
    
    return data


def _count_agent_artifacts(agent_path: Path, agent_naam: str) -> Dict[str, int]:
    """
    Tel agent artifacts in een agent folder conform schema v2.0.
    
    Args:
        agent_path: Path naar agent folder
        agent_naam: Naam van de agent (voor filtering)
        
    Returns:
        Dictionary met counts:
        - aantal_agent_files: *.agent.md bestanden
        - aantal_prompts: *.prompt.md bestanden  
        - aantal_templates: *template*.md bestanden
        - aantal_charters: *.charter.md bestanden (max 1)
    """
    counts = {
        'aantal_agent_files': 0,
        'aantal_prompts': 0,
        'aantal_templates': 0,
        'aantal_charters': 0
    }
    
    if not agent_path.exists() or not agent_path.is_dir():
        return counts
    
    for file in agent_path.iterdir():
        if not file.is_file():
            continue
            
        filename = file.name.lower()
        
        if filename.endswith('.agent.md'):
            counts['aantal_agent_files'] += 1
        elif filename.endswith('.prompt.md'):
            counts['aantal_prompts'] += 1
        elif 'template' in filename and filename.endswith('.md'):
            counts['aantal_templates'] += 1
        elif filename.endswith('.charter.md'):
            counts['aantal_charters'] += 1
    
    return counts


def publiceer_agents_json(data: Dict[str, Dict[str, List[Dict]]], output_path: Path) -> None:
    """
    Schrijft agents-publicatie.json conform schema v2.0.
    
    Args:
        data: Nested dict van scan_agent_folders() {value_stream: {fase: [agents]}}
        output_path: Pad naar output JSON bestand
    """
    # Bouw value_streams array
    value_streams = []
    total_agents = 0
    
    for vs_code in sorted(data.keys()):
        fasen = []
        
        for fase_nr in sorted(data[vs_code].keys()):
            agents = data[vs_code][fase_nr]
            total_agents += len(agents)
            
            fasen.append({
                'volgnummer': fase_nr,
                'agents': sorted(agents, key=lambda a: a['naam'])
            })
        
        value_streams.append({
            'code': vs_code,
            'fasen': fasen
        })
    
    # Bouw finale JSON structuur conform schema v2.0
    publicatie = {
        "metadata": {
            "gegenereerd_op": datetime.now().isoformat(),
            "versie": "2.0",
            "aantal_value_streams": len(value_streams),
            "aantal_agents": total_agents
        },
        "value_streams": value_streams
    }
    
    output_path.write_text(json.dumps(publicatie, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[INFO] JSON gepubliceerd: {output_path} (schema v2.0)")


def publiceer_agents_markdown(data: Dict[str, Dict[str, List[Dict]]], output_path: Path) -> None:
    """
    Schrijft markdown archief met agent-overzicht conform schema v2.0.
    
    Args:
        data: Nested dict van scan_agent_folders() {value_stream: {fase: [agents]}}
        output_path: Pad naar output markdown bestand
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Calculate totals
    total_agents = sum(len(agents) for vs_data in data.values() for agents in vs_data.values())
    
    # Genereer markdown
    lines = [
        f"# Agents Publicatie v2.0 - {timestamp}",
        "",
        "**Samenvatting**:",
        f"- Totaal aantal agents: {total_agents}",
        f"- Value streams: {', '.join(sorted(data.keys()))}",
        f"- Schema versie: 2.0",
        "",
        "---",
        ""
    ]
    
    # Per value stream en fase
    for vs_code in sorted(data.keys()):
        vs_data = data[vs_code]
        vs_total = sum(len(agents) for agents in vs_data.values())
        
        lines.append(f"## Value Stream: {vs_code.upper()}")
        lines.append("")
        lines.append(f"**Totaal agents**: {vs_total}")
        lines.append("")  
        
        for fase_nr in sorted(vs_data.keys()):
            fase_agents = vs_data[fase_nr]
            lines.append(f"### Fase {fase_nr}")
            lines.append("")
            
            for agent in sorted(fase_agents, key=lambda a: a['naam']):
                lines.append(f"**{agent['naam']}**")
                lines.append(f"- Agent files: {agent['aantal_agent_files']}")
                lines.append(f"- Prompt files: {agent['aantal_prompts']}")
                lines.append(f"- Templates: {agent['aantal_templates']}")
                lines.append(f"- Charter: {'✓' if agent['aantal_charters'] > 0 else '✗'}")
                lines.append("")
            
            lines.append("---")
            lines.append("")
    
    # Herkomstverantwoording
    lines.extend([
        "## Herkomstverantwoording",
        "",
        f"- Gegenereerd door: agent-curator v2.0",
        f"- Datum: {timestamp}",
        f"- Bron: artefacten/ (workspace scan)",
        f"- Schema versie: 2.0",
        f"- Conform: agents-publicatie-schema.json v2.0"
    ])
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[INFO] Markdown archief: {output_path}")


def handle_publiceer_agents_overzicht(scope: str = "volledig") -> int:
    """
    Intent: publiceer-agents-overzicht
    
    Genereert agents-publicatie.json en markdown archief conform schema v2.0.
    
    Args:
        scope: "volledig" of "incrementeel" (voor nu alleen volledig)
    
    Returns:
        0 bij succes, 1 bij fout
    """
    print("\nAgent Curator — Publiceer Agents Overzicht v2.0")
    print("=" * 60)
    print()
    
    # Scan agents
    data = scan_agent_folders()
    
    if not data:
        print("[ERROR] No agents found")
        return 1
    
    # Calculate statistics
    total_agents = sum(len(agents) for vs_data in data.values() for agents in vs_data.values())
    total_value_streams = len(data)
    
    print(f"\n[INFO] Gevonden {total_agents} agents in {total_value_streams} value streams")
    for vs in sorted(data.keys()):
        vs_total = sum(len(agents) for agents in data[vs].values())
        print(f"  - {vs}: {len(data[vs])} fasen, {vs_total} agents")
    
    # Publiceer JSON (root, voor externe consumptie)
    json_path = Path("agents-publicatie.json")
    publiceer_agents_json(data, json_path)
    
    # Publiceer markdown archief
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    md_path = Path(f"docs/resultaten/agent-publicaties/agents-publicatie-v2-{timestamp}.md")
    publiceer_agents_markdown(data, md_path)
    
    print(f"\n[SUCCESS] Publicatie v2.0 voltooid!")
    print(f"  - JSON: {json_path} (schema v2.0)")
    print(f"  - Archief: {md_path}")
    print(f"  - Value streams: {total_value_streams}")
    print(f"  - Total agents: {total_agents}")
    
    return 0


def main() -> int:
    """
    Main entry point voor agent-curator runner v2.0.
    
    Returns:
        0 bij succes, 1 bij fout
    """
    parser = argparse.ArgumentParser(description="Agent Curator v2.0 - Publiceer agents overzicht conform schema v2.0")
    parser.add_argument("--scope", choices=["volledig", "incrementeel"], default="volledig",
                       help="Publicatie scope (volledig = alle agents, incrementeel = alleen changes)")
    parser.add_argument("--version", action="version", version="agent-curator v2.0 (schema v2.0)")
    
    args = parser.parse_args()
    
    try:
        return handle_publiceer_agents_overzicht(args.scope)
    except FileNotFoundError as e:
        print(f"\n[ERROR] Bestand/folder niet gevonden: {e}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"\n[ERROR] JSON parsing fout: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"\n[ERROR] Onverwachte fout bij publiceren: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 99


if __name__ == "__main__":
    sys.exit(main())