---
# IDENTIFICATIE
template-id: "021"
template-naam: barker-validatierapport

# RELATIES
artefact-type-id: "021"
agent-id: sfw.03.logisch-modelleur

# META-DATA
versie: 1.0.0
status: vers
digest: 9b0d
---

# Template: Barker Validatierapport

## Doel en gebruik

Dit template beschrijft de structuur van een **validatierapport** zoals geproduceerd door de intent `valideer-barker-conformiteit`. Het rapport toetst een logisch datamodel tegen de regels en principes van de Barker-methode voor entiteit-relatie modellering.

Het template wordt gebruikt wanneer:
- Een logisch model getoetst moet worden op Barker-conformiteit
- Afwijkingen van Barker-regels geïdentificeerd en gedocumenteerd moeten worden
- Een go/no-go beslissing nodig is voor verdere verwerking van het model

## Structuur

Dit template beschrijft de OUTPUT structuur. Het gegenereerde artefact krijgt de volgende structuur:

```markdown
---
artefact_type: validatierapport
rapport_type: barker-conformiteit
gevalideerd_model: <pad naar gevalideerd logisch model>
validatie_resultaat: <conform|niet-conform|conditioneel-conform>
herkomstcode: <herkomstcode>
herkomstpositie: <voortbouwend>
initierend_artefact: <pad naar bronmodel>
gegenereerd_door: logisch-modelleur
datum: <datum>
---

# Barker Validatierapport

## Metadata

| Eigenschap | Waarde |
|------------|--------|
| Gevalideerd model | <model-naam> |
| Model pad | <pad naar model> |
| Validatiedatum | <datum> |
| Validatie-uitkomst | <conform/niet-conform/conditioneel-conform> |

## Samenvatting

<Korte samenvatting van validatie-uitkomst: aantal regels getoetst, aantal bevindingen, conclusie>

---

## Toegepaste Barker-regels

### Getoetste regels

| Regel-ID | Regel beschrijving | Status |
|----------|-------------------|--------|
| BRK-001 | <regel omschrijving> | ✓ Voldoet / ✗ Voldoet niet / ⚠ Waarschuwing |
| BRK-002 | <regel omschrijving> | ✓ / ✗ / ⚠ |

### Regels buiten scope

| Regel-ID | Reden niet getoetst |
|----------|---------------------|
| <regel-id> | <reden> |

---

## Bevindingen

### Kritieke bevindingen (blokkerend)

| # | Entiteit/Relatie | Regel | Bevinding | Aanbeveling |
|---|------------------|-------|-----------|-------------|
| 1 | <locatie> | <regel-id> | <wat is fout> | <hoe te corrigeren> |

### Niet-kritieke bevindingen (waarschuwingen)

| # | Entiteit/Relatie | Regel | Bevinding | Aanbeveling |
|---|------------------|-------|-----------|-------------|
| 1 | <locatie> | <regel-id> | <wat suboptimaal is> | <suggestie verbetering> |

### Positieve bevindingen

<Opsomming van aspecten die correct zijn geïmplementeerd>

- <positieve bevinding 1>
- <positieve bevinding 2>

---

## Detail per entiteit

### <Entiteit-1>

| Aspect | Status | Toelichting |
|--------|--------|-------------|
| Naamgeving | ✓/✗ | <toelichting> |
| Primaire sleutel | ✓/✗ | <toelichting> |
| Attributen | ✓/✗ | <toelichting> |
| Relaties | ✓/✗ | <toelichting> |

### <Entiteit-2>

[...structuur herhaalt per entiteit...]

---

## Relatie-analyse

| Relatie | Van | Naar | Cardinaliteit correct | Naamgeving correct | Opmerkingen |
|---------|-----|------|----------------------|-------------------|-------------|
| <relatie-1> | <ent-a> | <ent-b> | ✓/✗ | ✓/✗ | <opmerking> |

---

## Normalisatie-check

| Niveau | Criterium | Status | Bevinding |
|--------|-----------|--------|-----------|
| 1NF | Atomaire waarden | ✓/✗ | <bevinding> |
| 1NF | Geen herhalende groepen | ✓/✗ | <bevinding> |
| 2NF | Volledige functionele afhankelijkheid | ✓/✗ | <bevinding> |
| 3NF | Geen transitieve afhankelijkheden | ✓/✗ | <bevinding> |

---

## Conclusie en aanbevelingen

### Validatie-uitkomst: <CONFORM / NIET-CONFORM / CONDITIONEEL CONFORM>

**Samenvatting**:
<Korte conclusie over conformiteit van het model>

**Kritieke acties** (bij niet-conform):
1. <actie 1>
2. <actie 2>

**Aanbevelingen** (bij conditioneel conform):
1. <aanbeveling 1>
2. <aanbeveling 2>

---

## Herkomst

- Herkomstcode: <code>
- Herkomstpositie: voortbouwend
- Initierend artefact: <pad naar gevalideerd model>
- Gegenereerd door: logisch-modelleur
- Agent charter: artefacten/sfw/sfw.02.logisch-modelleur/logisch-modelleur.charter.md
- Datum: <datum>
```

## Placeholders

| Placeholder | Type | Beschrijving | Verplicht |
|-------------|------|--------------|-----------|
| `<gevalideerd_model>` | string | Pad naar het logisch model dat gevalideerd wordt | Ja |
| `<model-naam>` | string | Naam van het gevalideerde model | Ja |
| `<validatie_resultaat>` | enum | conform, niet-conform, conditioneel-conform | Ja |
| `<herkomstcode>` | string | JJMM.XXXX formaat, geërfd van bronmodel | Ja |
| `<regel-id>` | string | Identifier voor Barker-regel (BRK-xxx) | Ja |
| `<bevinding>` | string | Beschrijving van geconstateerde afwijking of conformiteit | Ja |
| `<aanbeveling>` | string | Suggestie voor correctie of verbetering | Nee |
| `<datum>` | date | ISO 8601 datum | Ja |

## Validatie-criteria

Een valide output volgens dit template:
- ✓ Bevat YAML frontmatter met alle verplichte velden (artefact_type, gevalideerd_model, validatie_resultaat, herkomstcode)
- ✓ Toegepaste Barker-regels sectie bevat minimaal 5 getoetste regels
- ✓ Bevindingen zijn gecategoriseerd (kritiek/niet-kritiek/positief)
- ✓ Elke bevinding heeft regel-referentie en aanbeveling
- ✓ Detail per entiteit is uitgewerkt voor alle entiteiten in bronmodel
- ✓ Normalisatie-check is volledig ingevuld (1NF, 2NF, 3NF)
- ✓ Conclusie bevat expliciete uitkomst en actiepunten
- ✓ Herkomstpositie is "voortbouwend" (validatie bouwt voort op bronmodel)

## Voorbeeld-output

```markdown
---
artefact_type: validatierapport
rapport_type: barker-conformiteit
gevalideerd_model: modellen/logisch/klantbeheer-logisch.md
validatie_resultaat: conditioneel-conform
herkomstcode: 2604.Xk9m
herkomstpositie: voortbouwend
initierend_artefact: modellen/logisch/klantbeheer-logisch.md
gegenereerd_door: logisch-modelleur
datum: 2026-04-13
---

# Barker Validatierapport

## Metadata

| Eigenschap | Waarde |
|------------|--------|
| Gevalideerd model | klantbeheer-logisch |
| Model pad | modellen/logisch/klantbeheer-logisch.md |
| Validatiedatum | 2026-04-13 |
| Validatie-uitkomst | Conditioneel conform |

## Samenvatting

Het model klantbeheer-logisch is getoetst tegen 12 Barker-regels. Er zijn 0 kritieke bevindingen en 2 waarschuwingen geconstateerd. Het model voldoet aan de kernprincipes van de Barker-methode en kan na adressering van de waarschuwingen als conform worden beschouwd.

---

## Toegepaste Barker-regels

### Getoetste regels

| Regel-ID | Regel beschrijving | Status |
|----------|-------------------|--------|
| BRK-001 | Elke entiteit heeft een unieke identifier | ✓ Voldoet |
| BRK-002 | Entiteitnamen zijn zelfstandige naamwoorden in enkelvoud | ✓ Voldoet |
| BRK-003 | Attributen zijn atomair (geen samengestelde waarden) | ✓ Voldoet |
| BRK-004 | Relaties hebben betekenisvolle namen | ⚠ Waarschuwing |
| BRK-005 | Cardinaliteiten zijn expliciet gedefinieerd | ✓ Voldoet |

---

## Bevindingen

### Kritieke bevindingen (blokkerend)

_Geen kritieke bevindingen._

### Niet-kritieke bevindingen (waarschuwingen)

| # | Entiteit/Relatie | Regel | Bevinding | Aanbeveling |
|---|------------------|-------|-----------|-------------|
| 1 | heeft_adres | BRK-004 | Relatienaam is generiek | Hernoem naar "resideert_op" of "bezoekadres_is" |
| 2 | Contactpersoon.functie | BRK-007 | Attribuut kan enum zijn | Overweeg waardelijst voor functie-types |

### Positieve bevindingen

- Alle entiteiten hebben correcte enkelvoudige naamgeving
- Primaire sleutels zijn consistent gedefinieerd
- 3NF normalisatie correct toegepast
- Traceerbaarheid naar bronconcepten is compleet

---

## Conclusie en aanbevelingen

### Validatie-uitkomst: CONDITIONEEL CONFORM

**Samenvatting**:
Het model voldoet aan de kernprincipes van de Barker-methode. De twee waarschuwingen zijn niet-blokkerend maar verbeteren de kwaliteit en leesbaarheid van het model.

**Aanbevelingen**:
1. Hernoem relatie "heeft_adres" naar meer specifieke naam
2. Definieer waardelijst voor Contactpersoon.functie attribuut

---

## Herkomst

- Herkomstcode: 2604.Xk9m
- Herkomstpositie: voortbouwend
- Initierend artefact: modellen/logisch/klantbeheer-logisch.md
- Gegenereerd door: logisch-modelleur
- Agent charter: artefacten/sfw/sfw.02.logisch-modelleur/logisch-modelleur.charter.md
- Datum: 2026-04-13
```

## Gebruiksinstructies

Voor agents die dit template gebruiken:
1. Lees het te valideren logisch model volledig
2. Identificeer de set van toepasbare Barker-regels
3. Toets elke entiteit, attribuut en relatie tegen de regels
4. Categoriseer bevindingen naar ernst (kritiek/waarschuwing/positief)
5. Voer normalisatie-check uit voor 1NF, 2NF, 3NF
6. Formuleer concrete aanbevelingen per bevinding
7. Bepaal eindoordeel (conform/niet-conform/conditioneel-conform)
8. Erf herkomstcode van bronmodel (voortbouwende positie)

## Versiebeheer

| Versie | Datum | Wijziging |
|--------|-------|-----------|
| 1.0.0 | 2026-04-13 | Initieel template voor logisch-modelleur |

---

**Template-categorie**: Agent-specifiek  
**Gebruikt door intents**: valideer-barker-conformiteit
