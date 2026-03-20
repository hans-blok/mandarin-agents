#!/usr/bin/env python3
"""
Runner voor agent: agent-engineer

Zuivere intents voor agent lifecycle engineering:
- realiseer-agent-prompts: Genereer .prompt.md bestanden uit agent-contracten
- realiseer-agent-runner: Genereer runner.py voor een agent
- realiseer-agent-taskconfiguratie: Genereer tasks.json configuratie

Pipeline orchestratie:
- pipeline: Voer alle 3 intents sequentieel uit voor een agent
- execute-from-execution-file: Voer execution-file uit via LLM API

Architectuur: One Agent, One Runner principe.
Cross-cutting functionaliteit (generate-instructions, merge-tasks) is gemigreerd
naar ecosysteem-coordinator.runner.py conform de doctrine.
"""
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import argparse
import hashlib
import io
import json
import os
import re
import subprocess
import sys

# Optionele imports voor LLM executie
try:
    import frontmatter
    HAS_FRONTMATTER = True
except ImportError:
    HAS_FRONTMATTER = False

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


# ==============================================================================
# SHARED UTILITIES
# ==============================================================================

def find_ecosysteem_coordinator_runner() -> Path:
    """Zoek de ecosysteem-coordinator runner."""
    # Probeer relatief pad vanuit deze runner
    this_file = Path(__file__).resolve()
    repo_root = this_file.parent.parent.parent.parent
    
    candidate = repo_root / "artefacten" / "aeo" / "aeo.02.ecosysteem-coordinator" / "runner" / "ecosysteem-coordinator.runner.py"
    if candidate.exists():
        return candidate
    
    # Fallback: zoek vanuit cwd
    cwd_candidate = Path.cwd() / "artefacten" / "aeo" / "aeo.02.ecosysteem-coordinator" / "runner" / "ecosysteem-coordinator.runner.py"
    if cwd_candidate.exists():
        return cwd_candidate
    
    raise FileNotFoundError("ecosysteem-coordinator.runner.py niet gevonden")


def run_generate_instructions(agent_naam: str, intent: str, params: Dict[str, str]):
    """
    Roep ecosysteem-coordinator aan om instructies te genereren.
    
    Dit is de brug tussen agent-engineer en de cross-cutting ecosysteem functionaliteit.
    """
    try:
        coordinator = find_ecosysteem_coordinator_runner()
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    
    # Genereer execution file naam
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    hash_input = f"{timestamp}{agent_naam}".encode('utf-8')
    hash_str = hashlib.md5(hash_input).hexdigest()[:4].lower()
    
    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    if not (repo_root / "artefacten").exists():
        repo_root = Path.cwd()
    
    exec_dir = repo_root / "prompt-instructions"
    exec_dir.mkdir(exist_ok=True)
    filename = exec_dir / f"{timestamp}-{agent_naam}.{intent}.md"
    
    # Bouw commando voor ecosysteem-coordinator
    cmd = [
        sys.executable, str(coordinator), "genereer-instructies",
        "--agent", agent_naam,
        "--intent", intent,
        "--execution-file", str(filename)
    ]
    
    # Voeg parameters toe
    for k, v in params.items():
        if v:
            cmd.extend(["-p", f"{k}={v}"])
    
    env = dict(os.environ)
    env['PYTHONIOENCODING'] = 'utf-8'
    
    print(f"🚀 Start {agent_naam} met intent '{intent}'...")
    print(f"   Via: ecosysteem-coordinator.runner.py genereer-instructies")
    print()
    
    result = subprocess.run(cmd, env=env)
    
    if result.returncode == 0:
        # Open execution file in VS Code
        subprocess.run(["code", str(filename)], shell=True)
    else:
        print(f"❌ Fout opgetreden bij genereren instructies voor {intent}.", file=sys.stderr)
        sys.exit(result.returncode)


# ==============================================================================
# PIPELINE
# ==============================================================================

def find_all_agents() -> List[Dict]:
    """
    Ontdek alle agents in de workspace met agent-contracten.
    """
    artefacten = Path("artefacten")
    if not artefacten.exists():
        print(f"ERROR: artefacten folder niet gevonden")
        return []
    
    agents = []
    
    for contract_dir in artefacten.rglob("agent-contracten"):
        if not contract_dir.is_dir():
            continue
            
        agent_folder = contract_dir.parent
        folder_name = agent_folder.name
        parts = folder_name.split('.')
        
        if len(parts) >= 3:
            agent_naam = '.'.join(parts[2:])
        else:
            agent_naam = folder_name
        
        contracten = list(contract_dir.glob("*.agent.md"))
        
        if contracten:
            agents.append({
                'naam': agent_naam,
                'path': agent_folder,
                'contract_dir': contract_dir,
                'contracten': contracten
            })
    
    return agents


class TeeOutput:
    """Write to both console and log file simultaneously."""
    def __init__(self, log_file, original_stdout):
        self.log_file = log_file
        self.original_stdout = original_stdout
    
    def write(self, text):
        self.original_stdout.write(text)
        self.log_file.write(text)
        self.log_file.flush()
    
    def flush(self):
        self.original_stdout.flush()
        self.log_file.flush()


def execute_agent_engineer(agent_naam: str, intent: str, skip_bootstrap: bool = False, 
                           dry_run: bool = False) -> bool:
    """
    Voer agent-engineer uit voor specifieke intent.
    """
    script = Path(__file__).resolve()
    
    cmd = [
        sys.executable,
        str(script),
        intent,
        "--agent-naam", agent_naam
    ]
    
    if dry_run:
        print(f"  [DRY-RUN] Zou uitvoeren: {' '.join(cmd)}")
        return True
    
    try:
        print(f"  Executing: agent-engineer {intent} for {agent_naam}")
        
        env = dict(os.environ)
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, 
                              encoding='utf-8', env=env)
        
        if result.stdout:
            for line in result.stdout.split('\n'):
                if any(keyword in line.lower() for keyword in ['success', 'error', 'warning', 'created', 'updated', '[ok]']):
                    print(f"    {line}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"  ERROR: {intent} failed for {agent_naam}")
        print(f"  Return code: {e.returncode}")
        if e.stdout:
            print(f"  STDOUT:\n{e.stdout}")
        if e.stderr:
            print(f"  STDERR:\n{e.stderr}")
        return False
    except Exception as e:
        print(f"  ERROR: Unexpected error: {e}")
        return False


def run_pipeline(target_agent: str = None, dry_run: bool = False, 
                 skip_bootstrap: bool = False) -> int:
    """
    Voer de volledige pipeline uit.
    """
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    log_filename = f"{timestamp}.agent-engineer-pipeline.log"
    log_path = logs_dir / log_filename
    
    original_stdout = sys.stdout
    log_file = open(log_path, 'w', encoding='utf-8')
    sys.stdout = TeeOutput(log_file, original_stdout)
    
    try:
        print("=" * 80)
        print("Agent-Engineer Pipeline: Realiseer Prompts, Runner & Tasks")
        print("=" * 80)
        print(f"Log file: {log_path}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        print("📋 Discovering agents...")
        agents = find_all_agents()
        
        if not agents:
            print("ERROR: Geen agents met agent-contracten gevonden")
            return 1
        
        if target_agent:
            agents = [a for a in agents if a['naam'] == target_agent]
            if not agents:
                print(f"ERROR: Agent '{target_agent}' niet gevonden")
                return 1
        
        print(f"Found {len(agents)} agent(s):")
        for agent in agents:
            print(f"  - {agent['naam']} ({len(agent['contracten'])} contract(en))")
        print()
        
        # Intents om uit te voeren (in volgorde)
        intents = [
            "realiseer-agent-prompts",
            "realiseer-agent-runner",
            "realiseer-agent-taskconfiguratie"
        ]
        
        stats = {
            'total': len(agents) * len(intents),
            'success': 0,
            'failed': 0
        }
        
        for i, agent in enumerate(agents, 1):
            print(f"[{i}/{len(agents)}] Processing: {agent['naam']}")
            print(f"          Location: {agent['path']}")
            
            agent_success = True
            
            for intent in intents:
                success = execute_agent_engineer(
                    agent['naam'],
                    intent,
                    skip_bootstrap=skip_bootstrap,
                    dry_run=dry_run
                )
                
                if success:
                    stats['success'] += 1
                else:
                    stats['failed'] += 1
                    agent_success = False
            
            status = "✓ SUCCESS" if agent_success else "✗ FAILED"
            print(f"          Status: {status}")
            print()
    
        print("=" * 80)
        print("Pipeline Summary")
        print("=" * 80)
        print(f"Total operations: {stats['total']}")
        print(f"Successful:       {stats['success']} ✓")
        print(f"Failed:           {stats['failed']} ✗")
        print()
        print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Log file: {log_path}")
        print()
        
        if stats['failed'] == 0:
            print("🎉 All operations completed successfully!")
            return 0
        else:
            print(f"⚠️ {stats['failed']} operation(s) failed. Check logs above.")
            return 1
    
    finally:
        sys.stdout = original_stdout
        log_file.close()
        print(f"\nLog saved to: {log_path}")


def pipeline_main(args: argparse.Namespace) -> int:
    """Main voor pipeline subcommand."""
    target_agent = None if args.all else args.agent
    
    return run_pipeline(
        target_agent=target_agent,
        dry_run=args.dry_run,
        skip_bootstrap=args.skip_bootstrap
    )


# ==============================================================================
# EXECUTE-FROM-EXECUTION-FILE: Automated LLM Pipeline
# ==============================================================================

def parse_execution_file(file_path: Path) -> Tuple[Dict, str]:
    """
    Parse execution file met YAML frontmatter.
    Returns: (metadata dict, instruction content)
    """
    if not HAS_FRONTMATTER:
        raise ImportError("python-frontmatter is vereist. Installeer met: pip install python-frontmatter")
    
    post = frontmatter.load(file_path)
    metadata = dict(post.metadata)
    content = post.content
    
    return metadata, content


def determine_output_config(metadata: Dict, workspace_root: Path) -> Dict:
    """
    Bepaal output configuratie op basis van agent/intent uit metadata.
    Leest agent-contract voor output-locatie specificatie.
    """
    agent = metadata.get('agent', 'unknown')
    intent = metadata.get('intent', 'unknown')
    value_stream_fase = metadata.get('value_stream_fase', 'unknown')
    
    # Parse value stream en fase
    vs_parts = value_stream_fase.split('.')
    vs = vs_parts[0] if len(vs_parts) >= 1 else 'unknown'
    fase = vs_parts[1] if len(vs_parts) >= 2 else '01'
    
    # Bepaal basis output folder
    agent_folder = workspace_root / "artefacten" / vs / f"{vs}.{fase}.{agent}"
    output_folder = agent_folder / "output"
    
    # Bepaal code prefix op basis van agent/intent
    code_prefixes = {
        'hypothese-vormer': 'HYP',
        'concept-curator': 'CON',
        'thema-verwoorder': 'THM',
        'gedragsspecificator': 'GED',
    }
    code_prefix = code_prefixes.get(agent, 'OUT')
    
    return {
        'agent': agent,
        'intent': intent,
        'value_stream': vs,
        'fase': fase,
        'agent_folder': agent_folder,
        'output_folder': output_folder,
        'code_prefix': code_prefix,
    }


def generate_output_code(output_folder: Path, code_prefix: str) -> str:
    """
    Genereer unieke output code: {PREFIX}-{YYYYMMDD}-{seq}
    Scant bestaande bestanden voor volgende sequence nummer.
    """
    today = datetime.now().strftime('%Y%m%d')
    pattern = f"{code_prefix}-{today}-"
    
    # Zoek bestaande bestanden met zelfde prefix en datum
    existing_seqs = []
    if output_folder.exists():
        for f in output_folder.glob(f"*{pattern}*.md"):
            # Extract sequence nummer uit bestandsnaam
            match = re.search(rf'{pattern}(\d+)', f.name)
            if match:
                existing_seqs.append(int(match.group(1)))
    
    # Bepaal volgende sequence (start bij 01)
    next_seq = max(existing_seqs, default=0) + 1
    
    return f"{code_prefix}-{today}-{next_seq:02d}"


def call_llm_api(system_prompt: str, user_prompt: str, model: str = None) -> str:
    """
    Roep LLM API aan (OpenAI/Azure OpenAI).
    Configuratie via environment variables:
    - OPENAI_API_KEY: API key
    - OPENAI_MODEL: Model naam (default: gpt-4o)
    - AZURE_OPENAI_ENDPOINT: Azure endpoint (optioneel)
    - AZURE_OPENAI_API_VERSION: Azure API version (optioneel)
    """
    if not HAS_OPENAI:
        raise ImportError("openai package is vereist. Installeer met: pip install openai")
    
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable niet gezet")
    
    model = model or os.environ.get('OPENAI_MODEL', 'gpt-4o')
    azure_endpoint = os.environ.get('AZURE_OPENAI_ENDPOINT')
    
    if azure_endpoint:
        # Azure OpenAI
        api_version = os.environ.get('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
        client = openai.AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint
        )
    else:
        # Standard OpenAI
        client = openai.OpenAI(api_key=api_key)
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_tokens=4000
    )
    
    return response.choices[0].message.content


def write_audit_log(audit_path: Path, execution_id: str, agent: str, intent: str,
                    input_files: List[str], output_files: List[str], 
                    output_code: str, success: bool, error_msg: str = None):
    """Schrijf audit log bestand."""
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    content = f"""---
execution_id: {execution_id}
agent: {agent}
intent: {intent}
timestamp: {timestamp}
success: {success}
output_code: {output_code}
---

# Execution Audit Log

**Execution ID**: {execution_id}
**Agent**: {agent}
**Intent**: {intent}
**Timestamp**: {timestamp}
**Status**: {'SUCCESS' if success else 'FAILED'}

## Input Files
"""
    for f in input_files:
        content += f"- `{f}`\n"
    
    content += "\n## Output Files\n"
    for f in output_files:
        content += f"- `{f}`\n"
    
    if error_msg:
        content += f"\n## Error\n```\n{error_msg}\n```\n"
    
    audit_path.write_text(content, encoding='utf-8')


def execute_from_execution_file_main(args: argparse.Namespace) -> int:
    """
    Main functie voor execute-from-execution-file subcommand.
    
    Workflow:
    1. Lees execution-file en parse YAML frontmatter
    2. Bepaal agent-context en output-locaties
    3. Genereer unieke output code
    4. Roep LLM API aan met instructies
    5. Schrijf output bestanden weg
    6. Schrijf audit log
    """
    execution_file = Path(args.execution_file).resolve()
    
    if not execution_file.exists():
        print(f"ERROR: Execution file niet gevonden: {execution_file}")
        return 1
    
    # Bepaal workspace root
    workspace_root = Path(__file__).resolve().parent.parent.parent.parent.parent
    if not (workspace_root / "artefacten").exists():
        workspace_root = Path.cwd()
    
    print("=" * 80)
    print("EXECUTE FROM EXECUTION FILE")
    print("=" * 80)
    print(f"Execution file: {execution_file}")
    print()
    
    input_files = [str(execution_file)]
    output_files = []
    output_code = "UNKNOWN"
    
    try:
        # 1. Parse execution file
        print("[1/6] Parsing execution file...")
        metadata, instruction_content = parse_execution_file(execution_file)
        
        execution_id = metadata.get('execution_id', 'unknown')
        agent = metadata.get('agent', 'unknown')
        intent = metadata.get('intent', 'unknown')
        
        print(f"      Execution ID: {execution_id}")
        print(f"      Agent: {agent}")
        print(f"      Intent: {intent}")
        print()
        
        # 2. Bepaal output configuratie
        print("[2/6] Determining output configuration...")
        output_config = determine_output_config(metadata, workspace_root)
        output_folder = output_config['output_folder']
        code_prefix = output_config['code_prefix']
        
        print(f"      Output folder: {output_folder}")
        print(f"      Code prefix: {code_prefix}")
        print()
        
        # 3. Genereer output code
        print("[3/6] Generating output code...")
        output_code = generate_output_code(output_folder, code_prefix)
        print(f"      Output code: {output_code}")
        print()
        
        # 4. Bouw prompts en roep LLM aan
        print("[4/6] Calling LLM API...")
        
        system_prompt = f"""Je bent de agent {agent}, intent {intent}.
Volg de instructies exact zoals beschreven in het agent charter en contract.
Genereer output volgens het gespecificeerde formaat.
Gebruik de volgende output code: {output_code}
Datum: {datetime.now().strftime('%Y-%m-%d')}

BELANGRIJK:
- Volg het exacte output-formaat uit het contract
- Gebruik de gegeven output code ({output_code}) in het document
- Lever alleen de markdown content, geen extra uitleg"""
        
        user_prompt = instruction_content
        
        if args.dry_run:
            print("      [DRY-RUN] Zou LLM aanroepen met:")
            print(f"      System prompt: {len(system_prompt)} chars")
            print(f"      User prompt: {len(user_prompt)} chars")
            llm_response = f"[DRY-RUN] Output zou hier komen voor {output_code}"
        else:
            model = args.model if hasattr(args, 'model') else None
            llm_response = call_llm_api(system_prompt, user_prompt, model)
        
        print(f"      Response length: {len(llm_response)} chars")
        print()
        
        # 5. Schrijf output bestanden
        print("[5/6] Writing output files...")
        
        # Maak output folder aan
        output_folder.mkdir(parents=True, exist_ok=True)
        
        # Bepaal output bestandsnaam op basis van agent
        output_filename_templates = {
            'hypothese-vormer': f"hypothese-{output_code}.md",
            'concept-curator': f"concept-{output_code}.md",
            'thema-verwoorder': f"thema-{output_code}.md",
            'gedragsspecificator': f"gedrag-{output_code}.md",
        }
        output_filename = output_filename_templates.get(agent, f"output-{output_code}.md")
        output_path = output_folder / output_filename
        
        if not args.dry_run:
            output_path.write_text(llm_response, encoding='utf-8')
        
        output_files.append(str(output_path))
        print(f"      Output: {output_path}")
        print()
        
        # 6. Schrijf audit log
        print("[6/6] Writing audit log...")
        
        timestamp = datetime.now().strftime('%Y%m%d-%H%M')
        audit_filename = f"{agent}-{timestamp}.log.md"
        audit_path = workspace_root / "audit" / audit_filename
        
        if not args.dry_run:
            write_audit_log(
                audit_path, execution_id, agent, intent,
                input_files, output_files, output_code, 
                success=True
            )
        
        output_files.append(str(audit_path))
        print(f"      Audit log: {audit_path}")
        print()
        
        # Samenvatting
        print("=" * 80)
        print("EXECUTION COMPLETE")
        print("=" * 80)
        print(f"Execution ID:  {execution_id}")
        print(f"Output Code:   {output_code}")
        print(f"Output File:   {output_path}")
        print(f"Audit Log:     {audit_path}")
        print()
        
        if not args.dry_run:
            # Open output in VS Code
            subprocess.run(["code", str(output_path)], shell=True)
        
        return 0
        
    except ImportError as e:
        print(f"ERROR: {e}")
        return 1
    except ValueError as e:
        print(f"ERROR: {e}")
        return 1
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        
        # Schrijf fout naar audit log
        timestamp = datetime.now().strftime('%Y%m%d-%H%M')
        audit_filename = f"{metadata.get('agent', 'unknown')}-{timestamp}.log.md"
        audit_path = workspace_root / "audit" / audit_filename
        
        if not args.dry_run:
            write_audit_log(
                audit_path, metadata.get('execution_id', 'unknown'),
                metadata.get('agent', 'unknown'), metadata.get('intent', 'unknown'),
                input_files, output_files, output_code,
                success=False, error_msg=str(e)
            )
        
        return 1


# ==============================================================================
# SAVE-OUTPUT: Handmatige LLM output opslaan
# ==============================================================================

def save_output_main(args: argparse.Namespace) -> int:
    """
    Sla handmatig gegenereerde LLM output op.
    
    Workflow:
    1. Lees execution-file voor metadata (agent, intent, execution_id)
    2. Lees output van temp/output-pending.md of --from-file
    3. Genereer unieke output code
    4. Schrijf naar juiste output folder
    5. Schrijf audit log
    """
    execution_file = Path(args.execution_file).resolve()
    
    if not execution_file.exists():
        print(f"ERROR: Execution file niet gevonden: {execution_file}")
        return 1
    
    # Bepaal workspace root
    workspace_root = Path(__file__).resolve().parent.parent.parent.parent.parent
    if not (workspace_root / "artefacten").exists():
        workspace_root = Path.cwd()
    
    # Bepaal output source
    if args.from_file:
        output_source = Path(args.from_file).resolve()
    else:
        output_source = workspace_root / "temp" / "output-pending.md"
    
    if not output_source.exists():
        print(f"ERROR: Output bestand niet gevonden: {output_source}")
        print()
        print("Plak je LLM output in één van deze locaties:")
        print(f"  1. {workspace_root / 'temp' / 'output-pending.md'}")
        print(f"  2. Of gebruik: --from-file <pad>")
        return 1
    
    print("=" * 80)
    print("SAVE OUTPUT")
    print("=" * 80)
    print(f"Execution file: {execution_file}")
    print(f"Output source:  {output_source}")
    print()
    
    input_files = [str(execution_file), str(output_source)]
    output_files = []
    
    try:
        # 1. Parse execution file
        print("[1/5] Parsing execution file...")
        metadata, _ = parse_execution_file(execution_file)
        
        execution_id = metadata.get('execution_id', 'unknown')
        agent = metadata.get('agent', 'unknown')
        intent = metadata.get('intent', 'unknown')
        
        print(f"      Execution ID: {execution_id}")
        print(f"      Agent: {agent}")
        print(f"      Intent: {intent}")
        print()
        
        # 2. Lees output content
        print("[2/5] Reading output content...")
        output_content = output_source.read_text(encoding='utf-8')
        print(f"      Content length: {len(output_content)} chars")
        print()
        
        # 3. Bepaal output configuratie en genereer code
        print("[3/5] Determining output location...")
        output_config = determine_output_config(metadata, workspace_root)
        output_folder = output_config['output_folder']
        code_prefix = output_config['code_prefix']
        output_code = generate_output_code(output_folder, code_prefix)
        
        print(f"      Output folder: {output_folder}")
        print(f"      Output code: {output_code}")
        print()
        
        # 4. Schrijf output bestand
        print("[4/5] Writing output file...")
        output_folder.mkdir(parents=True, exist_ok=True)
        
        output_filename_templates = {
            'hypothese-vormer': f"hypothese-{output_code}.md",
            'concept-curator': f"concept-{output_code}.md",
            'thema-verwoorder': f"thema-{output_code}.md",
            'gedragsspecificator': f"gedrag-{output_code}.md",
        }
        output_filename = output_filename_templates.get(agent, f"output-{output_code}.md")
        output_path = output_folder / output_filename
        
        output_path.write_text(output_content, encoding='utf-8')
        output_files.append(str(output_path))
        print(f"      Saved: {output_path}")
        print()
        
        # 5. Schrijf audit log
        print("[5/5] Writing audit log...")
        timestamp = datetime.now().strftime('%Y%m%d-%H%M')
        audit_filename = f"{agent}-{timestamp}.log.md"
        audit_path = workspace_root / "audit" / audit_filename
        
        write_audit_log(
            audit_path, execution_id, agent, intent,
            input_files, output_files, output_code,
            success=True
        )
        output_files.append(str(audit_path))
        print(f"      Audit log: {audit_path}")
        print()
        
        # Cleanup: verwijder output-pending.md als dat de source was
        if not args.from_file and not args.keep_source:
            output_source.unlink()
            print(f"      Cleaned up: {output_source}")
            print()
        
        # Samenvatting
        print("=" * 80)
        print("OUTPUT SAVED")
        print("=" * 80)
        print(f"Execution ID:  {execution_id}")
        print(f"Output Code:   {output_code}")
        print(f"Output File:   {output_path}")
        print(f"Audit Log:     {audit_path}")
        print()
        
        # Open output in VS Code
        subprocess.run(["code", str(output_path)], shell=True)
        
        return 0
        
    except Exception as e:
        print(f"ERROR: {e}")
        return 1


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Runner voor agent: agent-engineer",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="intent", required=True, help="Beschikbare intents")

    # realiseer-agent-prompts
    p_prompts = subparsers.add_parser("realiseer-agent-prompts", 
                                       help="Genereer .prompt.md bestanden uit agent-contracten")
    p_prompts.add_argument("--agent-naam", required=True, help="Agent naam")
    p_prompts.add_argument("--intent", required=False, help="Specifieke intent (optioneel)")

    # realiseer-agent-runner
    p_runner = subparsers.add_parser("realiseer-agent-runner", 
                                      help="Genereer runner.py voor een agent")
    p_runner.add_argument("--agent-naam", required=True, help="Agent naam")
    p_runner.add_argument("--contract-folder", required=False, help="Contract folder pad")
    p_runner.add_argument("--runner-output-folder", required=False, help="Output folder voor runner")
    p_runner.add_argument("--overwrite-existing", action="store_true", help="Overschrijf bestaande runner")

    # realiseer-agent-taskconfiguratie
    p_tasks = subparsers.add_parser("realiseer-agent-taskconfiguratie", 
                                     help="Genereer tasks.json configuratie")
    p_tasks.add_argument("--agent-naam", required=True, help="Agent naam")

    # pipeline
    p_pipeline = subparsers.add_parser("pipeline", 
                                        help="Voer alle intents sequentieel uit voor een agent")
    p_pipeline.add_argument("agent", type=str, nargs='?', help="Agent naam (verplicht tenzij --all)")
    p_pipeline.add_argument("--all", action="store_true", help="Verwerk alle agents")
    p_pipeline.add_argument("--dry-run", action="store_true", help="Toon wat uitgevoerd zou worden")
    p_pipeline.add_argument("--skip-bootstrap", action="store_true", help="Skip canon bootstrap")

    # execute-from-execution-file
    p_exec = subparsers.add_parser("execute-from-execution-file",
                                    help="Voer execution-file uit via LLM API")
    p_exec.add_argument("execution_file", type=str, help="Pad naar execution-file (.md)")
    p_exec.add_argument("--model", type=str, help="LLM model (default: gpt-4o of OPENAI_MODEL env var)")
    p_exec.add_argument("--dry-run", action="store_true", help="Toon wat uitgevoerd zou worden zonder LLM aan te roepen")

    # save-output
    p_save = subparsers.add_parser("save-output",
                                    help="Sla handmatig gegenereerde LLM output op")
    p_save.add_argument("execution_file", type=str, help="Pad naar execution-file (.md) voor metadata")
    p_save.add_argument("--from-file", type=str, help="Pad naar bestand met output (default: temp/output-pending.md)")
    p_save.add_argument("--keep-source", action="store_true", help="Verwijder source bestand niet na opslaan")

    args = parser.parse_args()

    if args.intent == "pipeline":
        if not args.agent and not args.all:
            parser.error("Agent naam is verplicht (of gebruik --all)")
        if args.agent and args.all:
            parser.error("Gebruik óf agent naam óf --all, niet beide")
        sys.exit(pipeline_main(args))
    elif args.intent == "execute-from-execution-file":
        sys.exit(execute_from_execution_file_main(args))
    elif args.intent == "save-output":
        sys.exit(save_output_main(args))
    else:
        # Standaard intents: roep ecosysteem-coordinator aan via run_generate_instructions
        params_dict = vars(args).copy()
        del params_dict['intent']
        
        # Converteer argument namen naar parameter namen (- naar _)
        formatted_params = {k.replace('-', '_'): v for k, v in params_dict.items() if v is not None}
        
        run_generate_instructions("agent-engineer", args.intent, formatted_params)


if __name__ == "__main__":
    main()
