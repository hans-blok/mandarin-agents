"""Copy aeo.02 agents into root .github/agents, .github/prompts, agent-charters and templates.

This script scans artefacten/ for agent folders that start with "aeo.02." and copies:

- *.agent.md files (agent contracts) to .github/agents/
- *.prompt.md files (prompt metadata) to .github/prompts/
- *.charter.md files (charters) to agent-charters/
- *template*.md files (agent-specific templates) to templates/

Existing files with the same name will be overwritten.
"""

from __future__ import annotations

import shutil
from pathlib import Path


def copy_aeo_02_agents(repo_root: Path) -> None:

	rel_artefacten = Path("artefacten")
	artefacten_dir = repo_root / rel_artefacten
	if not artefacten_dir.is_dir():
		raise SystemExit(f"Artefacten-map niet gevonden: {artefacten_dir}")

	# Doelmap-paden
	agents_dst = repo_root / ".github" / "agents"
	prompts_dst = repo_root / ".github" / "prompts"
	charters_dst = repo_root / "agent-charters"
	templates_dst = repo_root / "templates"

	for dst in (agents_dst, prompts_dst, charters_dst, templates_dst):
		dst.mkdir(parents=True, exist_ok=True)

	print("[copy_aeo_02_agents] Start kopiëren van aeo.02-agents...")

	# Tel-counters voor korte samenvatting aan het eind
	total_agents = 0
	total_prompts = 0
	total_charters = 0
	total_templates = 0

	# Zoek folders die starten met "aeo.02." (toelatend dat "ae0.02" een type is)
	for agent_dir in artefacten_dir.iterdir():
		name = agent_dir.name
		if not agent_dir.is_dir():
			continue
		if not (name.startswith("aeo.02.") or name.startswith("ae0.02.")):
			continue

		print(f"[copy_aeo_02_agents] Verwerk agent-folder: {name}")

		for path in agent_dir.iterdir():
			if not path.is_file():
				continue

			lower_name = path.name.lower()

			# Contracts
			if lower_name.endswith(".agent.md"):
				shutil.copy2(path, agents_dst / path.name)
				print(f"  → agent-contract gekopieerd: {path} -> {agents_dst / path.name}")
				total_agents += 1
				continue

			# Prompts
			if lower_name.endswith(".prompt.md"):
				shutil.copy2(path, prompts_dst / path.name)
				print(f"  → prompt gekopieerd:        {path} -> {prompts_dst / path.name}")
				total_prompts += 1
				continue

			# Charters
			if lower_name.endswith(".charter.md"):
				shutil.copy2(path, charters_dst / path.name)
				print(f"  → charter gekopieerd:       {path} -> {charters_dst / path.name}")
				total_charters += 1
				continue

			# Templates (ruim: alle markdown-bestanden met "template" in de naam)
			if "template" in lower_name and lower_name.endswith(".md"):
				shutil.copy2(path, templates_dst / path.name)
				print(f"  → template gekopieerd:      {path} -> {templates_dst / path.name}")
				total_templates += 1

	total_files = total_agents + total_prompts + total_charters + total_templates
	print("[copy_aeo_02_agents] Kopiëren afgerond.")
	print(
		f"[copy_aeo_02_agents] Samenvatting: "
		f"{total_agents} agent-contracten, "
		f"{total_prompts} prompts, "
		f"{total_charters} charters, "
		f"{total_templates} templates (totaal {total_files} bestanden)."
	)


def main() -> None:
	repo_root = Path(__file__).resolve().parents[2]
	copy_aeo_02_agents(repo_root)


if __name__ == "__main__":
	main()
