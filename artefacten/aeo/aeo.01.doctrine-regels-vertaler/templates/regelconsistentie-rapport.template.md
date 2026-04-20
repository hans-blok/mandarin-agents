---
# IDENTIFICATIE
template-id: "022"
template-naam: regelconsistentie-rapport

# RELATIES
artefact-type-id: "022"
agent-id: aeo.01.doctrine-regels-vertaler

# META-DATA
versie: 1.0.0
status: vers
digest: ~
---

# Template: Regelconsistentie Rapport

## Doel en gebruik

Dit template beschrijft de outputstructuur voor consistentierapporten die door de `doctrine-regels-vertaler` worden gegenereerd bij de validatie van regelsets. Het rapport identificeert contradicties, duplicaten, lacunes en andere consistentieproblemen.

**Gebruikt door intents**:
- `valideer-regelconsistentie` — validatie van interne consistentie van een regelset

## Bestandslocatie

Consistentierapporten worden opgeslagen als:
- `artefacten/aeo/aeo.01.doctrine-regels-vertaler/rapporten/{regelset-id}.consistentierapport.md`

## Structuur

```markdown
---
rapport_type: regelconsistentie
regelset_id: <regelset-id>
regelset_versie: <versie>
validatie_datum: <ISO-8601-timestamp>
validator: doctrine-regels-vertaler
status: <valide|invalide|waarschuwingen>
---

# Consistentierapport: <regelset-naam>

## Samenvatting

| Categorie | Aantal | Status |
|-----------|--------|--------|
| Contradicties | <n> | <✓/✗> |
| Duplicaten | <n> | <✓/✗> |
| Lacunes | <n> | <✓/○> |
| Referentiefouten | <n> | <✓/✗> |
| **Totaal** | <n> | <status> |

## Gedetailleerde bevindingen

### Contradicties

{Lijst van regels die elkaar tegenspreken}

| Regel A | Regel B | Conflict |
|---------|---------|----------|
| <id-A> | <id-B> | <beschrijving conflict> |

### Duplicaten

{Lijst van regels die semantisch overlappen}

| Regel | Duplicaat van | Overlap |
|-------|---------------|---------|
| <id> | <id> | <percentage of beschrijving> |

### Lacunes

{Geïdentificeerde ontbrekende regels op basis van doctrine-analyse}

| Doctrine-sectie | Verwachte regel | Status |
|-----------------|-----------------|--------|
| <sectie-ref> | <beschrijving> | ontbreekt |

### Referentiefouten

{Regels met ongeldige doctrine-verwijzingen}

| Regel | doctrine_ref | Probleem |
|-------|--------------|----------|
| <id> | <ref> | <bestand niet gevonden/sectie niet gevonden> |

## Aanbevelingen

{Geordende lijst van aanbevolen acties}

1. <aanbeveling 1>
2. <aanbeveling 2>
3. <aanbeveling 3>

## Metadata

- **Gevalideerde regels**: <aantal>
- **Betrokken doctrines**: <lijst>
- **Validatie-duur**: <ms>
```

## Placeholders

| Placeholder | Type | Beschrijving | Verplicht |
|-------------|------|--------------|-----------|
| `<regelset-id>` | string | ID van de gevalideerde regelset | Ja |
| `<versie>` | semver | Versie van de gevalideerde regelset | Ja |
| `<status>` | enum | `valide`, `invalide`, of `waarschuwingen` | Ja |
| `<n>` | integer | Aantal bevindingen per categorie | Ja |

## Status-definities

| Status | Betekenis | Actie vereist |
|--------|-----------|---------------|
| `valide` | Geen problemen gevonden | Nee |
| `waarschuwingen` | Alleen lacunes of suggesties | Optioneel |
| `invalide` | Contradicties, duplicaten of referentiefouten | Ja |

## Validatie-criteria

Een valide consistentierapport volgens dit template:
- ✓ Bevat verplichte metadata in frontmatter
- ✓ Samenvatting-tabel is volledig ingevuld
- ✓ Elke bevinding heeft regel-ID en beschrijving
- ✓ Status is consistent met bevindingen (invalide bij contradicties/duplicaten/referentiefouten)
- ✓ Aanbevelingen zijn concreet en actiegericht

## Voorbeeld-output

```markdown
---
rapport_type: regelconsistentie
regelset_id: RS-BRH-001
regelset_versie: 1.0.0
validatie_datum: 2026-04-19T11:00:00+02:00
validator: doctrine-regels-vertaler
status: waarschuwingen
---

# Consistentierapport: Bronhouding en exploratie regels

## Samenvatting

| Categorie | Aantal | Status |
|-----------|--------|--------|
| Contradicties | 0 | ✓ |
| Duplicaten | 0 | ✓ |
| Lacunes | 2 | ○ |
| Referentiefouten | 0 | ✓ |
| **Totaal** | 2 | waarschuwingen |

## Gedetailleerde bevindingen

### Contradicties

_Geen contradicties gevonden._

### Duplicaten

_Geen duplicaten gevonden._

### Lacunes

| Doctrine-sectie | Verwachte regel | Status |
|-----------------|-----------------|--------|
| §7.1 Logging-vereisten | Regel over logging-frequentie | ontbreekt |
| §8.2 Escalatie-protocol | Regel over escalatie-triggers | ontbreekt |

### Referentiefouten

_Geen referentiefouten gevonden._

## Aanbevelingen

1. Voeg regel toe voor logging-frequentie op basis van §7.1
2. Voeg regel toe voor escalatie-triggers op basis van §8.2

## Metadata

- **Gevalideerde regels**: 4
- **Betrokken doctrines**: doctrine.bronhouding-en-exploratie.md
- **Validatie-duur**: 45ms
```

## Versiebeheer

| Versie | Datum | Wijziging |
|--------|-------|-----------|
| 1.0.0 | 2026-04-19 | Initiële template voor consistentierapporten |

---

**Template-categorie**: Agent-specifiek  
**Gebruikt door intents**: valideer-regelconsistentie
