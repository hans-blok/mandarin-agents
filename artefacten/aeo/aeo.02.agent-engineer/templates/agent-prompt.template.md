---
agent: agent-engineer
intent: realiseer-agent-prompts
versie: 1.0.0
# Template voor minimalistische agent prompts (uitsluitend YAML)
digest: 90f9
status: vers
---
---
# Prompt Metadata (placeholders invullen)
agent: mandarin.{agent-naam}
intent: {intent-kortschrift}
bronhouding: {bronhouding}
versie: 1.0.0
input_parameters:
  - {parameter-naam}
  - {parameter-naam}
value_stream_fase: {value-stream-code}.{fase-nummer}


# Canon URL en grondslagen worden gelezen uit beleid-workspace.md
# Agent-instructies staan in {agent-naam}.{intent-kortschrift}.agent.md
# Charter wordt automatisch geladen: {agent-naam}.charter.md (zelfde folder)
---

1. mandarin.{agent-naam}
   - Namespace is altijd "mandarin" (ecosysteem-conventie)
   - Agent-naam: lowercase, kebab-case
   - Voorbeeld: "mandarin.agent-curator", "mandarin.engineer-steward"

2. {intent-kortschrift}
   - Kort, beschrijvend, kebab-case
   - Voorbeeld: "analyseer-ecosysteem", "schrijf-script", "formuleer-hypothese"
   - Moet overeenkomen met intent-naam in boundary en charter

3. {bronhouding}
   - Epistemische positie van de agent: de kennisbron op basis waarvan gehandeld wordt
   - Geldige waarden: "Input-gebonden", "Canon-gebonden", "Workspace-gebonden", "Externe-bron gebonden", "Exploratief"
   - Moet consistent zijn met de bronhouding gedeclareerd in het charter (classificatie-as)
   - Voorbeeld: "Exploratief" (gebruikt generatieve capaciteiten, aannames expliciet)

4. {value-stream-code}.{fase-nummer}
   - Value stream code + fase nummer
   - Voorbeeld: "aeo.02", "sfw.01", "fnd.02"
   - Bepaalt welke grondslagen worden geladen uit beleid-workspace.md (base code)
   - Consistent met folder structuur en agent-ID conventie

Naamgevingsconventie voor dit bestand:
  mandarin.{agent-naam}.{intent-kortschrift}.prompt.md

Voorbeeld: mandarin.agent-curator.analyseer-ecosysteem.prompt.md

ARCHITECTUUR: CONVENTION OVER CONFIGURATION (2024+)
====================================================

Minimalistische prompts bevatten ALLEEN metadata:

✓ Wat staat in de prompt:
  - agent: Volledige agent-naam met namespace
  - intent: Intent-kortschrift
  - bronhouding: Epistemische positie (stuurt LLM-gedrag via runner)
  - versie: Promptversie
  - input_parameters: Alleen expliciete runtime-input van de gebruiker
  - value_stream_fase: Value stream en fase
  - bootstrap: Bootstrap script (altijd scripts/bootstrap_canon_consult.py)
  - Comments: Verwijzingen naar waar andere informatie staat

✗ Wat NIET in de prompt staat:
  - boundary_file parameter: Wordt niet gebruikt
  - Agent-instructies: Staan in {agent-naam}.{intent-kortschrift}.agent.md
  - Charter: Wordt automatisch geladen uit {agent-naam}.charter.md
  - Agent-contract pad: Wordt automatisch afgeleid uit workspace-conventie
  - Canon URL: Wordt gelezen uit beleid-workspace.md
  - Grondslagen: Worden gelezen uit beleid-workspace.md per value_stream

Conventies (geen configuratie nodig):
  - Agent-instructies: {agent-naam}.{intent-kortschrift}.agent.md (zelfde folder als charter)
  - Charter: {agent-naam}.charter.md (parent folder van agent-contract)
  - Agent-contracten: automatisch ontdekken op basis van artefacten/{vs}/{vs}.{fase}.{agent}/
    * inclusief patronen zoals {agent}.agent-contract*.md
    * exclusief *.agent-boundary.md
  - Beleid: ./beleid-workspace.md (workspace root)
  - Bootstrap: scripts/bootstrap_canon_consult.py (altijd)
  - Input parameters: Worden via command-line parameters opgegeven (-p naam=waarde)

Voorbeelden command-line overschrijven:
  python scripts/run_prompt.py prompt.md -p agent=agent-curator
  python scripts/run_prompt.py prompt.md -p opdracht=valideer-concept

ARCHITECTUUR-PRINCIPES (SOLID)
================================

✓ Single Source of Truth:
  - Canon & grondslagen → beleid-workspace.md
  - Agent-instructies → {agent}.{intent}.agent.md
  - Charter → {agent}.charter.md (declareert bronhouding voor mensen)
  - Bronhouding (operationeel) → prompt frontmatter (stuurt runner en LLM)
  - Agent-contracten → workspace-conventie (auto-discovery)
  - Input parameters → command-line parameters

✓ Interface Segregation:
  - Prompt = ALLEEN metadata voor run_prompt.py
  - Instructies = ALLEEN werkwijze en contract
  - Charter = ALLEEN identiteit en governance
  - Geen overlap, geen duplicatie

✓ Convention over Configuration:
  - Standaard locaties en bestandsnamen
  - Expliciete configuratie alleen waar nodig
  - Vermindert onderhoudslast en inconsistenties

WORKFLOW
========

1. Agent-smeder vult placeholders in (agent, intent, value_stream_fase)
2. Sla op als mandarin.{agent-naam}.{intent-kortschrift}.prompt.md
3. Plaats in: artefacten/{value-stream}/{value-stream}.{fase}.{agent-naam}/prompts/
4. Agent-instructies staan al in {agent}.{intent}.agent.md (via leg-vast-agent-contract)
5. Test met: python scripts/run_prompt.py {pad-naar-prompt}.prompt.md -p param=waarde

VERWIJDER DEZE INSTRUCTIES NA INVULLING
========================================
-->