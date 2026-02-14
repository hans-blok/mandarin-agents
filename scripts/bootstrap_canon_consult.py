"""
Bootstrap Canon Consult

Purpose:
- Reads specified canon grondslagen (foundations) before agent execution
- Logs the consultation with timestamp and commit SHA to canon-consult.log.md
- Logs actual source: local path if read locally, GitHub URL if cloned from GitHub
- Returns summary of consulted files to verify the consultation occurred

This ensures every agent execution has a verifiable canon consultation.

Usage (for agent-curator):
    python scripts/bootstrap_canon_consult.py \
        --agent agent-curator \
        --workspace-file artefacten/aeo/aeo.02.agent-curator/agent-curator.charter.md \
        --value-stream aeo \
        --grondslagen "grondslagen/.algemeen/*,grondslagen/aeo/*" \
        --intent charter-execution \
        --canon-path ..\\mandarin-canon \
        --canon-github-url https://github.com/owner/mandarin-canon \
        --canon-branch main

Notes:
- Defaults canon path to ../mandarin-canon relative to workspace
- Requires Git on PATH to resolve branch and commit
- Reads and summarizes the specified grondslagen patterns
- Appends consultation entry to audit/canon-consult.log.md
"""

from __future__ import annotations

import argparse
import datetime as dt
import glob
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional


def _run_git(args: list[str], cwd: Optional[str] = None) -> Optional[str]:
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


def resolve_canon_info(canon_path: str) -> dict:
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


def append_markdown_entry(log_path: str, entry: dict, files_table: list[tuple[str, str]]) -> None:
    """Append a consultation entry as Markdown."""
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


def read_grondslagen(canon_path: str, patterns: list[str]) -> dict:
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
                            lines = f.readlines()
                            preview = "".join(lines[:5]).strip()
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
                        lines = f.readlines()
                        preview = "".join(lines[:5]).strip()
                        content_summary.append(f"\n### {pattern}\n{preview}...\n")
                except Exception as e:
                    content_summary.append(f"\n### {pattern}\n(Error reading: {e})\n")
    
    return {
        "files": consulted,
        "files_table": files_table,
        "summary": "".join(content_summary),
        "count": len(consulted)
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Bootstrap canon consultation before agent execution")
    parser.add_argument("--agent", required=True, help="Agent canonical name (e.g., agent-curator)")
    parser.add_argument("--workspace-file", required=True, help="Workspace file path where consult occurred")
    parser.add_argument("--value-stream", required=False, help="Value stream id (e.g., aeo, aod)")
    parser.add_argument("--grondslagen", required=True, help="Comma-separated grondslagen patterns (e.g., 'grondslagen/.algemeen/*,grondslagen/aeo/*')")
    parser.add_argument("--intent", required=False, default="execution", help="Intent or reason (e.g., bootstrap, execution)")
    parser.add_argument("--method", required=False, default="manual", help="manual|runner|pipeline")
    parser.add_argument("--canon-path", required=False, help="Path to mandarin-canon repo; defaults to ../mandarin-canon")
    parser.add_argument("--canon-github-url", required=False, help="GitHub URL to clone from if local canon not found")
    parser.add_argument("--canon-branch", required=False, default="main", help="Branch to clone (default: main)")
    parser.add_argument("--notes", required=False, help="Optional notes")

    args = parser.parse_args(argv)

    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    audit_dir = ensure_audit_dir(workspace_root)
    log_path = os.path.join(audit_dir, "canon-consult.log.md")

    canon_path = args.canon_path or os.path.abspath(os.path.join(workspace_root, os.pardir, "mandarin-canon"))
    
    # Track whether we're using local or cloned from GitHub
    source_type = "local"
    canon_source = canon_path  # default to local path

    # If local canon doesn't exist, try to clone from GitHub
    if not os.path.isdir(canon_path):
        if args.canon_github_url:
            success = clone_canon_from_github(canon_path, args.canon_github_url, args.canon_branch)
            if not success:
                print(f"ERROR: Could not find or clone canon repository", file=sys.stderr)
                return 1
            source_type = "github"
            canon_source = args.canon_github_url  # log the GitHub URL
        else:
            print(f"ERROR: Canon path not found: {canon_path}", file=sys.stderr)
            print(f"TIP: Provide --canon-github-url to clone automatically from GitHub", file=sys.stderr)
            return 1

    # Get canon info
    info = resolve_canon_info(canon_path)
    if not info.get("sha_full"):
        print(f"ERROR: Could not resolve canon commit SHA in: {canon_path}", file=sys.stderr)
        return 1

    # Read grondslagen
    patterns = [p.strip() for p in args.grondslagen.split(",")]
    grondslagen = read_grondslagen(canon_path, patterns)

    if grondslagen["count"] == 0:
        print(f"WARNING: No grondslagen files found matching patterns: {patterns}", file=sys.stderr)

    # Log the consultation
    # Use Central European Time for timestamp
    now_cet = dt.datetime.now()
    ts_str = now_cet.strftime("%Y-%m-%dT%H:%M:%S%z")
    # Add colon in timezone offset for ISO 8601 format: +0100 -> +01:00
    if len(ts_str) > 2 and ts_str[-5].isdigit():
        ts_str = ts_str[:-2] + ":" + ts_str[-2:]
    
    entry = {
        "ts": ts_str,
        "agent": args.agent,
        "valueStream": args.value_stream,
        "workspaceFile": args.workspace_file,
        "intent": args.intent,
        "method": args.method,
        "canonPath": canon_source,
        "branch": info.get("branch"),
        "shaShort": info.get("sha_short"),
        "grondslagePatterns": args.grondslagen,
        "notes": args.notes,
    }

    append_markdown_entry(log_path, entry, grondslagen["files_table"])

    # Report to stdout
    print("=" * 80)
    print("CANON CONSULTATION LOGGED")
    print("=" * 80)
    print(f"Agent:       {args.agent}")
    print(f"Timestamp:   {entry['ts']}")
    print(f"Canon SHA:   {info['sha_short']} (branch: {info['branch']})")
    print(f"Files read:  {grondslagen['count']}")
    print(f"Log:         {os.path.relpath(log_path, workspace_root)}")
    print()
    print("Consulted grondslagen:")
    for f in grondslagen["files"]:
        print(f"  - {f}")
    print()
    print("Content preview (first 5 lines per file):")
    print(grondslagen["summary"])
    print("=" * 80)
    print()
    print("✓ Canon consultation verified and logged")
    print("✓ Agent may now proceed with execution")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
