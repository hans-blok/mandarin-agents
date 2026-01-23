#!/usr/bin/env python3
"""
Initialize a workspace according to the workspace doctrine.

This script sets up a new workspace by:
1. Creating the required folder structure
2. Fetching fetch_agents.py and fetch-agents.bat from mandarin-agents repository
3. Creating .gitignore and workspace policy

Usage:
    python init-workspace.py
    python init-workspace.py <value-stream>
    python init-workspace.py kennispublicatie
    python init-workspace.py --help

Requirements:
    - Python 3.9+
    - Internet connection (to download fetch scripts)

Assumptions:
    - Running from the target workspace directory
    - GitHub raw content URLs are accessible

Design Decisions:
    - Downloads fetch scripts from mandarin-agents main branch
    - Uses urllib (standard library) to avoid external dependencies
    - Idempotent: safe to run multiple times
    - Follows Code Complete principles: defensive programming, clear contracts
"""

from __future__ import annotations

import argparse
import sys
import urllib.request
import urllib.error
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class WorkspaceConfig:
    """Configuration for workspace initialization."""
    
    value_stream: Optional[str] = None
    
    # GitHub raw content base URL
    github_base_url: str = "https://raw.githubusercontent.com/hans-blok/mandarin-agents/main"
    
    # Required folders per workspace doctrine
    required_folders: List[str] = None
    
    def __post_init__(self) -> None:
        """Initialize default folder structure."""
        if self.required_folders is None:
            self.required_folders = [
                ".github/prompts",
                "charters-agents",
                "scripts/runners",
                "docs/resultaten",
                "logs",
                "temp",
            ]


class InitializationError(Exception):
    """Raised when workspace initialization fails."""
    pass


def create_folder_structure(
    workspace: Path, 
    folders: List[str]
) -> None:
    """
    Create required workspace folder structure.
    
    Idempotent: safe to call multiple times. Existing folders are preserved.
    
    Args:
        workspace: Workspace root directory
        folders: List of folder paths relative to workspace root
    """
    print("[INFO] Creating folder structure...")
    
    created = 0
    existing = 0
    
    for folder in folders:
        folder_path = workspace / folder
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"  [CREATE] {folder}/")
            created += 1
        else:
            existing += 1
    
    print(f"[OK] Folder structure ready ({created} created, {existing} existed)")


def fetch_scripts_from_github(
    workspace: Path,
    github_base_url: str
) -> None:
    """
    Download fetch_agents.py and fetch-agents.bat from mandarin-agents repository.
    
    Args:
        workspace: Workspace root directory
        github_base_url: Base URL for GitHub raw content
        
    Raises:
        InitializationError: If download fails
    """
    print("[INFO] Downloading fetch scripts from mandarin-agents...")
    
    # Define files to download and their destinations
    files_to_fetch = [
        {
            "url": f"{github_base_url}/scripts/workspace-tools/fetch_agents.py",
            "destination": workspace / "scripts" / "fetch_agents.py",
            "name": "fetch_agents.py"
        },
        {
            "url": f"{github_base_url}/scripts/workspace-tools/fetch-agents.bat",
            "destination": workspace / "fetch-agents.bat",
            "name": "fetch-agents.bat"
        }
    ]
    
    for file_info in files_to_fetch:
        url = file_info["url"]
        destination = file_info["destination"]
        name = file_info["name"]
        
        try:
            print(f"  [DOWNLOAD] {name}...")
            
            # Download file
            with urllib.request.urlopen(url, timeout=30) as response:
                content = response.read()
            
            # Ensure parent directory exists
            destination.parent.mkdir(parents=True, exist_ok=True)
            
            # Write to destination
            destination.write_bytes(content)
            
            print(f"  [OK] {name} -> {destination.relative_to(workspace)}")
            
        except urllib.error.HTTPError as e:
            raise InitializationError(
                f"Failed to download {name}: HTTP {e.code} {e.reason}\n"
                f"URL: {url}\n"
                f"Check if the file exists in mandarin-agents repository."
            ) from e
        except urllib.error.URLError as e:
            raise InitializationError(
                f"Failed to download {name}: Network error\n"
                f"Reason: {e.reason}\n"
                f"Check your internet connection."
            ) from e
        except (OSError, IOError) as e:
            raise InitializationError(
                f"Failed to write {name} to {destination}: {e}"
            ) from e
    
    print(f"[OK] Fetch scripts downloaded successfully")


def create_gitignore(workspace: Path) -> None:
    """
    Create or update .gitignore file in workspace root.
    
    Ensures that logs/ and temp/ directories are ignored by Git.
    Preserves existing entries if .gitignore already exists.
    
    Args:
        workspace: Workspace root directory
    """
    print("[INFO] Creating/updating .gitignore...")
    
    gitignore_path = workspace / ".gitignore"
    
    # Entries that must be present
    required_entries = {
        "logs/",
        "temp/",
    }
    
    existing_lines = set()
    if gitignore_path.exists():
        try:
            content = gitignore_path.read_text(encoding="utf-8")
            existing_lines = {line.strip() for line in content.splitlines() if line.strip()}
            print("  [INFO] Existing .gitignore found, will preserve entries")
        except (OSError, IOError) as e:
            print(f"  [WARN] Could not read existing .gitignore: {e}")
    
    # Determine what needs to be added
    missing_entries = required_entries - existing_lines
    
    if not missing_entries and gitignore_path.exists():
        print("  [SKIP] .gitignore already contains logs/ and temp/")
        return
    
    # Build new content
    gitignore_content_parts = []
    
    # Preserve existing content
    if existing_lines:
        gitignore_content_parts.append("\n".join(sorted(existing_lines)))
    
    # Add new entries with header
    if missing_entries:
        if existing_lines:
            gitignore_content_parts.append("")  # Empty line separator
        gitignore_content_parts.append("# Workspace generated files and logs")
        gitignore_content_parts.extend(sorted(missing_entries))
    
    gitignore_content = "\n".join(gitignore_content_parts) + "\n"
    
    try:
        gitignore_path.write_text(gitignore_content, encoding="utf-8")
        if missing_entries:
            print(f"  [UPDATE] Added {len(missing_entries)} entries to .gitignore")
        else:
            print(f"  [CREATE] .gitignore")
    except (OSError, IOError) as e:
        print(f"  [WARN] Could not create/update .gitignore: {e}")


def create_beleid_workspace(
    workspace: Path,
    value_stream: str
) -> None:
    """
    Create beleid-workspace.md in workspace root.
    
    This file describes workspace-specific policy.
    
    Args:
        workspace: Workspace root directory
        value_stream: Value stream name for this workspace
    """
    print("[INFO] Creating beleid-workspace.md...")
    
    beleid_path = workspace / "beleid-workspace.md"
    
    # Don't overwrite existing policy
    if beleid_path.exists():
        print("  [SKIP] beleid-workspace.md already exists")
        return
    
    beleid_content = f"""# Beleid voor de {value_stream} workspace

Deze workspace hoort bij de waardestroom **{value_stream}**.

## Scope

- Deze workspace gaat over: [beschrijf hier de scope van je value stream]
- Andere domeinen vallen buiten deze workspace en horen in andere repositories.

## Folder Structuur

De workspace heeft de volgende standaard structuur:

```
.github/prompts/      # Agent prompts
charters-agents/      # Agent charters
scripts/runners/      # Agent runner scripts
docs/resultaten/      # Output van agents
logs/                 # Log bestanden (niet in Git)
temp/                 # Tijdelijke bestanden (niet in Git)
```

## Dit beleid is workspace-specifiek

Dit beleid beschrijft de workspace-specifieke scope en werkafspraken.
Pas dit document aan naar jouw specifieke behoeften.
"""
    
    try:
        beleid_path.write_text(beleid_content, encoding="utf-8")
        print(f"  [CREATE] beleid-workspace.md")
    except (OSError, IOError) as e:
        print(f"  [WARN] Could not create beleid-workspace.md: {e}")


def initialize_workspace(config: WorkspaceConfig) -> None:
    """
    Main initialization workflow.
    
    Args:
        config: Workspace configuration
        
    Raises:
        InitializationError: If any initialization step fails
    """
    workspace = Path.cwd()
    
    print("=" * 70)
    print("WORKSPACE INITIALIZATION")
    print("=" * 70)
    print(f"Value stream: {config.value_stream or '(niet opgegeven)'}")
    print(f"Workspace: {workspace}")
    print()
    
    # Step 1: Create folder structure
    print("[STEP 1] Creating folder structure...")
    create_folder_structure(workspace, config.required_folders)
    print()
    
    # Step 2: Download fetch scripts
    print("[STEP 2] Downloading fetch scripts...")
    try:
        fetch_scripts_from_github(workspace, config.github_base_url)
    except InitializationError as e:
        raise InitializationError(
            f"Failed to download fetch scripts: {e}\n"
            f"The workspace can function without these, but you'll need to add them manually."
        ) from e
    print()
    
    # Step 3: Create .gitignore
    print("[STEP 3] Setting up .gitignore...")
    create_gitignore(workspace)
    print()
    
    # Step 4: Create workspace policy (only if value stream specified)
    if config.value_stream:
        print("[STEP 4] Creating workspace policy...")
        create_beleid_workspace(workspace, config.value_stream)
        print()
    else:
        print("[STEP 4] Skipping workspace policy (no value stream specified)...")
        print()
    
    # Success summary
    print("=" * 70)
    print("✓ WORKSPACE INITIALIZATION COMPLETE")
    print("=" * 70)
    print()
    print("Workspace structure created:")
    print(f"  .github/prompts/    - Agent prompts")
    print(f"  charters-agents/    - Agent charters")
    print(f"  scripts/")
    print(f"    fetch_agents.py   - Fetch agents script")
    print(f"    runners/          - Agent runner scripts")
    print(f"  docs/resultaten/    - Output van agents")
    print(f"  logs/               - Log bestanden (ignored by Git)")
    print(f"  temp/               - Tijdelijke bestanden (ignored by Git)")
    print(f"  fetch-agents.bat    - Windows wrapper for fetch_agents.py")
    print(f"  .gitignore          - Git ignore configuration")
    if config.value_stream:
        print(f"  beleid-workspace.md - Workspace policy")
    print()
    print("Next steps:")
    if config.value_stream:
        print(f"  1. Review and customize beleid-workspace.md")
        print(f"  2. Fetch agents: fetch-agents.bat {config.value_stream}")
        print(f"  3. Add your scripts and documentation")
        print(f"  4. Initialize Git repository if needed: git init")
    else:
        print(f"  1. Create beleid-workspace.md for your workspace")
        print(f"  2. Fetch agents when ready: fetch-agents.bat <value-stream>")
        print(f"  3. Add your scripts and documentation")
        print(f"  4. Initialize Git repository if needed: git init")
    print()


def main() -> int:
    """
    Main entry point for workspace initialization.
    
    Returns:
        Exit code: 0 for success, 1 for failure
    """
    parser = argparse.ArgumentParser(
        description="Initialize a workspace by creating folder structure and fetching tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python init-workspace.py
  python init-workspace.py kennispublicatie
  python init-workspace.py architectuur-en-oplossingsontwerp
  
The script will:
  1. Create required folder structure (.github/prompts, scripts/runners, etc.)
  2. Download fetch_agents.py and fetch-agents.bat from mandarin-agents
  3. Create .gitignore with logs/ and temp/
  4. Create beleid-workspace.md template (if value stream provided)
        """
    )
    
    parser.add_argument(
        "value_stream",
        nargs="?",
        default=None,
        help="Value stream name for this workspace (e.g., kennispublicatie). Optional."
    )
    
    args = parser.parse_args()
    
    # Validate value stream name (if provided)
    value_stream = None
    if args.value_stream:
        value_stream = args.value_stream.strip().lower()
        if "/" in value_stream or "\\" in value_stream:
            print("[ERROR] Invalid value stream name")
            return 1
    
    config = WorkspaceConfig(
        value_stream=value_stream
    )
    
    try:
        initialize_workspace(config)
        return 0
    except InitializationError as e:
        print()
        print("=" * 70)
        print("✗ INITIALIZATION FAILED")
        print("=" * 70)
        print(f"Error: {e}")
        print()
        print("Troubleshooting:")
        print("  - Check internet connection (needed for downloading fetch scripts)")
        print("  - Ensure you have write permissions in current directory")
        print("  - Check available disk space")
        print("  - Verify GitHub is accessible: https://github.com/hans-blok/mandarin-agents")
        return 1
    except KeyboardInterrupt:
        print()
        print("[ABORT] Initialization cancelled by user")
        return 1
    except Exception as e:
        print()
        print("=" * 70)
        print("✗ UNEXPECTED ERROR")
        print("=" * 70)
        print(f"Error: {e}")
        print()
        print("Please report this issue with the full error message.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
