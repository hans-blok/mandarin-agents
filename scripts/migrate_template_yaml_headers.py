#!/usr/bin/env python3
"""
Migratiescript: canonical §4 YAML headers op alle .template.md bestanden.

Conform yaml-header.template.md §4 — TEMPLATE:

    ---
    # IDENTIFICATIE
    template-id: "NNN"
    template-naam: ""

    # RELATIES
    artefact-type-id: ""
    agent-id: ""

    # META-DATA
    versie: ""
    status: ""
    digest: ""
    ---

Bestaande YAML-headers worden vervangen. Body-inhoud blijft intact.
Bestanden zonder YAML-header krijgen de header vooraan.
"""

import hashlib
import re
import sys
from pathlib import Path

WORKSPACE = Path(r"c:\git\mandarin-agents")

# ── Template registry: (template-id, rel-path, agent-id, template-naam, artefact-type-id)
# artefact-type-id conform artefacttype-matrix-per-value-stream-fase.md v2.2.0 in mandarin-canon
TEMPLATE_REGISTRY = [
    ("001",
     "artefacten/aeo/aeo.01.capability-architect/templates/agent-boundary.template.md",
     "aeo.01.capability-architect", "agent-boundary", "001"),
    ("002",
     "artefacten/aeo/aeo.02.agent-curator/templates/ecosysteem-agent-prompt-contracten.template.md",
     "aeo.02.agent-curator", "ecosysteem-agent-prompt-contracten", "002"),
    ("003",
     "artefacten/aeo/aeo.02.agent-curator/templates/ecosysteem-overzicht.template.md",
     "aeo.02.agent-curator", "ecosysteem-overzicht", "003"),
    ("004",
     "artefacten/aeo/aeo.02.agent-curator/templates/validatierapport.template.md",
     "aeo.02.agent-curator", "validatierapport", "004"),
    ("005",
     "artefacten/aeo/aeo.02.agent-engineer/templates/agent-prompt.template.md",
     "aeo.02.agent-engineer", "agent-prompt", "005"),
    ("006",
     "artefacten/aeo/aeo.02.agent-ontwerper/templates/agent-charter.template.md",
     "aeo.02.agent-ontwerper", "agent-charter", "006"),
    ("007",
     "artefacten/aeo/aeo.02.agent-ontwerper/templates/agent-contract-intent.template.md",
     "aeo.02.agent-ontwerper", "agent-contract-intent", "007"),
    ("008",
     "artefacten/aeo/aeo.02.agent-ontwerper/templates/agent-prompt.template.md",
     "aeo.02.agent-ontwerper", "agent-prompt", "008"),
    ("009",
     "artefacten/aeo/aeo.02.ecosysteem-beschrijver/templates/beschrijf-agent-positionering.template.md",
     "aeo.02.ecosysteem-beschrijver", "beschrijf-agent-positionering", "009"),
    ("010",
     "artefacten/aeo/aeo.02.ecosysteem-beschrijver/templates/beschrijf-ecosysteem-artefacten.template.md",
     "aeo.02.ecosysteem-beschrijver", "beschrijf-ecosysteem-artefacten", "010"),
    ("011",
     "artefacten/aeo/aeo.02.ecosysteem-beschrijver/templates/beschrijf-ecosysteem-contracten.template.md",
     "aeo.02.ecosysteem-beschrijver", "beschrijf-ecosysteem-contracten", "011"),
    ("012",
     "artefacten/aeo/aeo.02.ecosysteem-beschrijver/templates/beschrijf-ecosysteem-value-streams-agents.template.md",
     "aeo.02.ecosysteem-beschrijver", "beschrijf-ecosysteem-value-streams-agents", "012"),
    ("013",
     "artefacten/aeo/aeo.03.handoff-steward/templates/handoff.template.md",
     "aeo.03.handoff-steward", "handoff", "013"),
    ("014",
     "artefacten/aod/aod.02.core-framework-architect/templates/core-framework-architect.structureer-actieve-structuur.template.md",
     "aod.02.core-framework-architect", "core-framework-architect.structureer-actieve-structuur", "014"),
    ("015",
     "artefacten/aod/aod.02.core-framework-architect/templates/core-framework-architect.structureer-gedrag.template.md",
     "aod.02.core-framework-architect", "core-framework-architect.structureer-gedrag", "015"),
    ("016",
     "artefacten/aod/aod.02.core-framework-architect/templates/core-framework-architect.structureer-totaal-view.template.md",
     "aod.02.core-framework-architect", "core-framework-architect.structureer-totaal-view", "016"),
    ("017",
     "artefacten/aod/aod.05.solution-architect/templates/solution-architect.definieer-architectuur-keuze-document.template.md",
     "aod.05.solution-architect", "solution-architect.definieer-architectuur-keuze-document", "017"),
    ("018",
     "artefacten/fnd/fnd.01.documentatie-omvormer/templates/mkdocs-yml.template.md",
     "fnd.01.documentatie-omvormer", "mkdocs-yml", "018"),
    ("019",
     "artefacten/fnd/fnd.02.concept-curator/templates/concept.template.md",
     "fnd.02.concept-curator", "concept", "019"),
    ("020",
     "artefacten/sfw/sfw.01.hypothese-vormer/templates/hypothese-template.md",
     "sfw.01.hypothese-vormer", "hypothese", "020"),
    ("021",
     "artefacten/sfw/sfw.02.logisch-modelleur/templates/barker-validatierapport.template.md",
     "sfw.02.logisch-modelleur", "barker-validatierapport", "021"),
    ("022",
     "artefacten/sfw/sfw.02.logisch-modelleur/templates/logisch-model.template.md",
     "sfw.02.logisch-modelleur", "logisch-model", "022"),
    ("023",
     "artefacten/sfw/sfw.02.logisch-modelleur/templates/modelleringsbeslissing.template.md",
     "sfw.02.logisch-modelleur", "modelleringsbeslissing", "023"),
    ("024",
     "artefacten/sfw/sfw.02.thema-verwoorder/templates/thema-verwoorder.definieer-epic-structuur.template.md",
     "sfw.02.thema-verwoorder", "thema-verwoorder.definieer-epic-structuur", "024"),
    ("025",
     "artefacten/sfw/sfw.02.thema-verwoorder/templates/thema-verwoorder.definieer-thematische-scope.template.md",
     "sfw.02.thema-verwoorder", "thema-verwoorder.definieer-thematische-scope", "025"),
    ("026",
     "artefacten/sfw/sfw.02.thema-verwoorder/templates/thema-verwoorder.definieer-verbeter-voorstellen.template.md",
     "sfw.02.thema-verwoorder", "thema-verwoorder.definieer-verbeter-voorstellen", "026"),
    ("027",
     "artefacten/sfw/sfw.03.gedragsspecificator/templates/gedragsspecificator.specificeer-gedrag.template.md",
     "sfw.03.gedragsspecificator", "gedragsspecificator.specificeer-gedrag", "027"),
    ("028",
     "artefacten/sfw/sfw.03.gedragsspecificator/templates/gedragsspecificator.valideer-scenario-consistentie.template.md",
     "sfw.03.gedragsspecificator", "gedragsspecificator.valideer-scenario-consistentie", "028"),
    ("029",
     "artefacten/sfw/sfw.03.gedragsspecificator/templates/gedragsspecificator.vertaal-naar-gherkin.template.md",
     "sfw.03.gedragsspecificator", "gedragsspecificator.vertaal-naar-gherkin", "029"),
]


def compute_digest(body: str) -> str:
    """Bereken 4-char MD5 hash van de body-inhoud."""
    return hashlib.md5(body.encode("utf-8")).hexdigest()[:4]


def parse_first_yaml_block(content: str):
    """
    Detecteer het eerste YAML-frontmatter blok (---...---).
    Strips leading BOM if present.

    Returns:
        (yaml_text, body, versie, status) of (None, content, None, None) als geen header.
    """
    # Strip BOM indien aanwezig
    text = content.lstrip("\ufeff")

    if not text.startswith("---"):
        return None, content, None, None

    # Zoek het sluitende ---
    end = text.find("\n---", 3)
    if end == -1:
        return None, content, None, None

    yaml_text = text[3:end].strip()
    # Body begint na de sluitende --- en eventuele newline
    body_start = end + 4
    if body_start < len(text) and text[body_start] == "\n":
        body_start += 1
    body = text[body_start:]

    # Lees versie en status uit de bestaande YAML
    versie = None
    status = None
    for line in yaml_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("versie:"):
            val = stripped[7:].strip().strip('"').strip("'")
            if val:
                versie = val
        elif stripped.startswith("status:"):
            val = stripped[7:].strip().strip('"').strip("'")
            if val and val not in ("{status}", ""):
                status = val

    return yaml_text, body, versie, status


def build_canonical_header(
    template_id: str,
    template_naam: str,
    artefact_type_id: str,
    agent_id: str,
    versie: str,
    status: str,
    digest: str,
) -> str:
    """Bouw de canonieke §4 YAML header op."""
    return (
        "---\n"
        "# IDENTIFICATIE\n"
        f'template-id: "{template_id}"\n'
        f"template-naam: {template_naam}\n"
        "\n"
        "# RELATIES\n"
        f"artefact-type-id: {artefact_type_id}\n"
        f"agent-id: {agent_id}\n"
        "\n"
        "# META-DATA\n"
        f"versie: {versie}\n"
        f"status: {status}\n"
        f"digest: {digest}\n"
        "---\n"
    )


def migrate_file(
    filepath: Path,
    template_id: str,
    template_naam: str,
    artefact_type_id: str,
    agent_id: str,
    dry_run: bool = False,
) -> tuple[bool, str]:
    """
    Verwerk één template-bestand.

    Returns:
        (modified: bool, preview: str)
    """
    raw = filepath.read_text(encoding="utf-8-sig")  # utf-8-sig strips BOM automatisch

    _, body, existing_versie, existing_status = parse_first_yaml_block(raw)

    versie = existing_versie or "0.1.0"
    status = existing_status or "vers"
    digest = compute_digest(body)

    new_header = build_canonical_header(
        template_id=template_id,
        template_naam=template_naam,
        artefact_type_id=f'"{artefact_type_id}"' if artefact_type_id else '""',
        agent_id=agent_id,
        versie=versie,
        status=status,
        digest=digest,
    )

    new_content = new_header + body

    # Controleer of er al een identieke canonieke header aanwezig is
    current = filepath.read_text(encoding="utf-8-sig")
    if current == new_content:
        return False, "(geen wijziging)"

    preview = new_header.strip()

    if not dry_run:
        filepath.write_text(new_content, encoding="utf-8")

    return True, preview


def main():
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print("=== DRY RUN MODE (geen bestanden worden gewijzigd) ===\n")

    modified_count = 0
    skipped_count = 0

    for template_id, rel_path, agent_id, template_naam, artefact_type_id in TEMPLATE_REGISTRY:
        filepath = WORKSPACE / rel_path.replace("/", "\\")

        if not filepath.exists():
            print(f"  [ONTBREEKT] {rel_path}")
            continue

        modified, preview = migrate_file(
            filepath=filepath,
            template_id=template_id,
            template_naam=template_naam,
            artefact_type_id=artefact_type_id,
            agent_id=agent_id,
            dry_run=dry_run,
        )

        if modified:
            status_label = "DRY-RUN" if dry_run else "GEWIJZIGD"
            print(f"  [{status_label}] {rel_path}")
            if dry_run:
                for line in preview.splitlines():
                    print(f"    {line}")
                print()
            modified_count += 1
        else:
            print(f"  [skip]    {rel_path}")
            skipped_count += 1

    print("=" * 60)
    action = "te wijzigen" if dry_run else "gewijzigd"
    print(f"Totaal {action}: {modified_count}  |  Overgeslagen: {skipped_count}")
    if dry_run:
        print("\nVoer opnieuw uit zonder --dry-run om de wijzigingen door te voeren.")


if __name__ == "__main__":
    main()
