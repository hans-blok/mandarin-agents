#!/usr/bin/env python3
"""
Agent Runner: agent-curator

Deterministic executor conforme agent-runner.template.md normen.
Beheert agent-lifecycle via twee front doors: publiceer-json en publiceer-overzicht.

Front Doors:
- publiceer-json: Genereert agents-publicatie.json conform schema v2.0 (externe consumptie)
- publiceer-overzicht: Genereert markdown overzichten in docs/ (interne documentatie)

Conformiteit: agents-publicatie-schema.json v2.0, runner-template.md normen
Datum: 2026-02-08
Versie: 2.0
"""

import sys
import json
import argparse
import subprocess
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
            
            print(f"  + {agent_naam} ({value_stream}.{fase}) - "
                  f"contracten:{counts['aantal_agent_files']} prompts:{counts['aantal_prompts']} "
                  f"templates:{counts['aantal_templates']} tasks:{counts['aantal_tasks']} "
                  f"charter:{'ja' if counts['aantal_charters'] else '-'}")
    
    return data


def _count_agent_artifacts(agent_path: Path, agent_naam: str) -> Dict[str, int]:
    """
    Tel agent artifacts in een agent folder conform nieuwe submap-structuur.

    Subfolders:
        agent-contracten/  *.agent.md      → aantal_agent_files
        prompts/           *.prompt.md     → aantal_prompts
        templates/         *.md            → aantal_templates
        tasks/             *.tasks.json    → aantal_tasks
    Root:
        *.charter.md                       → aantal_charters (max 1)
    """
    counts = {
        'aantal_agent_files': 0,
        'aantal_prompts': 0,
        'aantal_templates': 0,
        'aantal_charters': 0,
        'aantal_tasks': 0,
    }

    if not agent_path.exists() or not agent_path.is_dir():
        return counts

    # agent-contracten/
    contracten_dir = agent_path / 'agent-contracten'
    if contracten_dir.is_dir():
        counts['aantal_agent_files'] = sum(1 for f in contracten_dir.glob('*.agent.md') if f.is_file())

    # prompts/
    prompts_dir = agent_path / 'prompts'
    if prompts_dir.is_dir():
        counts['aantal_prompts'] = sum(1 for f in prompts_dir.glob('*.prompt.md') if f.is_file())

    # templates/
    templates_dir = agent_path / 'templates'
    if templates_dir.is_dir():
        counts['aantal_templates'] = sum(1 for f in templates_dir.glob('*.md') if f.is_file())

    # tasks/
    tasks_dir = agent_path / 'tasks'
    if tasks_dir.is_dir():
        counts['aantal_tasks'] = sum(1 for f in tasks_dir.glob('*.tasks.json') if f.is_file())

    # charter staat in de root van de agent-map
    counts['aantal_charters'] = sum(1 for f in agent_path.glob('*.charter.md') if f.is_file())

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
    
    # Timestamp voor publicatie header
    publicatie_timestamp = datetime.now()
    
    # Bouw finale JSON structuur conform schema v2.0
    publicatie = {
        "metadata": {
            "publicatie_timestamp": publicatie_timestamp.isoformat(),
            "publicatie_datum": publicatie_timestamp.strftime("%Y-%m-%d"),
            "publicatie_tijd": publicatie_timestamp.strftime("%H:%M:%S"),
            "gegenereerd_op": publicatie_timestamp.isoformat(),
            "versie": "2.0",
            "aantal_value_streams": len(value_streams),
            "aantal_agents": total_agents,
            "generator": "agent-curator.runner.py v2.0"
        },
        "value_streams": value_streams
    }
    
    output_path.write_text(json.dumps(publicatie, indent=2, ensure_ascii=False), encoding="utf-8")
    
    # Log publicatie timestamp in output
    timestamp_str = publicatie_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[INFO] JSON gepubliceerd: {output_path} (schema v2.0)")
    print(f"[INFO] Publicatie timestamp: {timestamp_str}")


def publiceer_agents_markdown(data: Dict[str, Dict[str, List[Dict]]], output_path: Path) -> None:
    """
    Schrijft markdown archief met agent-overzicht conform schema v2.0.
    
    Args:
        data: Nested dict van scan_agent_folders() {value_stream: {fase: [agents]}}
        output_path: Pad naar output markdown bestand
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Calculate totals and statistics
    total_agents = sum(len(agents) for vs_data in data.values() for agents in vs_data.values())
    total_value_streams = len(data)
    
    # Bouw overzichtstabel data
    tabel_rijen = []
    for vs_code in sorted(data.keys()):
        vs_data = data[vs_code]
        aantal_fasen = len(vs_data)
        aantal_agents = sum(len(agents) for agents in vs_data.values())
        
        # Bereken totalen per artifact type per value stream
        total_agent_files = sum(agent['aantal_agent_files'] for agents in vs_data.values() for agent in agents)
        total_prompts = sum(agent['aantal_prompts'] for agents in vs_data.values() for agent in agents)
        total_templates = sum(agent['aantal_templates'] for agents in vs_data.values() for agent in agents)
        total_charters = sum(agent['aantal_charters'] for agents in vs_data.values() for agent in agents)
        total_tasks = sum(agent.get('aantal_tasks', 0) for agents in vs_data.values() for agent in agents)

        tabel_rijen.append({
            'vs': vs_code.upper(),
            'fasen': aantal_fasen,
            'agents': aantal_agents,
            'files': total_agent_files,
            'prompts': total_prompts,
            'templates': total_templates,
            'charters': total_charters,
            'tasks': total_tasks,
        })

    # Genereer markdown met overzichtstabel
    lines = [
        f"# Agents Overzicht - {timestamp}",
        "",
        "## Globaal Overzicht",
        "",
        "| Value Stream | Fasen | Agents | Contracten | Prompts | Templates | Tasks | Charter |",
        "|--------------|-------|--------|------------|---------|-----------|-------|--------|",
    ]

    # Voeg tabel rijen toe
    for rij in tabel_rijen:
        lines.append(f"| {rij['vs']} | {rij['fasen']} | {rij['agents']} | {rij['files']} | {rij['prompts']} | {rij['templates']} | {rij['tasks']} | {rij['charters']} |")

    # Voeg totaalrij toe
    grand_total_files = sum(rij['files'] for rij in tabel_rijen)
    grand_total_prompts = sum(rij['prompts'] for rij in tabel_rijen)
    grand_total_templates = sum(rij['templates'] for rij in tabel_rijen)
    grand_total_charters = sum(rij['charters'] for rij in tabel_rijen)
    grand_total_tasks = sum(rij['tasks'] for rij in tabel_rijen)

    lines.extend([
        f"| **TOTAAL** | **{len(tabel_rijen)}** | **{total_agents}** | **{grand_total_files}** | **{grand_total_prompts}** | **{grand_total_templates}** | **{grand_total_tasks}** | **{grand_total_charters}** |",
        "",
        "## Samenvatting",
        "",
        f"- **Totaal agents**: {total_agents}",
        f"- **Value streams**: {total_value_streams} ({', '.join(sorted(data.keys()))})",
        f"- **Detail niveau**: uitgebreid",
        f"- **Scope**: volledig",
        "",
        "---",
        ""
    ])
    
# Per value stream
    for vs_code in sorted(data.keys()):
        vs_data = data[vs_code]
        vs_total = sum(len(agents) for agents in vs_data.values())

        lines.append(f"## Value Stream: {vs_code.upper()}")
        lines.append("")
        lines.append(f"**Totaal agents**: {vs_total}")
        lines.append("")
        
        # Matrix opzet: Agent Naam | Contracten | Prompts | Templates | Tasks | Charter
        lines.append("| Agent | Contracten | Prompts | Templates | Tasks | Charter |")
        lines.append("|-------|------------|---------|-----------|-------|---------|")

        # Verzamel alle agents in deze value stream om ze netjes in de matrix te printen
        alle_vs_agents = []
        for fase_nr in sorted(vs_data.keys()):
            for agent in vs_data[fase_nr]:
                agent['fase_weergave'] = fase_nr
                alle_vs_agents.append(agent)
                
        # Sorteer agents op (fase, naam)
        for agent in sorted(alle_vs_agents, key=lambda a: (a['fase_weergave'], a['naam'])):
            charter_str = '1' if agent['aantal_charters'] > 0 else '0'
            row = f"| **{agent['naam']}** ({vs_code}.{agent['fase_weergave']}) | {agent['aantal_agent_files']} | {agent['aantal_prompts']} | {agent['aantal_templates']} | {agent.get('aantal_tasks', 0)} | {charter_str} |"
            lines.append(row)

        lines.append("")
        lines.append("---")
        lines.append("")

    # Canon Aanbevelingen
    lines.append("## Canon Aanbevelingen")
    lines.append("")
    lines.append("Acties om volledig volgens de Mandarin agents canon te werken:")
    lines.append("")
    aanbevelingen_count = 0
    for vs_code in sorted(data.keys()):
        for fase_nr in sorted(data[vs_code].keys()):
            for agent in sorted(data[vs_code][fase_nr], key=lambda a: a['naam']):
                issues = []
                if agent['aantal_charters'] == 0:
                    issues.append("ontbrekend charter (`*.charter.md`)")
                if agent['aantal_agent_files'] == 0:
                    issues.append("ontbrekend contract (`*.agent.md`)")
                if agent['aantal_prompts'] == 0:
                    issues.append("ontbrekende prompt(s)")
                if agent.get('aantal_tasks', 0) == 0:
                    issues.append("ontbrekende tasks configuratie")
                
                if issues:
                    aanbevelingen_count += 1
                    lines.append(f"- **{agent['naam']}** ({vs_code}.{fase_nr}): {', '.join(issues)}")
    
    if aanbevelingen_count == 0:
        lines.append("- Alle agents voldoen aan de basis canon-richtlijnen.")
    
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


def handle_publiceer_json(scope: str = "volledig") -> int:
    """
    Intent: publiceer-json
    
    Genereert agents-publicatie.json conform schema v2.0 voor externe consumptie.
    
    Args:
        scope: "volledig" of "incrementeel" (voor nu alleen volledig)
    
    Returns:
        0 bij succes, 1 bij fout
    """
    print("\nAgent Curator — Publiceer JSON v2.0")
    print("=" * 50)
    print()
    
    # Scan agents
    data = scan_agent_folders()
    
    if not data:
        print("[ERROR] Geen agents gevonden")
        return 1
    
    # Calculate statistics  
    total_agents = sum(len(agents) for vs_data in data.values() for agents in vs_data.values())
    total_value_streams = len(data)
    
    print(f"\n[INFO] Gevonden {total_agents} agents in {total_value_streams} value streams")
    for vs in sorted(data.keys()):
        vs_total = sum(len(agents) for agents in data[vs].values())
        print(f"  - {vs}: {len(data[vs])} fasen, {vs_total} agents")
    
    # Publiceer JSON (workspace root voor externe consumptie)
    json_path = Path("agents-publicatie.json")
    publiceer_agents_json(data, json_path)
    
    print(f"\n[SUCCESS] JSON publicatie voltooid!")
    print(f"  - Bestand: {json_path} (schema v2.0)")
    print(f"  - Value streams: {total_value_streams}")
    print(f"  - Total agents: {total_agents}")
    
    return 0


def handle_publiceer_overzicht(scope: str = "volledig", detail_niveau: str = "uitgebreid") -> int:
    """
    Intent: publiceer-overzicht
    
    Genereert markdown overzicht in docs/ voor interne documentatie.
    
    Args:
        scope: "volledig", "value-stream", of "fase"
        detail_niveau: "basis" of "uitgebreid"
    
    Returns:
        0 bij succes, 1 bij fout
    """
    print("\nAgent Curator — Publiceer Overzicht")
    print("=" * 50)
    print()
    
    # Scan agents
    data = scan_agent_folders()
    
    if not data:
        print("[ERROR] Geen agents gevonden")
        return 1
    
    # Calculate statistics
    total_agents = sum(len(agents) for vs_data in data.values() for agents in vs_data.values())
    total_value_streams = len(data)
    
    print(f"\n[INFO] Gevonden {total_agents} agents in {total_value_streams} value streams")
    
    # Create docs/ folder if not exists
    output_dir = Path("docs")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate detailed markdown overview
    md_path = output_dir / "agents-overzicht.md"
    
    # Gebruik de nieuwe publiceer_agents_markdown functie met overzichtstabel
    publiceer_agents_markdown(data, md_path)

    print(f"\n[SUCCESS] Overzicht publicatie voltooid!")
    print(f"  - Bestand: {md_path}")
    print(f"  - Detail niveau: {detail_niveau}")
    print(f"  - Agents gedocumenteerd: {total_agents}")
    
    return 0


def handle_rapporteer_prompts_overzicht() -> int:
    """Intent: rapporteer-prompts-overzicht
    
    Roept de ecosysteem-coordinator runner aan met de intent
    ``genereer-instructies`` voor ``agent-curator.rapporteer-prompts-overzicht``.

    Deze runner genereert daarmee een execution-ready instructiebestand in
    de map ``prompt-instructions/``, conform de bestaande One Agent, One Runner
    architectuur (ecosysteem-coordinator als centrale instructie-assembler).
    
    Returns:
        Exit code van de onderliggende ecosysteem-coordinator runner.
    """

    print("\nAgent Curator — Rapporteer Prompts Overzicht")
    print("=" * 50)
    print()

    # Bepaal pad naar ecosysteem-coordinator runner relatief t.o.v. dit bestand
    # Padstructuur (workspace root = vier niveaus hoger):
    #   artefacten/aeo/aeo.02.agent-curator/runner/agent-curator.runner.py
    #   artefacten/aeo/aeo.02.ecosysteem-coordinator/runner/ecosysteem-coordinator.runner.py
    try:
        workspace_root = Path(__file__).resolve().parents[4]
    except Exception as e:
        print(f"[ERROR] Kan workspace root voor ecosysteem-coordinator niet bepalen: {e}", file=sys.stderr)
        return 1

    eco_runner = workspace_root / "artefacten" / "aeo" / "aeo.02.ecosysteem-coordinator" / "runner" / "ecosysteem-coordinator.runner.py"

    if not eco_runner.exists():
        print(f"[ERROR] ecosysteem-coordinator runner niet gevonden op: {eco_runner}", file=sys.stderr)
        return 1

    python_exe = sys.executable or "python"

    cmd = [
        python_exe,
        str(eco_runner),
        "genereer-instructies",
        "--agent",
        "agent-curator",
        "--intent",
        "rapporteer-prompts-overzicht",
    ]

    print("[INFO] Start ecosysteem-coordinator runner:")
    print("       ", " ".join(cmd))
    print()

    try:
        result = subprocess.run(cmd, check=False)
        exit_code = result.returncode
    except Exception as e:
        print(f"[ERROR] Fout bij aanroepen ecosysteem-coordinator runner: {e}", file=sys.stderr)
        return 99

    if exit_code == 0:
        print("\n[SUCCESS] Instructies voor rapporteer-prompts-overzicht gegenereerd.")
        print("Kijk in de map 'prompt-instructions/' voor het execution-bestand.")
    else:
        print(f"\n[ERROR] ecosysteem-coordinator runner eindigde met exit code {exit_code}", file=sys.stderr)

    return exit_code


def main() -> int:
    """
    Front Door: Main entry point voor agent-curator runner v2.0.
    
    Supports two intents:
    - publiceer-json: Genereert JSON voor externe consumptie
    - publiceer-overzicht: Genereert markdown voor interne documentatie
    - rapporteer-prompts-overzicht: Genereert execution-instructies voor prompts-overzicht
    
    Returns:
        0 bij succes, 1-99 bij fouten (conform runner template)
    """
    parser = argparse.ArgumentParser(
        description="Agent Curator v2.0 - Deterministic runner conform agent-runner template",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Intents:
  publiceer-json      Genereert agents-publicatie.json (schema v2.0) 
  publiceer-overzicht Genereert markdown overzichten in artefacten/

Examples:
  %(prog)s publiceer-json --scope volledig
  %(prog)s publiceer-overzicht --detail-niveau uitgebreid
"""
    )
    
    # Front door: Intent selection (required)
    parser.add_argument(
        "intent", 
        choices=["publiceer-json", "publiceer-overzicht", "rapporteer-prompts-overzicht"],
        help="Intent to execute"
    )
    
    # Common parameters
    parser.add_argument(
        "--scope", 
        choices=["volledig", "incrementeel", "value-stream", "fase"], 
        default="volledig",
        help="Publicatie scope (default: volledig)"
    )
    
    # Intent-specific parameters
    parser.add_argument(
        "--detail-niveau",
        choices=["basis", "uitgebreid"],
        default="uitgebreid", 
        help="Detail niveau voor publiceer-overzicht (default: uitgebreid)"
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version="agent-curator runner v2.0 (schema v2.0, deterministic)"
    )
    
    args = parser.parse_args()
    
    # Input Quality Gate
    print(f"[INFO] Agent Curator Runner v2.0")
    print(f"[INFO] Intent: {args.intent}")
    print(f"[INFO] Scope: {args.scope}")
    if args.intent == "publiceer-overzicht":
        print(f"[INFO] Detail niveau: {args.detail_niveau}")
    
    try:
        # Route to appropriate handler based on intent
        if args.intent == "publiceer-json":
            return handle_publiceer_json(args.scope)
        elif args.intent == "publiceer-overzicht":
            return handle_publiceer_overzicht(args.scope, args.detail_niveau)
        elif args.intent == "rapporteer-prompts-overzicht":
            return handle_rapporteer_prompts_overzicht()
        else:
            print(f"[ERROR] Onbekende intent: {args.intent}", file=sys.stderr)
            return 1
            
    except FileNotFoundError as e:
        print(f"\n[ERROR] Bestand/folder niet gevonden: {e}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"\n[ERROR] JSON parsing fout: {e}", file=sys.stderr)
        return 2
    except PermissionError as e:
        print(f"\n[ERROR] Toegangsfout: {e}", file=sys.stderr)
        return 3
    except Exception as e:
        print(f"\n[ERROR] Onverwachte fout bij {args.intent}: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 99


if __name__ == "__main__":
    sys.exit(main())