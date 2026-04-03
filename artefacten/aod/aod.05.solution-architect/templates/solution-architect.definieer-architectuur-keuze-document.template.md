---
agent: solution-architect
template_naam: definieer-architectuur-keuze-document
versie: 1.0.0
output_type: document
doel: Legt een architectuurkeuze gestructureerd vast met context, opties, afwegingen, advies en consequenties — vergelijkbaar met een ADR maar zonder het formele besluit (dat wordt door een andere agent of stakeholder genomen).
digest: 55b0
status: vers
---
# Template: Architectuur-keuze-document

## Doel en gebruik

Dit template structureert de output van de intent `definieer-architectuur-keuze-document`. Het produceert een leesbaar, gestructureerd document dat een architectuurkeuze onderbouwt vanuit meerdere perspectieven: strategisch, organisatorisch, technisch en financieel. Het document heeft raakvlakken met een Architecture Decision Record (ADR), maar legt het besluit zelf niet vast — alleen de onderbouwing, afweging en het advies.

Gebruikt door: `definieer-architectuur-keuze-document`

## Structuur

```markdown
---
agent: solution-architect
intent: definieer-architectuur-keuze-document
scope: {scope-omschrijving}
kaderdefinities: {kaderdefinities}
versie: 1.0.0
datum: {yyyy-mm-dd}
---

# Architectuurkeuze-document: {Onderwerp}

**Status**: {Concept | In review | Geadviseerd | Besloten}
**Datum**: {yyyy-mm-dd}
**Auteur(s)**: {agent of persoon}

## Samenvatting Keuze

{Beschrijf in 2-3 zinnen de kernkeuze: wat wordt voorgesteld, waarom, en wat het beoogde effect is.}

## Context

### Probleemstelling

{Beschrijf de huidige situatie en het probleem of de kans die aanleiding geeft tot deze architectuurkeuze. Maak expliciet:
- Wat is de huidige situatie?
- Waarom is de huidige situatie niet (meer) wenselijk?
- Welke opties liggen er?}

**Opties:**
1. {Optie 1: korte omschrijving}
2. {Optie 2: korte omschrijving}
3. {Optie N: korte omschrijving (indien van toepassing)}

### Achtergrond

{Beschrijf relevante achtergrondcontext:
- Strategisch beleid of kaders die van toepassing zijn
- Eerdere besluiten of architectuurprincipes
- Externe factoren (standaarden, wetgeving, marktbewegingen)}

## Afweging

{Herhaal per optiepaar of per individuele optie het voor- en nadelenblok. Minimaal de twee hoofdopties vergelijken.}

### Voordelen {Optie A} t.o.v. {Optie B}

- **{Aspect 1}**: {Toelichting voordeel}
- **{Aspect 2}**: {Toelichting voordeel}
- **{Aspect N}**: {Toelichting voordeel}

### Nadelen {Optie A} t.o.v. {Optie B}

- **{Aspect 1}**: {Toelichting nadeel}
- **{Aspect 2}**: {Toelichting nadeel}
- **{Aspect N}**: {Toelichting nadeel}

{Herhaal voordelen/nadelen-blokken voor aanvullende optievergelijkingen indien relevant.}

## Advies

**Voorkeur**: {Geadviseerde optie}

**Alternatief**: {Alternatieve optie met condities waaronder deze relevant wordt}

**Motivatie**:
{Onderbouw het advies: waarom wegen de voordelen zwaarder dan de nadelen? Hoe sluit het aan bij strategisch beleid, kaderdefinities en toekomstbestendigheid? Wat zijn de langetermijneffecten?}

> **Let op**: Dit document legt het advies vast, niet het besluit. Het besluit wordt genomen door de verantwoordelijke stakeholder(s) of besluitvormingsagent.

## Consequenties

{Beschrijf de consequenties van de geadviseerde keuze per architectuurlaag of perspectief. Gebruik de voor het domein relevante lagen.}

### Dienstverlening & Samenleving

- {Consequentie voor eindgebruikers, inwoners, klanten}
- {Consequentie voor transparantie en traceerbaarheid}

### Organisatie & (Keten)processen

- {Consequentie voor werkprocessen en rolverdeling}
- {Consequentie voor training en verandermanagement}
- {Consequentie voor samenwerking met ketenpartners}

### Informatie & Applicatie

- {Consequentie voor het applicatielandschap}
- {Consequentie voor gegevensuitwisseling en standaardisatie}
- {Consequentie voor integraties met andere systemen}

### Techniek & Infrastructuur

- {Consequentie voor API-beheer, protocollen en standaarden}
- {Consequentie voor beveiliging en toegangsbeheer}

### Financieel

- {Eenmalige kosten (ontwikkeling, migratie, training)}
- {Structurele kosten of besparingen}
- {Budgetimplicaties}

## Implementatie (voorstel)

### Acties

| Actie | Verantwoordelijke | Tijdspad |
|-------|-------------------|----------|
| {Actie 1} | {Rol/team} | {Periode} |
| {Actie 2} | {Rol/team} | {Periode} |
| {Actie N} | {Rol/team} | {Periode} |

## Verwijzingen

- {Referentie 1: document, standaard of beleidsstuk}
- {Referentie 2: technische documentatie of specificatie}
- {Referentie N: overige bronnen}

## Openstaande vragen

- {Vraag 1 die nog beantwoord moet worden voor of na het besluit}
- {Vraag N}

## Betrokkenen

| Functie/Rol | Naam | Geraadpleegd | Geïnformeerd |
|-------------|------|:------------:|:------------:|
| {Functie} | {Naam} | [ ] | [ ] |
| {Functie} | {Naam} | [ ] | [ ] |

## Aannames en beperkingen

{Expliciet gemaakte aannames en beperkingen bij de analyse en het advies.}
```

## Placeholders

| Placeholder | Type | Toelichting |
|-------------|------|-------------|
| `{scope-omschrijving}` | string | Afbakening van de keuze (bijv. "Zaaksysteem RUST", "Integratiestrategie domein X") |
| `{kaderdefinities}` | string | Canoniek pad naar kaderdefinitie(s), of "geen" |
| `{Onderwerp}` | string | Titel van de architectuurkeuze |
| `{Status}` | enum | Concept, In review, Geadviseerd, Besloten |
| `{Optie A/B/N}` | string | Korte naam per optie die vergeleken wordt |
| `{Aspect}` | string | Naam van het afwegingscriterium (bijv. Compliance, Automatisering, Kosten) |

## Naamgevingsconventie

**Bestandsnaam**: `architectuur-keuze-{onderwerp-kort}.md`
**Locatie**: `artefacten/aod/aod.05.solution-architect/output/`

## Relatie tot ADR

Dit document is verwant aan een Architecture Decision Record (ADR) maar verschilt op twee punten:
1. **Geen besluit**: Het document legt het advies vast; het besluit wordt door een stakeholder of besluitvormingsagent genomen.
2. **Consequenties per laag**: Waar een ADR consequenties vaak als vlakke lijst beschrijft, structureert dit template ze per architectuurlaag zodat impact zichtbaar is per perspectief.