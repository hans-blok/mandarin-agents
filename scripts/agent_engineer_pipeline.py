#!/usr/bin/env python3
"""
agent_engineer_pipeline.py - Agent-Engineer Pipeline voor Prompts en Tasks

Deze pipeline voert voor een specifieke agent (of alle agents) automatisch de volgende twee intents uit:
1. realiseer-agent-prompts (genereert .prompt.md bestanden)
2. realiseer-agent-taskconfiguratie (genereert tasks.json bestanden)

De pipeline:
- Neemt agent-naam als verplichte input parameter
- Voert beide intents sequentieel uit voor die agent
- Logt resultaten voor traceerbaarheid
- Gebruikt agent-contracten als input voor de generatie

Gebruik:
    python scripts/agent_engineer_pipeline.py AGENT_NAAM [opties]
    
Voorbeelden:
    # Specifieke agent verwerken
    python scripts/agent_engineer_pipeline.py capability-architect
    
    # Alle agents verwerken
    python scripts/agent_engineer_pipeline.py --all
    
    # Dry run (toon wat uitgevoerd wordt zonder executie)
    python scripts/agent_engineer_pipeline.py capability-architect --dry-run
    
    # Skip bootstrap (snellere iteratie, alleen voor ontwikkeling)
    python scripts/agent_engineer_pipeline.py agent-curator --skip-bootstrap

Output:
    - Console log met voortgang en status
    - Execution files in agent-execution/ folder (indien gewenst)
    - Gegenereerde prompts in artefacten/{vs}/{vs}.{fase}.{agent}/prompts/
    - Gegenereerde tasks in artefacten/{vs}/{vs}.{fase}.{agent}/tasks/
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime
import hashlib
import io


def find_all_agents():
    """
    Ontdek alle agents in de workspace met agent-contracten.
    
    Returns:
        List[dict]: Lijst met agent info: {'naam': str, 'path': Path, 'contracten': List[Path]}
    """
    artefacten = Path("artefacten")
    if not artefacten.exists():
        print(f"ERROR: artefacten folder niet gevonden in workspace root")
        return []
    
    agents = []
    
    # Zoek alle folders met 'agent-contracten' subfolder
    for contract_dir in artefacten.rglob("agent-contracten"):
        if not contract_dir.is_dir():
            continue
            
        agent_folder = contract_dir.parent
        
        # Extract agent naam uit de folder naam
        # Format: {vs}.{fase}.{agent-naam}
        folder_name = agent_folder.name
        parts = folder_name.split('.')
        
        if len(parts) >= 3:
            agent_naam = '.'.join(parts[2:])  # Alles na vs.fase
        else:
            # Fallback: gebruik de hele folder naam
            agent_naam = folder_name
        
        # Vind alle agent-contract bestanden
        contracten = list(contract_dir.glob("*.agent.md"))
        
        if contracten:
            agents.append({
                'naam': agent_naam,
                'path': agent_folder,
                'contract_dir': contract_dir,
                'contracten': contracten
            })
    
    return agents


def generate_execution_hash(agent_naam, intent):
    """Genereer unieke hash voor execution file naam."""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    hash_input = timestamp + agent_naam
    md5_hash = hashlib.md5(hash_input.encode()).hexdigest()[:4]
    return md5_hash


def execute_agent_engineer(agent_naam, intent, skip_bootstrap=False, dry_run=False, save_execution=False):
    """
    Voer agent-engineer uit voor specifieke intent.
    
    Args:
        agent_naam: Naam van de agent
        intent: Intent naam (realiseer-agent-prompts of realiseer-agent-taskconfiguratie)
        skip_bootstrap: Skip canon bootstrap (sneller, alleen voor development)
        dry_run: Toon alleen wat uitgevoerd zou worden
        save_execution: Sla execution file op
        
    Returns:
        bool: True indien succesvol, False indien gefaald
    """
    script = Path("scripts/agent-engineer.runner.py")
    
    if not script.exists():
        print(f"ERROR: {script.name} niet gevonden op {script}")
        return False
    
    # Bouw command
    cmd = [
        sys.executable,
        str(script),
        agent_naam,
        "--intent", intent
    ]
    
    if dry_run:
        print(f"  [DRY-RUN] Zou uitvoeren: {' '.join(cmd)}")
        return True
    
    # Voer uit
    try:
        print(f"  Executing: agent-engineer {intent} for {agent_naam}")
        
        # Zet UTF-8 encoding voor Python subprocess (Windows fix)
        env = dict(os.environ)
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, 
                              encoding='utf-8', env=env)
        
        # Toon relevante output
        if result.stdout:
            # Filter alleen belangrijke regels
            for line in result.stdout.split('\n'):
                if any(keyword in line.lower() for keyword in ['success', 'error', 'warning', 'created', 'updated']):
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
        import traceback
        traceback.print_exc()
        return False


class TeeOutput:
    """Write to both console and log file simultaneously."""
    def __init__(self, log_file, original_stdout):
        self.log_file = log_file
        self.original_stdout = original_stdout
        self.buffer = io.StringIO()
    
    def write(self, text):
        self.original_stdout.write(text)
        self.log_file.write(text)
        self.log_file.flush()
    
    def flush(self):
        self.original_stdout.flush()
        self.log_file.flush()


def run_pipeline(target_agent=None, dry_run=False, skip_bootstrap=False, save_execution=False):
    """
    Voer de volledige pipeline uit.
    
    Args:
        target_agent: Optionele specifieke agent naam (None = alle agents)
        dry_run: Dry run mode
        skip_bootstrap: Skip canon bootstrap
        save_execution: Sla execution files op
        
    Returns:
        int: Exit code (0 = success, 1 = failure)
    """
    # Maak logs folder aan indien nodig
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Genereer log bestandsnaam met timestamp
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    log_filename = f"{timestamp}.agent-engineer-pipeline.log"
    log_path = logs_dir / log_filename
    
    # Open log file en redirect stdout
    original_stdout = sys.stdout
    log_file = open(log_path, 'w', encoding='utf-8')
    sys.stdout = TeeOutput(log_file, original_stdout)
    
    try:
        print("=" * 80)
        print("Agent-Engineer Pipeline: Realiseer Prompts & Tasks")
        print("=" * 80)
        print(f"Log file: {log_path}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Ontdek agents
        print("📋 Discovering agents...")
        agents = find_all_agents()
        
        if not agents:
            print("ERROR: Geen agents met agent-contracten gevonden")
            return 1
        
        # Filter indien specifieke agent gevraagd
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
            "realiseer-agent-taskconfiguratie"
        ]
        
        # Statistieken
        stats = {
            'total': len(agents) * len(intents),
            'success': 0,
            'failed': 0
        }
        
        # Voer uit voor elke agent
        for i, agent in enumerate(agents, 1):
            print(f"[{i}/{len(agents)}] Processing: {agent['naam']}")
            print(f"          Location: {agent['path']}")
            
            agent_success = True
            
            for intent in intents:
                success = execute_agent_engineer(
                    agent['naam'],
                    intent,
                    skip_bootstrap=skip_bootstrap,
                    dry_run=dry_run,
                    save_execution=save_execution
                )
                
                if success:
                    stats['success'] += 1
                else:
                    stats['failed'] += 1
                    agent_success = False
            
            # Status voor deze agent
            status = "✓ SUCCESS" if agent_success else "✗ FAILED"
            print(f"          Status: {status}")
            print()
    
        # Samenvatting
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
            print(f"⚠️  {stats['failed']} operation(s) failed. Check logs above.")
            return 1
    
    finally:
        # Restore stdout en sluit log file
        sys.stdout = original_stdout
        log_file.close()
        print(f"\nLog saved to: {log_path}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Agent-Engineer Pipeline: Genereer prompts en tasks voor een agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Voorbeelden:
  # Specifieke agent (verplicht)
  python agent_engineer_pipeline.py capability-architect
  
  # Alle agents verwerken
  python agent_engineer_pipeline.py --all
  
  # Dry run
  python agent_engineer_pipeline.py capability-architect --dry-run
  
  # Met execution files
  python agent_engineer_pipeline.py agent-curator --save-execution
        """
    )
    
    parser.add_argument(
        "agent",
        type=str,
        nargs='?',
        help="Naam van de agent om te verwerken (verplicht, tenzij --all gebruikt wordt)"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Verwerk alle agents in de workspace"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Toon wat uitgevoerd zou worden zonder daadwerkelijke executie"
    )
    
    parser.add_argument(
        "--skip-bootstrap",
        action="store_true",
        help="Skip canon bootstrap (sneller, alleen voor development)"
    )
    
    parser.add_argument(
        "--save-execution",
        action="store_true",
        help="Sla execution files op in agent-execution/ folder"
    )
    
    args = parser.parse_args()
    
    # Validatie: ofwel agent naam, ofwel --all
    if not args.agent and not args.all:
        parser.error("Agent naam is verplicht (of gebruik --all voor alle agents)")
    
    if args.agent and args.all:
        parser.error("Gebruik óf een agent naam óf --all, niet beide")
    
    # Bepaal target agent
    target_agent = None if args.all else args.agent
    
    # Voer pipeline uit
    exit_code = run_pipeline(
        target_agent=target_agent,
        dry_run=args.dry_run,
        skip_bootstrap=args.skip_bootstrap,
        save_execution=args.save_execution
    )
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
