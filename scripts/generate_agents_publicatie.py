"""
Genereer vereenvoudigde agents-publicatie.json met aantallen.

Dit script scant alle value_stream folders in artefacten/ en genereert een
vereenvoudigd JSON-bestand met counts van agent artifacts per value stream en fase.

Alleen agents MET agent-contracten/ EN prompts/ subfolders worden meegenomen.
Dit zijn volwaardige agents (niet legacy of incomplete).

Output volgt het schema gedefinieerd in: schemas/agents-publicatie-schema.json

Versie: 2.1.0
Auteur: engineer-steward
Datum: 2026-02-15

"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


def parse_agent_folder_name(folder_name: str) -> Tuple[str, str, str] | None:
    """
    Parse agent folder naam naar (value_stream, fase, agent_naam).
    
    Args:
        folder_name: Folder naam zoals 'aeo.01.canon-curator'
        
    Returns:
        Tuple van (value_stream, fase, agent_naam) of None bij ongeldige naam
        
    Examples:
        >>> parse_agent_folder_name('aeo.01.canon-curator')
        ('aeo', '01', 'canon-curator')
        >>> parse_agent_folder_name('miv.02.investerings-verteller')
        ('miv', '02', 'investerings-verteller')
    """
    pattern = r'^([a-z]{3})\.(\d{2})\.([a-z][a-z0-9-]+)$'
    match = re.match(pattern, folder_name)
    if match:
        return match.group(1), match.group(2), match.group(3)
    return None


def count_agent_artifacts(agent_path: Path) -> Dict[str, int] | None:
    """
    Tel agent artifacts in een agent folder.
    
    Alleen agents MET agent-contracten/ EN prompts/ subfolders worden geteld.
    Dit zijn volwaardige agents (niet legacy of incomplete).
    
    Args:
        agent_path: Path naar agent folder
        
    Returns:
        Dictionary met counts of None als agent incomplete is:
        - aantal_agent_files: *.agent.md bestanden in agent-contracten/
        - aantal_prompts: *.prompt.md bestanden in prompts/
        - aantal_templates: *.template.md bestanden in templates/ (optioneel)
        - aantal_charters: *.charter.md bestanden in root (max 1)
    """
    # Valideer dat de verplichte subfolders bestaan
    agent_contracten_path = agent_path / 'agent-contracten'
    prompts_path = agent_path / 'prompts'
    
    if not agent_contracten_path.exists() or not prompts_path.exists():
        # Skip deze agent - incomplete structuur
        return None
    
    counts = {
        'aantal_agent_files': 0,
        'aantal_prompts': 0,
        'aantal_templates': 0,
        'aantal_charters': 0
    }
    
    # Tel agent-contracten in agent-contracten/
    if agent_contracten_path.is_dir():
        for file in agent_contracten_path.iterdir():
            if file.is_file() and file.name.endswith('.agent.md'):
                counts['aantal_agent_files'] += 1
    
    # Tel prompts in prompts/
    if prompts_path.is_dir():
        for file in prompts_path.iterdir():
            if file.is_file() and file.name.endswith('.prompt.md'):
                counts['aantal_prompts'] += 1
    
    # Tel templates in templates/ (optioneel)
    templates_path = agent_path / 'templates'
    if templates_path.exists() and templates_path.is_dir():
        for file in templates_path.iterdir():
            if file.is_file() and file.name.endswith('.template.md'):
                counts['aantal_templates'] += 1
    
    # Tel charter in root (max 1)
    for file in agent_path.iterdir():
        if file.is_file() and file.name.endswith('.charter.md'):
            counts['aantal_charters'] += 1
    
    return counts


def scan_value_stream_folders(artefacten_path: Path) -> Dict[str, Dict[str, List[Dict]]]:
    """
    Scan alle value_stream folders en bouw hierarchische datastructuur.
    
    Alleen agents MET agent-contracten/ EN prompts/ subfolders worden meegenomen.
    Dit zijn volwaardige agents (niet legacy of incomplete).
    
    Args:
        artefacten_path: Path naar artefacten/ folder
        
    Returns:
        Nested dict: {value_stream: {fase: [agents]}}
        
    Structuur:
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
    data: Dict[str, Dict[str, List[Dict]]] = {}
    
    if not artefacten_path.exists():
        raise FileNotFoundError(f"Artefacten folder niet gevonden: {artefacten_path}")
    
    # Scan alle subfolders in artefacten/
    for value_stream_folder in sorted(artefacten_path.iterdir()):
        if not value_stream_folder.is_dir():
            continue
        
        # Skip __pycache__ en andere non-value_stream folders
        if value_stream_folder.name.startswith('_'):
            continue
        
        # Verwacht value_stream code (3 letters lowercase)
        if not re.match(r'^[a-z]{3}$', value_stream_folder.name):
            continue
        
        value_stream = value_stream_folder.name
        
        # Scan alle agent folders in deze value_stream
        for agent_folder in sorted(value_stream_folder.iterdir()):
            if not agent_folder.is_dir():
                continue
            
            parsed = parse_agent_folder_name(agent_folder.name)
            if not parsed:
                continue
            
            vs, fase, agent_naam = parsed
            
            # Valideer dat value_stream uit folder naam matcht
            if vs != value_stream:
                print(f"Waarschuwing: Mismatch value_stream in {agent_folder.name}")
                continue
            
            # Tel artifacts (alleen volwaardige agents met agent-contracten/ en prompts/)
            counts = count_agent_artifacts(agent_folder)
            
            # Skip incomplete agents
            if counts is None:
                print(f"  Skip {agent_folder.name}: ontbrekende agent-contracten/ of prompts/ subfolder")
                continue
            
            # Bouw agent record
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
    
    return data


def build_json_structure(data: Dict[str, Dict[str, List[Dict]]]) -> Dict:
    """
    Bouw finale JSON structuur volgens schema v2.0.
    
    Args:
        data: Nested dict van scan_value_stream_folders()
        
    Returns:
        JSON-serializable dict volgens agents-publicatie-schema v2.0
    """
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
    
    return {
        'metadata': {
            'schema': 'schemas/agents-publicatie-schema.json',
            'schema_versie': '2.0',
            'beschrijving': 'Vereenvoudigde publicatie van Mandarin agents per value stream en fase. Alleen agents met agent-contracten/ en prompts/ subfolders worden meegenomen.',
            'gegenereerd_op': datetime.now().isoformat(),
            'versie': '2.0',
            'aantal_value_streams': len(value_streams),
            'aantal_agents': total_agents
        },
        'value_streams': value_streams
    }


def generate_agents_publicatie(
    workspace_root: Path,
    output_file: str = 'agents-publicatie.json'
) -> None:
    """
    Genereer agents-publicatie.json in workspace root.
    
    Args:
        workspace_root: Path naar workspace root folder
        output_file: Naam van output JSON file (default: agents-publicatie.json)
        
    Raises:
        FileNotFoundError: Als artefacten/ folder niet bestaat
        IOError: Bij schrijffouten
    """
    print("=" * 70)
    print("Genereer agents-publicatie.json")
    print("=" * 70)
    
    artefacten_path = workspace_root / 'artefacten'
    
    print(f"\n1. Scan artefacten folder: {artefacten_path}")
    data = scan_value_stream_folders(artefacten_path)
    
    print(f"\n2. Gevonden value streams: {', '.join(sorted(data.keys()))}")
    for vs in sorted(data.keys()):
        total_agents_vs = sum(len(agents) for agents in data[vs].values())
        print(f"   - {vs}: {len(data[vs])} fasen, {total_agents_vs} agents")
    
    print("\n3. Bouw JSON structuur volgens schema v2.0")
    json_data = build_json_structure(data)
    
    output_path = workspace_root / output_file
    print(f"\n4. Schrijf naar: {output_path}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Gereed!")
    print(f"  - {json_data['metadata']['aantal_value_streams']} value streams")
    print(f"  - {json_data['metadata']['aantal_agents']} agents totaal")
    print("=" * 70)


def main() -> None:
    """Main entry point."""
    try:
        # Bepaal workspace root (2 levels omhoog vanaf scripts/)
        script_path = Path(__file__).resolve()
        workspace_root = script_path.parent.parent
        
        generate_agents_publicatie(workspace_root)
        
    except FileNotFoundError as e:
        print(f"Fout: {e}")
        exit(1)
    except IOError as e:
        print(f"Schrijffout: {e}")
        exit(2)
    except Exception as e:
        print(f"Onverwachte fout: {e}")
        exit(99)


if __name__ == '__main__':
    main()
