"""
Merge tasks uit separate JSON files naar .vscode/tasks.json

Dit script scant alle JSON files in .vscode/tasks/ en merged ze naar
de hoofdtask.json. Dit maakt gestructureerd beheer per value stream fase mogelijk.

Versie: 1.0.0
Auteur: engineer-steward
Datum: 2026-02-15
"""

import json
from pathlib import Path
from typing import Dict, List


def load_task_file(file_path: Path) -> Dict:
    """Laad een task JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def merge_tasks(tasks_folder: Path) -> Dict:
    """
    Merge alle task files in folder naar één structuur.
    
    Args:
        tasks_folder: Pad naar .vscode/tasks/ folder
        
    Returns:
        Merged tasks dictionary
    """
    merged = {
        "version": "2.0.0",
        "tasks": [],
        "inputs": [
            {
                "id": "agentName",
                "type": "promptString",
                "description": "Agent naam (bijv. capability-architect, agent-smeder)"
            },
            {
                "id": "intentName",
                "type": "promptString",
                "description": "Intent naam (bijv. definieer-agent-boundary, leg-vast-agent-charter)"
            },
            {
                "id": "targetAgentName",
                "type": "promptString",
                "description": "Naam van de agent (bijv. core-framework-architect, hypothese-vormer)"
            },
            {
                "id": "valueStreamFase",
                "type": "promptString",
                "description": "Value stream fase (bijv. aeo.02, fnd.01)"
            },
            {
                "id": "korteBeschrijving",
                "type": "promptString",
                "description": "Korte beschrijving van de agent capability (1-3 zinnen)"
            },
            {
                "id": "landschapNaam",
                "type": "promptString",
                "description": "Naam van het landschap (bijv. Transport Logistiek, Financiële Administratie)"
            },
            {
                "id": "domeinNaam",
                "type": "promptString",
                "description": "Domein of value stream (bijv. transport, finance, hr)"
            },
            {
                "id": "archimateLagen",
                "type": "promptString",
                "description": "ArchiMate lagen (bijv. Business,Application,Technology)"
            },
            {
                "id": "activeStructuurFile",
                "type": "promptString",
                "description": "Pad naar actieve structuur bestand (bijv. artefacten/aod/aod.02.core-framework-architect/landschappen/transport/core-framework-architect.structureer-actieve-structuur.md)"
            },
            {
                "id": "gedragFile",
                "type": "promptString",
                "description": "Pad naar gedrag bestand (bijv. artefacten/aod/aod.02.core-framework-architect/landschappen/transport/core-framework-architect.structureer-gedrag.md)"
            }
        ]
    }
    
    # Verzamel alle .json files en sorteer
    task_files = sorted(tasks_folder.glob('*.json'))
    
    print(f"Merge {len(task_files)} task files:")
    for task_file in task_files:
        print(f"  - {task_file.name}")
        data = load_task_file(task_file)
        
        # Merge tasks
        if 'tasks' in data:
            merged['tasks'].extend(data['tasks'])
    
    print(f"\nTotaal: {len(merged['tasks'])} tasks")
    return merged


def main():
    """Hoofdfunctie."""
    workspace_root = Path(__file__).parent.parent
    tasks_folder = workspace_root / '.vscode' / 'tasks'
    output_file = workspace_root / '.vscode' / 'tasks.json'
    
    print("=" * 70)
    print("Merge Tasks naar .vscode/tasks.json")
    print("=" * 70)
    print()
    
    if not tasks_folder.exists():
        print(f"❌ Folder niet gevonden: {tasks_folder}")
        return
    
    # Merge alle tasks
    merged = merge_tasks(tasks_folder)
    
    # Schrijf output
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Geschreven naar: {output_file}")
    print("=" * 70)


if __name__ == '__main__':
    main()
