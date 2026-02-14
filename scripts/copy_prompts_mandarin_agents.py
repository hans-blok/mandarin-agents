"""
Copy Mandarin Agents Assets Script

Kopieert agent-artefacten naar centrale locaties en genereert agents.yaml:
- Prompts uit artefacten/{vs}/{agent}/prompts/ naar .github/prompts/
- Agent-contracten uit artefacten/{vs}/{agent}/agent-contracten/ naar .github/agents/
- Genereert .github/copilot/agents.yaml met alle agents
"""

import os
import shutil
import yaml
from pathlib import Path

def clean_folder(folder_path, pattern="*"):
    """Maak een folder leeg met optioneel pattern."""
    if folder_path.exists():
        files = list(folder_path.glob(pattern))
        if files:
            print(f"[Info] Leegmaken van {folder_path}")
            for file in files:
                file.unlink()
                print(f"  ✗ Verwijderd: {file.name}")
        return len(files)
    else:
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"[Info] Aangemaakt: {folder_path}")
        return 0

def build_agents_yaml(agents_data, output_path):
    """Bouw agents.yaml bestand met alle agent-definities."""
    yaml_content = {"agents": []}
    
    for agent in agents_data:
        agent_entry = {
            "id": agent["id"],
            "name": f"workspace.{agent['id']}",
            "type": agent.get("type", "uitvoerend"),
            "valueStream": agent.get("valueStream", "unknown"),
            "charter": agent["charter"],
            "prompts": sorted(agent["prompts"]),
            "runners": agent.get("runners", [])
        }
        yaml_content["agents"].append(agent_entry)
    
    # Schrijf YAML met mooie formatting
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(yaml_content, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"[Info] Gegenereerd: {output_path}")
    print(f"       {len(agents_data)} agents geregistreerd")

def extract_value_stream_from_path(agent_path):
    """Extraheer value stream code uit pad zoals aeo.02.agent-smeder -> aeo."""
    parts = agent_path.name.split(".")
    if len(parts) >= 2:
        return parts[0]
    return "utility"

def main():
    """Kopieer alle agent assets en genereer agents.yaml."""
    print("[copy_mandarin_agents] Start synchronisatie van agent assets...")
    print()
    
    # Gebruik relatieve paden ten opzichte van workspace root
    workspace_root = Path.cwd()
    artefacten_folder = workspace_root / "artefacten"
    prompts_dest = workspace_root / ".github" / "prompts"
    agents_dest = workspace_root / ".github" / "agents"
    agents_yaml_path = workspace_root / ".github" / "copilot" / "agents.yaml"
    
    if not artefacten_folder.exists():
        print(f"[Waarschuwing] Artefacten folder niet gevonden: {artefacten_folder}")
        print(f"[Debug] Current working directory: {workspace_root}")
        return
    
    # 1. Cleanup .github/prompts
    clean_folder(prompts_dest, "*.prompt.md")
    print()
    
    # 2. Cleanup .github/agents
    clean_folder(agents_dest, "*.agent.md")
    print()
    
    # 3. Verwijder oude agents.yaml
    if agents_yaml_path.exists():
        agents_yaml_path.unlink()
        print(f"[Info] Verwijderd: {agents_yaml_path}")
        print()
    
    # Tel statistieken
    total_prompts = 0
    total_contracts = 0
    agents_data = []
    
    # Zoek alle value stream folders (aeo, fnd, sfw, etc.)
    value_stream_folders = [f for f in artefacten_folder.iterdir() 
                            if f.is_dir() and not f.name.startswith("_")]
    
    print(f"[Info] Gevonden {len(value_stream_folders)} value stream folders")
    print()
    
    for vs_folder in value_stream_folders:
        vs_name = vs_folder.name
        
        # Zoek alle agent-folders binnen deze value stream
        agent_folders = [f for f in vs_folder.iterdir() 
                        if f.is_dir() and not f.name.startswith("_")]
        
        for agent_folder in agent_folders:
            # Filter: alleen aeo.02.* en fnd.01.* folders verwerken
            folder_prefix = ".".join(agent_folder.name.split(".")[:2])
            if folder_prefix not in ["aeo.02", "fnd.01"]:
                continue
            agent_name = agent_folder.name
            
            # Probeer prompts/ subfolder (nieuwe conventie)
            prompts_folder = agent_folder / "prompts"
            contracts_folder = agent_folder / "agent-contracten"
            
            # Als prompts/ niet bestaat, gebruik agent folder zelf (oude conventie)
            if not prompts_folder.exists():
                prompts_folder = agent_folder
            
            # Extract agent ID from folder name (last part after final dot)
            agent_id = agent_name.split(".")[-1]
            
            # Find charter file
            charter_files = list(agent_folder.glob("*.charter.md"))
            charter_file = charter_files[0] if charter_files else None
            
            # Check of er prompts of contracts zijn
            has_prompts = list(prompts_folder.glob("*.prompt.md"))
            has_contracts = contracts_folder.exists() and list(contracts_folder.glob("*.agent.md"))
            
            # Als contracts_folder niet bestaat, zoek in agent folder zelf (oude conventie)
            if not has_contracts:
                has_contracts = list(agent_folder.glob("*.agent.md"))
            if not (has_prompts or has_contracts):
                continue
            
            print(f"[Info] Verwerk: {vs_name}/{agent_name}")
            
            # Verzamel agent data voor YAML
            agent_prompts = []
            
            # Kopieer prompts
            if has_prompts:
                for prompt in prompts_folder.glob("*.prompt.md"):
                    dest = prompts_dest / prompt.name
                    shutil.copy2(prompt, dest)
                    total_prompts += 1
                    agent_prompts.append(f".github/prompts/{prompt.name}")
                    print(f"  ✓ Prompt: {prompt.name}")
            
            # Kopieer agent-contracten
            if has_contracts:
                # Eerst checken of contracts in subfolder staan
                if contracts_folder.exists():
                    contract_source = contracts_folder
                else:
                    # Anders in agent folder zelf (oude conventie)
                    contract_source = agent_folder
                
                for contract in contract_source.glob("*.agent.md"):
                    dest = agents_dest / contract.name
                    shutil.copy2(contract, dest)
                    total_contracts += 1
                    print(f"  ✓ Contract: {contract.name}")
            
            # Registreer agent voor YAML
            if has_prompts:  # Alleen agents met prompts in de YAML
                charter_path = str(charter_file.relative_to(workspace_root)).replace("\\", "/") if charter_file else f"charters/{agent_id}.charter.md"
                
                agent_data = {
                    "id": agent_id,
                    "type": "uitvoerend",
                    "valueStream": extract_value_stream_from_path(agent_folder),
                    "charter": charter_path,
                    "prompts": agent_prompts,
                    "runners": []
                }
                agents_data.append(agent_data)
            
            print()
    
    # 4. Genereer nieuwe agents.yaml
    if agents_data:
        build_agents_yaml(agents_data, agents_yaml_path)
        print()
    
    print(f"[copy_mandarin_agents] ✓ Synchronisatie afgerond")
    print(f"[Samenvatting]")
    print(f"  - {total_prompts} prompts gekopieerd naar .github/prompts/")
    print(f"  - {total_contracts} agent-contracten gekopieerd naar .github/agents/")
    print(f"  - {len(agents_data)} agents geregistreerd in agents.yaml")

if __name__ == "__main__":
    main()
