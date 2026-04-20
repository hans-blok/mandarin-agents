---
# IDENTIFICATIE
template-id: "003"
template-naam: ecosysteem-overzicht

# RELATIES
artefact-type-id: "003"
agent-id: aeo.02.agent-curator

# META-DATA
versie: 1.0.0
status: vers
digest: d02d
---
# Template: Ecosysteem-overzicht

## Doel en gebruik

Dit template beschrijft de outputstructuur van het ecosysteem-overzicht dat de agent-curator produceert bij de intent `rapporteer-ecosysteem-overzicht`. Het overzicht geeft een tabellarisch inzicht in de toestand van alle agents en maakt het voor een human-in-the-loop mogelijk om in één oogopslag de status van het ecosysteem te beoordelen.

Gebruikt door intents:
- `rapporteer-ecosysteem-overzicht`

## Structuur

Dit template beschrijft de OUTPUT structuur. Het gegenereerde ecosysteem-overzicht krijgt de volgende structuur:

```markdown
---
agent: agent-curator
intent: rapporteer-ecosysteem-overzicht
value_stream_fase: <vs.fase>
versie: 1.0.0
datum: <YYYY-MM-DD>
canon_ref: <commit-hash>
---

# Ecosysteem-overzicht: <Value Stream Fase>

**Gegenereerd door**: agent-curator  
**Datum**: <YYYY-MM-DD>  
**Canon-referentie**: <commit-hash>  
**Scope**: <value-stream-fase of "compleet ecosysteem">

---

## Samenvatting

| Totaal agents | Compliant | Deels compliant | Non-compliant | Niet getoetst |
|---------------|-----------|-----------------|---------------|---------------|
| <n> | <n> | <n> | <n> | <n> |

---

## Agents per value stream fase

### <Value Stream Fase: bijv. aeo.02>

| Agent | Boundary | Charter | Contracten | Prompts | Tasks | Status | Opmerking |
|-------|----------|---------|------------|---------|-------|--------|-----------|
| <agent-naam> | ✓/✗ | ✓/✗/⚠ | ✓/✗/⚠ | ✓/✗/⚠ | ✓/✗/⚠ | <COMPLIANT/DEELS/NON/—> | <optionele toelichting> |

**Legenda**:  
✓ = aanwezig en compliant  ✗ = ontbreekt  ⚠ = aanwezig maar afwijking gesignaleerd  — = niet van toepassing of niet getoetst

---

## Gesignaleerde aandachtspunten

> Samenvatting van bevindingen die opvolging vergen. Gedetailleerde bevindingen staan in het validatierapport.

| Agent | Artefact | Bevinding | Prioriteit | Actie |
|-------|----------|-----------|------------|-------|
| <agent-naam> | <artefact> | <korte bevinding> | <HOOG/MIDDEL/LAAG> | <aanbevolen actie> |

---

## Ecosysteem-lacunes

> Capabilities of domeinen waarvoor geen agent bestaat of waarvoor de verantwoordelijkheid onduidelijk is.

| Lacune | Omschrijving | Aanbeveling |
|--------|--------------|-------------|
| <lacune-naam> | <beschrijving> | <aanbeveling> |

_(leeg indien geen lacunes geïdentificeerd)_

---

## Referenties naar validatierapporten

| Agent | Validatierapport |
|-------|-----------------|
| <agent-naam> | <pad naar validatierapport of "niet beschikbaar"> |

---

**Volgende aanbevolen actie**: <concrete actie voor human-in-the-loop>
```

## Placeholders

| Placeholder | Type | Beschrijving | Verplicht |
|-------------|------|--------------|-----------|
| `<vs.fase>` | string | Value stream fase code, bijv. `aeo.02` | Ja |
| `<YYYY-MM-DD>` | date | Datum van overzicht-generatie | Ja |
| `<commit-hash>` | string | Korte hash van de canon-versie | Ja |
| `<agent-naam>` | string | Naam van de agent (kebab-case) | Ja |
| `✓/✗/⚠` | symbool | Status per artefact-type (aanwezig+ok / ontbreekt / afwijking) | Ja |
| `<COMPLIANT/DEELS/NON/—>` | enum | Eindstatus per agent | Ja |
| Aandachtspunten-tabel | list | Kan leeg zijn als er geen bevindingen zijn | Nee |
| Lacunes-tabel | list | Kan leeg zijn als er geen lacunes zijn | Nee |
| Validatierapport-referenties | list | Paden naar gedetailleerde rapporten | Nee |
| `<concrete actie>` | string | Aanbeveling voor human-in-the-loop in één zin | Ja |

## Validatie-criteria

Een valide ecosysteem-overzicht volgens dit template:
- ✓ Bevat YAML frontmatter met agent, intent, value_stream_fase, versie, datum, canon_ref
- ✓ Bevat een samenvatting-tabel met tellingen per statuscategorie
- ✓ Bevat een agents-tabel per value stream fase met kolommen Boundary, Charter, Contracten, Prompts, Tasks, Status
- ✓ Elke agent heeft een eindstatus (COMPLIANT, DEELS-COMPLIANT, NON-COMPLIANT of —)
- ✓ Afwijkingen zijn geconcretiseerd in de aandachtspunten-tabel met prioritering
- ✓ Eindigt met een "Volgende aanbevolen actie" in één zin gericht aan de human-in-the-loop

## Voorbeeld-output

```markdown
---
agent: agent-curator
intent: rapporteer-ecosysteem-overzicht
value_stream_fase: aeo.02
versie: 1.0.0
datum: 2026-03-03
canon_ref: 9675a6d
---

# Ecosysteem-overzicht: aeo.02

**Gegenereerd door**: agent-curator  
**Datum**: 2026-03-03  
**Canon-referentie**: 9675a6d  
**Scope**: aeo.02

---

## Samenvatting

| Totaal agents | Compliant | Deels compliant | Non-compliant | Niet getoetst |
|---------------|-----------|-----------------|---------------|---------------|
| 4 | 2 | 1 | 0 | 1 |

---

## Agents per value stream fase

### aeo.02

| Agent | Boundary | Charter | Contracten | Prompts | Tasks | Status | Opmerking |
|-------|----------|---------|------------|---------|-------|--------|-----------|
| capability-architect | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLIANT | |
| agent-ontwerper | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLIANT | |
| agent-engineer | ✓ | ⚠ | ✓ | ✓ | ✓ | DEELS-COMPLIANT | Interventieniveau ontbreekt in charter |
| agent-curator | ✓ | ✗ | ✗ | ✗ | ✗ | — | Nieuw — charter nog niet gerealiseerd |

**Legenda**:  
✓ = aanwezig en compliant  ✗ = ontbreekt  ⚠ = aanwezig maar afwijking gesignaleerd  — = niet van toepassing of niet getoetst

---

## Gesignaleerde aandachtspunten

| Agent | Artefact | Bevinding | Prioriteit | Actie |
|-------|----------|-----------|------------|-------|
| agent-engineer | agent-engineer.charter.md | Interventieniveau-as ontbreekt in classificatie-sectie | MIDDEL | Voeg Interventieniveau-as toe (verwachte waarde: Werk) |

---

## Ecosysteem-lacunes

| Lacune | Omschrijving | Aanbeveling |
|--------|--------------|-------------|
| agent-curator niet gerealiseerd | Charter, contracten en prompts zijn nog niet aangemaakt | Voer agent-ontwerper intent definieer-agent-charter uit voor agent-curator |

---

## Referenties naar validatierapporten

| Agent | Validatierapport |
|-------|-----------------|
| agent-engineer | niet beschikbaar |

---

**Volgende aanbevolen actie**: Realiseer het charter en de contracten voor agent-curator (via agent-ontwerper) en herstel de Interventieniveau-as in het charter van agent-engineer.
```

## Gebruiksinstructies

Voor de agent-curator bij het genereren van een ecosysteem-overzicht:
1. Bepaal de scope: alle agents in één value stream fase, of het volledige ecosysteem.
2. Inventariseer per agent welke artefact-typen aanwezig zijn (boundary, charter, contracten, prompts, tasks) via de artefacten-mapstructuur.
3. Toets elk aanwezig artefact op basisvolledigheid (frontmatter aanwezig, vereiste secties aanwezig) en markeer afwijkingen met ⚠.
4. Bepaal het eindstatus-oordeel per agent op basis van gevonden afwijkingen en vul de samenvatting-tabel.
5. Sluit af met één aanbevolen actie voor de human-in-the-loop in begrijpelijke, niet-technische taal.

## Versiebeheer

| Versie | Datum | Wijziging |
|--------|-------|-----------|
| 1.0.0 | 2026-03-03 | Initiële template voor agent-curator |

---

**Template-categorie**: Agent-specifiek  
**Gebruikt door intents**: rapporteer-ecosysteem-overzicht
