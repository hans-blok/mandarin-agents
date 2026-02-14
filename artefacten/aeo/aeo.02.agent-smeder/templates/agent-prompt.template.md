---
agent: agent-smeder
intent: leg-vast-agent-prompt
versie: 1.0.0
# Template voor agent charters. Generiek bruikbaar voor alle agents. De vastlegging van het intent hier is een bron voor het goed vastleggen van het agent-contract.
---

---
# Prompt Metadata (placeholders invullen)
agent: mandarin.{agent-naam}
intent: {intent-kortschrift}
value_stream_fase: {value-stream-code}.{fase-nummer}

input_files:
  # Verplichte input bestanden voor deze intent (placeholders invullen)
  # Gebruik {vs}, {fase}, {agent}, {intent} voor dynamische paden
  # Of vul exacte paden in indien bekend
  {input_key_1}: "artefacten/{vs}/{vs}.{fase}.{agent}/{bestandsnaam}"
  {input_key_2}: "artefacten/{vs}/{vs}.{fase}.{agent}/{subfolder}/{bestandsnaam}"
  # Verwijder niet-gebruikte keys, voeg eigen keys toe waar nodig

bootstrap:
  script: scripts/bootstrap_canon_consult.py
  
# Canon URL en grondslagen worden gelezen uit beleid-workspace.md
# Agent-instructies staan in {agent-naam}.{intent-kortschrift}.agent.md
# Charter wordt automatisch geladen: {agent-naam}.charter.md (zelfde folder)
---

<!-- 
INVULINSTRUCTIES VOOR TEMPLATE-GEBRUIKERS
==========================================

Verplichte placeholders (vervang {...}):

1. mandarin.{agent-naam}
   - Namespace is altijd "mandarin" (ecosysteem-conventie)
   - Agent-naam: lowercase, kebab-case
   - Voorbeeld: "mandarin.agent-curator", "mandarin.engineer-steward"

2. {intent-kortschrift}
   - Kort, beschrijvend, kebab-case
   - Voorbeeld: "analyseer-ecosysteem", "schrijf-script", "formuleer-hypothese"
   - Moet overeenkomen met intent-naam in boundary en charter

3. {value-stream-code}.{fase-nummer}
   - Value stream code + fase nummer
   - Voorbeeld: "aeo.02", "sfw.01", "fnd.02"
   - Bepaalt welke grondslagen worden geladen uit beleid-workspace.md (base code)
   - Consistent met folder structuur en agent-ID conventie

4. input_files sectie
   - Lijst van verplichte input bestanden voor deze intent
   - Keys: beschrijvende namen (bijv. boundary_file, contract_file, template_file)
   - Values: paden met placeholders of exacte paden
   - Placeholders: {vs}, {fase}, {agent}, {intent} worden automatisch ingevuld
   - Voorbeeld:
     ```yaml
     input_files:
       boundary_file: "artefacten/{vs}/{vs}.{fase}.{agent}/agent-boundary-{agent}.md"
       template_file: "artefacten/aeo/aeo.02.agent-smeder/templates/agent-contract-intent.template.md"
     ```
   - Command-line overschrijven blijft mogelijk: -p boundary_file=/ander/pad

Naamgevingsconventie voor dit bestand:
  {agent-naam}.{intent-kortschrift}.prompt.md

Voorbeeld: agent-curator.analyseer-ecosysteem.prompt.md

ARCHITECTUUR-PRINCIPES
======================

✓ Single Source of Truth:
  - Canon URL: beleid-workspace.md (YAML frontmatter)
  - Grondslagen: beleid-workspace.md (per value_stream)
  - Agent-instructies: {agent-naam}.{intent-kortschrift}.agent.md
  - Input bestanden: prompt.md (input_files sectie, reproduceerbaar)

✓ Interface Segregation (SOLID):
  - Prompt bevat ALLEEN metadata voor run_prompt.py
  - Geen charter_ref, canon_url, grondslagen in prompt
  - Scheiding: metadata (prompt) vs instructies (agent.md)

✓ Convention over Configuration:
  - Bootstrap script altijd: scripts/bootstrap_canon_consult.py
  - Agent-instructies altijd: {agent-naam}.{intent-kortschrift}.agent.md
  - Beleid-workspace altijd: ./beleid-workspace.md (workspace root)

WORKFLOW
========

1. Agent-smeder vult placeholders in
2. Sla op als {agent-naam}.{intent-kortschrift}.prompt.md
3. Plaats in juiste folder: artefacten/{value-stream}/{value-stream}.{fase}.{agent-naam}/
4. Creëer bijbehorend .agent.md bestand met volledige agent-instructies
5. Test met: python scripts/run_prompt.py {pad-naar-prompt}.prompt.md

Voor details zie: docs/README-PROMPT-ARCHITECTURE.md

VERWIJDER DEZE INSTRUCTIES NA INVULLING
========================================
-->