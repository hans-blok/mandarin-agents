"""Copy AEO and FND agents into root .github/agents, .github/prompts, agent-charters and templates.

This script scans artefacten/aeo/ and artefacten/fnd/ for all agent folders and copies:

- *.agent.md files (agent contracts) to .github/agents/
- *.prompt.md files (prompt metadata) to .github/prompts/
- *.charter.md files (charters) to agent-charters/
- *template*.md files (agent-specific templates) to templates/

The source agents remain in their original location. Existing files in destination folders will be overwritten.
"""

from __future__ import annotations

import shutil
from pathlib import Path


def copy_aeo_02_agents(repo_root: Path) -> None:

	# Bronmappen: AEO en FND agents
	aeo_dir = repo_root / "artefacten" / "aeo"
	fnd_dir = repo_root / "artefacten" / "fnd"
	
	# Doelmap-paden
	agents_dst = repo_root / ".github" / "agents"
	prompts_dst = repo_root / ".github" / "prompts"
	charters_dst = repo_root / "agent-charters"
	templates_dst = repo_root / "templates"

	for dst in (agents_dst, prompts_dst, charters_dst, templates_dst):
		dst.mkdir(parents=True, exist_ok=True)

	print("[copy_aeo_02_agents] Start kopiëren van AEO en FND agents...")

	# Tel-counters voor korte samenvatting aan het eind
	total_agents = 0
	total_prompts = 0
	total_charters = 0
	total_templates = 0

	# Scan beide bronmappen: AEO en FND
	# Folders volgen patroon: <vs-code>.<fase-nr>.<agent-naam>
	source_dirs = []
	if aeo_dir.is_dir():
		source_dirs.append(("AEO", aeo_dir, "aeo."))
	if fnd_dir.is_dir():
		source_dirs.append(("FND", fnd_dir, "fnd."))
	
	if not source_dirs:
		raise SystemExit("Geen AEO of FND mappen gevonden in artefacten/")

	for vs_name, vs_dir, prefix in source_dirs:
		print(f"[copy_aeo_02_agents] Scan {vs_name} agents in {vs_dir}...")
		
		for agent_dir in vs_dir.iterdir():
			name = agent_dir.name
			if not agent_dir.is_dir():
				continue
			if not name.startswith(prefix):
				continue

			print(f"[copy_aeo_02_agents] Verwerk agent-folder: {name}")

			for path in agent_dir.iterdir():
				if not path.is_file():
					continue

				lower_name = path.name.lower()

				# Contracts
				if lower_name.endswith(".agent.md"):
					shutil.copy2(path, agents_dst / path.name)
					print(f"  → agent-contract gekopieerd: {path.name}")
					total_agents += 1
					continue

				# Prompts
				if lower_name.endswith(".prompt.md"):
					shutil.copy2(path, prompts_dst / path.name)
					print(f"  → prompt gekopieerd:        {path.name}")
					total_prompts += 1
					continue

				# Charters
				if lower_name.endswith(".charter.md"):
					shutil.copy2(path, charters_dst / path.name)
					print(f"  → charter gekopieerd:       {path.name}")
					total_charters += 1
					continue

				# Templates (ruim: alle markdown-bestanden met "template" in de naam)
				if "template" in lower_name and lower_name.endswith(".md"):
					shutil.copy2(path, templates_dst / path.name)
					print(f"  → template gekopieerd:      {path.name}")
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
