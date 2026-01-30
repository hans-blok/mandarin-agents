#!/usr/bin/env python3
"""
Templates-naar-Contract Overzicht Generator

Genereert een tabel met alle templates in de folder templates/ en het agent-contract dat elk template gebruikt.

Usage:
    python scripts/runners/templates-contract-overzicht.py

Output:
    - docs/resultaten/templates-contract-overzicht/templates-contract-overzicht-<datum-tijd>.md

Traceability:
    Prompt: .github/prompts/mandarin.python-expert-schrijf.script.prompt.md
"""

import re
from datetime import datetime
from pathlib import Path
from typing import List, Tuple
import sys

def extract_contract_from_template(template_path: Path) -> str:
    """Zoek het agent-contract in het template-bestand (header)."""
    try:
        content = template_path.read_text(encoding="utf-8")
        # Zoek naar een regel als: **Contract**: agent-contract.template.md
        match = re.search(r"\*\*Contract\*\*:\s*([\w\-\.]+)", content)
        if match:
            return match.group(1)
        # Alternatief: zoek naar een expliciete verwijzing in de header
        match2 = re.search(r"agent-contract\.template\.md", content)
        if match2:
            return "agent-contract.template.md"
        return "-"
    except Exception as e:
        return f"[fout: {e}]"

def scan_templates_contracts(templates_dir: Path, workspace_root: Path) -> List[Tuple[str, str]]:
    """Genereer lijst van (template-naam, contract-naam) tuples.
    Als het contract niet in het template-bestand staat, zoek dan in exports/*/agents/*agent.md naar een contract dat het template gebruikt.
    """
    overzicht = []
    # Verzamel alle agent-contracts
    agent_contracts = []
    exports_dir = workspace_root / "exports"
    if exports_dir.exists():
        for vs_dir in exports_dir.iterdir():
            if vs_dir.is_dir():
                agents_dir = vs_dir / "agents"
                if agents_dir.exists():
                    for contract_file in agents_dir.glob("*.agent.md"):
                        agent_contracts.append(contract_file)
    for template_file in sorted(templates_dir.glob("*.md")):
        naam = template_file.stem  # zonder .md
        contract = extract_contract_from_template(template_file)
        if contract == "-":
            # Zoek in agent_contracts naar een contract dat naar dit template verwijst
            found = False
            for contract_file in agent_contracts:
                try:
                    content = contract_file.read_text(encoding="utf-8")
                    # Zoek naar een regel als: **Template**: thema-statement.template.md
                    if re.search(rf"\*\*Template\*\*:\s*{re.escape(template_file.name)}", content):
                        contract = contract_file.name
                        found = True
                        break
                except Exception:
                    continue
            if not found:
                contract = "-"
        overzicht.append((naam, contract))
    return overzicht

def generate_markdown(overzicht: List[Tuple[str, str]]) -> str:
    lines = []
    lines.append(f"# Templates-naar-Contract Overzicht\n\n")
    lines.append(f"**Publicatiedatum**: {datetime.now().strftime('%Y-%m-%d')}\n")
    lines.append(f"**Tijdstip**: {datetime.now().strftime('%H:%M:%S')}\n")
    lines.append(f"**Totaal templates**: {len(overzicht)}\n\n")
    lines.append("| Template | Agent-contract |\n")
    lines.append("|----------|---------------|\n")
    for naam, contract in overzicht:
        lines.append(f"| {naam} | {contract} |\n")
    lines.append("\n")
    lines.append("- Bron: templates/\n")
    lines.append("- Traceability: mandarin.python-expert-schrijf.script.prompt.md\n")
    return "".join(lines)

def write_output(markdown: str, workspace_root: Path) -> None:
    archive_dir = workspace_root / "docs" / "resultaten" / "templates-contract-overzicht"
    archive_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    md_path = archive_dir / f"templates-contract-overzicht-{timestamp}.md"
    md_path.write_text(markdown, encoding="utf-8")
    print(f"[MARKDOWN] {md_path.relative_to(workspace_root)}")

def main() -> int:
    workspace_root = Path(__file__).parent.parent.parent
    templates_dir = workspace_root / "templates"
    print("Templates-naar-Contract Overzicht Generator")
    print("=" * 60)
    try:
        overzicht = scan_templates_contracts(templates_dir, workspace_root)
        markdown = generate_markdown(overzicht)
        write_output(markdown, workspace_root)
        print("\n[SUCCESS] Overzicht gepubliceerd")
        return 0
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
