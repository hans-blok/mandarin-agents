# Ordeningsverslag — mandarin-architect (AOD.01)

**Agent**: mandarin-architect  
**Uitgevoerde ordening door**: agent-smeder (intent 4.orden-agent)  
**Datum**: 2026-02-04

---

## 1. Opdracht en gekozen positionering

- Opdracht: orden mandarin-architect als AOD.01-agent.
- Gekozen value stream: Architectuur- en Oplossingsontwerp (AOD).
- Gekozen fase: 01 — Vraagverkenning.
- Reden: mandarin-architect werkt adviserend, richt zich op canon, begrippen en domeinmodellen vóór concrete implementatie. Dit past bij architectuurvraagverkenning binnen AOD.01.

## 2. Gevonden bestaande artefacten

Bronlocaties onder artefacten/agent-enablement/:

- Charter:
  - artefacten/agent-enablement/charters-agents/mandarin-architect.charter.md
- Agent-contracten:
  - artefacten/agent-enablement/agents/mandarin-architect.schrijf-concept.agent.md
  - artefacten/agent-enablement/agents/mandarin-architect.werk-cdm-uit-conform-archimate.agent.md
- Prompts:
  - artefacten/agent-enablement/prompts/mandarin.mandarin-architect.schrijf-concept.prompt.md
  - artefacten/agent-enablement/prompts/mandarin.mandarin-architect.werk-cdm-uit-conform-archimate.prompt.md
- Boundary:
  - agent-boundaries/mandarin-architect.boundary.md

Assumpties:
- Er zijn geen andere mandarin-architect artefacten buiten bovenstaande paden die als canoniek moeten gelden.

## 3. Doelstructuur (canoniek)

Nieuwe per-agentfolder:

- artefacten/aod.01.mandarin-architect/
  - mandarin-architect.charter.md
  - mandarin-architect.schrijf-concept.agent.md
  - mandarin-architect.werk-cdm-uit-conform-archimate.agent.md
  - mandarin.mandarin-architect.schrijf-concept.prompt.md
  - mandarin.mandarin-architect.werk-cdm-uit-conform-archimate.prompt.md

Normatieve keuzes:
- Value stream: AOD (Architectuur- en Oplossingsontwerp).
- Fase: 01 Vraagverkenning → foldernaam aod.01.mandarin-architect.
- Alle agent-specifieke artefacten horen in dezelfde per-agentfolder te staan.

## 4. Uitgevoerde verplaatsingen en aanpassingen

### 4.1 Bestandsverplaatsingen

Van → Naar:

- artefacten/agent-enablement/charters-agents/mandarin-architect.charter.md  
  → artefacten/aod.01.mandarin-architect/mandarin-architect.charter.md

- artefacten/agent-enablement/agents/mandarin-architect.schrijf-concept.agent.md  
  → artefacten/aod.01.mandarin-architect/mandarin-architect.schrijf-concept.agent.md

- artefacten/agent-enablement/agents/mandarin-architect.werk-cdm-uit-conform-archimate.agent.md  
  → artefacten/aod.01.mandarin-architect/mandarin-architect.werk-cdm-uit-conform-archimate.agent.md

- artefacten/agent-enablement/prompts/mandarin.mandarin-architect.schrijf-concept.prompt.md  
  → artefacten/aod.01.mandarin-architect/mandarin.mandarin-architect.schrijf-concept.prompt.md

- artefacten/agent-enablement/prompts/mandarin.mandarin-architect.werk-cdm-uit-conform-archimate.prompt.md  
  → artefacten/aod.01.mandarin-architect/mandarin.mandarin-architect.werk-cdm-uit-conform-archimate.prompt.md

Oude bronbestanden zijn verwijderd na succesvolle kopie.

### 4.2 Charter-aanpassingen

In mandarin-architect.charter.md:

- Value Stream aangepast van "agent-enablement" naar:
  - "Architectuur- en Oplossingsontwerp (AOD, fase 01 - Vraagverkenning)".
- Traceerbaarheid bijgewerkt naar nieuwe paden onder artefacten/aod.01.mandarin-architect/.
- Output-locaties bijgewerkt van exports/agent-enablement/... naar artefacten/aod.01.mandarin-architect/.
- Semantiek (doel, capability boundary, kerntaken, grenzen) is ongewijzigd gelaten.

### 4.3 Contract- en prompt-aanpassingen

- Voor alle prompts is charter_ref aangepast van @main:exports/agent-enablement/charters-agents/mandarin-architect.charter.md naar:
  - @main:artefacten/aod.01.mandarin-architect/mandarin-architect.charter.md
- Voor het agent-contract mandarin-architect.werk-cdm-uit-conform-archimate.agent.md is charter_ref identiek aangepast.
- Het contract mandarin-architect.schrijf-concept.agent.md is inhoudelijk ongemoeid gelaten; er is geen semantiek gewijzigd.

### 4.4 Boundary-aanpassing

In agent-boundaries/mandarin-architect.boundary.md:

- "Opereert in Value stream fasen" aangepast van "architectuur-agent-enablement" naar "AOD.01 - Vraagverkenning".
- Overige boundary-tekst (capability-boundary, doelen, WEL/NIET) is ongewijzigd gelaten.

## 5. Aannames en openstaande punten

Aannames:
- De mandarin-architect is een adviserend AOD-agent in fase 01 (Vraagverkenning) en hoeft niet aan latere AOD-fasen gekoppeld te worden.
- Publicatie- en exportmechanismen werken vanuit de per-agentfolders onder artefacten/<code>.<fase>.<agent-naam>/ en niet meer vanuit exports/agent-enablement/.

Openstaande vragen (voor governance, niet geblokkeerd voor ordening):
- Of mandarin-architect in de toekomst ook AOD.02/03 moet ondersteunen, en zo ja, of dat via nieuwe intents of een aparte agent moet gebeuren.

---

**Status**: ordening uitgevoerd en consistent met de huidige value stream canon (AOD.01 Vraagverkenning).