"""
Copy AEO.02 Agents Script

Kopieert alle agents uit artefacten/aeo/aeo.02.* naar centrale workspace-locaties.
"""

import os
import shutil
from pathlib import Path

def main():
    """Kopieer AEO 02 agents naar workspace-locaties."""
    print("[copy_aeo_02_agents] Start kopiëren van AEO 02 agents...")
    
    # Gebruik relatieve paden ten opzichte van workspace root
    workspace_root = Path.cwd()
    aeo_folder = workspace_root / "artefacten" / "aeo"
    
    if not aeo_folder.exists():
        print(f"[Waarschuwing] AEO folder niet gevonden: {aeo_folder}")
        print(f"[Debug] Current working directory: {workspace_root}")
        return
    
    # Tel statistieken
    total_contracts = 0
    total_prompts = 0
    total_charters = 0
    total_templates = 0
    total_runners = 0
    
    # Zoek alle aeo.02.* folders
    aeo_02_folders = [f for f in aeo_folder.iterdir() 
                      if f.is_dir() and f.name.startswith("aeo.02.")]
    
    print(f"[Info] Gevonden {len(aeo_02_folders)} aeo.02 agent-folders")
    
    for agent_folder in aeo_02_folders:
        agent_name = agent_folder.name.replace("aeo.02.", "")
        print(f"[Info] Verwerk: {agent_name}")
        
        # Kopieer agent-contracten naar .github/agents
        for contract in agent_folder.glob("*.agent.md"):
            dest = workspace_root / ".github" / "agents" / contract.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(contract, dest)
            total_contracts += 1
            print(f"  ✓ {contract.name} → .github/agents/")
        
        # Kopieer prompts naar .github/prompts
        for prompt in agent_folder.glob("*.prompt.md"):
            dest = workspace_root / ".github" / "prompts" / prompt.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(prompt, dest)
            total_prompts += 1
            print(f"  ✓ {prompt.name} → .github/prompts/")
        
        # Kopieer charters naar agent-charters
        for charter in agent_folder.glob("*.charter.md"):
            dest = workspace_root / "agent-charters" / charter.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(charter, dest)
            total_charters += 1
            print(f"  ✓ {charter.name} → agent-charters/")
        
        # Kopieer templates naar templates
        for template in agent_folder.glob("*template*.md"):
            dest = workspace_root / "templates" / template.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(template, dest)
            total_templates += 1
            print(f"  ✓ {template.name} → templates/")
        
        # Kopieer runners naar scripts (niet scripts/runners)
        for runner in agent_folder.glob("*.runner.py"):
            dest = workspace_root / "scripts" / runner.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(runner, dest)
            total_runners += 1
            print(f"  ✓ {runner.name} → scripts/")
    
    print(f"\n[copy_aeo_02_agents] ✓ Kopiëren afgerond")
    total = total_contracts + total_prompts + total_charters + total_templates + total_runners
    print(f"[Samenvatting] {total_contracts} agent-contracten, {total_prompts} prompts, "
          f"{total_charters} charters, {total_templates} templates, {total_runners} runners (totaal: {total} bestanden)")

if __name__ == "__main__":
    main()