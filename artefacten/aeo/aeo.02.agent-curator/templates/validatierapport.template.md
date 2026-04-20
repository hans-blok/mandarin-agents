---
# IDENTIFICATIE
template-id: "004"
template-naam: validatierapport

# RELATIES
artefact-type-id: "004"
agent-id: aeo.02.agent-curator

# META-DATA
versie: 1.0.0
status: vers
digest: 1684
---
# Template: Validatierapport

## Doel en gebruik

Dit template beschrijft de outputstructuur van het validatierapport dat de agent-curator produceert bij de intents `valideer-agent-consistentie` en `valideer-boundary-overlap`. Het rapport legt per agent vast of de artefacten (charter, contracten, prompts, tasks) consistent zijn met de canon, en signaleert afwijkingen ter escalatie aan human-in-the-loop.

Gebruikt door intents:
- `valideer-agent-consistentie`
- `valideer-boundary-overlap`

## Structuur

Dit template beschrijft de OUTPUT structuur. Het gegenereerde validatierapport krijgt de volgende structuur:

```markdown
---
agent: agent-curator
intent: <valideer-agent-consistentie|valideer-boundary-overlap>
scope: <agent-naam of value-stream-fase>
value_stream_fase: <vs.fase>
versie: 1.0.0
datum: <YYYY-MM-DD>
canon_ref: <commit-hash>
---

# Validatierapport: <Scope>

**Scope**: <agent-naam of "alle agents in aeo.02">  
**Toetssteen**: canon-ref <commit-hash> — constitutie, doctrines, ordeningsconcepten  
**Status**: <COMPLIANT | NON-COMPLIANT | DEELS-COMPLIANT>

---

## Samenvatting

<Één alinea: wat is getoetst, wat was de uitkomst, wat vereist opvolging.>

| Zwaarte | Aantal |
|---------|--------|
| Kritiek | <n> |
| Waarschuwing | <n> |
| Informatief | <n> |

---

## Toetsresultaten per agent

### <Agent-naam>

**Artefacten getoetst**:
- [ ] Charter aanwezig en volledig (11 secties)
- [ ] Contract(en) aanwezig per intent
- [ ] Classificatie-assen consistent met boundary
- [ ] Traceerbaarheid boundary → charter → contract aantoonbaar
- [ ] Templatebinding aanwezig in contract per intent
- [ ] Templateveld aanwezig in prompt-frontmatter per intent
- [ ] Contract- en prompt-template zijn identiek per intent
- [ ] Verwezen templatebestand bestaat of `template: ~` is expliciet vastgelegd
- [ ] Doctrine-naleving: <doctrine-naam> voldaan

**Bevindingen**:

| ID | Zwaarte | Artefact | Bevinding | Aanbeveling |
|----|---------|----------|-----------|-------------|
| <scope>-001 | <KRITIEK/WAARSCHUWING/INFORMATIEF> | <bestandspad> | <wat is gevonden> | <wat moet gebeuren> |

**Eindoordeel**: <COMPLIANT | NON-COMPLIANT | DEELS-COMPLIANT>

---

## Boundary-overlap analyse (indien van toepassing)

> Alleen ingevuld bij intent `valideer-boundary-overlap`.

| Agent A | Agent B | Overlappend aspect | Zwaarte | Aanbeveling |
|---------|---------|--------------------|---------|-------------|
| <agent-a> | <agent-b> | <wat overlapt> | <KRITIEK/WAARSCHUWING> | <actie voor curator of escalatie> |

---

## Template-conformiteit

> Alleen gevuld wanneer templategebruik is meegetoetst binnen de scope van het rapport.

| Intent | Contract-template | Prompt-template | Bestaat bestand | Status | Opmerking |
|--------|-------------------|-----------------|-----------------|--------|-----------|
| <intent-naam> | <template-pad of ~> | <template-pad of ~> | <ja/nee/n.v.t.> | <COMPLIANT/NON-COMPLIANT/DEELS-COMPLIANT> | <toelichting> |

---

## Lacunes in het ecosysteem

> Capabilities of verantwoordelijkheden waarvoor geen agent bestaat of waarvoor de boundary onduidelijk is.

- <Lacune 1: beschrijving>
- <Lacune 2: beschrijving>

---

## Escalaties

> Bevindingen die niet door agent-curator opgelost kunnen worden en doorgestuurd moeten worden.

| Escalatie naar | Onderwerp | Reden |
|----------------|-----------|-------|
| <agent-smeder | constitutioneel-auteur | capability-architect> | <onderwerp> | <waarom escalatie nodig is> |

---

## Gebruikte bronnen

- Canon-referentie: <commit-hash>
- Getoetste artefacten: <lijst van bestanden>
- Doctrine-versies: <doctrine-naam v.x.y.z>

---

**Gegenereerd door**: agent-curator  
**Datum**: <YYYY-MM-DD>  
**Canon-referentie**: <commit-hash>
```

## Placeholders

| Placeholder | Type | Beschrijving | Verplicht |
|-------------|------|--------------|-----------|
| `<scope>` | string | Agent-naam of value-stream-fase die getoetst is | Ja |
| `<vs.fase>` | string | Value stream fase code, bijv. `aeo.02` | Ja |
| `<commit-hash>` | string | Korte hash van de canon-versie waarop getoetst is | Ja |
| `<YYYY-MM-DD>` | date | Datum van rapport-generatie | Ja |
| `<agent-naam>` | string | Naam van de getoetste agent (kebab-case) | Ja |
| `<bestandspad>` | string | Relatief pad naar het getoetste artefact | Ja |
| `<wat is gevonden>` | string | Concrete bevinding in één zin | Ja |
| `<actie voor curator of escalatie>` | string | Concrete aanbeveling voor opvolging | Ja |
| Overlap-tabel | list | Alleen bij `valideer-boundary-overlap`; één rij per overlap-paar | Conditioneel |
| Lacunes-lijst | list | Kan leeg zijn als er geen lacunes zijn | Nee |
| Escalaties-tabel | list | Kan leeg zijn als alle bevindingen intern oplosbaar zijn | Nee |

## Validatie-criteria

Een valide validatierapport volgens dit template:
- ✓ Bevat YAML frontmatter met agent, intent, scope, value_stream_fase, versie, datum, canon_ref
- ✓ Heeft een samenvatting-tabel met aantallen per zwaartecategorie (KRITIEK/WAARSCHUWING/INFORMATIEF)
- ✓ Bevat toetsresultaten voor elke getoetste agent met minimaal de verplichte checkboxes
- ✓ Elke bevinding heeft een uniek ID, zwaarte, artefact-pad en aanbeveling
- ✓ Eindoordeel per agent is één van: COMPLIANT, NON-COMPLIANT, DEELS-COMPLIANT
- ✓ Kan templateconformiteit per intent expliciet weergeven in een aparte sectie of via bevindingen
- ✓ Escalaties zijn traceerbaar naar een ontvanger
- ✓ Gebruikte bronnen (canon-ref en artefactlijst) zijn gedocumenteerd

## Voorbeeld-output

```markdown
---
agent: agent-curator
intent: valideer-agent-consistentie
scope: agent-engineer
value_stream_fase: aeo.02
versie: 1.0.0
datum: 2026-03-03
canon_ref: 9675a6d
---

# Validatierapport: agent-engineer

**Scope**: agent-engineer  
**Toetssteen**: canon-ref 9675a6d — constitutie, doctrine-agent-charter-normering.md v2.1.0  
**Status**: DEELS-COMPLIANT

---

## Samenvatting

De agent-engineer is getoetst op canonieke consistentie binnen aeo.02. Charter en contracten zijn aanwezig. Er is één waarschuwing: de classificatie-as Interventieniveau ontbreekt in het charter. Geen kritieke bevindingen; geen escalaties noodzakelijk.

| Zwaarte | Aantal |
|---------|--------|
| Kritiek | 0 |
| Waarschuwing | 1 |
| Informatief | 1 |

---

## Toetsresultaten per agent

### agent-engineer

**Artefacten getoetst**:
- [x] Charter aanwezig en volledig (11 secties)
- [x] Contract(en) aanwezig per intent
- [ ] Classificatie-assen consistent met boundary
- [x] Traceerbaarheid boundary → charter → contract aantoonbaar
- [x] Templatebinding aanwezig in contract per intent
- [x] Templateveld aanwezig in prompt-frontmatter per intent
- [x] Contract- en prompt-template zijn identiek per intent
- [x] Verwezen templatebestand bestaat of `template: ~` is expliciet vastgelegd
- [x] Doctrine-naleving: doctrine-agent-charter-normering.md v2.1.0 voldaan

**Bevindingen**:

| ID | Zwaarte | Artefact | Bevinding | Aanbeveling |
|----|---------|----------|-----------|-------------|
| agent-engineer-001 | WAARSCHUWING | artefacten/aeo/aeo.02.agent-engineer/agent-engineer.charter.md | Interventieniveau-as ontbreekt in classificatie-sectie | Voeg Interventieniveau-as toe; verwachte waarde: Werk |
| agent-engineer-002 | INFORMATIEF | artefacten/aeo/aeo.02.agent-engineer/agent-engineer.charter.md | Change log bevat geen entry voor meest recente update | Voeg change log entry toe bij volgende revisie |

**Eindoordeel**: DEELS-COMPLIANT

---

## Template-conformiteit

| Intent | Contract-template | Prompt-template | Bestaat bestand | Status | Opmerking |
|--------|-------------------|-----------------|-----------------|--------|-----------|
| realiseer-agent-prompts | templates/agent-prompt.template.md | templates/agent-prompt.template.md | ja | COMPLIANT | Prompt spiegelt contractuele templatekeuze |

---

## Escalaties

Geen escalaties noodzakelijk.

---

## Gebruikte bronnen

- Canon-referentie: 9675a6d
- Getoetste artefacten: artefacten/aeo/aeo.02.agent-engineer/agent-engineer.charter.md, artefacten/aeo/aeo.02.agent-engineer/agent-contracten/
- Doctrine-versies: doctrine-agent-charter-normering.md v2.1.0

---

**Gegenereerd door**: agent-curator  
**Datum**: 2026-03-03  
**Canon-referentie**: 9675a6d
```

## Gebruiksinstructies

Voor de agent-curator bij het genereren van een validatierapport:
1. Stel de scope vast (één agent of alle agents in een value stream fase) op basis van de input-parameter.
2. Bepaal de canon-referentie (commit-hash) die als toetssteen dient.
3. Doorloop per agent de verplichte checkboxes in volgorde; markeer met `[x]` indien voldaan.
4. Registreer elke bevinding in de tabel met uniek ID (formaat: `<agent-naam>-<volgnummer>`), zwaarte, artefact-pad en concrete aanbeveling.
5. Bepaal het eindoordeel per agent op basis van zwaarte: KRITIEK → NON-COMPLIANT, alleen WAARSCHUWING → DEELS-COMPLIANT, alles voldaan → COMPLIANT.

## Versiebeheer

| Versie | Datum | Wijziging |
|--------|-------|-----------|
| 1.0.0 | 2026-03-03 | Initiële template voor agent-curator |

---

**Template-categorie**: Agent-specifiek  
**Gebruikt door intents**: valideer-agent-consistentie, valideer-boundary-overlap
