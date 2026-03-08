#!/usr/bin/env python3
"""
Runner voor agent: agent-engineer

Zuivere intents voor agent lifecycle engineering:
- realiseer-agent-prompts: Genereer .prompt.md bestanden uit agent-contracten
- realiseer-agent-runner: Genereer runner.py voor een agent
- realiseer-agent-taskconfiguratie: Genereer tasks.json configuratie

Pipeline orchestratie:
- pipeline: Voer alle 3 intents sequentieel uit voor een agent

Architectuur: One Agent, One Runner principe.
Cross-cutting functionaliteit (generate-instructions, merge-tasks) is gemigreerd
naar ecosysteem-coordinator.runner.py conform de doctrine.
"""
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import argparse
import hashlib
import io
import os
import subprocess
import sys


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

    args = parser.parse_args()

    if args.intent == "pipeline":
        if not args.agent and not args.all:
            parser.error("Agent naam is verplicht (of gebruik --all)")
        if args.agent and args.all:
            parser.error("Gebruik óf agent naam óf --all, niet beide")
        sys.exit(pipeline_main(args))
    else:
        # Standaard intents: roep ecosysteem-coordinator aan via run_generate_instructions
        params_dict = vars(args).copy()
        del params_dict['intent']
        
        # Converteer argument namen naar parameter namen (- naar _)
        formatted_params = {k.replace('-', '_'): v for k, v in params_dict.items() if v is not None}
        
        run_generate_instructions("agent-engineer", args.intent, formatted_params)


if __name__ == "__main__":
    main()
