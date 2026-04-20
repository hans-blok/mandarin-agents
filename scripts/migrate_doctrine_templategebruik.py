#!/usr/bin/env python3
"""
Migration script: doctrine-templategebruik compliance.

Adds:
1. Contractuele templatebinding block to all contracts (before ### Foutafhandeling)
2. doctrine-templategebruik.md to contract governance (before **Canon-consultatie:**)
3. template: field to prompt YAML frontmatter (after value_stream_fase:)
4. doctrine-templategebruik.md to charter governance/herkomstverantwoording

Skips files that already contain these additions.
"""

import os
import re
import sys
from pathlib import Path

WORKSPACE = Path(r"c:\git\mandarin-agents")

# ── Template mapping: (agent_slug, intent) → template path ──────────────────
# '~' means no separate template file exists
TEMPLATE_MAP = {
    # Fase 2: agents WITH templates
    # capability-architect
    ("capability-architect", "definieer-agent-boundary"): "templates/agent-boundary.template.md",
    # ecosysteem-beschrijver
    ("ecosysteem-beschrijver", "beschrijf-agent-positionering"): "templates/beschrijf-agent-positionering.template.md",
    ("ecosysteem-beschrijver", "beschrijf-ecosysteem-artefacten"): "templates/beschrijf-ecosysteem-artefacten.template.md",
    ("ecosysteem-beschrijver", "beschrijf-ecosysteem-contracten"): "templates/beschrijf-ecosysteem-contracten.template.md",
    ("ecosysteem-beschrijver", "beschrijf-ecosysteem-value-streams-agents"): "templates/beschrijf-ecosysteem-value-streams-agents.template.md",
    # core-framework-architect
    ("core-framework-architect", "structureer-actieve-structuur"): "templates/core-framework-architect.structureer-actieve-structuur.template.md",
    ("core-framework-architect", "structureer-gedrag"): "templates/core-framework-architect.structureer-gedrag.template.md",
    ("core-framework-architect", "structureer-passieve-structuur"): "~",
    ("core-framework-architect", "structureer-totaal-view"): "templates/core-framework-architect.structureer-totaal-view.template.md",
    # solution-architect
    ("solution-architect", "definieer-architectuur-keuze-document"): "templates/solution-architect.definieer-architectuur-keuze-document.template.md",
    ("solution-architect", "definieer-integrale-architectuur"): "~",
    ("solution-architect", "definieer-oplossingsscenarios"): "~",
    # documentatie-omvormer
    ("documentatie-omvormer", "genereer-publicatiestructuur"): "templates/mkdocs-yml.template.md",
    ("documentatie-omvormer", "genereer-navigatiebestand"): "~",
    ("documentatie-omvormer", "genereer-correcte-links"): "~",
    # concept-curator
    ("concept-curator", "definieer-concept"): "templates/concept.template.md",
    ("concept-curator", "rapporteer-concept-status"): "~",
    ("concept-curator", "valideer-concept-coherentie"): "~",
    ("concept-curator", "verweef-concepten"): "~",
    # hypothese-vormer
    ("hypothese-vormer", "beschrijf-hypothese"): "templates/hypothese-template.md",
    ("hypothese-vormer", "beschrijf-aannames"): "templates/hypothese-template.md",
    ("hypothese-vormer", "beschrijf-toetsbaarheid"): "templates/hypothese-template.md",
    # thema-verwoorder
    ("thema-verwoorder", "definieer-epic-structuur"): "templates/thema-verwoorder.definieer-epic-structuur.template.md",
    ("thema-verwoorder", "definieer-thematische-scope"): "templates/thema-verwoorder.definieer-thematische-scope.template.md",
    ("thema-verwoorder", "definieer-verbeter-voorstel"): "templates/thema-verwoorder.definieer-verbeter-voorstellen.template.md",
    # gedragsspecificator
    ("gedragsspecificator", "specificeer-gedrag"): "templates/gedragsspecificator.specificeer-gedrag.template.md",
    ("gedragsspecificator", "valideer-scenario-consistentie"): "templates/gedragsspecificator.valideer-scenario-consistentie.template.md",
    ("gedragsspecificator", "vertaal-naar-gherkin"): "templates/gedragsspecificator.vertaal-naar-gherkin.template.md",

    # Fase 3: agents WITHOUT templates (all ~)
    # canon-curator
    ("canon-curator", "adviseer-grondslag-verbeteringen"): "~",
    ("canon-curator", "valideer-grondslag-consistentie"): "~",
    ("canon-curator", "valideer-terminologische-scherpte"): "~",
    ("canon-curator", "publiceer-grondslagen"): "~",
    # ecosysteem-coordinator
    ("ecosysteem-coordinator", "aggregeer-tasks"): "~",
    ("ecosysteem-coordinator", "genereer-instructies"): "~",
    # documentvertaler
    ("documentvertaler", "zet-om-naar-docx"): "~",
    # behoefteprofiel-opsteller
    ("behoefteprofiel-opsteller", "formuleer-behoefteprofiel"): "~",
    ("behoefteprofiel-opsteller", "beschrijf-selectiecriteria"): "~",
    ("behoefteprofiel-opsteller", "structureer-eisenpakket"): "~",
    # positionering-en-monetisatie-toetser
    ("positionering-en-monetisatie-toetser", "toets-strategische-compatibiliteit"): "~",
    ("positionering-en-monetisatie-toetser", "stel-toetsingsrapport-op"): "~",
    ("positionering-en-monetisatie-toetser", "signaleer-spanningsvelden"): "~",
    # leveranciers-verkenner
    ("leveranciers-verkenner", "beschrijf-longlist"): "~",
    ("leveranciers-verkenner", "beschrijf-leveranciersfit"): "~",
    ("leveranciers-verkenner", "beschrijf-uitsluitingsgronden"): "~",
}

# Agents to SKIP (already compliant or stubs)
SKIP_AGENTS = {
    "agent-ontwerper", "agent-engineer", "agent-curator",  # Already compliant
    "handoff-steward",  # Just completed in Fase 1
    "architectuur-verkenner", "strategy-framework-architect",  # Stubs
}

# Charter-level mapping: agent_slug → list of intents that the charter covers
# (built from TEMPLATE_MAP keys)
CHARTER_AGENTS = {}
for (agent, intent), tmpl in TEMPLATE_MAP.items():
    CHARTER_AGENTS.setdefault(agent, []).append((intent, tmpl))


def parse_agent_intent_from_contract(filename: str):
    """Extract (agent_slug, intent) from contract filename like
    'agent-slug.intent-name.agent.md'"""
    name = filename.replace(".agent.md", "")
    dot_idx = name.find(".")
    if dot_idx == -1:
        return None, None
    return name[:dot_idx], name[dot_idx + 1:]


def parse_agent_intent_from_prompt(filename: str):
    """Extract (agent_slug, intent) from prompt filename like
    'mandarin.agent-slug.intent-name.prompt.md'"""
    name = filename.replace(".prompt.md", "")
    parts = name.split(".", 2)
    if len(parts) < 3:
        return None, None
    return parts[1], parts[2]


def modify_contract(filepath: Path, template_value: str, dry_run: bool = False) -> bool:
    """Add Contractuele templatebinding and doctrine-templategebruik to a contract."""
    content = filepath.read_text(encoding="utf-8")
    modified = False

    # 1. Insert Contractuele templatebinding before ### Foutafhandeling
    if "Contractuele templatebinding" not in content:
        fout_match = re.search(r"\n### Foutafhandeling\n", content)
        if fout_match:
            binding_block = (
                "\n**Contractuele templatebinding**:\n\n"
                "```yaml\n"
                f"template: {template_value}\n"
                "```\n\n"
                "### Foutafhandeling\n"
            )
            content = content[:fout_match.start()] + binding_block + content[fout_match.end():]
            modified = True
        else:
            print(f"  WARNING: No ### Foutafhandeling found in {filepath.name}")

    # 2. Add doctrine-templategebruik to governance section
    if "doctrine-templategebruik" not in content:
        doctrine_line = (
            "- **doctrine-templategebruik.md** (v1.0.0):\n"
            "  - Contractuele templatebinding expliciet opgenomen\n"
        )
        # Strategy A: Insert before **Canon-consultatie:** (most contracts)
        canon_match = re.search(r"\n\*\*Canon-consultatie", content)
        if canon_match:
            content = content[:canon_match.start()] + "\n" + doctrine_line + content[canon_match.start():]
            modified = True
        else:
            # Strategy B: Contracts with simple Governance section (e.g., gedragsspecificator)
            # Find ## Governance section and add after last bullet
            gov_match = re.search(r"## Governance\n", content)
            if gov_match:
                # Find the next ## section after Governance
                next_section = re.search(r"\n## ", content[gov_match.end():])
                if next_section:
                    insert_pos = gov_match.end() + next_section.start()
                    content = content[:insert_pos] + "\n" + doctrine_line + content[insert_pos:]
                    modified = True
                else:
                    # No next section — append at end
                    content = content.rstrip() + "\n\n" + doctrine_line
                    modified = True
            else:
                print(f"  WARNING: No governance section found in {filepath.name}")

    if modified and not dry_run:
        filepath.write_text(content, encoding="utf-8")
    
    return modified


def modify_prompt(filepath: Path, template_value: str, dry_run: bool = False) -> bool:
    """Add template: field to prompt YAML frontmatter after value_stream_fase:."""
    content = filepath.read_text(encoding="utf-8")
    
    if "template:" in content:
        return False  # Already has template field

    # Strategy A: Find value_stream_fase: line and insert template: after it
    vsf_match = re.search(r"(value_stream_fase: .+)\n", content)
    if vsf_match:
        insert_pos = vsf_match.end()
        template_line = f"template: {template_value}\n"
        content = content[:insert_pos] + template_line + content[insert_pos:]
        if not dry_run:
            filepath.write_text(content, encoding="utf-8")
        return True

    # Strategy B: No value_stream_fase — insert before closing --- 
    # Find the second --- (closing frontmatter)
    first_delim = content.find("---")
    if first_delim != -1:
        second_delim = content.find("---", first_delim + 3)
        if second_delim != -1:
            template_line = f"template: {template_value}\n"
            content = content[:second_delim] + template_line + content[second_delim:]
            if not dry_run:
                filepath.write_text(content, encoding="utf-8")
            return True

    print(f"  WARNING: Cannot find insertion point in {filepath.name}")
    return False


def modify_charter(filepath: Path, dry_run: bool = False) -> bool:
    """Add doctrine-templategebruik to charter governance/herkomstverantwoording."""
    content = filepath.read_text(encoding="utf-8")

    if "doctrine-templategebruik" in content:
        return False  # Already present

    # Strategy: Find "- Governance en doctrines:" line in section 10 (Herkomstverantwoording)
    # and append doctrine-templategebruik to that line
    gov_line_match = re.search(
        r"(- Governance en doctrines: .+?`doctrine-agent-charter-normering\.md`[^\n]*)",
        content
    )
    if gov_line_match:
        old_line = gov_line_match.group(1)
        new_line = old_line + " en `doctrine-templategebruik.md` (v1.0.0)"
        content = content[:gov_line_match.start(1)] + new_line + content[gov_line_match.end(1):]
        if not dry_run:
            filepath.write_text(content, encoding="utf-8")
        return True

    # Fallback: Find "- Governance:" line (shorter form, e.g., thema-verwoorder)
    gov_short_match = re.search(
        r"(- Governance: .*?`beleid-workspace\.md`[^\n]*)",
        content
    )
    if gov_short_match:
        old_line = gov_short_match.group(1)
        new_line = old_line + ", `doctrine-templategebruik.md` (v1.0.0)"
        content = content[:gov_short_match.start(1)] + new_line + content[gov_short_match.end(1):]
        if not dry_run:
            filepath.write_text(content, encoding="utf-8")
        return True

    # Fallback: "- Volgt doctrine-agent-charter-normering.md" (no backticks, e.g., ecosysteem-beschrijver)
    volgt_match = re.search(
        r"(- Volgt doctrine-agent-charter-normering\.md)\n",
        content
    )
    if volgt_match:
        old_line = volgt_match.group(1)
        content = content[:volgt_match.end()] + "- Volgt doctrine-templategebruik.md (v1.0.0)\n" + content[volgt_match.end():]
        if not dry_run:
            filepath.write_text(content, encoding="utf-8")
        return True

    # Fallback: "Conform: `doctrine-agent-charter-normering.md`" (e.g., gedragsspecificator)
    conform_match = re.search(
        r"(- +Conform: `doctrine-agent-charter-normering\.md`[^\n]*)\n",
        content
    )
    if conform_match:
        content = content[:conform_match.end()] + "-   Conform: `doctrine-templategebruik.md` v1.0.0\n" + content[conform_match.end():]
        if not dry_run:
            filepath.write_text(content, encoding="utf-8")
        return True

    print(f"  WARNING: No governance line found in charter {filepath.name}")
    return False


def find_contracts():
    """Find all contract files that need migration."""
    results = []
    for agent_dir in WORKSPACE.glob("artefacten/*/*"):
        if not agent_dir.is_dir():
            continue
        contracts_dir = agent_dir / "agent-contracten"
        if not contracts_dir.exists():
            continue
        
        for contract in contracts_dir.glob("*.agent.md"):
            agent, intent = parse_agent_intent_from_contract(contract.name)
            if agent in SKIP_AGENTS:
                continue
            key = (agent, intent)
            if key not in TEMPLATE_MAP:
                print(f"  SKIP (not in map): {contract.name}")
                continue
            results.append((contract, agent, intent, TEMPLATE_MAP[key]))
    return results


def find_prompts():
    """Find all prompt files in artefacten/ that need migration."""
    results = []
    for prompt in WORKSPACE.glob("artefacten/**/prompts/*.prompt.md"):
        agent, intent = parse_agent_intent_from_prompt(prompt.name)
        if agent in SKIP_AGENTS:
            continue
        key = (agent, intent)
        if key not in TEMPLATE_MAP:
            print(f"  SKIP prompt (not in map): {prompt.name}")
            continue
        results.append((prompt, agent, intent, TEMPLATE_MAP[key]))
    return results


def find_charters():
    """Find all charter files that need migration."""
    results = []
    for charter in WORKSPACE.glob("artefacten/**/*.charter.md"):
        agent = charter.stem.replace(".charter", "")
        if agent in SKIP_AGENTS:
            continue
        if agent in CHARTER_AGENTS:
            results.append((charter, agent))
    return results


def main():
    dry_run = "--dry-run" in sys.argv
    if dry_run:
        print("=== DRY RUN MODE ===\n")

    # ── Contracts ──
    print("=" * 60)
    print("CONTRACTS")
    print("=" * 60)
    contracts = find_contracts()
    contract_count = 0
    for filepath, agent, intent, template in sorted(contracts):
        result = modify_contract(filepath, template, dry_run)
        status = "MODIFIED" if result else "skip (already done)"
        print(f"  [{status}] {filepath.relative_to(WORKSPACE)}")
        if result:
            contract_count += 1
    print(f"\nContracts modified: {contract_count}/{len(contracts)}")

    # ── Prompts ──
    print("\n" + "=" * 60)
    print("PROMPTS")
    print("=" * 60)
    prompts = find_prompts()
    prompt_count = 0
    for filepath, agent, intent, template in sorted(prompts):
        result = modify_prompt(filepath, template, dry_run)
        status = "MODIFIED" if result else "skip (already done)"
        print(f"  [{status}] {filepath.relative_to(WORKSPACE)}")
        if result:
            prompt_count += 1
    print(f"\nPrompts modified: {prompt_count}/{len(prompts)}")

    # ── Charters ──
    print("\n" + "=" * 60)
    print("CHARTERS")
    print("=" * 60)
    charters = find_charters()
    charter_count = 0
    for filepath, agent in sorted(charters):
        result = modify_charter(filepath, dry_run)
        status = "MODIFIED" if result else "skip (already done)"
        print(f"  [{status}] {filepath.relative_to(WORKSPACE)}")
        if result:
            charter_count += 1
    print(f"\nCharters modified: {charter_count}/{len(charters)}")

    # ── Summary ──
    total = contract_count + prompt_count + charter_count
    print(f"\n{'=' * 60}")
    print(f"TOTAL: {total} files modified")
    if dry_run:
        print("(DRY RUN - no files were actually changed)")


if __name__ == "__main__":
    main()
