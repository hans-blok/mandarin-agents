#!/usr/bin/env python3
"""
Templates Curator Runner — Publiceer Templates Overzicht

Dit script scant alle relevante template-bestanden in de workspace,
verzamelt metadata (naam, locatie, type), en publiceert een overzicht in Markdown.

Usage:
    python scripts/runners/templates-curator.py

Output:
    - docs/resultaten/templates-publicatie-<datum-tijd>.md (archief)

Traceability:
    Prompt: .github/prompts/mandarin.python-expert-schrijf.script.prompt.md
"""

import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import sys

# Metadata structuur voor een template
class TemplateMetadata:
    def __init__(self, naam: str, pad: Path, template_type: str):
        self.naam = naam
        self.pad = pad
        self.template_type = template_type


def scan_templates(workspace_root: Path) -> List[TemplateMetadata]:
    """Scan alle relevante template-bestanden in de workspace."""
    templates: List[TemplateMetadata] = []
    # 1. templates/
    templates_dir = workspace_root / "templates"
    if templates_dir.exists():
        for f in templates_dir.glob("*.md"):
            templates.append(TemplateMetadata(f.name, f.relative_to(workspace_root), "charter/contract"))
        for f in templates_dir.glob("*.yaml"):
            templates.append(TemplateMetadata(f.name, f.relative_to(workspace_root), "prompt-yaml"))
    # 2. .github/prompts/
    gh_prompts = workspace_root / ".github" / "prompts"
    if gh_prompts.exists():
        for f in gh_prompts.glob("*.prompt.md"):
            templates.append(TemplateMetadata(f.name, f.relative_to(workspace_root), "prompt-md"))
    # 3. exports/*/prompts/
    exports_dir = workspace_root / "exports"
    if exports_dir.exists():
        for vs_dir in exports_dir.iterdir():
            if vs_dir.is_dir():
                vs_prompts = vs_dir / "prompts"
                if vs_prompts.exists():
                    for f in vs_prompts.glob("*.prompt.md"):
                        templates.append(TemplateMetadata(f.name, f.relative_to(workspace_root), "prompt-md"))
    return templates


def generate_markdown(templates: List[TemplateMetadata]) -> str:
    """Genereer Markdown-overzicht van alle templates."""
    lines = []
    lines.append(f"# Templates Publicatie Overzicht\n\n")
    lines.append(f"**Publicatiedatum**: {datetime.now().strftime('%Y-%m-%d')}\n")
    lines.append(f"**Tijdstip**: {datetime.now().strftime('%H:%M:%S')}\n")
    lines.append(f"**Totaal templates**: {len(templates)}\n\n")
    lines.append("| Naam | Pad | Type |\n")
    lines.append("|------|-----|------|\n")
    for t in sorted(templates, key=lambda x: x.naam):
        lines.append(f"| {t.naam} | {t.pad} | {t.template_type} |\n")
    lines.append("\n")
    lines.append("## Metadata\n\n")
    lines.append("- Gescande folders:\n")
    lines.append("  - templates/\n  - .github/prompts/\n  - exports/*/prompts/\n")
    lines.append("- Traceability: mandarin.python-expert-schrijf.script.prompt.md\n")
    return "".join(lines)


def write_output(markdown: str, workspace_root: Path) -> None:
    """Schrijf het Markdown-overzicht weg naar docs/resultaten/templates-publicatie-<datum-tijd>.md"""
    archive_dir = workspace_root / "docs" / "resultaten" / "templates-publicatie"
    archive_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    md_path = archive_dir / f"templates-publicatie-{timestamp}.md"
    md_path.write_text(markdown, encoding="utf-8")
    print(f"[MARKDOWN] {md_path.relative_to(workspace_root)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Templates Curator — Publiceer Templates Overzicht")
    args = parser.parse_args()
    workspace_root = Path(__file__).parent.parent.parent
    print("Templates Curator — Publiceer Templates Overzicht")
    print("=" * 60)
    try:
        templates = scan_templates(workspace_root)
        print(f"[INFO] {len(templates)} templates gevonden")
        markdown = generate_markdown(templates)
        write_output(markdown, workspace_root)
        print("\n[SUCCESS] Templates overzicht gepubliceerd")
        return 0
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
