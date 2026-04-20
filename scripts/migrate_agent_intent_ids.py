#!/usr/bin/env python3
"""
Migratiescript: agent-id en intent-id toevoegen aan alle agents.

Acties per bestandstype:
  Charter  (*.charter.md)        → voeg 'agent-id:' toe na 'agent:'-regel
  Boundary (*boundary*.md)       → voeg 'agent-id:' toe na 'agent:'-regel
  Contract (*.agent.md)          → voeg 'intent-id:' toe na 'intent:'-regel
  Prompt   (*.prompt.md)         → voeg 'intent-id:' toe na 'intent:'-regel

Slaat bestanden over als het veld al aanwezig is.
Ondersteunt --dry-run en --only <type> [charters|boundaries|contracts|prompts].
"""

import re
import sys
from pathlib import Path

WORKSPACE = Path(r"c:\git\mandarin-agents")

# ── Agent-ID registry ──────────────────────────────────────────────────────────
AGENT_ID = {
    "canon-curator":                        "aeo.01.canon-curator",
    "capability-architect":                 "aeo.01.capability-architect",
    "agent-ontwerper":                      "aeo.02.agent-ontwerper",
    "agent-engineer":                       "aeo.02.agent-engineer",
    "agent-curator":                        "aeo.02.agent-curator",
    "ecosysteem-beschrijver":               "aeo.02.ecosysteem-beschrijver",
    "handoff-steward":                      "aeo.03.handoff-steward",
    "core-framework-architect":             "aod.02.core-framework-architect",
    "solution-architect":                   "aod.05.solution-architect",
    "documentatie-omvormer":               "fnd.01.documentatie-omvormer",
    "ecosysteem-coordinator":              "fnd.01.ecosysteem-coordinator",
    "concept-curator":                      "fnd.02.concept-curator",
    "documentvertaler":                     "fnd.02.documentvertaler",
    "behoefteprofiel-opsteller":            "miv.07.behoefteprofiel-opsteller",
    "leveranciers-verkenner":               "miv.07.leveranciers-verkenner",
    "positionering-en-monetisatie-toetser": "miv.07.positionering-en-monetisatie-toetser",
    "hypothese-vormer":                     "sfw.01.hypothese-vormer",
    "thema-verwoorder":                     "sfw.02.thema-verwoorder",
    "gedragsspecificator":                  "sfw.03.gedragsspecificator",
    # Stubs (geen charters/contracts, wel boundary)
    "architectuur-verkenner":              "aod.01.architectuur-verkenner",
    "logisch-modelleur":                    "sfw.03.logisch-modelleur",
}

# ── Intent-ID mapping: (agent-naam, intent-slug) → samengestelde sleutel ────────
INTENT_ID = {
    # agent-ontwerper
    ("agent-ontwerper", "definieer-agent-charter"):     "aeo.02.agent-ontwerper.01",
    ("agent-ontwerper", "definieer-agent-contract"):    "aeo.02.agent-ontwerper.02",
    ("agent-ontwerper", "definieer-agent-template"):    "aeo.02.agent-ontwerper.03",
    # agent-engineer
    ("agent-engineer", "realiseer-agent-prompts"):          "aeo.02.agent-engineer.01",
    ("agent-engineer", "realiseer-agent-taskconfiguratie"): "aeo.02.agent-engineer.02",
    ("agent-engineer", "realiseer-agent-runner"):           "aeo.02.agent-engineer.03",
    # agent-curator
    ("agent-curator", "valideer-boundary-overlap"):              "aeo.02.agent-curator.01",
    ("agent-curator", "valideer-agent-consistentie"):            "aeo.02.agent-curator.02",
    ("agent-curator", "valideer-runner-contract-consistentie"):  "aeo.02.agent-curator.03",
    ("agent-curator", "rapporteer-ecosysteem-overzicht"):        "aeo.02.agent-curator.04",
    ("agent-curator", "rapporteer-prompts-overzicht"):           "aeo.02.agent-curator.05",
    # handoff-steward
    ("handoff-steward", "realiseer-initiele-handoff"):               "aeo.03.handoff-steward.01",
    ("handoff-steward", "realiseer-handoff-sluiting"):               "aeo.03.handoff-steward.02",
    ("handoff-steward", "realiseer-overzicht-inspectie-handoffs"):   "aeo.03.handoff-steward.03",
    # canon-curator
    ("canon-curator", "valideer-terminologische-scherpte"): "aeo.01.canon-curator.01",
    ("canon-curator", "valideer-grondslag-consistentie"):   "aeo.01.canon-curator.02",
    ("canon-curator", "adviseer-grondslag-verbeteringen"):  "aeo.01.canon-curator.03",
    ("canon-curator", "publiceer-grondslagen"):             "aeo.01.canon-curator.04",
    # capability-architect
    ("capability-architect", "definieer-agent-boundary"):  "aeo.01.capability-architect.01",
    # ecosysteem-beschrijver
    ("ecosysteem-beschrijver", "beschrijf-agent-positionering"):            "aeo.02.ecosysteem-beschrijver.01",
    ("ecosysteem-beschrijver", "beschrijf-ecosysteem-artefacten"):          "aeo.02.ecosysteem-beschrijver.02",
    ("ecosysteem-beschrijver", "beschrijf-ecosysteem-contracten"):          "aeo.02.ecosysteem-beschrijver.03",
    ("ecosysteem-beschrijver", "beschrijf-ecosysteem-value-streams-agents"): "aeo.02.ecosysteem-beschrijver.04",
    # core-framework-architect
    ("core-framework-architect", "structureer-actieve-structuur"):  "aod.02.core-framework-architect.01",
    ("core-framework-architect", "structureer-gedrag"):             "aod.02.core-framework-architect.02",
    ("core-framework-architect", "structureer-passieve-structuur"): "aod.02.core-framework-architect.03",
    ("core-framework-architect", "structureer-totaal-view"):        "aod.02.core-framework-architect.04",
    # solution-architect
    ("solution-architect", "definieer-oplossingsscenarios"):         "aod.05.solution-architect.01",
    ("solution-architect", "definieer-integrale-architectuur"):      "aod.05.solution-architect.02",
    ("solution-architect", "definieer-architectuur-keuze-document"): "aod.05.solution-architect.03",
    # documentatie-omvormer
    ("documentatie-omvormer", "genereer-correcte-links"):     "fnd.01.documentatie-omvormer.01",
    ("documentatie-omvormer", "genereer-navigatiebestand"):   "fnd.01.documentatie-omvormer.02",
    ("documentatie-omvormer", "genereer-publicatiestructuur"): "fnd.01.documentatie-omvormer.03",
    # ecosysteem-coordinator
    ("ecosysteem-coordinator", "aggregeer-tasks"):       "fnd.01.ecosysteem-coordinator.01",
    ("ecosysteem-coordinator", "genereer-instructies"):  "fnd.01.ecosysteem-coordinator.02",
    # concept-curator
    ("concept-curator", "definieer-concept"):           "fnd.02.concept-curator.01",
    ("concept-curator", "rapporteer-concept-status"):   "fnd.02.concept-curator.02",
    ("concept-curator", "valideer-concept-coherentie"): "fnd.02.concept-curator.03",
    ("concept-curator", "verweef-concepten"):           "fnd.02.concept-curator.04",
    # documentvertaler
    ("documentvertaler", "zet-om-naar-docx"): "fnd.02.documentvertaler.01",
    # behoefteprofiel-opsteller
    ("behoefteprofiel-opsteller", "beschrijf-selectiecriteria"): "miv.07.behoefteprofiel-opsteller.01",
    ("behoefteprofiel-opsteller", "formuleer-behoefteprofiel"):  "miv.07.behoefteprofiel-opsteller.02",
    ("behoefteprofiel-opsteller", "structureer-eisenpakket"):    "miv.07.behoefteprofiel-opsteller.03",
    # leveranciers-verkenner
    ("leveranciers-verkenner", "beschrijf-uitsluitingsgronden"): "miv.07.leveranciers-verkenner.01",
    ("leveranciers-verkenner", "beschrijf-longlist"):            "miv.07.leveranciers-verkenner.02",
    ("leveranciers-verkenner", "beschrijf-leveranciersfit"):     "miv.07.leveranciers-verkenner.03",
    # positionering-en-monetisatie-toetser
    ("positionering-en-monetisatie-toetser", "signaleer-spanningsvelden"):         "miv.07.positionering-en-monetisatie-toetser.01",
    ("positionering-en-monetisatie-toetser", "toets-strategische-compatibiliteit"): "miv.07.positionering-en-monetisatie-toetser.02",
    ("positionering-en-monetisatie-toetser", "stel-toetsingsrapport-op"):          "miv.07.positionering-en-monetisatie-toetser.03",
    # hypothese-vormer
    ("hypothese-vormer", "beschrijf-aannames"):    "sfw.01.hypothese-vormer.01",
    ("hypothese-vormer", "beschrijf-hypothese"):   "sfw.01.hypothese-vormer.02",
    ("hypothese-vormer", "beschrijf-toetsbaarheid"): "sfw.01.hypothese-vormer.03",
    # thema-verwoorder
    ("thema-verwoorder", "definieer-thematische-scope"):     "sfw.02.thema-verwoorder.01",
    ("thema-verwoorder", "definieer-epic-structuur"):        "sfw.02.thema-verwoorder.02",
    ("thema-verwoorder", "definieer-verbeter-voorstel"):     "sfw.02.thema-verwoorder.03",
    # gedragsspecificator
    ("gedragsspecificator", "specificeer-gedrag"):              "sfw.03.gedragsspecificator.01",
    ("gedragsspecificator", "valideer-scenario-consistentie"):  "sfw.03.gedragsspecificator.02",
    ("gedragsspecificator", "vertaal-naar-gherkin"):            "sfw.03.gedragsspecificator.03",
}


# ── Hulpfuncties ──────────────────────────────────────────────────────────────

def insert_after_field(content: str, field: str, new_line: str) -> tuple[bool, str]:
    """
    Voeg 'new_line' in direct na de eerste regel die begint met 'field:' in de
    eerste YAML-frontmatter block (--- ... ---).

    Returns (modified, new_content).
    """
    # Zorg dat we alleen binnen het eerste YAML-block werken
    # Detecteer einde van eerste block
    text = content.lstrip("\ufeff")
    if not text.startswith("---"):
        return False, content

    block_end = text.find("\n---", 3)
    if block_end == -1:
        return False, content

    header = text[:block_end]
    rest = text[block_end:]

    # Zoek de field-regel (case-sensitive, exact begin van de regel)
    pattern = re.compile(r"^(" + re.escape(field) + r":[ \t]*.*)$", re.MULTILINE)
    m = pattern.search(header)
    if not m:
        return False, content

    insert_pos = m.end()
    new_header = header[:insert_pos] + "\n" + new_line + header[insert_pos:]
    return True, new_header + rest


def get_yaml_field(content: str, field: str) -> str | None:
    """Lees de waarde van een YAML-veld uit het eerste frontmatter block."""
    text = content.lstrip("\ufeff")
    if not text.startswith("---"):
        return None
    block_end = text.find("\n---", 3)
    header = text[:block_end] if block_end != -1 else text
    m = re.search(r"^" + re.escape(field) + r":\s*(.+)$", header, re.MULTILINE)
    return m.group(1).strip() if m else None


def has_field(content: str, field: str) -> bool:
    """Controleert of een YAML-veld al aanwezig is in het eerste frontmatter block."""
    text = content.lstrip("\ufeff")
    if not text.startswith("---"):
        return False
    block_end = text.find("\n---", 3)
    header = text[:block_end] if block_end != -1 else text
    return bool(re.search(r"^" + re.escape(field) + r":", header, re.MULTILINE))


def agent_from_charter(filepath: Path) -> str:
    """Extraheer agent-naam uit charter bestandsnaam: {agent}.charter.md"""
    return filepath.name.replace(".charter.md", "")


def agent_from_boundary(filepath: Path) -> str:
    """Extraheer agent-naam uit boundary bestandsnaam (twee patronen)."""
    name = filepath.name
    if name.endswith(".agent-boundary.md"):
        return name.replace(".agent-boundary.md", "")
    if name.startswith("agent-boundary-"):
        return name.replace("agent-boundary-", "").replace(".md", "")
    return name.replace(".md", "")


def agent_intent_from_contract(filepath: Path) -> tuple[str, str]:
    """
    Extraheer (agent, intent) uit contract bestandsnaam:
    {agent}.{intent}.agent.md
    De agent-naam kan punten bevatten (bijv. positionering-en-monetisatie-toetser).
    Gebruik de AGENT_ID registry als oracle.
    """
    stem = filepath.name.replace(".agent.md", "")
    # Probeer alle bekende agent-namen (langste eerst om ambiguïteit te vermijden)
    for agent_name in sorted(AGENT_ID.keys(), key=len, reverse=True):
        prefix = agent_name + "."
        if stem.startswith(prefix):
            intent = stem[len(prefix):]
            return agent_name, intent
    # Fallback: splits op eerste punt
    parts = stem.split(".", 1)
    return (parts[0], parts[1]) if len(parts) == 2 else (stem, "")


def agent_intent_from_prompt(filepath: Path) -> tuple[str, str]:
    """
    Extraheer (agent, intent) uit prompt bestandsnaam:
    mandarin.{agent}.{intent}.prompt.md
    De agent-naam kan punten bevatten.
    """
    stem = filepath.name.replace(".prompt.md", "")
    # Strip 'mandarin.' prefix
    if stem.startswith("mandarin."):
        stem = stem[len("mandarin."):]
    # Gebruik registry als oracle
    for agent_name in sorted(AGENT_ID.keys(), key=len, reverse=True):
        prefix = agent_name + "."
        if stem.startswith(prefix):
            intent = stem[len(prefix):]
            return agent_name, intent
    parts = stem.split(".", 1)
    return (parts[0], parts[1]) if len(parts) == 2 else (stem, "")


# ── Verwerking per bestandstype ───────────────────────────────────────────────

def process_charter_or_boundary(filepath: Path, dry_run: bool) -> str:
    """Voeg agent-id toe aan charter of boundary. Retourneert status-label."""
    content = filepath.read_text(encoding="utf-8-sig")

    if has_field(content, "agent-id"):
        return "skip (al aanwezig)"

    # Bepaal agent-naam
    if filepath.name.endswith(".charter.md"):
        agent_name = agent_from_charter(filepath)
    else:
        agent_name = agent_from_boundary(filepath)

    agent_id = AGENT_ID.get(agent_name)
    if not agent_id:
        return f"WARN (onbekende agent: {agent_name})"

    new_line = f"agent-id: {agent_id}"
    modified, new_content = insert_after_field(content, "agent", new_line)

    if not modified:
        return "WARN (geen 'agent:'-veld gevonden)"

    if not dry_run:
        filepath.write_text(new_content, encoding="utf-8")
    return "GEWIJZIGD"


def process_contract_or_prompt(filepath: Path, dry_run: bool) -> str:
    """Voeg intent-id toe aan contract of prompt. Retourneert status-label."""
    content = filepath.read_text(encoding="utf-8-sig")

    if has_field(content, "intent-id"):
        return "skip (al aanwezig)"

    # Probeer intent te lezen uit YAML-veld
    intent_from_yaml = get_yaml_field(content, "intent")

    if filepath.suffix == ".md" and ".agent.md" in filepath.name:
        agent_name, intent_from_filename = agent_intent_from_contract(filepath)
    else:
        agent_name, intent_from_filename = agent_intent_from_prompt(filepath)

    intent = intent_from_yaml or intent_from_filename

    if not intent:
        return f"WARN (geen intent gevonden in {filepath.name})"

    # Strip eventuele 'mandarin.' prefix uit agent-veld
    if not agent_name:
        agent_raw = get_yaml_field(content, "agent") or ""
        agent_name = agent_raw.replace("mandarin.", "")

    key = (agent_name, intent)
    intent_id = INTENT_ID.get(key)
    if not intent_id:
        return f"WARN (onbekende combinatie: {agent_name}.{intent})"

    new_line = f"intent-id: {intent_id}"
    modified, new_content = insert_after_field(content, "intent", new_line)

    if not modified:
        return "WARN (geen 'intent:'-veld gevonden)"

    if not dry_run:
        filepath.write_text(new_content, encoding="utf-8")
    return "GEWIJZIGD"


# ── Bestandsverzamelingen ─────────────────────────────────────────────────────

def find_charters():
    return sorted(WORKSPACE.glob("artefacten/**/*.charter.md"))


def find_boundaries():
    """Alleen echte boundary-bestanden, geen contracts/prompts."""
    candidates = list(WORKSPACE.glob("artefacten/**/*boundary*.md"))
    return sorted(
        p for p in candidates
        if p.name.endswith(".agent-boundary.md") or p.name.startswith("agent-boundary-")
    )


def find_contracts():
    artefacten = sorted(WORKSPACE.glob("artefacten/**/agent-contracten/*.agent.md"))
    github = sorted((WORKSPACE / ".github" / "agents").glob("*.agent.md"))
    return artefacten + github


def find_prompts():
    artefacten = sorted(WORKSPACE.glob("artefacten/**/prompts/*.prompt.md"))
    github = sorted((WORKSPACE / ".github" / "prompts").glob("*.prompt.md"))
    return artefacten + github


# ── Main ──────────────────────────────────────────────────────────────────────

def run_section(label: str, files, processor, dry_run: bool):
    print(f"\n{'=' * 60}")
    print(label)
    print("=" * 60)
    modified = skipped = warned = 0
    for filepath in files:
        status = processor(filepath, dry_run)
        rel = filepath.relative_to(WORKSPACE)
        if status == "GEWIJZIGD":
            tag = "DRY-RUN" if dry_run else "GEWIJZIGD"
            print(f"  [{tag}] {rel}")
            modified += 1
        elif status.startswith("WARN"):
            print(f"  [{status}] {rel}")
            warned += 1
        else:
            skipped += 1
    action = "te wijzigen" if dry_run else "gewijzigd"
    print(f"\n  Totaal {action}: {modified}  |  Overgeslagen: {skipped}  |  Waarschuwingen: {warned}")
    return modified


def main():
    dry_run = "--dry-run" in sys.argv
    only_arg = None
    if "--only" in sys.argv:
        idx = sys.argv.index("--only")
        if idx + 1 < len(sys.argv):
            only_arg = sys.argv[idx + 1]

    if dry_run:
        print("=== DRY RUN MODE (geen bestanden worden gewijzigd) ===")

    total = 0

    if only_arg in (None, "charters"):
        total += run_section(
            "CHARTERS",
            find_charters(),
            process_charter_or_boundary,
            dry_run,
        )

    if only_arg in (None, "boundaries"):
        total += run_section(
            "BOUNDARIES",
            find_boundaries(),
            process_charter_or_boundary,
            dry_run,
        )

    if only_arg in (None, "contracts"):
        total += run_section(
            "CONTRACTS",
            find_contracts(),
            process_contract_or_prompt,
            dry_run,
        )

    if only_arg in (None, "prompts"):
        total += run_section(
            "PROMPTS",
            find_prompts(),
            process_contract_or_prompt,
            dry_run,
        )

    action = "te wijzigen" if dry_run else "gewijzigd"
    print(f"\n{'=' * 60}")
    print(f"TOTAAL {action}: {total}")
    if dry_run:
        print("Voer opnieuw uit zonder --dry-run om de wijzigingen door te voeren.")


if __name__ == "__main__":
    main()
