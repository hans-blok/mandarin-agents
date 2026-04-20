---
# IDENTIFICATIE
template-id: "023"
template-naam: modelleringsbeslissing

# RELATIES
artefact-type-id: "023"
agent-id: sfw.03.logisch-modelleur

# META-DATA
versie: 1.0.0
status: vers
digest: aa0f
---

# Template: Modelleringsbeslissing

## Doel en gebruik

Dit template beschrijft de structuur van een **modelleringsbeslissing** zoals geproduceerd door de intent `documenteer-modelleringsbeslissing`. Het document legt een specifieke ontwerpkeuze vast met volledige traceerbaarheid naar bronnen, motivatie en overwogen alternatieven.

Het template wordt gebruikt wanneer:
- Een significante modelleringskeuze gedocumenteerd moet worden
- De motivatie achter een ontwerpbeslissing expliciet vastgelegd moet worden
- Traceerbaarheid vereist is voor audit of toekomstige wijzigingen
- Alternatieven en hun afwijzing gedocumenteerd moeten worden

## Structuur

Dit template beschrijft de OUTPUT structuur. Het gegenereerde artefact krijgt de volgende structuur:

```markdown
---
artefact_type: modelleringsbeslissing
beslissing_id: <beslissing-id>
model: <model-naam>
onderwerp: <kort onderwerp>
status: <voorgesteld|geaccepteerd|verworpen|vervangen>
herkomstcode: <herkomstcode>
herkomstpositie: <initierend|voortbouwend>
gegenereerd_door: logisch-modelleur
datum: <datum>
---

# Modelleringsbeslissing: <Titel>

## Metadata

| Eigenschap | Waarde |
|------------|--------|
| Beslissing ID | <beslissing-id> |
| Model | <model-naam> |
| Status | <status> |
| Datum | <datum> |
| Auteur | logisch-modelleur |

---

## Context

<Beschrijf de situatie en aanleiding voor deze beslissing. Wat is het probleem of de vraag die beantwoord moet worden?>

### Relevante bronnen

| Bron | Type | Relevantie |
|------|------|------------|
| <bron-1> | <concept/regel/model> | <waarom relevant> |
| <bron-2> | <concept/regel/model> | <waarom relevant> |

---

## Probleemstelling

<Formuleer in 1-3 zinnen het kernprobleem of de kernvraag>

### Constraints

- <constraint 1: wat moet gerespecteerd worden>
- <constraint 2: wat moet gerespecteerd worden>

### Kwaliteitseisen

- <eis 1: wat is belangrijk in de oplossing>
- <eis 2: wat is belangrijk in de oplossing>

---

## Beslissing

### Gekozen oplossing

<Beschrijf de gekozen oplossing in concrete termen>

### Rationale

<Leg uit waarom deze oplossing gekozen is. Verwijs naar constraints en kwaliteitseisen.>

### Impact

| Aspect | Impact |
|--------|--------|
| Entiteiten | <welke entiteiten zijn geraakt> |
| Relaties | <welke relaties zijn geraakt> |
| Normalisatie | <effect op normalisatieniveau> |
| Traceerbaarheid | <effect op herleidbaarheid> |

---

## Alternatieven

### Alternatief 1: <naam>

**Beschrijving**: <korte beschrijving van het alternatief>

**Voordelen**:
- <voordeel 1>
- <voordeel 2>

**Nadelen**:
- <nadeel 1>
- <nadeel 2>

**Reden voor afwijzing**: <waarom niet gekozen>

### Alternatief 2: <naam>

[...structuur herhaalt per alternatief...]

---

## Bronverwijzingen

### Canonieke bronnen

| Bron | Sectie | Relevante passage |
|------|--------|-------------------|
| <bron-pad-1> | <sectie> | <citaat of samenvatting> |
| <bron-pad-2> | <sectie> | <citaat of samenvatting> |

### Domeinbronnen

| Bron | Relevantie |
|------|------------|
| <bron-1> | <hoe deze bron de beslissing ondersteunt> |

---

## Gevolgen

### Directe gevolgen

- <gevolg 1 voor het model>
- <gevolg 2 voor het model>

### Afhankelijkheden

| Type | Beschrijving |
|------|--------------|
| Vereist | <wat moet eerst gebeuren/bestaan> |
| Beïnvloedt | <wat wordt door deze beslissing beïnvloed> |

### Risico's

| Risico | Mitigatie |
|--------|-----------|
| <risico 1> | <hoe te mitigeren> |

---

## Herkomst

- Herkomstcode: <code>
- Herkomstpositie: <initierend|voortbouwend>
- Initierend artefact: <pad indien voortbouwend>
- Gegenereerd door: logisch-modelleur
- Agent charter: artefacten/sfw/sfw.02.logisch-modelleur/logisch-modelleur.charter.md
- Datum: <datum>

---

## Versiebeheer

| Versie | Datum | Wijziging | Auteur |
|--------|-------|-----------|--------|
| 1.0.0 | <datum> | Initiële beslissing | logisch-modelleur |
```

## Placeholders

| Placeholder | Type | Beschrijving | Verplicht |
|-------------|------|--------------|-----------|
| `<beslissing-id>` | string | Unieke identifier voor de beslissing (bijv. MB-001) | Ja |
| `<model-naam>` | string | Naam van het model waarop de beslissing betrekking heeft | Ja |
| `<onderwerp>` | string | Kort onderwerp van de beslissing (max 50 tekens) | Ja |
| `<status>` | enum | voorgesteld, geaccepteerd, verworpen, vervangen | Ja |
| `<herkomstcode>` | string | JJMM.XXXX formaat | Ja |
| `<context>` | string | Beschrijving van de situatie en aanleiding | Ja |
| `<probleemstelling>` | string | Kernprobleem in 1-3 zinnen | Ja |
| `<gekozen-oplossing>` | string | Beschrijving van de gekozen oplossing | Ja |
| `<rationale>` | string | Motivatie voor de keuze | Ja |
| `<alternatief>` | object | Beschrijving van overwogen alternatief | Nee |
| `<bronverwijzing>` | string | Pad naar canonieke of domeinbron | Ja |
| `<datum>` | date | ISO 8601 datum | Ja |

## Validatie-criteria

Een valide output volgens dit template:
- ✓ Bevat YAML frontmatter met alle verplichte velden (artefact_type, beslissing_id, model, status, herkomstcode)
- ✓ Context-sectie beschrijft situatie en relevante bronnen
- ✓ Probleemstelling is scherp geformuleerd (1-3 zinnen)
- ✓ Beslissing-sectie bevat concrete oplossing met rationale
- ✓ Minimaal 1 alternatief is gedocumenteerd met voordelen, nadelen en afwijzingsreden
- ✓ Bronverwijzingen bevatten minimaal 1 canonieke bron
- ✓ Gevolgen-sectie beschrijft directe impact en afhankelijkheden
- ✓ Herkomst-sectie is volledig conform doctrine-traceability.md

## Voorbeeld-output

```markdown
---
artefact_type: modelleringsbeslissing
beslissing_id: MB-001
model: klantbeheer-logisch
onderwerp: Adresgegevens als aparte entiteit
status: geaccepteerd
herkomstcode: 2604.Xk9m
herkomstpositie: voortbouwend
initierend_artefact: modellen/logisch/klantbeheer-logisch.md
gegenereerd_door: logisch-modelleur
datum: 2026-04-13
---

# Modelleringsbeslissing: Adresgegevens als aparte entiteit

## Metadata

| Eigenschap | Waarde |
|------------|--------|
| Beslissing ID | MB-001 |
| Model | klantbeheer-logisch |
| Status | Geaccepteerd |
| Datum | 2026-04-13 |
| Auteur | logisch-modelleur |

---

## Context

In het conceptueel model zijn adresgegevens opgenomen als attributen van de entiteit Klant. Bij transformatie naar het logisch model moet bepaald worden of deze structuur behouden blijft of dat adresgegevens genormaliseerd worden naar een aparte entiteit.

### Relevante bronnen

| Bron | Type | Relevantie |
|------|------|------------|
| klantbeheer-conceptueel.md | concept | Bron van adresgegevens als klant-attributen |
| Barker-methode | regel | Normalisatieprincipes voor 3NF |

---

## Probleemstelling

Moeten adresgegevens (straat, huisnummer, postcode, plaats) als attributen van Klant behouden blijven, of als aparte Adres-entiteit gemodelleerd worden?

### Constraints

- Model moet voldoen aan 3NF volgens Barker-methode
- Bestaande integraties met legacy-systemen moeten mogelijk blijven
- Performance bij queries op klantgegevens mag niet significant verslechteren

### Kwaliteitseisen

- Elimineren van data-redundantie
- Ondersteunen van meerdere adressen per klant
- Behoud van historische adresgegevens mogelijk maken

---

## Beslissing

### Gekozen oplossing

Adresgegevens worden gemodelleerd als aparte entiteit **Adres** met een 1:N relatie naar **Klant**. De Adres-entiteit bevat: adres_id (PK), klant_id (FK), straat, huisnummer, postcode, plaats, adres_type.

### Rationale

Deze oplossing elimineert de herhalende groep (adresgegevens) uit Klant en brengt het model naar 1NF/3NF. Het maakt meerdere adressen per klant mogelijk (bijv. bestel- en factuuradres) en ondersteunt adreshistorie. Dit volgt direct de Barker-normalisatieprincipes.

### Impact

| Aspect | Impact |
|--------|--------|
| Entiteiten | Nieuwe entiteit Adres toegevoegd |
| Relaties | Nieuwe relatie Klant → Adres (1:N) |
| Normalisatie | Verhoogd naar 3NF |
| Traceerbaarheid | Adresgegevens apart traceerbaar |

---

## Alternatieven

### Alternatief 1: Adres als embedded attributen

**Beschrijving**: Behoud adresgegevens als attributen van Klant (straat, huisnummer, etc.)

**Voordelen**:
- Eenvoudiger model (minder entiteiten)
- Geen joins nodig voor klant met adres

**Nadelen**:
- Schendt 1NF (herhalende groep bij meerdere adressen)
- Geen ondersteuning voor meerdere adressen
- Adreswijzigingen overschrijven historie

**Reden voor afwijzing**: Schendt Barker-normalisatieprincipes en beperkt functionaliteit

### Alternatief 2: JSON-attribuut voor adressen

**Beschrijving**: Eén JSON-attribuut met array van adresobjecten

**Voordelen**:
- Flexibel aantal adressen
- Geen aparte entiteit nodig

**Nadelen**:
- Schendt atomiciteitsprincipe (niet 1NF)
- Moeilijk querybaar
- Geen referentiële integriteit

**Reden voor afwijzing**: Niet conform Barker-methode, beperkt query-mogelijkheden

---

## Bronverwijzingen

### Canonieke bronnen

| Bron | Sectie | Relevante passage |
|------|--------|-------------------|
| Barker-methode | Normalisatie | "Herhalende groepen moeten geëlimineerd worden door extractie naar aparte entiteiten" |

### Domeinbronnen

| Bron | Relevantie |
|------|------------|
| CRM domeinanalyse | Klanten hebben vaak meerdere adressen (bestel, factuur, bezoek) |

---

## Gevolgen

### Directe gevolgen

- Queries voor klant met adres vereisen join
- Applicatielaag moet omgaan met 1:N adresstructuur
- Adreshistorie wordt mogelijk (soft delete of versioning)

### Afhankelijkheden

| Type | Beschrijving |
|------|--------------|
| Vereist | Klant-entiteit moet bestaan |
| Beïnvloedt | Alle queries die adresgegevens ophalen |

### Risico's

| Risico | Mitigatie |
|--------|-----------|
| Query-complexiteit neemt toe | Definieer standaard views voor klant-met-adres |
| Performance bij grote datasets | Index op klant_id in Adres-entiteit |

---

## Herkomst

- Herkomstcode: 2604.Xk9m
- Herkomstpositie: voortbouwend
- Initierend artefact: modellen/logisch/klantbeheer-logisch.md
- Gegenereerd door: logisch-modelleur
- Agent charter: artefacten/sfw/sfw.02.logisch-modelleur/logisch-modelleur.charter.md
- Datum: 2026-04-13

---

## Versiebeheer

| Versie | Datum | Wijziging | Auteur |
|--------|-------|-----------|--------|
| 1.0.0 | 2026-04-13 | Initiële beslissing | logisch-modelleur |
```

## Gebruiksinstructies

Voor agents die dit template gebruiken:
1. Identificeer de modelleringsvraag of -keuze die gedocumenteerd moet worden
2. Verzamel relevante bronnen (canoniek en domein-specifiek)
3. Formuleer de probleemstelling scherp en concreet
4. Beschrijf de gekozen oplossing met concrete impact
5. Documenteer minimaal 1 overwogen alternatief met voor/nadelen
6. Leg bronverwijzingen vast voor traceerbaarheid
7. Analyseer gevolgen, afhankelijkheden en risico's
8. Bepaal herkomstpositie (initierend bij eerste beslissing, voortbouwend bij wijziging)

## Versiebeheer

| Versie | Datum | Wijziging |
|--------|-------|-----------|
| 1.0.0 | 2026-04-13 | Initieel template voor logisch-modelleur |

---

**Template-categorie**: Agent-specifiek  
**Gebruikt door intents**: documenteer-modelleringsbeslissing
