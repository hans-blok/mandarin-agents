#!/usr/bin/env python3
"""
Fetch and organize agents from mandarin-agents repository.

This script fetches agent definitions from the mandarin-agents repository
based on a value stream and fase filter (e.g., "miv.01"). After git pull,
it scans all folders matching the filter pattern and copies files to the
workspace according to their type.

Usage:
    python fetch_mandarin_agents.py miv.01
    python fetch_mandarin_agents.py aeo.02
    python fetch_mandarin_agents.py fnd.01

The script performs:
- Git clone/pull of mandarin-agents repository
- Folder scanning based on value-stream.fase pattern
- File organization by type:
  * *.template.md → templates/
  * *.charter.md → agent-charters/
  * *.prompt.md → .github/prompts/
  * *.agent.md → .github/agents/
  * runners → scripts/runners/
- *.boundary.md files are ignored

Design decisions:
- Direct folder scanning, no manifest parsing
- mandarin-agents folder is kept for efficient git pull reuse
- Boundary files are explicitly ignored
- Type hints used throughout for maintainability
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List


@dataclass
class FileOperation:
	"""Represents a file copy operation."""
	
	source: Path
	destination: Path
	file_type: str  # template, charter, prompt, agent, runner


class RepositoryManager:
	"""Manage Git operations for mandarin-agents repository."""
	
	def __init__(self, repo_url: str, target_dir: Path):
		"""Initialize repository manager."""
		self.repo_url = repo_url
		self.target_dir = target_dir
	
	def fetch(self) -> Path:
		"""Clone or pull repository."""
		if self.target_dir.exists() and (self.target_dir / ".git").exists():
			print(f"[INFO] Repository exists, pulling latest changes...")
			self._run_git(["pull"], cwd=self.target_dir)
		else:
			print(f"[INFO] Cloning repository from {self.repo_url}...")
			self.target_dir.mkdir(parents=True, exist_ok=True)
			self._run_git(["clone", "--depth", "1", self.repo_url, str(self.target_dir)])
		
		return self.target_dir
	
	def _run_git(self, args: List[str], cwd: Path | None = None) -> str:
		"""Run git command with error handling."""
		cmd = ["git"] + args
		result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
		
		if result.returncode != 0:
			raise RuntimeError(
				f"Git command failed: {' '.join(cmd)}\n"
				f"Exit code: {result.returncode}\n"
				f"Error: {result.stderr}"
			)
		
		return result.stdout.strip()


class AgentScanner:
	"""Scanner for agent folders based on value-stream.fase pattern."""
	
	def __init__(self, repo_path: Path, workspace: Path):
		"""Initialize scanner."""
		self.repo_path = repo_path
		self.workspace = workspace
		
		# Target directories in workspace
		self.templates_dir = workspace / "templates"
		self.charters_dir = workspace / "agent-charters"
		self.prompts_dir = workspace / ".github" / "prompts"
		self.agents_dir = workspace / ".github" / "agents"
		self.runners_dir = workspace / "scripts" / "runners"
		
		# Create target directories
		for target_dir in [
			self.templates_dir,
			self.charters_dir,
			self.prompts_dir,
			self.agents_dir,
			self.runners_dir,
		]:
			target_dir.mkdir(parents=True, exist_ok=True)
	
	def scan_folders(self, pattern: str) -> List[FileOperation]:
		"""
		Scan artefacten/ for folders matching pattern.
		
		Pattern format: "miv.01" -> matches folders starting with "miv.01."
		Scans both flat (artefacten/miv.01.*) and nested (artefacten/miv/miv.01.*)
		
		Args:
			pattern: Value stream and fase code (e.g., "miv.01", "aeo.02", "fnd.01")
		
		Returns:
			List of file operations to execute
		"""
		operations: List[FileOperation] = []
		artefacten_dir = self.repo_path / "artefacten"
		
		if not artefacten_dir.exists():
			raise RuntimeError(f"Artefacten directory not found: {artefacten_dir}")
		
		print(f"[INFO] Scanning for folders matching pattern: {pattern}.*")
		
		# Extract value stream code for nested folder check
		vs_code = pattern.split(".")[0] if "." in pattern else pattern
		
		# Scan nested structure: artefacten/<vs-code>/<pattern>.*
		nested_vs_dir = artefacten_dir / vs_code
		if nested_vs_dir.exists() and nested_vs_dir.is_dir():
			for folder in nested_vs_dir.iterdir():
				if folder.is_dir() and folder.name.startswith(f"{pattern}."):
					print(f"  [FOUND] {folder.relative_to(self.repo_path)}")
					operations.extend(self._scan_agent_folder(folder))
		
		# Scan flat structure: artefacten/<pattern>.*
		for folder in artefacten_dir.iterdir():
			if folder.is_dir() and folder.name.startswith(f"{pattern}."):
				print(f"  [FOUND] {folder.relative_to(self.repo_path)}")
				operations.extend(self._scan_agent_folder(folder))
		
		if not operations:
			print(f"[WARNING] No folders found matching pattern: {pattern}.*")
		
		return operations
	
	def _scan_agent_folder(self, folder: Path) -> List[FileOperation]:
		"""
		Scan single agent folder and create file operations.
		
		Maps files by extension:
		- *.template.md → templates/
		- *.charter.md → agent-charters/
		- *.prompt.md → .github/prompts/
		- *.agent.md → .github/agents/
		- <agent>-runner.py or <agent>-runner/ → scripts/runners/
		
		Ignores:
		- *.boundary.md files
		"""
		operations: List[FileOperation] = []
		
		for file_path in folder.iterdir():
			filename = file_path.name
			
			# Ignore boundary files
			if filename.endswith(".boundary.md"):
				continue
			
			# Templates
			if "template" in filename.lower() and filename.endswith(".md"):
				dest = self.templates_dir / filename
				operations.append(FileOperation(
					source=file_path,
					destination=dest,
					file_type="template"
				))
				continue
			
			# Charters
			if filename.endswith(".charter.md"):
				dest = self.charters_dir / filename
				operations.append(FileOperation(
					source=file_path,
					destination=dest,
					file_type="charter"
				))
				continue
			
			# Prompts
			if filename.endswith(".prompt.md"):
				dest = self.prompts_dir / filename
				operations.append(FileOperation(
					source=file_path,
					destination=dest,
					file_type="prompt"
				))
				continue
			
			# Agent contracts
			if filename.endswith(".agent.md"):
				dest = self.agents_dir / filename
				operations.append(FileOperation(
					source=file_path,
					destination=dest,
					file_type="agent"
				))
				continue
			
			# Runners (files or directories)
			if "runner" in filename.lower():
				if file_path.is_file() and filename.endswith(".py"):
					dest = self.runners_dir / filename
					operations.append(FileOperation(
						source=file_path,
						destination=dest,
						file_type="runner"
					))
				elif file_path.is_dir():
					dest = self.runners_dir / filename
					operations.append(FileOperation(
						source=file_path,
						destination=dest,
						file_type="runner"
					))
		
		return operations
	
	def execute_operations(self, operations: List[FileOperation]) -> dict[str, int]:
		"""Execute file copy operations."""
		stats = {
			"template": 0,
			"charter": 0,
			"prompt": 0,
			"agent": 0,
			"runner": 0,
			"error": 0,
		}
		
		if not operations:
			print("[WARNING] No files to copy")
			return stats
		
		print(f"\n[INFO] Executing {len(operations)} file operations...")
		
		for op in operations:
			try:
				# Handle directories (runner modules)
				if op.source.is_dir():
					if op.destination.exists():
						shutil.rmtree(op.destination)
						print(f"  [REMOVE] Existing module {op.destination.name}/")
					shutil.copytree(op.source, op.destination)
					print(f"  [{op.file_type.upper()}] {op.source.name}/ -> {op.destination.relative_to(self.workspace)}")
				else:
					# Regular file
					shutil.copy2(op.source, op.destination)
					print(f"  [{op.file_type.upper()}] {op.source.name} -> {op.destination.relative_to(self.workspace)}")
				
				stats[op.file_type] += 1
				
			except Exception as e:
				stats["error"] += 1
				print(f"  [ERROR] Failed to copy {op.source.name}: {e}")
		
		return stats


def main() -> int:
	"""Main entry point."""
	parser = argparse.ArgumentParser(
		description="Fetch agents from mandarin-agents repository by value-stream.fase pattern",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog="""
Examples:
  python fetch_mandarin_agents.py miv.01    # Fetch MIV fase 01 agents
  python fetch_mandarin_agents.py aeo.02    # Fetch AEO fase 02 agents
  python fetch_mandarin_agents.py fnd.01    # Fetch FND fase 01 agents
		""",
	)
	parser.add_argument(
		"pattern",
		help="Value stream and fase pattern (e.g., 'miv.01', 'aeo.02', 'fnd.01')",
	)
	parser.add_argument(
		"--repo-url",
		default="https://github.com/hans-blok/mandarin-agents.git",
		help="Repository URL (default: mandarin-agents)",
	)
	
	args = parser.parse_args()
	
	workspace = Path.cwd()
	repo_dir = workspace / "mandarin-agents"
	
	try:
		# Fetch repository
		print(f"[INFO] Fetching mandarin-agents repository...")
		repo_mgr = RepositoryManager(args.repo_url, repo_dir)
		repo_path = repo_mgr.fetch()
		
		# Scan for matching folders
		scanner = AgentScanner(repo_path, workspace)
		operations = scanner.scan_folders(args.pattern)
		
		if not operations:
			print(f"[ERROR] No agent folders found matching pattern: {args.pattern}.*")
			return 1
		
		# Execute operations
		stats = scanner.execute_operations(operations)
		
		# Print summary
		timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		print(f"\n{'='*60}")
		print(f"SUMMARY - {timestamp}")
		print(f"{'='*60}")
		print(f"Pattern: {args.pattern}")
		print(f"\nFiles copied:")
		print(f"  Templates:  {stats['template']}")
		print(f"  Charters:   {stats['charter']}")
		print(f"  Prompts:    {stats['prompt']}")
		print(f"  Agents:     {stats['agent']}")
		print(f"  Runners:    {stats['runner']}")
		
		if stats['error'] > 0:
			print(f"  Errors:     {stats['error']}")
		
		total = sum(stats[k] for k in ['template', 'charter', 'prompt', 'agent', 'runner'])
		print(f"\nTotal: {total} files/modules copied")
		print(f"\n[SUCCESS] Agents fetched for pattern: {args.pattern}")
		
		return 0
		
	except RuntimeError as e:
		print(f"[ERROR] {e}")
		return 1
	except Exception as e:
		print(f"[ERROR] Unexpected error: {e}")
		import traceback
		traceback.print_exc()
		return 1


if __name__ == "__main__":
	sys.exit(main())
