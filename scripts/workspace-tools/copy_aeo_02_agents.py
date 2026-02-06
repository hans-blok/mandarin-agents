"""Copy AEO 02 agents into root .github/agents, .github/prompts, agent-charters and templates.

This script scans artefacten/aeo/ and artefacten/fnd/ for agent folders matching 'aeo.02.*' pattern
and copies:

- *.agent.md files (agent contracts) to .github/agents/
- *.prompt.md files (prompt metadata) to .github/prompts/
- *.charter.md files (charters) to agent-charters/
- *template*.md files (agent-specific templates) to templates/

The source agents remain in their original location. Existing files in destination folders 
are forcefully overwritten.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import NamedTuple


class CopyStats(NamedTuple):
	"""Statistics for copied files."""
	agents: int = 0
	prompts: int = 0
	charters: int = 0
	templates: int = 0
	
	@property
	def total(self) -> int:
		return self.agents + self.prompts + self.charters + self.templates


def copy_file_with_force(src: Path, dst: Path) -> None:
	"""Copy file from src to dst, forcefully overwriting if exists."""
	dst.parent.mkdir(parents=True, exist_ok=True)
	shutil.copy2(src, dst)


def scan_and_copy_agent_folder(agent_dir: Path, destinations: dict[str, Path]) -> CopyStats:
	"""Scan one agent folder and copy files to appropriate destinations.
	
	Args:
		agent_dir: Path to agent folder (e.g., artefacten/aeo/aeo.02.agent-smeder/)
		destinations: Mapping of file types to destination folders
		
	Returns:
		CopyStats with counts per file type
	"""
	stats = {"agents": 0, "prompts": 0, "charters": 0, "templates": 0}
	
	print(f"  [Verwerk] {agent_dir.name}")
	
	for file_path in agent_dir.iterdir():
		if not file_path.is_file():
			continue
			
		lower_name = file_path.name.lower()
		
		# Agent contracts: *.agent.md
		if lower_name.endswith(".agent.md"):
			copy_file_with_force(file_path, destinations["agents"] / file_path.name)
			print(f"    → agent-contract: {file_path.name}")
			stats["agents"] += 1
			
		# Prompts: *.prompt.md
		elif lower_name.endswith(".prompt.md"):
			copy_file_with_force(file_path, destinations["prompts"] / file_path.name)
			print(f"    → prompt:         {file_path.name}")
			stats["prompts"] += 1
			
		# Charters: *.charter.md
		elif lower_name.endswith(".charter.md"):
			copy_file_with_force(file_path, destinations["charters"] / file_path.name)
			print(f"    → charter:        {file_path.name}")
			stats["charters"] += 1
			
		# Templates: any markdown file with "template" in name
		elif "template" in lower_name and lower_name.endswith(".md"):
			copy_file_with_force(file_path, destinations["templates"] / file_path.name)
			print(f"    → template:       {file_path.name}")
			stats["templates"] += 1
	
	return CopyStats(**stats)


def copy_aeo_02_agents(repo_root: Path) -> None:
	"""Copy all AEO 02 and FND agents to workspace root folders.
	
	Args:
		repo_root: Root of the repository
	"""
	# Source folders
	aeo_dir = repo_root / "artefacten" / "aeo"
	fnd_dir = repo_root / "artefacten" / "fnd"
	
	# Destination folders
	destinations = {
		"agents": repo_root / ".github" / "agents",
		"prompts": repo_root / ".github" / "prompts",
		"charters": repo_root / "agent-charters",
		"templates": repo_root / "templates",
	}
	
	# Ensure all destination folders exist
	for dst in destinations.values():
		dst.mkdir(parents=True, exist_ok=True)
	
	print("[copy_aeo_02_agents] Start kopiëren van AEO 02 agents...")
	
	total_stats = CopyStats()
	
	# Scan AEO folders matching aeo.02.* pattern
	if aeo_dir.is_dir():
		print(f"\n[Scan] AEO agents in {aeo_dir.relative_to(repo_root)}")
		
		for agent_dir in sorted(aeo_dir.iterdir()):
			if not agent_dir.is_dir():
				continue
			if not agent_dir.name.startswith("aeo.02."):
				continue
			
			stats = scan_and_copy_agent_folder(agent_dir, destinations)
			total_stats = CopyStats(
				agents=total_stats.agents + stats.agents,
				prompts=total_stats.prompts + stats.prompts,
				charters=total_stats.charters + stats.charters,
				templates=total_stats.templates + stats.templates,
			)
	else:
		print(f"[Waarschuwing] AEO folder niet gevonden: {aeo_dir}")
	
	# Scan FND folders (all FND agents)
	if fnd_dir.is_dir():
		print(f"\n[Scan] FND agents in {fnd_dir.relative_to(repo_root)}")
		
		for agent_dir in sorted(fnd_dir.iterdir()):
			if not agent_dir.is_dir():
				continue
			if not agent_dir.name.startswith("fnd."):
				continue
			
			stats = scan_and_copy_agent_folder(agent_dir, destinations)
			total_stats = CopyStats(
				agents=total_stats.agents + stats.agents,
				prompts=total_stats.prompts + stats.prompts,
				charters=total_stats.charters + stats.charters,
				templates=total_stats.templates + stats.templates,
			)
	else:
		print(f"[Waarschuwing] FND folder niet gevonden: {fnd_dir}")
	
	# Summary
	print(f"\n[copy_aeo_02_agents] ✓ Kopiëren afgerond")
	print(f"[Samenvatting] {total_stats.agents} agent-contracten, "
		  f"{total_stats.prompts} prompts, "
		  f"{total_stats.charters} charters, "
		  f"{total_stats.templates} templates "
		  f"(totaal: {total_stats.total} bestanden)")


def main() -> None:
	"""Main entry point."""
	repo_root = Path(__file__).resolve().parents[2]
	copy_aeo_02_agents(repo_root)


if __name__ == "__main__":
	main()
