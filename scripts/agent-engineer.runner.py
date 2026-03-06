#!/usr/bin/env python3
"""
Agent Runner: agent-engineer

Deterministische executor voor de intent 'realiseer-agent-prompts' en 'realiseer-agent-taskconfiguratie'.
Vervangt de LLM-gebaseerde generatie met een 100% deterministische script-flow conform het contract.

Gebruik:
    python scripts/agent-engineer.runner.py <agent_naam> [--intent <intent_naam>]
"""

import sys
import argparse
import json
from pathlib import Path
import re

def find_agent_dir(agent_naam):
    """Zoek de juiste directory voor de gegeven agent in artefacten/."""
    artefacten = Path("artefacten")
    for agent_dir in artefacten.glob(f"*/*.*.{agent_naam}"):
        if agent_dir.is_dir() and (agent_dir / "agent-contracten").is_dir():
            return agent_dir
    return None

def parse_agent_info(agent_dir):
    """Extraheer vs en fase uit de mapnaam (bijv. aeo.02.agent-engineer)."""
    parts = agent_dir.name.split('.')
    if len(parts) >= 2:
        return parts[0], parts[1]
    return "onbekend", "00"

def get_intents(agent_dir, agent_naam):
    """Lees alle beschikbare intents uit de agent-contracten map."""
    intents = []
    contract_dir = agent_dir / "agent-contracten"
    if contract_dir.is_dir():
        for file_path in contract_dir.glob("*.agent.md"):
            # Bestandsnaam is agent_naam.intent_naam.agent.md
            filename = file_path.name
            prefix = f"{agent_naam}."
            suffix = ".agent.md"
            if filename.startswith(prefix) and filename.endswith(suffix):
                intent = filename[len(prefix):-len(suffix)]
                intents.append(intent)
    return intents

def realiseer_prompts(agent_dir, agent_naam, vs, fase, intents):
    prompts_dir = agent_dir / "prompts"
    prompts_dir.mkdir(exist_ok=True)
    
    for intent in intents:
        prompt_file = prompts_dir / f"mandarin.{agent_naam}.{intent}.prompt.md"
        contract_file = agent_dir / "agent-contracten" / f"{agent_naam}.{intent}.agent.md"
        
        # Extract inputs from contract
        input_params = []
        if contract_file.exists():
            content = contract_file.read_text(encoding='utf-8')
            
            # Zoek verplichte parameters
            m_verplicht = re.search(r'\*\*Verplichte parameters\*\*:?\n((?:-[^\n]+\n)+)', content)
            if m_verplicht:
                for line in m_verplicht.group(1).strip().split('\n'):
                    if line.startswith('- '):
                        param = line[2:].split(':')[0].strip()
                        if param and param.lower() != 'geen':
                            input_params.append(param)
                            
            # Zoek optionele parameters
            m_optioneel = re.search(r'\*\*Optionele parameters\*\*:?\n((?:-[^\n]+\n)+)', content)
            if m_optioneel:
                for line in m_optioneel.group(1).strip().split('\n'):
                    if line.startswith('- '):
                        param = line[2:].split(':')[0].strip()
                        if param and param.lower() != 'geen':
                            input_params.append(param)
        
        inputs_yaml = ""
        if input_params:
            inputs_yaml = "\ninput_parameters:\n" + "\n".join([f"  - {p}" for p in input_params])
            
        content = f"""---
agent: mandarin.{agent_naam}
intent: {intent}
versie: 1.0.0{inputs_yaml}
value_stream_fase: {vs}.{fase}

bootstrap:
  script: scripts/bootstrap_canon_consult.py
---
"""
        prompt_file.write_text(content, encoding='utf-8')
        print(f"[SUCCESS] Created prompt: {prompt_file}")

def realiseer_tasks(agent_dir, agent_naam, vs, fase, intents):
    tasks_dir = agent_dir / "tasks"
    tasks_dir.mkdir(exist_ok=True)
    
    task_file = tasks_dir / f"{vs}-{fase}.{agent_naam}.tasks.json"
    
    task_json = {
        "version": "2.0.0",
        "tasks": []
    }
    
    for intent in intents:
        label = f"{vs}.{fase} - {agent_naam}: {intent}"
        script_cmd = (
            f"$generator = Join-Path $PWD 'scripts/generate_instructions.py'; "
            f"$timestamp = Get-Date -Format 'yyyyMMddHHmmss'; $agent = '{agent_naam}'; "
            f"$intent = '{intent}'; $hashInput = $timestamp + $agent; "
            f"$md5 = [System.Security.Cryptography.MD5]::Create(); "
            f"$hashBytes = $md5.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($hashInput)); "
            f"$hash = [System.BitConverter]::ToString($hashBytes).Replace('-','').Substring(0,4).ToLower(); "
            f"$filename = \"agent-execution/$hash.$agent.$intent.md\"; "
            f"[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; "
            f"$env:PYTHONIOENCODING='utf-8'; "
            f"python $generator --agent $agent --intent $intent --execution-file $filename; "
            f"if ($LASTEXITCODE -eq 0) {{ code $filename }}"
        )
        
        task_json["tasks"].append({
            "label": label,
            "type": "process",
            "command": "powershell",
            "args": ["-Command", script_cmd],
            "problemMatcher": [],
            "presentation": {
                "reveal": "always",
                "panel": "shared"
            }
        })
        
    task_file.write_text(json.dumps(task_json, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"[SUCCESS] Created task configuratie: {task_file}")

def main():
    parser = argparse.ArgumentParser(description="Deterministische Agent Engineer Runner")
    parser.add_argument("agent_naam", help="De naam van de agent (bijv. gedragsspecificator)")
    parser.add_argument("--intent", choices=["realiseer-agent-prompts", "realiseer-agent-taskconfiguratie", "all"], default="all")
    
    args = parser.parse_args()
    
    agent_dir = find_agent_dir(args.agent_naam)
    if not agent_dir:
        print(f"[ERROR] Map voor agent {args.agent_naam} niet gevonden in artefacten/")
        sys.exit(1)
        
    vs, fase = parse_agent_info(agent_dir)
    intents = get_intents(agent_dir, args.agent_naam)
    
    if not intents:
        print(f"[WARNING] Geen intents (agent-contracten) gevonden voor {args.agent_naam}")
        sys.exit(0)
        
    if args.intent in ["realiseer-agent-prompts", "all"]:
        realiseer_prompts(agent_dir, args.agent_naam, vs, fase, intents)
        
    if args.intent in ["realiseer-agent-taskconfiguratie", "all"]:
        realiseer_tasks(agent_dir, args.agent_naam, vs, fase, intents)

if __name__ == "__main__":
    main()
