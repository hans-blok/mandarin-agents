#!/usr/bin/env python3
"""
run_prompt.py - Prompt Runner met Verplichte Canon Bootstrap

Dit script voert een agent-prompt uit met geautomatiseerde canon-consultatie.
Het zorgt ervoor dat 'stap 0' (canon raadplegen) nooit wordt vergeten.

Architectuur Principes:
    - SOLID Interface Segregation: Prompts bevatten minimale metadata
    - Single Source of Truth: beleid-workspace.md bevat canon URL en grondslagen-patronen
    - Separation of Concerns: Splitsing tussen proces (scripts) en regels (canon/beleid)
    - Convention over Configuration: beleid-workspace.md in workspace root (hardcoded)

Workspace Configuratie:
    Het script leest automatisch 'beleid-workspace.md' uit de workspace root voor:
    - canon_github_url: URL naar de mandarin-canon repository
    - grondslagen: Map van value_stream -> grondslagen-patronen
    
    Dit ontkoppelt configuratie van prompt-bestanden en zorgt voor centrale governance.

Logging:
    Het script logt automatisch alle gegenereerde instructies naar:
    - audit/agent-instructions.log.md (append-only format, git-tracked)
    
    Elk log entry bevat:
    - Timestamp (ISO 8601, CET/CEST)
    - Agent metadata (agent, intent, value_stream)
    - Parameters
    - Volledige samengestelde instructies
    
    Dit zorgt voor traceerbaarheid en monitoring van ecosysteem-activiteit.

Gebruik:
    python scripts/run_prompt.py <prompt-file> [-p key=value] [--input-file input.md]

Voorbeeld:
    python scripts/run_prompt.py .github/prompts/mandarin.agent-curator.bepaal-agent-boundary.prompt.md \
        -p agent_naam=agent-smeder \
        -p value_stream_fase=aeo.02 \
        --input-file input/boundary-beschrijving.md

Prompt Bestand Structuur (minimaal):
    ---
    agent: mandarin.agent-curator
    intent: bepaal-agent-boundary
    value_stream: aeo
    
    bootstrap:
      script: scripts/bootstrap_canon_consult.py
    ---
    
    # Agent instructies hier (optioneel, meestal in .agent.md)
"""

import argparse
import sys
import subprocess
import re
from pathlib import Path
from datetime import datetime

try:
    import frontmatter
except ImportError:
    print("ERROR: python-frontmatter is niet geïnstalleerd.")
    print("Installeer met: pip install python-frontmatter")
    sys.exit(1)


def parse_arguments():
    """Parse command-line argumenten."""
    parser = argparse.ArgumentParser(
        description="Voer een agent-prompt uit met verplichte canon-consultatie.",
        epilog="""Gebruik:
  Methode 1 (nieuw): python run_prompt.py --agent <agent-naam> --intent <intent>
  Methode 2 (klassiek): python run_prompt.py <prompt-file-pad> [-p key=value]

Voorbeeld:
  python run_prompt.py --agent capability-architect --intent leg-vast-agent-prompt
  python run_prompt.py .github/prompts/mandarin.agent-smeder.leg-vast-agent-prompt.prompt.md -p agent=capability-architect
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "prompt_file",
        type=str,
        nargs='?',  # Maak optioneel
        help="Pad naar het prompt-bestand (optioneel indien --agent en --intent gegeven)"
    )
    parser.add_argument(
        "--agent",
        type=str,
        help="Agent naam voor auto-discovery (bijv. 'capability-architect', 'engineer-steward')"
    )
    parser.add_argument(
        "--intent",
        type=str,
        help="Intent naam voor auto-discovery (bijv. 'leg-vast-agent-prompt', 'schrijf-script')"
    )
    parser.add_argument(
        "-p", "--param",
        action="append",
        dest="params",
        default=[],
        help="Parameter in het formaat key=value (kan meerdere keren gebruikt worden)"
    )
    parser.add_argument(
        "--input-file",
        type=str,
        default="input/input.md",
        help="Pad naar het input-bestand met meerregelige tekst (default: input/input.md)"
    )
    parser.add_argument(
        "--method",
        type=str,
        default="manual",
        choices=["manual", "runner", "pipeline"],
        help="Methode van uitvoering (default: manual)"
    )
    
    args = parser.parse_args()
    
    # Validatie: ofwel prompt_file, ofwel agent+intent
    if not args.prompt_file and not (args.agent and args.intent):
        parser.error("Geef ofwel een prompt_file, ofwel --agent en --intent")
    
    if args.prompt_file and (args.agent or args.intent):
        parser.error("Gebruik ofwel prompt_file, ofwel --agent/--intent, niet beide")
    
    return args


def load_prompt_file(prompt_path):
    """Laad prompt-bestand en parse YAML frontmatter."""
    prompt_file = Path(prompt_path)
    
    if not prompt_file.exists():
        print(f"ERROR: Prompt-bestand niet gevonden: {prompt_path}")
        sys.exit(1)
    
    with open(prompt_file, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
    
    return post.metadata, post.content


def load_input_file(input_path):
    """Laad de inhoud van het input-bestand."""
    input_file = Path(input_path)
    
    if not input_file.exists():
        print(f"WARNING: Input-bestand niet gevonden: {input_path}")
        print("Placeholder [INPUT_CONTENT] zal niet worden vervangen.")
        return ""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        return f.read()


def parse_params(param_list):
    """Parse parameter lijst naar dictionary."""
    params = {}
    for param in param_list:
        if '=' not in param:
            print(f"WARNING: Ongeldige parameter (verwacht key=value): {param}")
            continue
        key, value = param.split('=', 1)
        params[key.strip()] = value.strip()
    return params


def find_boundary_file(agent_naam):
    """Zoek boundary file voor gegeven agent naam.
    
    Zoekt recursief in artefacten/ naar agent-boundary-{agent}.md of 
    {agent}.boundary.md patronen.
    
    Returns:
        Path object of None indien niet gevonden
    """
    artefacten = Path("artefacten")
    if not artefacten.exists():
        return None
    
    # Zoekpatronen
    patterns = [
        f"**/agent-boundary-{agent_naam}.md",
        f"**/{agent_naam}.boundary.md",
        f"**/agent-boundary*.md"  # Fallback: kijk in agent folders
    ]
    
    for pattern in patterns:
        matches = list(artefacten.glob(pattern))
        for match in matches:
            # Check of agent naam in pad of bestandsnaam voorkomt
            if agent_naam in str(match):
                return match
    
    return None


def find_prompt_file(intent, agent=None):
    """Zoek prompt file in .github/prompts/ voor gegeven intent.
    
    Zoekt naar mandarin.*.{intent}.prompt.md patronen.
    Als agent is opgegeven, zoekt specifiek naar mandarin.{agent}.{intent}.prompt.md
    
    Returns:
        Path object of None indien niet gevonden
    """
    prompts_dir = Path(".github/prompts")
    if not prompts_dir.exists():
        return None
    
    # Als agent specifiek is opgegeven, zoek exact die combinatie
    if agent:
        specific_pattern = f"mandarin.{agent}.{intent}.prompt.md"
        specific_file = prompts_dir / specific_pattern
        if specific_file.exists():
            return specific_file
            
        # Fallback: probeer ook patterns waar de agent naam in zit (voor variaties)
        pattern = f"*{agent}*.{intent}.prompt.md"
        matches = list(prompts_dir.glob(pattern))
        if matches:
            return matches[0]

    # Generieke zoektocht (fallback of als geen agent is opgegeven)
    pattern = f"*.{intent}.prompt.md"
    matches = list(prompts_dir.glob(pattern))
    
    if matches:
        # Als er meerdere matches zijn, geef voorkeur aan mandarin.agent-smeder.*
        for match in matches:
            if "agent-smeder" in match.name:
                return match
        # Anders pak de eerste
        return matches[0]
    
    return None


def load_workspace_config():
    """Laad workspace configuratie uit beleid-workspace.md."""
    workspace_file = Path('beleid-workspace.md')
    
    if not workspace_file.exists():
        return {}
    
    try:
        with open(workspace_file, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        return post.metadata
    except Exception as e:
        print(f"WARNING: Kan beleid-workspace.md niet lezen: {e}")
        return {}


def run_bootstrap(metadata, prompt_file, method, params, workspace_config):
    """Voer bootstrap_canon_consult.py uit."""
    bootstrap = metadata.get('bootstrap', {})
    
    if not bootstrap:
        print("WARNING: Geen 'bootstrap' sectie gevonden in prompt-bestand.")
        print("Canon consultatie wordt overgeslagen.")
        return False
    
    script = bootstrap.get('script', 'scripts/bootstrap_canon_consult.py')
    
    # Bepaal value stream fase (uit parameters of uit prompt metadata)
    value_stream_fase = params.get('value_stream_fase', metadata.get('value_stream_fase', 'unknown'))
    # Extraheer alleen de value stream code (bijv. 'aeo' uit 'aeo.02') voor grondslagen lookup
    value_stream = value_stream_fase.split('.')[0] if '.' in value_stream_fase else value_stream_fase
    
    # Gebruik grondslagen uit beleid-workspace.md op basis van value stream, met fallback naar prompt metadata
    grondslagen_map = workspace_config.get('grondslagen', {})
    grondslagen = grondslagen_map.get(value_stream, bootstrap.get('grondslagen', ''))
    
    # Gebruik canon URL uit beleid-workspace.md, met fallback naar prompt metadata
    canon_github_url = workspace_config.get('canon_github_url') or bootstrap.get('canon-github-url', 'https://github.com/minvws/mandarin-canon')
    
    # Bepaal agent-naam (uit parameters of uit prompt metadata)
    agent = params.get('agent_naam', metadata.get('agent', 'unknown-agent'))
    
    # Bepaal intent (uit prompt metadata of bestandsnaam)
    intent = metadata.get('intent', '')
    if not intent:
        # Probeer intent uit bestandsnaam te halen (bijv. 'bepaal-agent-boundary' uit 'mandarin.agent-curator.bepaal-agent-boundary.prompt.md')
        match = re.search(r'\.([a-z\-]+)\.prompt\.md$', str(prompt_file))
        if match:
            intent = match.group(1)
    
    # Bouw het commando
    cmd = [
        'python',
        script,
        '--agent', agent,
        '--value-stream', value_stream,  # Dit is de base code (aeo) voor grondslagen lookup
        '--workspace-file', str(prompt_file),
        '--intent', intent,
        '--method', method,
        '--grondslagen', grondslagen,
        '--canon-github-url', canon_github_url
    ]
    
    print("=" * 80)
    print("STAP 0: CANON CONSULTATIE (VERPLICHT)")
    print("=" * 80)
    print(f"Uitvoeren: {' '.join(cmd)}")
    print()
    
    # Voer het bootstrap script uit
    result = subprocess.run(cmd, capture_output=False, text=True)
    
    if result.returncode != 0:
        print()
        print("ERROR: Bootstrap script mislukt. Uitvoering afgebroken.")
        sys.exit(1)
    
    print()
    print("=" * 80)
    print("✓ Bootstrap succesvol voltooid")
    print("=" * 80)
    print()
    
    return True


def load_agent_instructions(prompt_file, metadata, params):
    """Laad agent-instructies uit .agent.md bestand.
    
    Zoekt eerst in de uitvoerende agent's folder (uit metadata), dan in doel-agent folder (params), dan prompt-folder.
    """
    # Extract agent-naam uit metadata (bijv. 'mandarin.agent-curator' -> 'agent-curator')
    agent_full = metadata.get('agent', '')
    agent_naam = agent_full.split('.')[-1] if '.' in agent_full else agent_full
    
    intent = metadata.get('intent', '')
    
    if not (agent_naam and intent):
        return None
    
    agent_file_name = f"{agent_naam}.{intent}.agent.md"
    
    # Strategie 1: Zoek in uitvoerende agent's folder (auto-discover in artefacten/**)
    artefacten_path = Path("artefacten")
    if artefacten_path.exists():
        # Zoek naar folders die eindigen op de uitvoerende agent naam
        for agent_folder in artefacten_path.rglob(f"*.{agent_naam}"):
            if agent_folder.is_dir():
                # Check in agent-contracten subfolder
                agent_contracten_folder = agent_folder / "agent-contracten"
                agent_file = agent_contracten_folder / agent_file_name
                if agent_file.exists():
                    print(f"✓ Agent-instructies geladen: {agent_file}")
                    with open(agent_file, 'r', encoding='utf-8') as f:
                        return f.read()
                
                # Check in agent folder root (oude conventie)
                agent_file = agent_folder / agent_file_name
                if agent_file.exists():
                    print(f"✓ Agent-instructies geladen: {agent_file}")
                    with open(agent_file, 'r', encoding='utf-8') as f:
                        return f.read()
    
    # Strategie 2: Zoek in doel-agent folder (gebaseerd op vs, fase, agent uit params)
    vs = params.get('vs', params.get('value_stream', ''))
    fase = params.get('fase', '')
    agent = params.get('agent', params.get('agent_naam', ''))
    
    if vs and fase and agent:
        agent_folder = Path(f"artefacten/{vs}/{vs}.{fase}.{agent}")
        agent_contracten_folder = agent_folder / "agent-contracten"
        
        # Check in agent-contracten subfolder
        agent_file = agent_contracten_folder / agent_file_name
        if agent_file.exists():
            print(f"✓ Agent-instructies geladen: {agent_file}")
            with open(agent_file, 'r', encoding='utf-8') as f:
                return f.read()
        
        # Check in agent folder root (oude conventie)
        agent_file = agent_folder / agent_file_name
        if agent_file.exists():
            print(f"✓ Agent-instructies geladen: {agent_file}")
            with open(agent_file, 'r', encoding='utf-8') as f:
                return f.read()
    
    # Strategie 3: Fallback - zoek in prompt folder (klassieke methode)
    prompt_path = Path(prompt_file)
    prompt_dir = prompt_path.parent
    agent_file = prompt_dir / agent_file_name
    
    if agent_file.exists():
        print(f"✓ Agent-instructies geladen: {agent_file}")
        with open(agent_file, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        print(f"INFO: Agent-instructies niet gevonden: {agent_file_name}")
    
    return None


def load_charter(prompt_file, metadata, params):
    """Laad charter uit conventie: {agent-naam}.charter.md.
    
    Zoekt eerst in de uitvoerende agent's folder (uit metadata), dan in doel-agent folder (params), dan prompt-folder.
    """
    # Extract agent-naam uit metadata (bijv. 'mandarin.agent-curator' -> 'agent-curator')
    agent_full = metadata.get('agent', '')
    agent_naam = agent_full.split('.')[-1] if '.' in agent_full else agent_full
    
    if not agent_naam:
        print("INFO: Geen agent-naam gevonden in metadata, charter overgeslagen.")
        return None
    
    charter_file_name = f"{agent_naam}.charter.md"
    
    # Strategie 1: Zoek in uitvoerende agent's folder (auto-discover in artefacten/**)
    artefacten_path = Path("artefacten")
    if artefacten_path.exists():
        # Zoek naar folders die eindigen op de uitvoerende agent naam
        for agent_folder in artefacten_path.rglob(f"*.{agent_naam}"):
            if agent_folder.is_dir():
                charter_file = agent_folder / charter_file_name
                if charter_file.exists():
                    print(f"✓ Charter geladen: {charter_file}")
                    with open(charter_file, 'r', encoding='utf-8') as f:
                        return f.read()
    
    # Strategie 2: Zoek in doel-agent folder (gebaseerd op vs, fase, agent uit params)
    vs = params.get('vs', params.get('value_stream', ''))
    fase = params.get('fase', '')
    agent = params.get('agent', params.get('agent_naam', ''))
    
    if vs and fase and agent:
        agent_folder = Path(f"artefacten/{vs}/{vs}.{fase}.{agent}")
        charter_file = agent_folder / charter_file_name
        
        if charter_file.exists():
            print(f"✓ Charter geladen: {charter_file}")
            with open(charter_file, 'r', encoding='utf-8') as f:
                return f.read()
    
    # Strategie 3: Fallback - zoek in prompt folder (klassieke methode)
    prompt_path = Path(prompt_file)
    prompt_dir = prompt_path.parent
    charter_file = prompt_dir / charter_file_name
    
    if charter_file.exists():
        print(f"✓ Charter geladen: {charter_file}")
        with open(charter_file, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        print(f"INFO: Charter niet gevonden (optioneel): {charter_file_name}")
    
    return None


def load_and_process_input_files(metadata, params):
    """Laad input_files uit metadata, vervang placeholders, laad bestanden.
    
    Extraheert ook value_stream en value_stream_fase uit boundary_file YAML indien aanwezig.
    
    Returns:
        tuple: (loaded_content, extracted_params)
            - loaded_content: dict met key = uppercase bestandsnaam, value = inhoud
            - extracted_params: dict met value_stream, value_stream_fase uit boundary
    """
    input_files = metadata.get('input_files', {})
    loaded_content = {}
    extracted_params = {}
    
    if not input_files:
        return loaded_content, extracted_params
    
    print("[Info] Verwerk input_files uit prompt metadata...")
    
    for key, path_template in input_files.items():
        # Vervang {vs}, {fase}, {agent}, {intent} placeholders
        # Fallback naar params indien niet expliciet gegeven
        path = path_template.format(
            vs=params.get('vs', params.get('value_stream', '')),
            fase=params.get('fase', ''),
            agent=params.get('agent', params.get('agent_naam', '')),
            intent=params.get('intent', '')
        )
        
        # Als path nog steeds placeholders bevat, gebruik command-line override
        if key in params:
            path = params[key]
        
        file_path = Path(path)
        
        # Laad bestand indien bestaat
        if file_path.exists():
            if file_path.is_file():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Maak placeholder: BOUNDARY_FILE, TEMPLATE_FILE, etc.
                    placeholder_key = key.upper()
                    loaded_content[placeholder_key] = content
                    print(f"  ✓ Geladen: {key} -> {path}")
                    
                    # Extraheer metadata uit boundary_file YAML frontmatter
                    if key == 'boundary_file':
                        try:
                            boundary_meta = frontmatter.loads(content)
                            if boundary_meta.metadata:
                                # Extraheer value_stream en value_stream_fase uit boundary
                                if 'value_stream' in boundary_meta.metadata:
                                    extracted_params['vs'] = boundary_meta.metadata['value_stream']
                                    extracted_params['value_stream'] = boundary_meta.metadata['value_stream']
                                if 'value_stream_fase' in boundary_meta.metadata:
                                    extracted_params['value_stream_fase'] = boundary_meta.metadata['value_stream_fase']
                                    # Ook fase apart extraheren (bijv. '02' uit 'aeo.02')
                                    fase_parts = boundary_meta.metadata['value_stream_fase'].split('.')
                                    if len(fase_parts) == 2:
                                        extracted_params['fase'] = fase_parts[1]
                                if 'agent' in boundary_meta.metadata:
                                    extracted_params['agent'] = boundary_meta.metadata['agent']
                                    extracted_params['agent_naam'] = boundary_meta.metadata['agent']
                                print(f"  ✓ Metadata geëxtraheerd uit boundary: {', '.join(extracted_params.keys())}")
                        except Exception as e:
                            print(f"  ⚠ Kan boundary metadata niet parsen: {e}")
            else:
                print(f"  ⚠ Folder: {key} -> {path} (wordt niet ingeladen, alleen pad beschikbaar)")
                # Voor folders: maak placeholder beschikbaar met pad
                loaded_content[key.upper()] = str(file_path)
        else:
            print(f"  ✗ Niet gevonden: {key} -> {path}")
    
    if loaded_content:
        print()
    
    return loaded_content, extracted_params


def replace_placeholders(content, params, input_content, input_files_content=None):
    """Vervang placeholders in de prompt content."""
    # Vervang [INPUT_CONTENT] met de inhoud van het input-bestand
    content = content.replace('[INPUT_CONTENT]', input_content)
    
    # Vervang [BOUNDARY_FILE], [TEMPLATE_FILE], etc. met geladen bestandsinhoud
    if input_files_content:
        for key, file_content in input_files_content.items():
            placeholder = f'[{key}]'
            content = content.replace(placeholder, file_content)
    
    # Vervang [KEY] placeholders met waarden uit params
    # Ondersteunt zowel [key] als [KEY] (case-insensitive)
    for key, value in params.items():
        # Vervang [key] en [KEY]
        content = re.sub(rf'\[{key}\]', value, content, flags=re.IGNORECASE)
    
    return content


def assemble_full_instructions(metadata, prompt_content, prompt_file, params, input_content, input_files_content):
    """Stel volledige agent-instructies samen uit alle bronnen."""
    parts = []
    
    # 1. Charter (afgeleid uit conventie)
    charter_content = load_charter(prompt_file, metadata, params)
    if charter_content:
        parts.append("# Agent Charter\n\n")
        parts.append(charter_content)
        parts.append("\n\n---\n\n")
    
    # 2. Agent-instructies uit .agent.md (indien beschikbaar)
    agent_instructions = load_agent_instructions(prompt_file, metadata, params)
    if agent_instructions:
        parts.append(agent_instructions)
    elif prompt_content.strip():
        # Fallback: gebruik prompt body als die niet leeg is
        parts.append(prompt_content)
    
    # 3. Voeg alles samen en vervang placeholders
    combined = ''.join(parts)
    return replace_placeholders(combined, params, input_content, input_files_content)
    
    # 3. Voeg alles samen en vervang placeholders
    combined = ''.join(parts)
    return replace_placeholders(combined, params, input_content)


def log_agent_instructions(metadata, params, final_prompt, prompt_file):
    """Log de gegenereerde agent-instructies naar audit/agent-instructions.log.md."""
    log_file = Path('audit/agent-instructions.log.md')
    
    # Maak audit folder aan als die niet bestaat
    log_file.parent.mkdir(exist_ok=True)
    
    # Als log bestand niet bestaat, maak header aan
    if not log_file.exists():
        header = """# Agent Instructions Log

Dit logbestand registreert alle gegenereerde agent-instructies door run_prompt.py.
Elk entry bevat metadata, parameters en de volledige samengestelde instructies.

**Formaat**: Markdown  
**Locatie**: `audit/agent-instructions.log.md`  
**Update methode**: Append-only (entries worden toegevoegd met `---` separator)

**Velden per entry**:
- Timestamp: ISO 8601 formaat (CET/CEST)
- Agent: Agent naam uit prompt metadata
- Intent: De intent/taak die uitgevoerd moet worden
- Value Stream: Value stream identifier
- Prompt File: Pad naar gebruikte prompt bestand
- Parameters: Key-value pairs die zijn meegegeven
- Instructions: Volledige samengestelde agent-instructies

---

"""
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(header)
    
    # Timestamp in CET/CEST
    timestamp = datetime.now().astimezone().isoformat()
    
    # Parameters als bullets
    params_text = "\n".join([f"  - `{k}`: {v}" for k, v in params.items()]) if params else "  (geen)"
    
    # Bouw log entry
    log_entry = f"""
---

## Agent Instructions — {timestamp}

- **Agent**: {metadata.get('agent', 'unknown')}
- **Intent**: {metadata.get('intent', 'unknown')}
- **Value Stream Fase**: {metadata.get('value_stream_fase', 'unknown')}
- **Prompt File**: `{prompt_file}`
- **Parameters**:
{params_text}

### Generated Instructions

```markdown
{final_prompt}
```

"""
    
    # Append naar log bestand
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)
    
    print(f"✓ Instructies gelogd naar: {log_file}")
    print()


def main():
    """Hoofdfunctie."""
    args = parse_arguments()
    
    # Laad workspace configuratie
    workspace_config = load_workspace_config()
    
    # === AUTO-DISCOVERY FLOW (nieuw) ===
    if args.agent and args.intent:
        print("=" * 80)
        print(f"AUTO-DISCOVERY MODE: Agent='{args.agent}' Intent='{args.intent}'")
        print("=" * 80)
        print()
        
        # 1. Zoek boundary file
        print(f"[1/2] Zoek boundary file voor '{args.agent}'...")
        boundary_file = find_boundary_file(args.agent)
        if not boundary_file:
            print(f"ERROR: Geen boundary file gevonden voor agent '{args.agent}'")
            print(f"Verwacht: artefacten/**/agent-boundary-{args.agent}.md")
            sys.exit(1)
        print(f"  ✓ Gevonden: {boundary_file}")
        print()
        
        # 2. Zoek prompt file
        print(f"[2/2] Zoek prompt file voor intent '{args.intent}'...")
        # Probeer eerst met opgegeven agent (als target)
        # Maar let op: args.agent kan ook het ONDERWERP zijn (zoals bij smeder)
        # We zoeken dus eerst 'breed', en als we de smeder vinden heeft die voorrang.
        # Als we specifiek de opdracht gaven om agent X te draaien, willen we die.
        
        # We gebruiken find_prompt_file nu met de agent parameter, maar als die niet 
        # matcht (omdat de agent de smeder moet zijn), valt hij terug op de intent search.
        # ECHTER: In het geval van 'leg-vast-agent-prompt' is de agent parameter het ONDERWERP.
        # Dus we moeten voorzichtig zijn.
        
        # Strategie:
        # 1. Kijk of er een prompt is voor mandarin.{args.agent}.{intent}
        # 2. Zo nee, kijk of er een prompt is voor *.{intent} (en pak bijv. smeder)
        
        prompt_file = find_prompt_file(args.intent, args.agent)
        
        if not prompt_file:
            # Fallback: probeer zonder agent (voor het geval args.agent het onderwerp is)
            prompt_file = find_prompt_file(args.intent)
            
        if not prompt_file:
            print(f"ERROR: Geen prompt file gevonden voor intent '{args.intent}'")
            print(f"Verwacht: .github/prompts/*.{args.intent}.prompt.md")
            sys.exit(1)
        print(f"  ✓ Gevonden: {prompt_file}")
        print()
        
        # Gebruik gevonden prompt_file
        args.prompt_file = str(prompt_file)
        
        # Voeg agent naam toe aan params voor placeholder vervanging
        params = parse_params(args.params)
        params['agent'] = args.agent
        params['agent_naam'] = args.agent
        
        # 3. Extraheer vs en fase uit boundary YAML (nodig voor file loading)
        print(f"[3/3] Extraheer metadata uit boundary...")
        try:
            with open(boundary_file, 'r', encoding='utf-8') as f:
                boundary_content = f.read()
                boundary_meta = frontmatter.loads(boundary_content)
                if boundary_meta.metadata:
                    if 'value_stream' in boundary_meta.metadata:
                        params['vs'] = boundary_meta.metadata['value_stream']
                        params['value_stream'] = boundary_meta.metadata['value_stream']
                        print(f"  ✓ Value stream: {params['vs']}")
                    if 'value_stream_fase' in boundary_meta.metadata:
                        params['value_stream_fase'] = boundary_meta.metadata['value_stream_fase']
                        # Extraheer fase (bijv. '02' uit 'aeo.02')
                        fase_parts = boundary_meta.metadata['value_stream_fase'].split('.')
                        if len(fase_parts) == 2:
                            params['fase'] = fase_parts[1]
                            print(f"  ✓ Fase: {params['fase']}")
                    print()
                else:
                    print(f"  ⚠ Geen YAML metadata in boundary, vs/fase niet geëxtraheerd")
                    print()
        except Exception as e:
            print(f"  ⚠ Kan boundary metadata niet lezen: {e}")
            print()
        
    # === KLASSIEKE FLOW (backward compatible) ===
    else:
        # Parse parameters
        params = parse_params(args.params)
    
    # === GEMEENSCHAPPELIJKE FLOW ===
    
    # Laad prompt-bestand
    metadata, prompt_content = load_prompt_file(args.prompt_file)
    
    # Laad input-bestand
    input_content = load_input_file(args.input_file)
    
    # Laad input_files uit metadata (boundary, templates, etc.)
    # Extraheer ook value_stream en fase uit boundary YAML
    input_files_content, extracted_params = load_and_process_input_files(metadata, params)
    
    # Voeg geëxtraheerde params toe (boundary YAML heeft voorrang indien niet via command-line gegeven)
    for key, value in extracted_params.items():
        if key not in params or not params[key]:  # Alleen toevoegen als nog niet ingesteld
            params[key] = value
    
    # Voer verplichte bootstrap uit
    run_bootstrap(metadata, args.prompt_file, args.method, params, workspace_config)
    
    # Stel volledige instructies samen (charter + agent.md + placeholders)
    final_prompt = assemble_full_instructions(metadata, prompt_content, args.prompt_file, params, input_content, input_files_content)
    
    # Log de gegenereerde instructies
    log_agent_instructions(metadata, params, final_prompt, args.prompt_file)
    
    # Print de volledige, samengestelde instructie
    print()
    print("=" * 80)
    print("AGENT INSTRUCTIES")
    print("=" * 80)
    print()
    print(final_prompt)
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
