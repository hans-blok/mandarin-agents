---
agent: agent-curator
intent: valideer-agent-consistentie
scope: agent-ontwerper
value_stream_fase: aeo.02
versie: 1.0.0
datum: 2026-03-23
canon_ref: ceb3327
execution_id: e491
---

# Validatierapport: agent-ontwerper

**Scope**: agent-ontwerper  
**Toetssteen**: canon-ref ceb3327 — constitutie, doctrines, ordeningsconcepten  
**Status**: **NON-COMPLIANT**

---

## Samenvatting

De agent-ontwerper (aeo.02) is getoetst op canonieke consistentie van alle artefacten: charter, 3 contracten, 3 prompts, 1 tasks-configuratie en 1 runner. De agent beschikt over alle verwachte artefact-typen en een werkende runner-pipeline. Echter, het charter bevat twee kritieke afwijkingen: ontbrekende YAML frontmatter en een onjuiste bestandsnaam-verwijzing in herkomstverantwoording. Daarnaast zijn er 8 waarschuwingen waaronder verwijzingen naar de niet-bestaande `aeo.02.agent-smeder`, een typo in een contract, inconsistente metadata-terminologie en een ontbrekend kaderdefinities-veld. Opvolging is vereist om NON-COMPLIANT-status op te heffen.

| Zwaarte | Aantal |
|---------|--------|
| Kritiek | 2 |
| Waarschuwing | 8 |
| Informatief | 2 |

---

## Toetsresultaten per agent

### agent-ontwerper

**Artefacten getoetst**:
- [x] Charter aanwezig en volledig (11 secties)
- [x] Contract(en) aanwezig per intent (3 van 3)
- [x] Classificatie-assen consistent met boundary
- [ ] Traceerbaarheid boundary → charter → contract aantoonbaar
- [ ] Doctrine-naleving: template-conformiteit voldaan

**Bevindingen**:

| ID | Zwaarte | Artefact | Bevinding | Aanbeveling |
|----|---------|----------|-----------|-------------|
| agent-ontwerper-001 | KRITIEK | `agent-ontwerper.charter.md` | YAML frontmatter ontbreekt. Charter begint direct met `# Agent Charter - agent-ontwerper` zonder `---` delimiters. Het eigen contract `definieer-agent-charter` specificeert YAML frontmatter (agent, versie, domein, value_stream, governance) als verplicht output-element. | Voeg YAML frontmatter toe conform de output-specificatie in `agent-ontwerper.definieer-agent-charter.agent.md` en het template `agent-charter.template.md` v1.1.0. |
| agent-ontwerper-002 | KRITIEK | `agent-ontwerper.charter.md` §10 | Herkomstverantwoording verwijst naar `agent-boundary-agent-ontwerper.md`, maar het feitelijke boundary-bestand heet `agent-ontwerper.agent-boundary.md`. Traceerbaarheid naar boundary is hierdoor verbroken. | Corrigeer de verwijzing naar `artefacten/aeo/aeo.02.agent-ontwerper/agent-ontwerper.agent-boundary.md`. |
| agent-ontwerper-003 | WAARSCHUWING | `agent-ontwerper.charter.md` §7, §10 | Template-paden verwijzen naar `artefacten/aeo/aeo.02.agent-smeder/templates/agent-charter.template.md` en `agent-contract-intent.template.md`. De map `aeo.02.agent-smeder` bestaat niet in deze workspace. De templates staan feitelijk in `artefacten/aeo/aeo.02.agent-ontwerper/templates/`. | Corrigeer alle template-padverwijzingen in §7 (Traceerbaarheid) en §10 (Herkomstverantwoording) naar `artefacten/aeo/aeo.02.agent-ontwerper/templates/`. |
| agent-ontwerper-004 | WAARSCHUWING | `agent-ontwerper.charter.md` classificatie | Classificatie-sectie header luidt "Classificatie-assen (vink aan wat van toepassing is)" i.p.v. "Mandarin-agent-classificatie (4 orthogonale assen)" conform de huidige template-conventie (agent-charter.template.md v1.1.0). | Hernorm header naar "Mandarin-agent-classificatie (4 orthogonale assen)". |
| agent-ontwerper-005 | WAARSCHUWING | `agent-ontwerper.charter.md` classificatie | Het "Classificatie-validatie (verplicht)" blok ontbreekt. Dit blok is aanwezig in nieuwere charters (bijv. agent-curator) en borgt dat gekozen as-posities onderling compatibel zijn en definities uit `mandarin-ordeningsconcepten.md` worden gevolgd. | Voeg classificatie-validatieblok toe met twee verplichte checkboxes: (1) as-posities compatibel, (2) positionering volgt definities uit ordeningsconcepten. |
| agent-ontwerper-006 | WAARSCHUWING | `agent-ontwerper.charter.md` | Charter mist het veld "Kaderdefinities" dat in template `agent-charter.template.md` v1.1.0 is opgenomen als `**Kaderdefinities**: {kaderdefinities}`. De agent-ontwerper's eigen contract vermeldt kaderdefinities als afgeleide informatie. | Voeg `**Kaderdefinities**: geen` toe aan charter header (of relevante canonieke paden indien van toepassing). |
| agent-ontwerper-007 | WAARSCHUWING | `agent-ontwerper.definieer-agent-template.agent.md` | Typo in parameternaam: `file_naam_inspiriratie` (dubbele 'ri'). Moet `file_naam_inspiratie` zijn. Prompt-bestand gebruikt wel de correcte spelling (`file_naam_inspiratie`). | Corrigeer typo naar `file_naam_inspiratie` in het contract. |
| agent-ontwerper-008 | WAARSCHUWING | Alle 3 contracten (Metadata-sectie) | Metadata-secties gebruiken "Interventieniveau: Werk" als classificatie-as. Dit is geen onderdeel van het huidige 4-assen model (Vormingsfase, Betekeniseffect, Werking, Bronhouding). De term "Interventieniveau" komt niet voor in de boundary of het charter. | Vervang "Interventieniveau: Werk" door de juiste as-positie, of verwijder de regel als "Vormingsfase: Vastlegging" al in de boundary staat. |
| agent-ontwerper-009 | WAARSCHUWING | `mandarin.agent-ontwerper.definieer-agent-template.prompt.md` | YAML frontmatter bronhouding is `canon-gebonden` (lowercase), terwijl de andere twee prompts `Canon-gebonden` (met hoofdletter) gebruiken. | Uniformeer naar `Canon-gebonden` in alle prompt-bestanden. |
| agent-ontwerper-010 | WAARSCHUWING | Runner vs contracten | Runner `agent-ontwerper.runner.py` accepteert `--boundary-file` als optionele parameter voor de intents `definieer-agent-charter` en `definieer-agent-contract`. Dit is niet gedocumenteerd als optionele parameter in de betreffende contracten. | Voeg `boundary_file` toe als optionele parameter in beide contracten, of verwijder de parameter uit de runner als deze altijd wordt afgeleid. |
| agent-ontwerper-011 | INFORMATIEF | `agent-ontwerper.charter.md` §5 | NIET-lijst vermeldt "Maakt geen prompts of prompt-metadata aan" terwijl de templates-folder een `agent-prompt.template.md` bevat. De relatie tussen "template voor prompts definiëren" (wat ontwerper doet) en "prompts aanmaken" (wat engineer doet) is onduidelijk. | Overweeg verduidelijking in charter §5: de agent-ontwerper definieert de template-structuur voor prompts, maar maakt geen concrete prompt-bestanden aan. |
| agent-ontwerper-012 | INFORMATIEF | Mapstructuur | Lege `runners/` map bestaat naast de gebruikte `runner/` map. Dit creëert verwarring over de correcte locatie. | Verwijder de lege `runners/` map om dubbelzinnigheid te voorkomen. |

**Eindoordeel**: **NON-COMPLIANT**

---

## Escalaties

| Escalatie naar | Onderwerp | Reden |
|----------------|-----------|-------|
| agent-ontwerper | Charter YAML frontmatter + boundary-verwijzing (agent-ontwerper-001, -002) | Kritieke afwijkingen in charter die traceerbaarheid en parsability verbreken. Correctie vereist door agent-ontwerper of direct handmatig. |
| agent-ontwerper | Template-padverwijzingen agent-smeder → agent-ontwerper (agent-ontwerper-003) | Verwijzingen naar niet-bestaande agent-smeder moeten gecorrigeerd worden naar feitelijke templatelocatie. |
| agent-ontwerper | Contracten metadata + typo (agent-ontwerper-007, -008) | Inconsistente terminologie en typo vereisen correctie in contracten. |
| agent-engineer | Runner parameter --boundary-file niet in contract (agent-ontwerper-010) | Runner-contract synchronisatie vereist afstemming. |

---

## Getoetste artefacten (volledig pad)

### Charter
- `artefacten/aeo/aeo.02.agent-ontwerper/agent-ontwerper.charter.md` — 11 secties aanwezig, YAML frontmatter ontbreekt

### Boundary
- `artefacten/aeo/aeo.02.agent-ontwerper/agent-ontwerper.agent-boundary.md` — Volledig, classificatie-assen consistent met charter

### Contracten
- `artefacten/aeo/aeo.02.agent-ontwerper/agent-contracten/agent-ontwerper.definieer-agent-charter.agent.md` — Compleet (frontmatter, rolbeschrijving, contract, werkwijze, governance, metadata)
- `artefacten/aeo/aeo.02.agent-ontwerper/agent-contracten/agent-ontwerper.definieer-agent-contract.agent.md` — Compleet
- `artefacten/aeo/aeo.02.agent-ontwerper/agent-contracten/agent-ontwerper.definieer-agent-template.agent.md` — Compleet (typo in parameternaam)

### Prompts
- `artefacten/aeo/aeo.02.agent-ontwerper/prompts/mandarin.agent-ontwerper.definieer-agent-charter.prompt.md` — YAML-only, conform generatiemodel
- `artefacten/aeo/aeo.02.agent-ontwerper/prompts/mandarin.agent-ontwerper.definieer-agent-contract.prompt.md` — YAML-only, conform generatiemodel
- `artefacten/aeo/aeo.02.agent-ontwerper/prompts/mandarin.agent-ontwerper.definieer-agent-template.prompt.md` — YAML-only, casing-inconsistentie

### Tasks
- `artefacten/aeo/aeo.02.agent-ontwerper/tasks/aeo-02.agent-ontwerper.tasks.json` — Valide JSON, 3 taken, 11 inputs, alle intents gedekt

### Runner
- `artefacten/aeo/aeo.02.agent-ontwerper/runner/agent-ontwerper.runner.py` — Werkend, 3 intents via subparsers, delegeert naar ecosysteem-coordinator

### Templates
- `artefacten/aeo/aeo.02.agent-ontwerper/templates/agent-charter.template.md` — v1.1.0
- `artefacten/aeo/aeo.02.agent-ontwerper/templates/agent-contract-intent.template.md` — aanwezig
- `artefacten/aeo/aeo.02.agent-ontwerper/templates/agent-prompt.template.md` — aanwezig
- `artefacten/aeo/aeo.02.agent-ontwerper/templates/agent-runner.skeleton.py` — aanwezig

### Classificatie-assen consistentie (boundary ↔ charter)

| As | Boundary | Charter | Status |
|----|----------|---------|--------|
| Vormingsfase | Vastlegging | Vastlegging | ✓ Consistent |
| Betekeniseffect | Normerend | Normerend | ✓ Consistent |
| Werking | Inhoudelijk | Inhoudelijk | ✓ Consistent |
| Bronhouding | Canon-gebonden | Canon-gebonden | ✓ Consistent |
