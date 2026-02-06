#!/usr/bin/env python3

"""
Agent Curator Runner — Publiceer Agents Overzicht

Deze runner scant alle agent-charters in de artefacten/ folder, leest metadata uit de headers
en folder-structuur, telt contracts, templates en runners, en publiceert een overzicht in JSON en Markdown
gestructureerd per value stream en fase.

Usage:
    python scripts/runners/agent-curator.py

Output:
    - agents-publicatie.json (root, voor fetching)
    - docs/resultaten/agent-publicaties/agents-publicatie-<datum>.md (archief)

Traceability:
    Charter: artefacten/aeo.02.agent-curator/agent-curator.charter.md
    Contract: artefacten/aeo.02.agent-curator/agent-curator.publiceer-agents.overzicht.agent.md
    Prompt: .github/prompts/mandarin.agent-curator.publiceer-agents.overzicht.prompt.md
    Schema: schemas/agents-publicatie-schema.json
"""

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Mapping van value stream codes naar volledige namen
VALUE_STREAM_NAMES = {
    "aeo": "Agent Ecosysteem Ontwikkeling",
    "sfw": "Softwareontwikkeling",
    "aod": "Architectuur- en Oplossingsontwerp",
    "kvl": "Kennisvastlegging",
    "miv": "Markt- en Investeringsvorming",
    "fnd": "Foundational (value-stream-overstijgend)"
}

# Mapping van fasenummers naar namen per value stream
FASE_NAMES = {
    "aeo": {
        "01": "Grondslagvorming",
        "02": "Ecosysteeminrichting"
    },
    "sfw": {
        "01": "Veranderkenning",
        "02": "Werkvoorbereiding",
        "03": "Behoefte- en requirements analyse",
        "04": "Ontwerp",
        "05": "Realisatie",
        "06": "Validatie",
        "07": "Vrijgave",
        "08": "Beheer en Evolutie"
    },
    "aod": {
        "01": "Vraagverkenning",
        "02": "Architectuurkadering",
        "03": "Oplossingsontwerp",
        "04": "Besluitvorming en Borging"
    },
    "kvl": {
        "01": "Kennisverkenning",
        "02": "Structurering",
        "03": "Vastlegging",
        "04": "Publicatie en Onderhoud"
    },
    "miv": {
        "01": "Strategische intentie expliciteren",
        "02": "Waarde-hypotheses formuleren",
        "03": "Positioneringsrichtingen verkennen",
        "04": "Monetisatie-logica's scheiden",
        "05": "Investering en kostenrealiteit expliciet maken",
        "06": "Keuzeruimte structureren"
    },
    "fnd": {
        "00": "Stewardship",
        "01": "Technische ondersteuning"
    }
}


@dataclass
class AgentMetadata:
    """Metadata extracted from agent charter header and folder structure."""
    naam: str
    value_stream_code: str
    fase_nummer: str
    domein: str = ""
    charter_path: Optional[Path] = None
    aantal_contracts: int = 0
    aantal_templates: int = 0
    aantal_runners: int = 0


def parse_folder_name(folder_name: str) -> Optional[Tuple[str, str, str]]:
    """Parse agent folder name to extract value stream code, fase nummer en agent naam.
    
    Verwacht patroon: <vs-code>.<fase-nr>.<agent-naam>
    Bijvoorbeeld: aeo.02.agent-curator, sfw.01.hypothese-vormer, fnd.01.workspace-steward
    
    Args:
        folder_name: Name of the agent folder
        
    Returns:
        Tuple van (value_stream_code, fase_nummer, agent_naam) of None bij ongeldige naam
    """
    pattern = r"^([a-z]{3})\.(\d{2})\.(.+)$"
    match = re.match(pattern, folder_name)
    if match:
        return match.group(1), match.group(2), match.group(3)
    return None


def scan_charter(charter_path: Path, folder_info: Tuple[str, str, str]) -> Optional[AgentMetadata]:
    """Scan a charter file and extract metadata.
    
    Args:
        charter_path: Path to charter file
        folder_info: Tuple van (value_stream_code, fase_nummer, agent_naam) uit folder naam
        
    Returns:
        AgentMetadata if successful, None if charter is invalid
    """
    try:
        content = charter_path.read_text(encoding="utf-8")
        
        vs_code, fase_nr, agent_naam = folder_info
        
        # Extract domein from header
        domein_pattern = r"\*\*Domein\*\*:\s*(.+?)(?:\n|$)"
        domein_match = re.search(domein_pattern, content, re.IGNORECASE)
        domein = domein_match.group(1).strip() if domein_match else ""
        
        return AgentMetadata(
            naam=agent_naam,
            value_stream_code=vs_code,
            fase_nummer=fase_nr,
            domein=domein,
            charter_path=charter_path
        )
    except UnicodeDecodeError as e:
        print(f"[ERROR] Encoding error in charter {charter_path}: {e}")
        return None
    except OSError as e:
        print(f"[ERROR] Failed to read charter {charter_path}: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error scanning charter {charter_path}: {e}")
        return None


def count_contracts(agent_naam: str, agent_folder: Path) -> int:
    """Count contract files (*.agent.md) for an agent in its folder.
    
    Args:
        agent_naam: Name of the agent
        agent_folder: Path to agent's folder
        
    Returns:
        Total number of contract files found
    """
    try:
        pattern = f"{agent_naam}.*.agent.md"
        return len(list(agent_folder.glob(pattern)))
    except OSError as e:
        print(f"[WARN] Error scanning contracts for {agent_naam}: {e}")
        return 0


def count_templates(agent_folder: Path) -> int:
    """Count templates that exist as files in agent folder AND are mentioned in charter.
    
    Strategie:
    1. Vind alle *template*.md bestanden in de agent folder
    2. Check of de exacte bestandsnaam voorkomt in de charter
    3. Tel alleen templates die aan beide voorwaarden voldoen
    
    Args:
        agent_folder: Path to agent's folder
        
    Returns:
        Total number of templates found (exist as file + mentioned in charter)
    """
    try:
        # Find charter in folder
        charter_files = list(agent_folder.glob("*.charter.md"))
        if not charter_files:
            return 0
        
        charter_path = charter_files[0]
        charter_content = charter_path.read_text(encoding="utf-8")
        
        # Find all template files in agent folder
        template_files = list(agent_folder.glob("*template*.md"))
        
        # Count only templates that are also mentioned in charter
        count = 0
        for template_file in template_files:
            if template_file.is_file():
                # Check if exact filename appears in charter
                if template_file.name in charter_content:
                    count += 1
        
        return count
        
    except Exception as e:
        print(f"[WARN] Error counting templates in {agent_folder}: {e}")
        return 0


def count_runners(agent_naam: str, agent_folder: Path, workspace_root: Path) -> int:
    """Count runners for an agent.
    
    Checks two locations:
    1. New pattern: <agent-naam>.py in agent-folder itself
    2. Legacy pattern: scripts/runners/<agent-naam>.py or scripts/runners/<agent-naam>/
    
    Args:
        agent_naam: Name of the agent
        agent_folder: Path to agent's folder (where runner should be per new normering)
        workspace_root: Root directory of workspace
        
    Returns:
        Total number of runners found for this agent (max 2: new + legacy)
    """
    try:
        count = 0
        
        # NEW PATTERN: Runner in agent-folder as <agent-naam>.py
        runner_in_folder = agent_folder / f"{agent_naam}.py"
        if runner_in_folder.exists() and runner_in_folder.is_file():
            count += 1
        
        # LEGACY PATTERN: Runner in scripts/runners/
        runners_dir = workspace_root / "scripts" / "runners"
        if runners_dir.exists() and runners_dir.is_dir():
            # Individual runner script
            runner_file = runners_dir / f"{agent_naam}.py"
            if runner_file.exists() and runner_file.is_file():
                count += 1
            
            # Runner module folder
            runner_module = runners_dir / agent_naam
            if runner_module.exists() and runner_module.is_dir():
                # Verify it's a valid Python module (has __init__.py)
                init_file = runner_module / "__init__.py"
                if init_file.exists():
                    count += 1
        
        return count
    except OSError as e:
        print(f"[WARN] Error scanning runners for {agent_naam}: {e}")
        return 0


def scan_all_agents(workspace_root: Path) -> List[AgentMetadata]:
    """Scan all agent folders under artefacten/.
    
    Verwacht structuur: 
    - artefacten/<vs-code>.<fase-nr>.<agent-naam>/  (flat)
    - artefacten/<vs-code>/<vs-code>.<fase-nr>.<agent-naam>/  (nested)
    
    Args:
        workspace_root: Root directory of workspace
        
    Returns:
        List of AgentMetadata for all discovered agents
    """
    agents = []
    scanned_names = set()  # Track duplicates
    
    try:
        artefacten_dir = workspace_root / "artefacten"
        if not artefacten_dir.exists() or not artefacten_dir.is_dir():
            print(f"[ERROR] artefacten/ folder not found")
            return []
        
        # Scan all folders and subfolders in artefacten/
        folders_to_scan = []
        
        for item in artefacten_dir.iterdir():
            if not item.is_dir():
                continue
            
            # Skip special folders
            if item.name in ["__pycache__", "runners", "utility"]:
                continue
            
            # Check if this is a valid agent folder
            if parse_folder_name(item.name):
                folders_to_scan.append(item)
            else:
                # This might be a parent folder (like 'aeo', 'sfw'), scan one level deeper
                for subfolder in item.iterdir():
                    if subfolder.is_dir() and parse_folder_name(subfolder.name):
                        folders_to_scan.append(subfolder)
        
        # Now scan all collected agent folders
        for agent_folder in folders_to_scan:
            folder_info = parse_folder_name(agent_folder.name)
            if not folder_info:
                continue
            
            vs_code, fase_nr, agent_naam = folder_info
            
            # Find charter in folder
            charter_files = list(agent_folder.glob("*.charter.md"))
            if not charter_files:
                print(f"[WARN] No charter found in {agent_folder.name}")
                continue
            
            charter_path = charter_files[0]
            
            # Scan charter
            metadata = scan_charter(charter_path, folder_info)
            if not metadata:
                continue
            
            # Check for duplicates
            if metadata.naam in scanned_names:
                print(f"[WARN] Duplicate agent found: {metadata.naam} in {agent_folder.name}")
                continue
            
            # Count artifacts
            metadata.aantal_contracts = count_contracts(agent_naam, agent_folder)
            metadata.aantal_templates = count_templates(agent_folder)
            metadata.aantal_runners = count_runners(agent_naam, agent_folder, workspace_root)
            
            agents.append(metadata)
            scanned_names.add(metadata.naam)
    
    except OSError as e:
        print(f"[ERROR] Error scanning agents: {e}")
    
    return agents


def calculate_digest(agents: List[AgentMetadata]) -> str:
    """Calculate 5-character SHA-256 digest of agents list for change tracking.
    
    Creates a deterministic hash based on agent names, value streams, fases and artifact counts.
    Sorted by agent name to ensure consistent results.
    
    Args:
        agents: List of agent metadata
        
    Returns:
        First 5 characters of SHA-256 hash (hex format)
    """
    # Sort by name for deterministic results
    sorted_agents = sorted(agents, key=lambda a: (a.value_stream_code, a.fase_nummer, a.naam))
    
    # Create deterministic string representation
    agent_data = json.dumps(
        [
            {
                "naam": agent.naam,
                "valueStreamCode": agent.value_stream_code,
                "faseNummer": agent.fase_nummer,
                "aantalContracts": agent.aantal_contracts,
                "aantalTemplates": agent.aantal_templates,
                "aantalRunners": agent.aantal_runners
            }
            for agent in sorted_agents
        ],
        sort_keys=True,
        ensure_ascii=False
    )
    
    # Calculate SHA-256 and take first 5 characters
    hash_obj = hashlib.sha256(agent_data.encode('utf-8'))
    return hash_obj.hexdigest()[:5]


def generate_json(agents: List[AgentMetadata]) -> Dict:
    """Generate JSON structure for agents-publicatie.json volgens schema.
    
    Args:
        agents: List of agent metadata
        
    Returns:
        Dictionary with complete publication structure per schema
    """
    # Group agents by value stream and fase
    by_stream_fase: Dict[str, Dict[str, List[AgentMetadata]]] = defaultdict(lambda: defaultdict(list))
    
    for agent in agents:
        by_stream_fase[agent.value_stream_code][agent.fase_nummer].append(agent)
    
    # Build value streams list
    value_streams_list = []
    
    for vs_code in sorted(by_stream_fase.keys()):
        vs_naam = VALUE_STREAM_NAMES.get(vs_code, vs_code.upper())
        
        fases_list = []
        for fase_nr in sorted(by_stream_fase[vs_code].keys()):
            fase_naam = FASE_NAMES.get(vs_code, {}).get(fase_nr, f"Fase {fase_nr}")
            
            agents_list = []
            for agent in sorted(by_stream_fase[vs_code][fase_nr], key=lambda a: a.naam):
                agent_obj = {
                    "naam": agent.naam,
                    "aantalContracts": agent.aantal_contracts,
                    "aantalTemplates": agent.aantal_templates,
                    "aantalRunners": agent.aantal_runners
                }
                
                agents_list.append(agent_obj)
            
            fases_list.append({
                "naam": fase_naam,
                "volgnummer": fase_nr,
                "agents": agents_list
            })
        
        value_streams_list.append({
            "naam": vs_naam,
            "code": vs_code,
            "fases": fases_list
        })
    
    return {
        "versie": "3.0",
        "publicatiedatum": datetime.now().strftime("%Y-%m-%d"),
        "digest": calculate_digest(agents),
        "valueStreams": value_streams_list
    }


def generate_markdown(agents: List[AgentMetadata]) -> str:
    """Generate Markdown archive with full metadata per value stream en fase.
    
    Args:
        agents: List of agent metadata
        
    Returns:
        Markdown content as string
    """
    lines = []
    
    # Header
    lines.append(f"# Agents Publicatie Overzicht\n\n")
    lines.append(f"**Publicatiedatum**: {datetime.now().strftime('%Y-%m-%d')}\n")
    lines.append(f"**Tijdstip**: {datetime.now().strftime('%H:%M:%S')}\n")
    lines.append(f"**Digest**: {calculate_digest(agents)}\n")
    lines.append(f"**Totaal agents**: {len(agents)}\n\n")
    
    # Group by value stream and fase
    by_stream_fase: Dict[str, Dict[str, List[AgentMetadata]]] = defaultdict(lambda: defaultdict(list))
    
    for agent in agents:
        by_stream_fase[agent.value_stream_code][agent.fase_nummer].append(agent)
    
    # Generate tables per value stream and fase
    for vs_code in sorted(by_stream_fase.keys()):
        vs_naam = VALUE_STREAM_NAMES.get(vs_code, vs_code.upper())
        lines.append(f"## Value Stream: {vs_naam} ({vs_code.upper()})\n\n")
        
        for fase_nr in sorted(by_stream_fase[vs_code].keys()):
            fase_naam = FASE_NAMES.get(vs_code, {}).get(fase_nr, f"Fase {fase_nr}")
            fase_agents = sorted(by_stream_fase[vs_code][fase_nr], key=lambda a: a.naam)
            
            lines.append(f"### Fase {fase_nr}: {fase_naam}\n\n")
            lines.append(f"**Aantal agents**: {len(fase_agents)}\n\n")
            
            # Table
            lines.append("| Agent | Domein | Contracts | Templates | Runners |\n")
            lines.append("|-------|--------|-----------|-----------|----------|\n")
            for agent in fase_agents:
                lines.append(f"| {agent.naam} | {agent.domein} | {agent.aantal_contracts} | {agent.aantal_templates} | {agent.aantal_runners} |\n")
            lines.append("\n")
    
    # Metadata
    lines.append("## Metadata\n\n")
    lines.append(f"- **Gescande folders**:\n")
    lines.append(f"  - `artefacten/<vs-code>.<fase-nr>.<agent-naam>/` (alle agent folders)\n")
    lines.append(f"- **Folder naamgevingsconventie**: `<vs-code>.<fase-nr>.<agent-naam>`\n")
    lines.append(f"  - `vs-code`: 3-letter value stream code (aeo, sfw, aod, kvl, miv, fnd)\n")
    lines.append(f"  - `fase-nr`: 2-cijferig fasenummer (01, 02, ...)\n")
    lines.append(f"  - `agent-naam`: agent identifier (lowercase met hyphens)\n")
    lines.append(f"- **Contracts**: `<agent-naam>.*.agent.md` bestanden in agent folder\n")
    lines.append(f"- **Templates**: Template veld in charter (niet '-' of '—')\n")
    lines.append(f"- **Runners**: `scripts/runners/<agent-naam>.py` of `scripts/runners/<agent-naam>/__init__.py`\n")
    lines.append(f"- **Digest**: 5-karakter SHA-256 hash van agents-lijst (gesorteerd) voor change-tracking\n")
    lines.append(f"- **Schema**: `schemas/agents-publicatie-schema.json`\n")
    lines.append(f"- **Traceability**: Agent Curator charter, publiceer-agents-overzicht contract & prompt\n")
    
    return "".join(lines)


def write_outputs(json_data: Dict, markdown_content: str, workspace_root: Path) -> None:
    """Write JSON and Markdown outputs.
    
    Args:
        json_data: JSON publication data
        markdown_content: Markdown archive content
        workspace_root: Root directory of workspace
        
    Raises:
        OSError: If file writing fails
    """
    try:
        # Write JSON to root
        json_path = workspace_root / "agents-publicatie.json"
        json_content = json.dumps(json_data, indent=2, ensure_ascii=False)
        json_path.write_text(json_content, encoding="utf-8")
        print(f"[JSON] {json_path.relative_to(workspace_root)}")
        
        # Write Markdown to archive
        archive_dir = workspace_root / "docs" / "resultaten" / "agent-publicaties"
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        md_filename = f"agents-publicatie-{timestamp}.md"
        
        md_path = archive_dir / md_filename
        md_path.write_text(markdown_content, encoding="utf-8")
        print(f"[MARKDOWN] {md_path.relative_to(workspace_root)}")
    except OSError as e:
        print(f"[ERROR] Failed to write output files: {e}", file=sys.stderr)
        raise


def main() -> int:
    """Main entry point for Agent Curator runner.
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    workspace_root = Path(__file__).parent.parent.parent
    
    print("Agent Curator — Publiceer Agents Overzicht")
    print("=" * 60)
    print()
    
    try:
        # Scan all agents
        print("[INFO] Scanning agent folders in artefacten/...")
        agents = scan_all_agents(workspace_root)
        
        if not agents:
            print("[ERROR] No agents found", file=sys.stderr)
            return 1
        
        print(f"[INFO] Found {len(agents)} agents")
        
        # Group counts per value stream
        vs_counts: Dict[str, int] = defaultdict(int)
        for agent in agents:
            vs_counts[agent.value_stream_code] += 1
        
        for vs_code in sorted(vs_counts.keys()):
            vs_naam = VALUE_STREAM_NAMES.get(vs_code, vs_code.upper())
            print(f"  - {vs_naam} ({vs_code.upper()}): {vs_counts[vs_code]} agents")
        
        print()
        
        # Generate outputs
        print("[INFO] Generating outputs...")
        json_data = generate_json(agents)
        markdown_content = generate_markdown(agents)
        
        # Write outputs
        write_outputs(json_data, markdown_content, workspace_root)
        
        print("\n[SUCCESS] Agents overzicht gepubliceerd")
        return 0
        
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())