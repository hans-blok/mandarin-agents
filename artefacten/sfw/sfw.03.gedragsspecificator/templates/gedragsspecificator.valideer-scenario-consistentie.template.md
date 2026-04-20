---
# IDENTIFICATIE
template-id: "028"
template-naam: gedragsspecificator.valideer-scenario-consistentie

# RELATIES
artefact-type-id: "028"
agent-id: sfw.03.gedragsspecificator

# META-DATA
versie: 0.1.0
status: vers
digest: 1380
---
# Validatierapport Scenario-Consistentie

**Datum Audit**: {YYYY-MM-DD}
**Gevalideerde Feature(s)**: {Lijst met feature files of capabilities}
**Status**: {Valid | Consistent / Has Issues}
**Auditor**: {Agent Naam / Tool}

## 1. Samenvatting
*Korte beschrijving van de bevindingen (e.g., "Feature X is consistent met Y, maar terminologie wijkt af in Z").*

## 2. Bevindingen per Categorie

### 2.1 Ambiguïteit en Interpretatie
*Zijn er termen met meerdere betekenissen of onduidelijke definities?*

| Scenario/Stap | Term | Probleem | Advies |
|---|---|---|---|
| {Scenario A} | {Gebruiker} | {Wordt ook als 'Klant' aangeduid} | {Kies één term} |

### 2.2 Ontbrekende Scenario's / Edge Cases
*Zijn er logische gaten in de coverage? (Bijv. lege invoer, timeout, permissies)*

- [MISSING-01] {Scenario beschrijving}

### 2.3 Terminologie Consistentie (Ubiquitous Language)
*Worden concepten consistent gebruikt over feature files heen?*

- **Term**: {Term A} vs {Term B} in bestand {X} en {Y}

### 2.4 Traceerbaarheid
*Zijn scenario's herleidbaar naar Business Requirements / User Stories?*

- [TRACE-01] {Scenario mist referentie naar requirement ID}

## 3. Aanbevelingen
*Acties om de consistentie te herstellen.*

1. {Actie 1: e.g. Hernoem ... naar ...}
2. {Actie 2: Voeg scenario toe voor ...}

## 4. Conclusie
*Eindoordeel.*
- [ ] Goedgekeurd voor Engineering
- [ ] Revisie vereist
