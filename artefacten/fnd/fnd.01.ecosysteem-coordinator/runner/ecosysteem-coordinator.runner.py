#!/usr/bin/env python3
"""
Runner voor agent: ecosysteem-coordinator

Cross-cutting ecosysteem lifecycle taken:
- consulteer-canon: Raadpleeg de canon en log SHA
- genereer-instructies: Genereer execution-ready agent-instructies
- aggregeer-tasks: Aggregeer tasks op basis van beleid-workspace.md value_stream-fasen
- valideer-agent-structuur: Valideer agent folder structuur tegen doctrine
- list-agents: Toon beschikbare agents per value stream fase
- fetch-agents: Haal prompts, agents en tasks op voor een value stream fase

Architectuur: One Agent, One Runner principe.
"""
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set, TextIO
import argparse
import glob
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys

try:
    import frontmatter
except ImportError:
    print("ERROR: python-frontmatter is niet geïnstalleerd.")
    print("Installeer met: pip install python-frontmatter")
    sys.exit(1)


# ==============================================================================
# WINDOWS UTF-8 ENCODING FIX
# ==============================================================================

def setup_utf8_encoding():
    """Configureer UTF-8 encoding voor Windows console output.
    
    Voorkomt UnicodeEncodeError bij het printen van speciale tekens
    zoals pijlen (→), checkmarks (✓), etc.
    """
    if sys.platform == 'win32':
        # Reconfigure stdout/stderr to use UTF-8 with error handling
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
        
        # Set environment variable for child processes
        os.environ['PYTHONIOENCODING'] = 'utf-8'

# Apply UTF-8 fix immediately
setup_utf8_encoding()


# ==============================================================================
# SHARED UTILITIES
# ==============================================================================

class TeeWriter:
    """Schrijf output naar zowel console als logbestand."""
    
    def __init__(self, console: TextIO, logfile: TextIO):
        self.console = console
        self.logfile = logfile
    
    def write(self, text: str):
        self.console.write(text)
        self.logfile.write(text)
        self.logfile.flush()
    
    def flush(self):
        self.console.flush()
        self.logfile.flush()


def archive_existing_logs(logs_dir: Path, prefix: str) -> int:
    """Verplaats bestaande logs met gegeven prefix naar logs/history."""
    if not logs_dir.exists():
        return 0
    
    history_dir = logs_dir / "history"
    existing_logs = list(logs_dir.glob(f"{prefix}*.log"))
    
    if not existing_logs:
        return 0
    
    history_dir.mkdir(parents=True, exist_ok=True)
    
    for log_file in existing_logs:
        dest = history_dir / log_file.name
        shutil.move(str(log_file), str(dest))
    
    return len(existing_logs)


def get_workspace_root() -> Path:
    """Centrale functie voor workspace root detectie.
    
    Probeert eerst relatief aan dit script, dan fallback naar cwd.
    Script staat in: artefacten/fnd/fnd.01.ecosysteem-coordinator/runner/
    Dus 5 niveaus omhoog naar repo root.
    """
    repo_root = Path(__file__).resolve().parent.parent.parent.parent.parent
    if (repo_root / "artefacten").exists():
        return repo_root
    return Path.cwd()


def get_agent_source_root() -> Path:
    """Retourneert de root van de agent-definities (mandarin-agents).
    
    Dit is de repo waar dit script zelf in staat.
    """
    return Path(__file__).resolve().parent.parent.parent.parent.parent


def get_target_workspace() -> Path:
    """Retourneert de doelworkspace (cwd) waar output naartoe gaat."""
    return Path.cwd()


def compute_relative_agent_path(target_workspace: Path, agent_source: Path) -> str:
    """Bereken relatief pad van target workspace naar agent source.
    
    Returns:
        Relatief pad string zoals '../mandarin-agents'
    """
    try:
        rel = os.path.relpath(agent_source, target_workspace)
        # Normaliseer naar forward slashes voor cross-platform compatibiliteit
        return rel.replace("\\", "/")
    except ValueError:
        # Verschillende drives op Windows
        return str(agent_source).replace("\\", "/")


def find_agent_file(agent_naam: str, filename: str, extra_search_paths: List[Path] = None, search_root: Path = None) -> Optional[Path]:
    """Generieke file finder voor charter, boundary, agent-instructions, etc.
    
    Zoekt in artefacten structuur met optionele extra zoekpaden.
    
    Args:
        agent_naam: Naam van de agent
        filename: Bestandsnaam om te zoeken
        extra_search_paths: Extra paden om te doorzoeken
        search_root: Root folder om in te zoeken (default: agent source root)
    """
    if search_root is None:
        search_root = get_agent_source_root()
    artefacten_path = search_root / "artefacten"
    
    # Zoek in artefacten structuur
    if artefacten_path.exists():
        for agent_folder in artefacten_path.rglob(f"*.{agent_naam}"):
            if agent_folder.is_dir():
                # Direct in agent folder
                candidate = agent_folder / filename
                if candidate.exists():
                    return candidate
                # In agent-contracten subfolder
                candidate = agent_folder / "agent-contracten" / filename
                if candidate.exists():
                    return candidate
    
    # Extra zoekpaden
    if extra_search_paths:
        for search_path in extra_search_paths:
            candidate = search_path / filename
            if candidate.exists():
                return candidate
    
    return None


def load_workspace_config() -> Dict:
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


def load_prompt_file(prompt_path: str) -> Tuple[Dict, str]:
    """Laad prompt-bestand en parse YAML frontmatter."""
    prompt_file = Path(prompt_path)
    
    if not prompt_file.exists():
        print(f"ERROR: Prompt-bestand niet gevonden: {prompt_path}")
        sys.exit(1)
    
    with open(prompt_file, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
    
    return post.metadata, post.content


def find_prompt_file(intent: str, agent: str = None, search_root: Path = None) -> Optional[Path]:
    """Zoek prompt file voor gegeven intent.
    
    Zoekt eerst in artefacten structuur (modern), dan fallback naar .github/prompts/ (legacy).
    
    Args:
        intent: De intent naam om te zoeken
        agent: Optionele agent naam voor specifiekere match
        search_root: Root folder om in te zoeken (default: agent source root)
    """
    if search_root is None:
        search_root = get_agent_source_root()
    
    # Eerst zoeken in artefacten structuur (modern)
    artefacten = search_root / "artefacten"
    if artefacten.exists() and agent:
        pattern = f"**/prompts/mandarin.{agent}.{intent}.prompt.md"
        matches = list(artefacten.glob(pattern))
        if matches:
            return matches[0]
        
        pattern = f"**/prompts/*{intent}.prompt.md"
        matches = list(artefacten.glob(pattern))
        for match in matches:
            if agent in str(match):
                return match
    
    # Fallback naar .github/prompts/ (legacy structuur)
    prompts_dir = search_root / ".github/prompts"
    if not prompts_dir.exists():
        return None
    
    if agent:
        specific_pattern = f"mandarin.{agent}.{intent}.prompt.md"
        specific_file = prompts_dir / specific_pattern
        if specific_file.exists():
            return specific_file
            
        pattern = f"*{agent}*.{intent}.prompt.md"
        matches = list(prompts_dir.glob(pattern))
        if matches:
            return matches[0]

    if not agent:
        pattern = f"*.{intent}.prompt.md"
        matches = list(prompts_dir.glob(pattern))
        
        if matches:
            for match in matches:
                if "agent-smeder" in match.name:
                    return match
            return matches[0]
            
    return None


def find_boundary_file(agent_naam: str, search_root: Path = None) -> Optional[Path]:
    """Zoek boundary file voor gegeven agent naam.
    
    Args:
        agent_naam: Naam van de agent
        search_root: Root folder om in te zoeken (default: agent source root)
    """
    if search_root is None:
        search_root = get_agent_source_root()
    
    artefacten = search_root / "artefacten"
    if not artefacten.exists():
        return None
    
    patterns = [
        f"**/{agent_naam}.agent-boundary.md", 
        f"**/agent-boundary-{agent_naam}.md",
        f"**/{agent_naam}.boundary.md",
    ]
    
    for pattern in patterns:
        matches = list(artefacten.glob(pattern))
        for match in matches:
            if agent_naam in str(match):
                return match
    
    return None


def parse_params(param_list: List[str]) -> Dict[str, str]:
    """Parse parameter lijst naar dictionary."""
    params = {}
    for param in param_list:
        if '=' not in param:
            print(f"WARNING: Ongeldige parameter (verwacht key=value): {param}")
            continue
        key, value = param.split('=', 1)
        params[key.strip()] = value.strip()
    return params


# ==============================================================================
# CONSULTEER-CANON
# ==============================================================================

def _run_git(args: List[str], cwd: Optional[str] = None) -> Optional[str]:
    """Execute git command and return output."""
    try:
        out = subprocess.check_output(["git", *args], cwd=cwd, stderr=subprocess.DEVNULL, text=True)
        return out.strip()
    except Exception:
        return None


def get_github_url(canon_path: str) -> Optional[str]:
    """Get GitHub remote URL from canon repository."""
    url = _run_git(["config", "--get", "remote.origin.url"], cwd=canon_path)
    if not url:
        return None
    # Convert SSH to HTTPS format if needed
    if url.startswith("git@github.com:"):
        url = url.replace("git@github.com:", "https://github.com/").replace(".git", "")
    elif url.endswith(".git"):
        url = url[:-4]
    return url


def clone_canon_from_github(target_path: str, github_url: str, branch: str = "main") -> bool:
    """Clone canon repository from GitHub if local copy doesn't exist."""
    try:
        print(f"Local canon not found at: {target_path}", file=sys.stderr)
        print(f"Attempting to clone from: {github_url}", file=sys.stderr)
        
        # Shallow clone for efficiency (only latest commit)
        subprocess.check_call(
            ["git", "clone", "--depth", "1", "--branch", branch, github_url, target_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE
        )
        print(f"✓ Successfully cloned canon to: {target_path}", file=sys.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to clone from GitHub: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error during clone: {e}", file=sys.stderr)
        return False


def resolve_canon_info(canon_path: str) -> Dict:
    """Get current branch and commit SHA from canon repo."""
    branch = _run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=canon_path)
    sha_full = _run_git(["rev-parse", "HEAD"], cwd=canon_path)
    sha_short = _run_git(["rev-parse", "--short", "HEAD"], cwd=canon_path)
    return {
        "branch": branch,
        "sha_full": sha_full,
        "sha_short": sha_short,
    }


def ensure_audit_dir(workspace_root: str) -> str:
    """Create audit directory if it doesn't exist."""
    audit_dir = os.path.join(workspace_root, "audit")
    os.makedirs(audit_dir, exist_ok=True)
    return audit_dir


def append_canon_log_entry(log_path: str, entry: Dict, files_table: List[Tuple[str, str]], 
                           charter_file: str = None, template_files: List[str] = None) -> None:
    """Append a consultation entry as Markdown to canon-consult.log.md."""
    lines = ["\n---\n\n"]
    lines.append(f"## Canon Consultation — {entry['ts']}\n\n")
    lines.append(f"- **Agent**: {entry['agent']}\n")
    lines.append(f"- **Value Stream**: {entry['valueStream'] or 'n/a'}\n")
    lines.append(f"- **Workspace File**: `{entry['workspaceFile']}`\n")
    lines.append(f"- **Intent**: {entry['intent']}\n")
    lines.append(f"- **Method**: {entry['method']}\n")
    lines.append(f"- **Canon Path**: `{entry['canonPath']}`\n")
    lines.append(f"- **Branch**: {entry['branch']}\n")
    lines.append(f"- **SHA**: {entry['shaShort']}\n")
    lines.append(f"- **Grondslagen Patterns**: `{entry['grondslagePatterns']}`\n")
    if charter_file:
        lines.append(f"- **Charter**: `{charter_file}`\n")
    if template_files:
        template_list = ", ".join([f"`{t}`" for t in template_files])
        lines.append(f"- **Templates**: {template_list}\n")
    if entry.get('notes'):
        lines.append(f"- **Notes**: {entry['notes']}\n")
    
    lines.append("\n### Consulted Files\n\n")
    lines.append("| Folder | Bestand |\n")
    lines.append("|--------|---------|\n")
    for folder, filename in files_table:
        lines.append(f"| `{folder}` | `{filename}` |\n")
    lines.append("\n")

    with open(log_path, "a", encoding="utf-8") as f:
        f.writelines(lines)


def read_grondslagen(canon_path: str, patterns: List[str]) -> Dict:
    """Read grondslagen files matching the patterns."""
    consulted = []
    files_table = []  # (folder, filename) tuples
    content_summary = []
    
    for pattern in patterns:
        full_pattern = os.path.join(canon_path, pattern)
        # Handle glob patterns
        if "*" in pattern:
            matches = glob.glob(full_pattern, recursive=True)
            for match in matches:
                if os.path.isfile(match):
                    rel_path = os.path.relpath(match, canon_path)
                    consulted.append(rel_path)
                    folder = os.path.dirname(rel_path) or "."
                    filename = os.path.basename(rel_path)
                    files_table.append((folder, filename))
                    try:
                        with open(match, "r", encoding="utf-8") as f:
                            file_lines = f.readlines()
                            preview = "".join(file_lines[:5]).strip()
                            content_summary.append(f"\n### {rel_path}\n{preview}...\n")
                    except Exception as e:
                        content_summary.append(f"\n### {rel_path}\n(Error reading: {e})\n")
        else:
            # Single file
            full_path = os.path.join(canon_path, pattern)
            if os.path.isfile(full_path):
                consulted.append(pattern)
                folder = os.path.dirname(pattern) or "."
                filename = os.path.basename(pattern)
                files_table.append((folder, filename))
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        file_lines = f.readlines()
                        preview = "".join(file_lines[:5]).strip()
                        content_summary.append(f"\n### {pattern}\n{preview}...\n")
                except Exception as e:
                    content_summary.append(f"\n### {pattern}\n(Error reading: {e})\n")
    
    return {
        "files": consulted,
        "files_table": files_table,
        "summary": "".join(content_summary),
        "count": len(consulted)
    }


def execute_canon_consultation(
    agent: str,
    value_stream: str,
    intent: str,
    grondslagen_patterns: str,
    workspace_file: str = "runner",
    method: str = "runner",
    canon_path: Optional[str] = None,
    canon_github_url: Optional[str] = None,
    canon_branch: str = "main",
    charter_file: Optional[str] = None,
    template_files: Optional[List[str]] = None,
    notes: Optional[str] = None,
    quiet: bool = False
) -> Tuple[bool, Optional[str]]:
    """
    Execute canon consultation and log to audit/canon-consult.log.md.
    
    Returns:
        Tuple of (success: bool, sha_short: Optional[str])
    """
    # Determine workspace root
    workspace_root = str(get_workspace_root())
    
    audit_dir = ensure_audit_dir(workspace_root)
    log_path = os.path.join(audit_dir, "canon-consult.log.md")
    
    # Resolve canon path
    if canon_path:
        resolved_canon_path = canon_path
    else:
        resolved_canon_path = os.path.abspath(os.path.join(workspace_root, os.pardir, "mandarin-canon"))
    
    # Track source
    source_type = "local"
    canon_source = resolved_canon_path
    
    # If local canon doesn't exist, try to clone from GitHub
    if not os.path.isdir(resolved_canon_path):
        if canon_github_url:
            success = clone_canon_from_github(resolved_canon_path, canon_github_url, canon_branch)
            if not success:
                print("ERROR: Could not find or clone canon repository", file=sys.stderr)
                return (False, None)
            source_type = "github"
            canon_source = canon_github_url
        else:
            print(f"ERROR: Canon path not found: {resolved_canon_path}", file=sys.stderr)
            print("TIP: Provide canon_github_url to clone automatically from GitHub", file=sys.stderr)
            return (False, None)
    
    # Get canon info
    info = resolve_canon_info(resolved_canon_path)
    if not info.get("sha_full"):
        print(f"ERROR: Could not resolve canon commit SHA in: {resolved_canon_path}", file=sys.stderr)
        return (False, None)
    
    # Read grondslagen - constitutie altijd eerst
    CONSTITUTIE_PATH = "grondslagen/.algemeen/constitutie.md"
    patterns = [CONSTITUTIE_PATH]  # Constitutie is verplicht en altijd eerste
    patterns.extend([p.strip() for p in grondslagen_patterns.split(",") if p.strip() != CONSTITUTIE_PATH])
    grondslagen = read_grondslagen(resolved_canon_path, patterns)
    
    if grondslagen["count"] == 0:
        print(f"WARNING: No grondslagen files found matching patterns: {patterns}", file=sys.stderr)
    
    # Create log entry
    now_cet = datetime.now()
    ts_str = now_cet.strftime("%Y-%m-%dT%H:%M:%S")
    
    entry = {
        "ts": ts_str,
        "agent": agent,
        "valueStream": value_stream,
        "workspaceFile": workspace_file,
        "intent": intent,
        "method": method,
        "canonPath": canon_source,
        "branch": info.get("branch"),
        "shaShort": info.get("sha_short"),
        "grondslagePatterns": grondslagen_patterns,
        "notes": notes,
    }
    
    # Log the consultation
    append_canon_log_entry(log_path, entry, grondslagen["files_table"], charter_file, template_files)
    
    # Report
    if quiet:
        charter_info = f" charter={os.path.basename(charter_file)}" if charter_file else ""
        template_info = f" templates={len(template_files)}" if template_files else ""
        print(
            f"[canon] ok agent={agent} sha={info['sha_short']} files={grondslagen['count']}{charter_info}{template_info} "
            f"log={os.path.relpath(log_path, workspace_root)}"
        )
    else:
        print("=" * 80)
        print("CANON CONSULTATION LOGGED")
        print("=" * 80)
        print(f"Agent:       {agent}")
        print(f"Timestamp:   {entry['ts']}")
        print(f"Canon SHA:   {info['sha_short']} (branch: {info['branch']})")
        print(f"Files read:  {grondslagen['count']}")
        if charter_file:
            print(f"Charter:     {charter_file}")
        if template_files:
            print(f"Templates:   {len(template_files)} file(s)")
            for tmpl in template_files:
                print(f"             - {tmpl}")
        print(f"Log:         {os.path.relpath(log_path, workspace_root)}")
        print()
        print("Consulted grondslagen:")
        for f in grondslagen["files"]:
            print(f"  - {f}")
        print()
        print("=" * 80)
        print()
        print("✓ Canon consultation verified and logged")
        print("✓ Agent may now proceed with execution")
        print()
    
    return (True, info.get("sha_short"))


def consulteer_canon_main(args: argparse.Namespace) -> int:
    """Voer canon consultatie uit (geïntegreerd in runner)."""
    
    workspace_config = load_workspace_config()
    
    # Bepaal grondslagen patterns
    grondslagen = args.grondslagen
    if not grondslagen:
        grondslagen_map = workspace_config.get('grondslagen', {})
        grondslagen = grondslagen_map.get(args.value_stream, 'grondslagen/.algemeen/*')
    
    # Bepaal canon GitHub URL
    canon_github_url = args.canon_github_url
    if not canon_github_url:
        canon_github_url = workspace_config.get('canon_github_url', 'https://github.com/minvws/mandarin-canon')
    
    print("=" * 80)
    print("CONSULTEER CANON")
    print("=" * 80)
    print(f"Agent: {args.agent}")
    print(f"Value Stream: {args.value_stream}")
    print(f"Intent: {args.intent}")
    print()
    
    success, sha = execute_canon_consultation(
        agent=args.agent,
        value_stream=args.value_stream,
        intent=args.intent,
        grondslagen_patterns=grondslagen,
        workspace_file="runner",
        method="runner",
        canon_path=args.canon_path,
        canon_github_url=canon_github_url,
        quiet=False
    )
    
    if not success:
        print("ERROR: Canon consultatie mislukt.")
        return 1
    
    print()
    print("[OK] Canon consultatie voltooid")
    return 0


# ==============================================================================
# GENEREER-INSTRUCTIES
# ==============================================================================

def load_input_file(input_path: str) -> str:
    """Laad de inhoud van het input-bestand."""
    input_file = Path(input_path)
    
    if not input_file.exists():
        print(f"WARNING: Input-bestand niet gevonden: {input_path}")
        return ""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        return f.read()


def load_minimal_template(template_path: str) -> Optional[str]:
    """Laad minimal template content. Retourneert None indien niet gevonden."""
    template_file = Path(template_path)

    if not template_file.exists():
        print(f"ERROR: Minimal template niet gevonden: {template_path}")
        return None

    with open(template_file, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)

    return post.content


def run_bootstrap(metadata: Dict, prompt_file: str, method: str, params: Dict, 
                  workspace_config: Dict, quiet: bool = False, 
                  charter_path: str = None, template_paths: List[str] = None) -> bool:
    """Voer canon consultatie uit (geïntegreerd - geen extern script meer nodig)."""
    
    # Bepaal value stream
    value_stream_fase = params.get('value_stream_fase', metadata.get('value_stream_fase', 'unknown'))
    value_stream = value_stream_fase.split('.')[0] if '.' in value_stream_fase else value_stream_fase
    
    # Bepaal grondslagen patterns
    grondslagen_map = workspace_config.get('grondslagen', {})
    grondslagen = grondslagen_map.get(value_stream, 'grondslagen/.algemeen/*')
    
    # Bepaal canon URL
    canon_github_url = workspace_config.get('canon_github_url', 'https://github.com/minvws/mandarin-canon')
    
    # Bepaal agent naam
    agent = params.get('agent_naam', metadata.get('agent', 'unknown-agent'))
    if '.' in agent:
        agent = agent.split('.')[-1]
    
    # Bepaal intent
    intent = metadata.get('intent', '')
    if not intent:
        match = re.search(r'\.([a-z\-]+)\.prompt\.md$', str(prompt_file))
        if match:
            intent = match.group(1)
    
    print("=" * 80)
    print("STAP 0: CANON CONSULTATIE (VERPLICHT)")
    print("=" * 80)
    print(f"Agent: {agent}")
    print(f"Value Stream: {value_stream}")
    print(f"Intent: {intent}")
    print(f"Grondslagen: {grondslagen}")
    print()
    
    success, sha = execute_canon_consultation(
        agent=agent,
        value_stream=value_stream,
        intent=intent,
        grondslagen_patterns=grondslagen,
        workspace_file=str(prompt_file),
        method=method,
        canon_github_url=canon_github_url,
        charter_file=charter_path,
        template_files=template_paths,
        quiet=quiet
    )
    
    if not success:
        print()
        print("ERROR: Canon consultatie mislukt.")
        return False
    
    print()
    print("=" * 80)
    print("[OK] Bootstrap succesvol voltooid")
    print("=" * 80)
    print()
    
    return True


def load_agent_instructions(prompt_file: str, metadata: Dict, params: Dict) -> Optional[str]:
    """Laad agent-instructies uit .agent.md bestand.
    
    Zoekt in de agent source root (mandarin-agents), niet in cwd.
    """
    agent_full = metadata.get('agent', '')
    agent_naam = agent_full.split('.')[-1] if '.' in agent_full else agent_full
    
    intent = metadata.get('intent', '')
    
    if not (agent_naam and intent):
        return None
    
    agent_file_name = f"{agent_naam}.{intent}.agent.md"
    agent_source = get_agent_source_root()
    
    # Strategie 1: Zoek in uitvoerende agent's folder
    artefacten_path = agent_source / "artefacten"
    if artefacten_path.exists():
        for agent_folder in artefacten_path.rglob(f"*.{agent_naam}"):
            if agent_folder.is_dir():
                agent_contracten_folder = agent_folder / "agent-contracten"
                agent_file = agent_contracten_folder / agent_file_name
                if agent_file.exists():
                    print(f"[OK] Agent-instructies geladen: {agent_file}")
                    with open(agent_file, 'r', encoding='utf-8') as f:
                        return f.read()
                
                agent_file = agent_folder / agent_file_name
                if agent_file.exists():
                    print(f"[OK] Agent-instructies geladen: {agent_file}")
                    with open(agent_file, 'r', encoding='utf-8') as f:
                        return f.read()
    
    # Strategie 2: Zoek in doel-agent folder
    vs = params.get('vs', params.get('value_stream', ''))
    fase = params.get('fase', '')
    agent = params.get('agent', params.get('agent_naam', ''))
    
    if vs and fase and agent:
        agent_folder = agent_source / f"artefacten/{vs}/{vs}.{fase}.{agent}"
        agent_contracten_folder = agent_folder / "agent-contracten"
        
        agent_file = agent_contracten_folder / agent_file_name
        if agent_file.exists():
            print(f"[OK] Agent-instructies geladen: {agent_file}")
            with open(agent_file, 'r', encoding='utf-8') as f:
                return f.read()
        
        agent_file = agent_folder / agent_file_name
        if agent_file.exists():
            print(f"[OK] Agent-instructies geladen: {agent_file}")
            with open(agent_file, 'r', encoding='utf-8') as f:
                return f.read()
    
    # Strategie 3: Fallback - zoek in prompt folder
    prompt_path = Path(prompt_file)
    prompt_dir = prompt_path.parent
    agent_file = prompt_dir / agent_file_name
    
    if agent_file.exists():
        print(f"[OK] Agent-instructies geladen: {agent_file}")
        with open(agent_file, 'r', encoding='utf-8') as f:
            return f.read()

    # Strategie 4: Fallback - zoek in .github/agents
    github_agents_dir = agent_source / ".github/agents"
    agent_file = github_agents_dir / agent_file_name
    if agent_file.exists():
        print(f"[OK] Agent-instructies geladen: {agent_file}")
        with open(agent_file, 'r', encoding='utf-8') as f:
            return f.read()

    print(f"INFO: Agent-instructies niet gevonden: {agent_file_name}")
    
    return None


def load_charter(prompt_file: str, metadata: Dict, params: Dict) -> Tuple[Optional[str], Optional[str]]:
    """Laad charter uit conventie: {agent-naam}.charter.md.
    
    Zoekt in de agent source root (mandarin-agents), niet in cwd.
    """
    agent_full = metadata.get('agent', '')
    agent_naam = agent_full.split('.')[-1] if '.' in agent_full else agent_full
    
    if not agent_naam:
        return None, None
    
    charter_file_name = f"{agent_naam}.charter.md"
    agent_source = get_agent_source_root()
    
    # Strategie 1: Zoek in uitvoerende agent's folder
    artefacten_path = agent_source / "artefacten"
    if artefacten_path.exists():
        for agent_folder in artefacten_path.rglob(f"*.{agent_naam}"):
            if agent_folder.is_dir():
                charter_file = agent_folder / charter_file_name
                if charter_file.exists():
                    print(f"[OK] Charter geladen: {charter_file}")
                    with open(charter_file, 'r', encoding='utf-8') as f:
                        return f.read(), str(charter_file)
    
    # Strategie 2: Zoek in doel-agent folder
    vs = params.get('vs', params.get('value_stream', ''))
    fase = params.get('fase', '')
    agent = params.get('agent', params.get('agent_naam', ''))
    
    if vs and fase and agent:
        agent_folder = agent_source / f"artefacten/{vs}/{vs}.{fase}.{agent}"
        charter_file = agent_folder / charter_file_name
        
        if charter_file.exists():
            print(f"[OK] Charter geladen: {charter_file}")
            with open(charter_file, 'r', encoding='utf-8') as f:
                return f.read(), str(charter_file)
    
    # Strategie 3: Fallback - zoek in prompt folder
    prompt_path = Path(prompt_file)
    prompt_dir = prompt_path.parent
    charter_file = prompt_dir / charter_file_name
    
    if charter_file.exists():
        print(f"[OK] Charter geladen: {charter_file}")
        with open(charter_file, 'r', encoding='utf-8') as f:
            return f.read(), str(charter_file)

    print(f"INFO: Charter niet gevonden (optioneel): {charter_file_name}")
    
    return None, None


def load_and_process_input_files(metadata: Dict, params: Dict) -> Tuple[Dict, Dict, Dict]:
    """Laad input_files uit metadata, vervang placeholders, laad bestanden."""
    input_files = metadata.get('input_files', {})
    loaded_content = {}
    extracted_params = {}
    file_paths = {}
    
    if not input_files:
        return loaded_content, extracted_params, file_paths
    
    print("[Info] Verwerk input_files uit prompt metadata...")
    
    for key, path_template in input_files.items():
        path = path_template.format(
            vs=params.get('vs', params.get('value_stream', '')),
            fase=params.get('fase', ''),
            agent=params.get('agent', params.get('agent_naam', '')),
            intent=params.get('intent', '')
        )
        
        if key in params:
            path = params[key]
        
        file_path = Path(path)
        
        if file_path.exists():
            if file_path.is_file():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    placeholder_key = key.upper()
                    loaded_content[placeholder_key] = content
                    file_paths[key] = str(file_path.resolve())
                    print(f"  [OK] Geladen: {key} -> {path}")
                    
                    if key == 'boundary_file':
                        try:
                            boundary_meta = frontmatter.loads(content)
                            if boundary_meta.metadata:
                                if 'value_stream' in boundary_meta.metadata:
                                    extracted_params['vs'] = boundary_meta.metadata['value_stream']
                                    extracted_params['value_stream'] = boundary_meta.metadata['value_stream']
                                if 'value_stream_fase' in boundary_meta.metadata:
                                    extracted_params['value_stream_fase'] = boundary_meta.metadata['value_stream_fase']
                                    fase_parts = boundary_meta.metadata['value_stream_fase'].split('.')
                                    if len(fase_parts) == 2:
                                        extracted_params['fase'] = fase_parts[1]
                                if 'agent' in boundary_meta.metadata:
                                    extracted_params['agent'] = boundary_meta.metadata['agent']
                                    extracted_params['agent_naam'] = boundary_meta.metadata['agent']
                                print(f"  [OK] Metadata geëxtraheerd uit boundary: {', '.join(extracted_params.keys())}")
                        except Exception as e:
                            print(f"  ⚠ Kan boundary metadata niet parsen: {e}")
            else:
                loaded_content[key.upper()] = str(file_path)
        else:
            print(f"  ✗ Niet gevonden: {key} -> {path}")
    
    if loaded_content:
        print()
    
    return loaded_content, extracted_params, file_paths


def replace_placeholders(content: str, params: Dict, input_content: str, 
                         input_files_content: Dict = None) -> str:
    """Vervang placeholders in de prompt content."""
    content = content.replace('[INPUT_CONTENT]', input_content)
    
    if input_files_content:
        for key, file_content in input_files_content.items():
            placeholder = f'[{key}]'
            content = content.replace(placeholder, file_content)
    
    for key, value in params.items():
        content = re.sub(rf'\[{key}\]', lambda _: value, content, flags=re.IGNORECASE)
    
    return content


# ==============================================================================
# BRONHOUDING
# ==============================================================================

BRONHOUDING_INSTRUCTIES = {
    "Input-gebonden": (
        "Je handelt uitsluitend op basis van de meegeleverde inputparameters. "
        "Voeg geen kennis toe die niet expliciet in de input staat. "
        "Als informatie ontbreekt, stop dan en vraag om verduidelijking."
    ),
    "Canon-gebonden": (
        "Je handelt op basis van de canon. Elke conclusie is herleidbaar naar "
        "een canonieke bron die in deze sessie is meegegeven. "
        "Eigen interpretaties die niet canon-herleidbaar zijn, zijn niet toegestaan."
    ),
    "Externe-bron gebonden": (
        "Je handelt uitsluitend op basis van de externe bronnen die als input zijn "
        "meegegeven. Voeg geen eigen kennis of canonreferenties toe die niet "
        "in die bronnen staan. Bronvermelding is verplicht."
    ),
    "Workspace-gebonden": (
        "Je handelt uitsluitend op basis van wat aanwezig is in de workspace: "
        "bestanden, artefacten en configuraties die expliciet zijn meegegeven of "
        "aantoonbaar in de workspace staan. Je voegt geen externe kennis of "
        "canonreferenties toe die niet uit de workspace afkomstig zijn."
    ),
    "Exploratief": (
        "Je handelt exploratief: je gebruikt je generatieve capaciteiten om "
        "inzichten, hypothesen en aannames te formuleren. Je bronnen zijn breed "
        "en gevarieerd. Aannames die je maakt, maak je expliciet zichtbaar in de output."
    ),
}


def load_constitutie() -> Optional[str]:
    """Laad de constitutie uit de canon repository.
    
    Zoekt in: ../mandarin-canon/grondslagen/.algemeen/constitutie.md
    """
    workspace_root = get_workspace_root()
    canon_paths = [
        workspace_root.parent / "mandarin-canon" / "grondslagen" / ".algemeen" / "constitutie.md",
        workspace_root / "mandarin-canon" / "grondslagen" / ".algemeen" / "constitutie.md",
    ]
    
    for canon_path in canon_paths:
        if canon_path.exists():
            try:
                with open(canon_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"WARNING: Kon constitutie niet lezen: {e}")
                return None
    
    return None


def assemble_full_instructions(metadata: Dict, prompt_content: str, prompt_file: str, 
                               params: Dict, input_content: str, 
                               input_files_content: Dict) -> Tuple[str, Optional[str]]:
    """Stel volledige agent-instructies samen uit alle bronnen.
    
    Volgorde: constitutie → bronhouding → charter → agent instructies
    """
    parts = []
    
    # 1. Constitutie (fundament uit canon)
    constitutie = load_constitutie()
    if constitutie:
        parts.append("# Constitutie\n\n")
        parts.append(constitutie)
        parts.append("\n\n---\n\n")

    # 2. Bronhouding
    bronhouding = metadata.get('bronhouding')
    if bronhouding and bronhouding in BRONHOUDING_INSTRUCTIES:
        parts.append(f"## Bronhouding: {bronhouding}\n\n")
        parts.append(BRONHOUDING_INSTRUCTIES[bronhouding])
        parts.append("\n\n---\n\n")
    elif bronhouding:
        print(f"WARNING: Onbekende bronhouding '{bronhouding}'. Geldige waarden: {', '.join(BRONHOUDING_INSTRUCTIES.keys())}")

    # 3. Charter
    charter_content, charter_path = load_charter(prompt_file, metadata, params)
    if charter_content:
        parts.append("# Agent Charter\n\n")
        parts.append(charter_content)
        parts.append("\n\n---\n\n")
    
    agent_instructions = load_agent_instructions(prompt_file, metadata, params)
    if agent_instructions:
        parts.append(agent_instructions)
    elif prompt_content.strip():
        parts.append(prompt_content)
    
    combined = ''.join(parts)
    final_instructions = replace_placeholders(combined, params, input_content, input_files_content)
    
    return final_instructions, charter_path


def write_execution_file(filepath: str, metadata: Dict, params: Dict, final_prompt: str) -> bool:
    """Schrijf execution-ready instructies naar bestand met metadata header.
    
    Returns:
        True als succesvol, False bij fout.
    """
    execution_file = Path(filepath)
    execution_file.parent.mkdir(parents=True, exist_ok=True)
    
    execution_dir = execution_file.parent
    history_dir = execution_dir / "history"

    existing_files = [
        f for f in execution_dir.glob("*.md")
        if f.name.lower() != "readme.md" and f.resolve() != execution_file.resolve()
    ]
    
    if existing_files:
        history_dir.mkdir(exist_ok=True)
        
        for existing_file in existing_files:
            target = history_dir / existing_file.name
            if target.exists():
                timestamp_suffix = datetime.now().strftime('%Y%m%d-%H%M%S')
                target = history_dir / f"{existing_file.stem}.{timestamp_suffix}{existing_file.suffix}"
            existing_file.rename(target)
        
        print(f"[OK] {len(existing_files)} bestaand(e) execution file(s) verplaatst naar {history_dir}")
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    agent_name = metadata.get('agent', 'unknown').split('.')[-1]
    intent = metadata.get('intent', 'unknown')
    value_stream_fase = metadata.get('value_stream_fase', params.get('value_stream_fase', 'unknown'))
    
    hash_input = datetime.now().strftime('%Y%m%d%H%M%S') + agent_name
    hash_digest = hashlib.md5(hash_input.encode('utf-8')).hexdigest()[:4]
    
    # Lees canon hash
    canon_hash = None
    workspace_root = get_workspace_root()
    canon_log_candidates = [
        (workspace_root / 'audit/canon-consult.log.md').resolve(),
        (Path.cwd() / 'audit/canon-consult.log.md').resolve(),
    ]
    
    unique_candidates = list(dict.fromkeys(canon_log_candidates))
    existing_logs = [p for p in unique_candidates if p.exists()]
    canon_log = max(existing_logs, key=lambda p: p.stat().st_mtime) if existing_logs else unique_candidates[0]

    if canon_log.exists():
        try:
            log_content = canon_log.read_text(encoding='utf-8')
            sha_matches = re.findall(r'-\s+\*\*SHA\*\*:\s+([a-f0-9]+)', log_content, re.IGNORECASE)
            if sha_matches:
                canon_hash = sha_matches[-1]
            else:
                old_matches = re.findall(r'Canon SHA:\s+([a-f0-9]+)', log_content)
                if old_matches:
                    canon_hash = old_matches[-1]
        except Exception as e:
            print(f"WARNING: Kan canon-consult.log.md niet lezen: {e}")
    
    if not canon_hash:
        print()
        print("=" * 80)
        print("ERROR: Geen geldige canon SHA gevonden")
        print("=" * 80)
        return False
    
    params_text = "\n".join([f"  - `{k}`: {v}" for k, v in params.items()]) if params else "  (geen)"
    
    header = f"""---
execution_id: {hash_digest}
timestamp: {timestamp}
agent: {agent_name}
intent: {intent}
value_stream_fase: {value_stream_fase}
canon_ref: {canon_hash}
---

**Voer de volgende instructie uit:**

# Agent Execution: {agent_name} — {intent}

**Execution ID**: `{hash_digest}`  
**Timestamp**: {timestamp}  
**Canon Reference**: {canon_hash}  
**Value Stream**: {value_stream_fase}

## Parameters

{params_text}

## Instructies

"""
    
    with open(execution_file, 'w', encoding='utf-8') as f:
        f.write(header)
        f.write(final_prompt)
    
    return True


def log_agent_instructions(metadata: Dict, params: Dict, final_prompt: str, 
                           prompt_file: str, log_mode: str = "full"):
    """Log de gegenereerde agent-instructies naar audit/agent-instructions.log.md."""
    log_file = Path('audit/agent-instructions.log.md')
    log_file.parent.mkdir(exist_ok=True)
    
    if not log_file.exists():
        header = """# Agent Instructions Log

Dit logbestand registreert alle gegenereerde agent-instructies.

---

"""
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(header)
    
    timestamp = datetime.now().astimezone().isoformat()
    params_text = "\n".join([f"  - `{k}`: {v}" for k, v in params.items()]) if params else "  (geen)"
    
    if log_mode == "compact":
        snippet = final_prompt[:400].replace("```", "'''")
        log_entry = f"""
---

## Agent Instructions — {timestamp}

- **Agent**: {metadata.get('agent', 'unknown')}
- **Intent**: {metadata.get('intent', 'unknown')}
- **Value Stream Fase**: {metadata.get('value_stream_fase', 'unknown')}
- **Prompt File**: `{prompt_file}`
- **Mode**: compact
- **Instruction Length**: {len(final_prompt)} chars

### Preview

```markdown
{snippet}
```

"""
    else:
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
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)
    
    print(f"[OK] Instructies gelogd naar: {log_file}")
    print()


def genereer_instructies_main(args: argparse.Namespace) -> int:
    """Hoofdfunctie voor genereer-instructies."""
    
    workspace_config = load_workspace_config()
    
    # === AUTO-DISCOVERY FLOW ===
    if args.agent and args.intent:
        print("=" * 80)
        print(f"AUTO-DISCOVERY MODE: Agent='{args.agent}' Intent='{args.intent}'")
        print("=" * 80)
        print()
        
        boundary_file = None
        
        print(f"[1/2] Zoek prompt file voor intent '{args.intent}'...")
        prompt_file = find_prompt_file(args.intent, args.agent)
        
        if not prompt_file:
            prompt_file = find_prompt_file(args.intent)
            
        if not prompt_file:
            print(f"ERROR: Geen prompt file gevonden voor intent '{args.intent}'")
            return 1
        print(f"  [OK] Gevonden: {prompt_file}")
        print()
        
        args.prompt_file = str(prompt_file)
        
        params = parse_params(args.params) if args.params else {}
        
        if 'agent' not in params:
            params['agent'] = args.agent
        if 'agent_naam' not in params:
            params['agent_naam'] = args.agent

        try:
            probe_metadata, _ = load_prompt_file(args.prompt_file)
            if ('value_stream_fase' not in params or not params.get('value_stream_fase')) and probe_metadata.get('value_stream_fase'):
                params['value_stream_fase'] = str(probe_metadata.get('value_stream_fase'))
                fase_parts = params['value_stream_fase'].split('.')
                if len(fase_parts) == 2:
                    params['vs'] = fase_parts[0]
                    params['value_stream'] = fase_parts[0]
                    params['fase'] = fase_parts[1]
        except Exception:
            pass
        
        print(f"[2/2] Extraheer metadata uit prompt/boundary (indien nodig)...")
        
        if 'value_stream_fase' in params and params['value_stream_fase']:
            fase_parts = params['value_stream_fase'].split('.')
            if len(fase_parts) == 2:
                params['vs'] = fase_parts[0]
                params['value_stream'] = fase_parts[0]
                params['fase'] = fase_parts[1]
                print(f"  [OK] Value stream uit parameter: {params['vs']}")
                print(f"  [OK] Fase uit parameter: {params['fase']}")
            print()
        else:
            if 'agent_naam' in params and params['agent_naam'] != args.agent:
                print(f"  >> Target agent gedetecteerd: '{params['agent_naam']}'")
                
                target_boundary = find_boundary_file(params['agent_naam'])
                if target_boundary:
                    print(f"  [OK] Target boundary gevonden: {target_boundary}")
                    try:
                        with open(target_boundary, 'r', encoding='utf-8') as f:
                            target_content = f.read()
                            target_meta = frontmatter.loads(target_content)
                            if target_meta.metadata:
                                if 'value_stream' in target_meta.metadata:
                                    params['vs'] = target_meta.metadata['value_stream']
                                    params['value_stream'] = target_meta.metadata['value_stream']
                                if 'value_stream_fase' in target_meta.metadata:
                                    params['value_stream_fase'] = target_meta.metadata['value_stream_fase']
                                    fase_parts = target_meta.metadata['value_stream_fase'].split('.')
                                    if len(fase_parts) == 2:
                                        params['fase'] = fase_parts[1]
                                params['boundary_file'] = str(target_boundary)
                    except Exception as e:
                        print(f"  ⚠ Kan target boundary niet lezen: {e}")
            
            if 'vs' not in params or not params.get('vs'):
                if not boundary_file:
                    boundary_file = find_boundary_file(args.agent)
                    
                if boundary_file:
                    try:
                        with open(boundary_file, 'r', encoding='utf-8') as f:
                            boundary_content = f.read()
                            boundary_meta = frontmatter.loads(boundary_content)
                            if boundary_meta.metadata:
                                if 'value_stream' in boundary_meta.metadata:
                                    params['vs'] = boundary_meta.metadata['value_stream']
                                    params['value_stream'] = boundary_meta.metadata['value_stream']
                                if 'value_stream_fase' in boundary_meta.metadata:
                                    params['value_stream_fase'] = boundary_meta.metadata['value_stream_fase']
                                    fase_parts = boundary_meta.metadata['value_stream_fase'].split('.')
                                    if len(fase_parts) == 2:
                                        params['fase'] = fase_parts[1]
                    except Exception as e:
                        print(f"  ⚠ Kan boundary metadata niet lezen: {e}")
            print()
        
    else:
        params = parse_params(args.params) if args.params else {}
    
    # === GEMEENSCHAPPELIJKE FLOW ===
    
    metadata, prompt_content = load_prompt_file(args.prompt_file)

    input_content = ""
    input_files_content = {}
    template_paths = []
    charter_path = None

    minimal_mode = getattr(args, 'minimal', False)
    
    if not minimal_mode:
        if hasattr(args, 'input_file') and args.input_file:
            input_content = load_input_file(args.input_file)

        input_files_content, extracted_params, file_paths = load_and_process_input_files(metadata, params)

        template_paths = [path for key, path in file_paths.items() if 'template' in key.lower()]

        for key, value in extracted_params.items():
            if key not in params or not params[key]:
                params[key] = value
        
        _, charter_path = load_charter(args.prompt_file, metadata, params)
    
    skip_bootstrap = getattr(args, 'skip_bootstrap', False)
    if skip_bootstrap:
        print("[Info] Bootstrap overgeslagen via --skip-bootstrap.")
    else:
        method = getattr(args, 'method', 'manual')
        quiet = getattr(args, 'bootstrap_quiet', False)
        bootstrap_ok = run_bootstrap(metadata, args.prompt_file, method, params, workspace_config, quiet=quiet, 
                     charter_path=charter_path, template_paths=template_paths if template_paths else None)
        if not bootstrap_ok:
            print("ERROR: Bootstrap mislukt.")
            return 1
    
    if minimal_mode:
        minimal_template = getattr(args, 'minimal_template', 'temp/llm-minimal.md')
        minimal_content = load_minimal_template(minimal_template)
        if minimal_content is None:
            print("ERROR: Kon minimal template niet laden.")
            return 1
        final_prompt = replace_placeholders(minimal_content, params, "", None)
    else:
        final_prompt, _ = assemble_full_instructions(metadata, prompt_content, args.prompt_file, params, input_content, input_files_content)
    
    log_mode = getattr(args, 'log_mode', 'full')
    log_agent_instructions(metadata, params, final_prompt, args.prompt_file, log_mode)
    
    # Bepaal execution file pad
    no_save = getattr(args, 'no_save', False)
    execution_file_path = None
    
    if hasattr(args, 'execution_file') and args.execution_file:
        # Expliciet opgegeven execution file
        execution_file_path = args.execution_file
    elif not no_save:
        # Auto-genereer pad naar prompt-instructions/
        workspace_root = get_workspace_root()
        prompt_instructions_dir = workspace_root / "prompt-instructions"
        
        agent_name = metadata.get('agent', 'unknown').split('.')[-1]
        intent = metadata.get('intent', 'unknown')
        
        hash_input = datetime.now().strftime('%Y%m%d%H%M%S') + agent_name
        hash_digest = hashlib.md5(hash_input.encode('utf-8')).hexdigest()[:4]
        
        execution_file_path = str(prompt_instructions_dir / f"{hash_digest}.{agent_name}.{intent}.md")
    
    if execution_file_path:
        success = write_execution_file(execution_file_path, metadata, params, final_prompt)
        if not success:
            print("ERROR: Kon execution file niet schrijven.")
            return 1
        print()
        print(f"[OK] Execution file geschreven: {execution_file_path}")
    
    print()
    print("=" * 80)
    print("AGENT INSTRUCTIES")
    print("=" * 80)
    print()
    print(final_prompt)
    print()
    print("=" * 80)
    
    return 0


# ==============================================================================
# AGGREGEER-TASKS / MERGE helpers
# ==============================================================================

def load_task_file(file_path: Path) -> Dict:
    """Laad een task JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def transform_task_paths(task: Dict, relative_agent_path: str) -> Dict:
    """Transformeer paden in een task definitie naar relatieve paden.
    
    Zet 'artefacten/...' om naar '{relative_agent_path}/artefacten/...'
    zodat tasks vanuit de target workspace kunnen worden uitgevoerd.
    """
    task = task.copy()
    
    # Transformeer args array
    if 'args' in task:
        new_args = []
        for arg in task['args']:
            if isinstance(arg, str) and arg.startswith('artefacten/'):
                new_args.append(f"{relative_agent_path}/{arg}")
            else:
                new_args.append(arg)
        task['args'] = new_args
    
    # Transformeer command als het een pad is
    if 'command' in task and isinstance(task['command'], str):
        cmd = task['command']
        if cmd.startswith('artefacten/'):
            task['command'] = f"{relative_agent_path}/{cmd}"
    
    # Transformeer options.cwd indien aanwezig
    if 'options' in task and 'cwd' in task['options']:
        cwd = task['options']['cwd']
        if cwd.startswith('artefacten/'):
            task['options']['cwd'] = f"{relative_agent_path}/{cwd}"
    
    return task


def merge_tasks(tasks_folder: Path, workspace_root: Path, filter_fase: str = None) -> Dict:
    """Merge alle task files in folder naar één structuur."""
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
            }
        ]
    }
    
    task_files = sorted(tasks_folder.glob('*.json'))
    
    artefacten_folder = workspace_root / "artefacten"
    if artefacten_folder.exists():
        found = sorted(artefacten_folder.rglob('tasks/*.tasks.json'))
        if filter_fase:
            # Normalize filter: "aeo.02" -> "aeo-02" for filename matching
            normalized_filter = filter_fase.replace(".", "-")
            found = [f for f in found if normalized_filter in f.name]
        task_files.extend(found)
    
    print(f"Merge {len(task_files)} task files:")
    for task_file in task_files:
        try:
            rel_path = task_file.relative_to(workspace_root)
        except ValueError:
            rel_path = task_file.name
            
        print(f"  - {rel_path}")
        data = load_task_file(task_file)
        
        if 'tasks' in data:
            merged['tasks'].extend(data['tasks'])
            
        if 'inputs' in data:
            bestaande_ids = {inp['id'] for inp in merged.get('inputs', [])}
            for inp in data['inputs']:
                if inp['id'] not in bestaande_ids:
                    merged['inputs'].append(inp)
                    bestaande_ids.add(inp['id'])
    
    print(f"\nTotaal: {len(merged['tasks'])} tasks")
    return merged


def aggregeer_tasks_main(args: argparse.Namespace) -> int:
    """Hoofdfunctie voor aggregeer-tasks.

    Verwijdert de huidige tasks.json en bouwt deze opnieuw op:
    1. Altijd fnd.01 (fundamentele agents)
    2. Plus value_stream-fasen uit beleid-workspace.md
    
    Leest task-bestanden uit mandarin-agents (agent source).
    Schrijft naar de huidige workspace (cwd).
    Logt naar /logs met archivering van bestaande logs naar /logs/history.
    """
    agent_source = get_agent_source_root()
    target_workspace = get_target_workspace()
    
    # Setup logging in target workspace
    logs_dir = target_workspace / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Archiveer bestaande logs
    n_archived = archive_existing_logs(logs_dir, "aggregeer-tasks-")
    
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_file = logs_dir / f"aggregeer-tasks-{timestamp}.log"
    
    with open(log_file, "w", encoding="utf-8") as logf:
        original_stdout = sys.stdout
        sys.stdout = TeeWriter(original_stdout, logf)
        
        try:
            if n_archived > 0:
                print(f"Gearchiveerd: {n_archived} bestaande log(s) naar logs/history/")
                print()
            return _execute_aggregeer_tasks(args, agent_source, target_workspace, log_file)
        finally:
            sys.stdout = original_stdout


def _execute_aggregeer_tasks(args: argparse.Namespace, agent_source: Path, target_workspace: Path, log_file: Path) -> int:
    """Voer de eigenlijke aggregeer-tasks uit (met logging actief).
    
    Args:
        agent_source: Root van mandarin-agents (bron van task-bestanden)
        target_workspace: Doelworkspace (cwd) voor output en beleid
        log_file: Pad naar logbestand
    """
    output_file = Path(args.output_file) if args.output_file else target_workspace / '.vscode' / 'tasks.json'

    print("=" * 70)
    print(f"Aggregeer Tasks naar {output_file}")
    print(f"Bron: {agent_source}")
    print("=" * 70)
    print()

    # Verwijder bestaande tasks.json
    if output_file.exists() and not args.dry_run:
        output_file.unlink()
        print(f"✗ Verwijderd: {output_file}")
        print()

    # Lees beleid uit target workspace
    workspace_config = load_workspace_config()
    geconfigureerde_fasen = workspace_config.get('value_stream-fasen', [])

    # Bouw fasenlijst: fnd.01 altijd + geconfigureerde fasen
    fasen = ["fnd.01"]
    for fase in geconfigureerde_fasen:
        if fase not in fasen:
            fasen.append(fase)

    print(f"Fundamentele fase: fnd.01 (altijd)")
    print(f"Geconfigureerde fasen in beleid-workspace.md: {geconfigureerde_fasen}")
    print(f"Totaal te verwerken fasen: {fasen}")
    print()

    merged: Dict[str, Any] = {"version": "2.0.0", "tasks": [], "inputs": []}
    totaal_bestanden = 0
    artefacten_folder = agent_source / "artefacten"
    tasks_folder = target_workspace / '.vscode' / 'tasks'
    
    # Bereken relatief pad voor path-transformatie
    relative_agent_path = compute_relative_agent_path(target_workspace, agent_source)
    print(f"Relatief pad naar agent source: {relative_agent_path}")
    print()

    for fase in fasen:
        print(f"--- Fase: {fase} ---")
        fase_bestanden = 0

        if artefacten_folder.exists():
            normalized_filter = fase.replace(".", "-")
            found = sorted(f for f in artefacten_folder.rglob('tasks/*.tasks.json')
                           if normalized_filter in f.name)

            for task_file in found:
                try:
                    rel_path = task_file.relative_to(agent_source)
                except ValueError:
                    rel_path = task_file.name
                print(f"  + {rel_path}")
                data = load_task_file(task_file)
                if 'tasks' in data:
                    # Transformeer paden in elke task
                    for task in data['tasks']:
                        transformed = transform_task_paths(task, relative_agent_path)
                        merged['tasks'].append(transformed)
                if 'inputs' in data:
                    bestaande_ids = {inp['id'] for inp in merged['inputs']}
                    for inp in data['inputs']:
                        if inp['id'] not in bestaande_ids:
                            merged['inputs'].append(inp)
                            bestaande_ids.add(inp['id'])
                fase_bestanden += 1

        if fase_bestanden == 0:
            print(f"  (geen task-bestanden gevonden voor {fase})")
        totaal_bestanden += fase_bestanden
        print()

    if tasks_folder.exists():
        handmatig = sorted(tasks_folder.glob('*.json'))
        if handmatig:
            print("--- Handmatige tasks (.vscode/tasks/) ---")
            for task_file in handmatig:
                print(f"  + {task_file.name}")
                data = load_task_file(task_file)
                if 'tasks' in data:
                    merged['tasks'].extend(data['tasks'])
                if 'inputs' in data:
                    bestaande_ids = {inp['id'] for inp in merged['inputs']}
                    for inp in data['inputs']:
                        if inp['id'] not in bestaande_ids:
                            merged['inputs'].append(inp)
                            bestaande_ids.add(inp['id'])
                totaal_bestanden += 1
            print()

    print(f"Totaal: {len(merged['tasks'])} tasks uit {totaal_bestanden} bestanden")

    if totaal_bestanden == 0:
        print("ERROR: Geen task-bestanden gevonden voor geconfigureerde fasen.")
        return 1

    if args.dry_run:
        print(f"\n[DRY-RUN] Zou schrijven naar: {output_file}")
        print(f"[DRY-RUN] {len(merged['tasks'])} tasks, {len(merged['inputs'])} inputs")
        print(f"Log: {log_file.relative_to(target_workspace)}")
        return 0

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Geschreven naar: {output_file}")
    print(f"Log: {log_file.relative_to(target_workspace)}")
    print("=" * 70)
    return 0


# ==============================================================================
# FETCH-AGENTS: Agent Discovery en Distribution
# ==============================================================================

def parse_value_stream_fase(value: str) -> Tuple[str, str]:
    """Parseer 'aeo.02' -> ('aeo', '02')."""
    if "." not in value:
        raise ValueError(f"Gebruik formaat <code>.<fase>, bijv. aeo.02 (gegeven: {value!r})")
    code, fase = value.split(".", 1)
    code = code.strip().lower()
    fase = fase.strip().zfill(2)
    if not code.isalpha() or not fase.isdigit():
        raise ValueError(f"Ongeldige value stream fase: {value!r}")
    return code, fase


def find_fase_dirs(artefacten_root: Path, code: str, fase: str) -> List[Path]:
    """Geeft alle mappen terug van de vorm artefacten/<code>/<code>.<fase>.<agent>/."""
    base = artefacten_root / code
    if not base.is_dir():
        return []
    prefix = f"{code}.{fase}."
    return sorted(p for p in base.iterdir() if p.is_dir() and p.name.startswith(prefix))


def discover_agents(workspace_root: Path, value_stream: str = None, fase: str = None) -> List[Dict]:
    """
    Discover all agents in the artefacten folder structure.
    
    Returns list of dicts with agent metadata.
    """
    agents = []
    artefacten_path = workspace_root / "artefacten"
    
    if not artefacten_path.exists():
        return agents
    
    for vs_dir in artefacten_path.iterdir():
        if not vs_dir.is_dir():
            continue
        if value_stream and vs_dir.name != value_stream:
            continue
        
        for agent_dir in vs_dir.iterdir():
            if not agent_dir.is_dir():
                continue
            
            # Parse agent folder name: <code>.<fase>.<agent-name>
            parts = agent_dir.name.split(".", 2)
            if len(parts) < 3:
                continue
            
            agent_code, agent_fase, agent_name = parts
            
            # Filter on fase if specified
            if fase and agent_fase != fase:
                continue
            
            # Check for charter file
            charter_file = agent_dir / f"{agent_name}.charter.md"
            boundary_file = agent_dir / f"{agent_name}.agent-boundary.md"
            
            # Collect metadata
            agent_info = {
                "name": agent_name,
                "id": agent_dir.name,
                "value_stream": vs_dir.name,
                "fase": agent_fase,
                "path": str(agent_dir),
                "has_charter": charter_file.exists(),
                "has_boundary": boundary_file.exists(),
                "has_runner": (agent_dir / "runner").exists(),
                "has_prompts": (agent_dir / "prompts").exists(),
                "has_templates": (agent_dir / "templates").exists(),
                "has_tasks": (agent_dir / "tasks").exists(),
            }
            
            # Count files if dirs exist
            if agent_info["has_prompts"]:
                agent_info["prompt_count"] = len(list((agent_dir / "prompts").glob("*.prompt.md")))
            if agent_info["has_templates"]:
                agent_info["template_count"] = len(list((agent_dir / "templates").glob("*")))
            if agent_info["has_tasks"]:
                agent_info["task_count"] = len(list((agent_dir / "tasks").glob("*.tasks.json")))
            
            agents.append(agent_info)
    
    return sorted(agents, key=lambda a: a["id"])


def collect_agent_files(fase_dirs: List[Path]) -> Tuple[List[Tuple[Path, str]], List[Tuple[Path, str]]]:
    """
    Zoek alle prompt- en agent-bestanden in de fase-mappen.
    Retourneert (prompts, contracts) als lijsten van (src_path, dest_name).
    """
    prompts: List[Tuple[Path, str]] = []
    contracts: List[Tuple[Path, str]] = []

    for fase_dir in fase_dirs:
        prompts_dir = fase_dir / "prompts"
        if prompts_dir.is_dir():
            for f in sorted(prompts_dir.glob("*.prompt.md")):
                prompts.append((f, f.name))

        contracts_dir = fase_dir / "agent-contracten"
        if contracts_dir.is_dir():
            for f in sorted(contracts_dir.glob("*.agent.md")):
                contracts.append((f, f.name))

    return prompts, contracts


def copy_agent_files(
    items: List[Tuple[Path, str]],
    target_dir: Path,
    dry_run: bool,
    label: str,
) -> List[str]:
    """Kopieer bestanden naar target_dir; retourneert lijst van gekopieerde namen."""
    copied: List[str] = []
    if not items:
        return copied
    if not dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)

    for src, name in items:
        dest = target_dir / name
        copied.append(name)
        if dry_run:
            print(f"  [dry] {label}: {src.name}")
        else:
            shutil.copy2(src, dest)
            print(f"  OK {label}: {src.name}")

    return copied


def collect_task_files_for_fetch(fase_dirs: List[Path]) -> List[Path]:
    """Zoek alle *.tasks.json bestanden in tasks/-submappen."""
    found: List[Path] = []
    for fase_dir in fase_dirs:
        tasks_dir = fase_dir / "tasks"
        if tasks_dir.is_dir():
            found.extend(sorted(tasks_dir.glob("*.tasks.json")))
    return found


def strip_jsonc_comments(content: str) -> str:
    """Verwijder JSONC-commentaar, string-aware (slaat string-literals over)."""
    result: List[str] = []
    i, n = 0, len(content)
    in_string = False
    while i < n:
        c = content[i]
        if in_string:
            if c == "\\" and i + 1 < n:
                result.append(c)
                result.append(content[i + 1])
                i += 2
                continue
            if c == '"':
                in_string = False
            result.append(c)
            i += 1
        else:
            if c == '"':
                in_string = True
                result.append(c)
                i += 1
            elif c == "/" and i + 1 < n and content[i + 1] == "/":
                while i < n and content[i] != "\n":
                    i += 1
            elif c == "/" and i + 1 < n and content[i + 1] == "*":
                i += 2
                while i < n - 1 and not (content[i] == "*" and content[i + 1] == "/"):
                    i += 1
                i += 2
            else:
                result.append(c)
                i += 1
    return "".join(result)


def load_tasks_json_file(path: Path) -> Dict:
    """Laad tasks.json met JSONC-support."""
    if not path.exists():
        return {"version": "2.0.0", "tasks": [], "inputs": []}
    raw = path.read_text(encoding="utf-8")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return json.loads(strip_jsonc_comments(raw))


def load_artefact_tasks(task_files: List[Path]) -> Tuple[List[Dict], List[Dict]]:
    """Laad alle tasks + inputs vanuit artefact task-bestanden."""
    all_tasks: List[Dict] = []
    all_inputs: List[Dict] = []
    seen_labels: Set[str] = set()

    for f in task_files:
        try:
            data = json.loads(strip_jsonc_comments(f.read_text(encoding="utf-8")))
        except Exception as e:
            print(f"  WAARSCHUWING: Kan {f.name} niet lezen: {e}", file=sys.stderr)
            continue
        for task in data.get("tasks", []):
            label = task.get("label", "")
            if label in seen_labels:
                print(f"  WAARSCHUWING: Duplicate label '{label}' in {f.name} -- overgeslagen")
                continue
            seen_labels.add(label)
            all_tasks.append(task)
        all_inputs.extend(data.get("inputs", []))

    return all_tasks, all_inputs


def extract_input_ids_from_tasks(tasks: List[Dict]) -> Set[str]:
    """Extract input IDs referenced in tasks."""
    blob = json.dumps(tasks, ensure_ascii=False)
    return set(re.findall(r"\$\{input:([^}]+)\}", blob))


def merge_tasks_into_target_file(
    target: Dict,
    new_tasks: List[Dict],
    new_inputs: List[Dict],
) -> Tuple[int, int, int]:
    """Merge nieuwe tasks en inputs in target dict. Retourneert (added, replaced, inputs_changed)."""
    existing_by_label: Dict[str, Dict] = {
        str(t.get("label", "")): t for t in target.get("tasks", [])
    }
    added = replaced = 0

    for task in new_tasks:
        label = str(task.get("label", ""))
        if label in existing_by_label:
            replaced += 1
        else:
            added += 1
        existing_by_label[label] = task

    target["tasks"] = list(existing_by_label.values())

    required_ids = extract_input_ids_from_tasks(new_tasks)
    existing_inputs: Dict[str, Dict] = {
        str(i.get("id", "")): i for i in target.get("inputs", []) if i.get("id")
    }
    source_inputs: Dict[str, Dict] = {
        str(i.get("id", "")): i for i in new_inputs if i.get("id")
    }

    inputs_changed = 0
    for iid in required_ids:
        src = source_inputs.get(iid)
        if not src:
            continue
        if existing_inputs.get(iid) != src:
            existing_inputs[iid] = src
            inputs_changed += 1

    target["inputs"] = sorted(existing_inputs.values(), key=lambda i: str(i.get("id", "")))
    return added, replaced, inputs_changed


def list_agents_main(args: argparse.Namespace) -> int:
    """Toon beschikbare agents per value stream fase."""
    
    workspace_root = get_workspace_root()
    
    value_stream = None
    fase = None
    
    if args.value_stream_fase:
        try:
            value_stream, fase = parse_value_stream_fase(args.value_stream_fase)
        except ValueError as e:
            print(f"ERROR: {e}")
            return 1
    
    print("=" * 80)
    print("BESCHIKBARE AGENTS")
    if args.value_stream_fase:
        print(f"Filter: {args.value_stream_fase}")
    print("=" * 80)
    print()
    
    agents = discover_agents(workspace_root, value_stream, fase)
    
    if not agents:
        print("Geen agents gevonden.")
        return 0
    
    # Group by value stream
    by_vs: Dict[str, List[Dict]] = {}
    for agent in agents:
        vs = agent["value_stream"]
        if vs not in by_vs:
            by_vs[vs] = []
        by_vs[vs].append(agent)
    
    if args.output_format == "json":
        print(json.dumps(agents, indent=2, ensure_ascii=False))
        return 0
    
    # Markdown table output
    for vs in sorted(by_vs.keys()):
        print(f"## {vs.upper()}")
        print()
        print("| Agent | Fase | Charter | Runner | Prompts | Templates |")
        print("|-------|------|---------|--------|---------|-----------|")
        for agent in by_vs[vs]:
            charter = "✓" if agent["has_charter"] else "-"
            runner = "✓" if agent["has_runner"] else "-"
            prompts = str(agent.get("prompt_count", 0)) if agent["has_prompts"] else "-"
            templates = str(agent.get("template_count", 0)) if agent["has_templates"] else "-"
            print(f"| {agent['name']} | {agent['fase']} | {charter} | {runner} | {prompts} | {templates} |")
        print()
    
    print(f"Totaal: {len(agents)} agents")
    return 0


def fetch_agents_main(args: argparse.Namespace) -> int:
    """Haal prompts, agents en tasks op voor een value stream fase."""
    
    try:
        code, fase = parse_value_stream_fase(args.value_stream_fase)
    except ValueError as e:
        print(f"ERROR: {e}")
        return 1
    
    # Determine source and target
    source_root = Path(args.source).expanduser().resolve() if args.source else get_workspace_root()
    
    target_root = Path(args.target).expanduser().resolve() if args.target else source_root
    artefacten_root = source_root / "artefacten"
    
    if not artefacten_root.is_dir():
        print(f"ERROR: artefacten/ map ontbreekt in {source_root}")
        return 1
    
    print("=" * 80)
    print(f"FETCH AGENTS: {code}.{fase}")
    print("=" * 80)
    print(f"Bron:  {source_root}")
    print(f"Doel:  {target_root}")
    print()
    
    fase_dirs = find_fase_dirs(artefacten_root, code, fase)
    if not fase_dirs:
        print(f"WAARSCHUWING: Geen agent-mappen gevonden voor {code}.{fase}")
        return 1
    
    agents_found = [d.name.split(".", 2)[2] for d in fase_dirs]
    print(f"Gevonden agents ({len(fase_dirs)}): {', '.join(agents_found)}")
    print()
    
    # Collect and copy prompts and contracts
    prompts, contracts = collect_agent_files(fase_dirs)
    
    print(f"Prompts ({len(prompts)}):")
    copied_prompts = copy_agent_files(
        prompts, 
        target_root / ".github" / "prompts", 
        args.dry_run, 
        "prompt"
    )
    if not prompts:
        print("  (geen)")
    
    print(f"\nAgents ({len(contracts)}):")
    copied_contracts = copy_agent_files(
        contracts, 
        target_root / ".github" / "agents", 
        args.dry_run, 
        "agent"
    )
    if not contracts:
        print("  (geen)")
    
    # Merge tasks
    task_files = collect_task_files_for_fetch(fase_dirs)
    print(f"\nTasks-bestanden ({len(task_files)}):")
    
    tasks_added = tasks_replaced = inputs_changed = 0
    if task_files:
        artefact_tasks, artefact_inputs = load_artefact_tasks(task_files)
        if artefact_tasks:
            target_tasks_path = target_root / ".vscode" / "tasks.json"
            target_tasks = load_tasks_json_file(target_tasks_path)
            tasks_added, tasks_replaced, inputs_changed = merge_tasks_into_target_file(
                target_tasks, artefact_tasks, artefact_inputs
            )
            if not args.dry_run:
                target_tasks_path.parent.mkdir(parents=True, exist_ok=True)
                target_tasks_path.write_text(
                    json.dumps(target_tasks, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
            for f in task_files:
                prefix = "[dry] " if args.dry_run else ""
                print(f"  OK {prefix}{f.parent.parent.name}/tasks/{f.name}")
    else:
        print("  (geen)")
    
    # Summary
    mode = "[DRY-RUN] " if args.dry_run else ""
    print(f"\n{'-'*60}")
    print(f"{mode}Klaar voor {code}.{fase}")
    print(f"  Prompts gekopieerd : {len(copied_prompts)}")
    print(f"  Agents gekopieerd  : {len(copied_contracts)}")
    print(f"  Tasks toegevoegd   : {tasks_added}")
    print(f"  Tasks vervangen    : {tasks_replaced}")
    print(f"  Inputs bijgewerkt  : {inputs_changed}")
    print()
    
    return 0


# ==============================================================================
# VALIDEER-AGENT-STRUCTUUR
# ==============================================================================

def valideer_agent_structuur_main(args: argparse.Namespace) -> int:
    """Valideer agent folder structuur tegen doctrine."""

    artefacten = Path("artefacten")
    if not artefacten.exists():
        print("ERROR: artefacten/ folder niet gevonden")
        return 1

    # Verzamel te valideren agent-folders
    if args.agent_naam:
        agent_folders = []
        for folder in artefacten.rglob(f"*.{args.agent_naam}"):
            if folder.is_dir():
                agent_folders.append(folder)
                break
        if not agent_folders:
            print(f"ERROR: Agent folder niet gevonden voor '{args.agent_naam}'")
            return 1
    else:
        # Alle agents in value_stream_fase (of alle agents als geen fase gegeven)
        vs_fase = getattr(args, 'value_stream_fase', None)
        agent_folders = []
        for folder in sorted(artefacten.rglob("*.runner.py")):
            agent_folder = folder.parent.parent
            if agent_folder not in agent_folders and agent_folder.is_dir():
                if vs_fase and vs_fase not in str(agent_folder):
                    continue
                agent_folders.append(agent_folder)
        if not agent_folders:
            print("Geen agent-folders gevonden.")
            return 1

    overall_exit = 0
    for agent_folder in agent_folders:
        exit_code = _valideer_agent_folder(agent_folder)
        if exit_code != 0:
            overall_exit = exit_code
    return overall_exit


def _valideer_agent_folder(agent_folder: Path) -> int:
    """Valideer één agent-folder en return exit code."""
    print("=" * 80)
    print(f"VALIDEER AGENT STRUCTUUR: {agent_folder.name}")
    print("=" * 80)
    print()

    agent_naam = agent_folder.name.split(".", 2)[-1] if "." in agent_folder.name else agent_folder.name

    print(f"Agent folder: {agent_folder}")
    print()
    
    # Verwachte structuur
    required_files = [
        f"{agent_naam}.charter.md",
        f"{agent_naam}.agent-boundary.md",
    ]
    
    required_folders = [
        "agent-contracten",
        "prompts",
        "runner",
        "tasks",
    ]
    
    issues = []
    successes = []
    
    # Check required files
    print("Controleer verplichte bestanden:")
    for req_file in required_files:
        file_path = agent_folder / req_file
        if file_path.exists():
            successes.append(f"  ✓ {req_file}")
        else:
            issues.append(f"  ✗ {req_file} ONTBREEKT")
    
    for msg in successes + issues:
        print(msg)
    print()
    
    # Check required folders
    print("Controleer verplichte folders:")
    folder_issues = []
    folder_successes = []
    for req_folder in required_folders:
        folder_path = agent_folder / req_folder
        if folder_path.exists() and folder_path.is_dir():
            folder_successes.append(f"  ✓ {req_folder}/")
        else:
            folder_issues.append(f"  ✗ {req_folder}/ ONTBREEKT")
    
    for msg in folder_successes + folder_issues:
        print(msg)
    issues.extend(folder_issues)
    print()
    
    # Check agent-contracten content
    contracten_folder = agent_folder / "agent-contracten"
    if contracten_folder.exists():
        contracts = list(contracten_folder.glob("*.agent.md"))
        print(f"Agent contracten: {len(contracts)} gevonden")
        for contract in contracts:
            print(f"  - {contract.name}")
    print()
    
    # Check prompts content
    prompts_folder = agent_folder / "prompts"
    if prompts_folder.exists():
        prompts = list(prompts_folder.glob("*.prompt.md"))
        print(f"Prompts: {len(prompts)} gevonden")
        for prompt in prompts:
            print(f"  - {prompt.name}")
    print()
    
    # Check runner
    runner_folder = agent_folder / "runner"
    if runner_folder.exists():
        runners = list(runner_folder.glob("*.runner.py"))
        print(f"Runner: {len(runners)} gevonden")
        for runner in runners:
            print(f"  - {runner.name}")
        if len(runners) != 1:
            issues.append(f"  ⚠ Verwacht exact 1 runner (One Agent, One Runner doctrine)")
    print()
    
    # Summary
    print("=" * 80)
    if issues:
        print(f"VALIDATIE: {len(issues)} issue(s) gevonden")
        for issue in issues:
            print(issue)
        return 1
    else:
        print("VALIDATIE: ✓ Agent structuur voldoet aan doctrine")
        return 0


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Runner voor agent: ecosysteem-coordinator",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="subcommand", required=True, help="Beschikbare intents")

    # consulteer-canon
    p_canon = subparsers.add_parser("consulteer-canon", help="Raadpleeg de canon en log SHA")
    p_canon.add_argument("--agent", required=True, help="Agent naam")
    p_canon.add_argument("--value-stream", required=True, help="Value stream code (bijv. aeo)")
    p_canon.add_argument("--intent", required=True, help="Intent naam")
    p_canon.add_argument("--canon-path", help="Pad naar lokale canon directory")
    p_canon.add_argument("--grondslagen", help="Komma-gescheiden lijst van grondslagen")
    p_canon.add_argument("--canon-github-url", help="GitHub URL voor canon repository")

    # genereer-instructies
    p_gen = subparsers.add_parser("genereer-instructies", help="Genereer execution-ready agent-instructies")
    p_gen.add_argument("prompt_file", type=str, nargs='?', help="Pad naar prompt bestand (optioneel)")
    p_gen.add_argument("--agent", type=str, help="Agent naam voor auto-discovery")
    p_gen.add_argument("--intent", type=str, help="Intent naam voor auto-discovery")
    p_gen.add_argument("-p", "--param", action="append", dest="params", default=[], help="Parameter key=value")
    p_gen.add_argument("--input-file", type=str, help="Pad naar input bestand")
    p_gen.add_argument("--method", type=str, default="manual", choices=["manual", "runner", "pipeline"])
    p_gen.add_argument("--execution-file", type=str, help="Output execution file")
    p_gen.add_argument("--minimal", action="store_true", help="Minimal mode")
    p_gen.add_argument("--minimal-template", type=str, default="temp/llm-minimal.md")
    p_gen.add_argument("--skip-bootstrap", action="store_true", help="Skip canon bootstrap")
    p_gen.add_argument("--log-mode", type=str, default="full", choices=["full", "compact"])
    p_gen.add_argument("--bootstrap-quiet", action="store_true", help="Compacte bootstrap output")
    p_gen.add_argument("--no-save", action="store_true", help="Schrijf geen execution file naar prompt-instructions/")

    # aggregeer-tasks
    p_activeer = subparsers.add_parser("aggregeer-tasks", help="Aggregeer tasks op basis van beleid-workspace.md value_stream-fasen")
    p_activeer.add_argument("--output-file", type=str, help="Output bestand (default: .vscode/tasks.json)")
    p_activeer.add_argument("--dry-run", action="store_true", help="Toon wat gedaan zou worden")

    # valideer-agent-structuur
    p_val = subparsers.add_parser("valideer-agent-structuur", help="Valideer agent folder structuur")
    p_val.add_argument("--agent-naam", required=False, default=None, help="Agent naam om te valideren (leeg = alle agents in value_stream_fase)")
    p_val.add_argument("--value-stream-fase", help="Value stream fase")
    p_val.add_argument("--output-format", type=str, default="markdown", choices=["markdown", "json"])
    p_val.add_argument("--strict", action="store_true", help="Stricte validatie")

    # list-agents
    p_list = subparsers.add_parser("list-agents", help="Toon beschikbare agents per value stream fase")
    p_list.add_argument("value_stream_fase", nargs="?", help="Filter op value stream fase (bijv. aeo.02)")
    p_list.add_argument("--output-format", type=str, default="markdown", choices=["markdown", "json"])

    # fetch-agents
    p_fetch = subparsers.add_parser("fetch-agents", help="Haal prompts, agents en tasks op voor een value stream fase")
    p_fetch.add_argument("value_stream_fase", help="Value stream fase (bijv. aeo.02, fnd.02, sfw.03)")
    p_fetch.add_argument("--source", type=str, help="Pad naar mandarin-agents bron (default: workspace root)")
    p_fetch.add_argument("--target", type=str, help="Doel workspace (default: zelfde als source)")
    p_fetch.add_argument("--dry-run", action="store_true", help="Toon wat gedaan zou worden zonder te schrijven")

    args = parser.parse_args()

    if args.subcommand == "consulteer-canon":
        sys.exit(consulteer_canon_main(args))
    elif args.subcommand == "genereer-instructies":
        sys.exit(genereer_instructies_main(args))
    elif args.subcommand == "aggregeer-tasks":
        sys.exit(aggregeer_tasks_main(args))
    elif args.subcommand == "valideer-agent-structuur":
        sys.exit(valideer_agent_structuur_main(args))
    elif args.subcommand == "list-agents":
        sys.exit(list_agents_main(args))
    elif args.subcommand == "fetch-agents":
        sys.exit(fetch_agents_main(args))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
