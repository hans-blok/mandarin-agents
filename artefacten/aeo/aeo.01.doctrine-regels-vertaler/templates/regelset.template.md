---
# IDENTIFICATIE
template-id: "021"
template-naam: regelset

# RELATIES
artefact-type-id: "021"
agent-id: aeo.01.doctrine-regels-vertaler

# META-DATA
versie: 1.0.0
status: vers
digest: ~
---

# Template: Regelset

## Doel en gebruik

Dit template beschrijft de outputstructuur voor regelsets die door de `doctrine-regels-vertaler` worden gegenereerd. Een regelset is een gestructureerde YAML-representatie van individuele, toetsbare regels die zijn geëxtraheerd uit doctrine-documenten.

**Gebruikt door intents**:
- `definieer-regels-uit-doctrine` — initiële extractie van regels uit doctrine
- `normaliseer-regel` — normalisatie naar consistente formulering
- `structureer-regelset` — structureren als filterbaar geheel
- `publiceer-regelset` — finaliseren voor operationeel gebruik

## Bestandslocatie

Regelsets worden opgeslagen als:
- `artefacten/aeo/aeo.01.doctrine-regels-vertaler/regelsets/{doctrine-naam}.regels.yaml`

## Structuur

Het regelset-bestand is een YAML-document met de volgende structuur:

```yaml
# Regelset metadata
regelset:
  id: <regelset-id>
  naam: <regelset-naam>
  versie: <versie>
  doctrine_bron: <pad-naar-doctrine>
  gegenereerd: <ISO-8601-timestamp>
  status: <draft|actief|gearchiveerd>

# Regels
regels:
  - id: <regel-id>
    type: <gebod|verbod|eis|richtlijn|aanbeveling>
    entiteit: <agent|artefact|proces|systeem|gebruiker>
    actie: <actie-beschrijving-kebab-case>
    tekst: >
      <volledige regelformulering in natuurlijke taal>
    conditie:
      veld: <veldnaam>
      operator: <eq|neq|in|not_in|contains|gt|lt|gte|lte>
      waarde: <waarde-of-lijst>
    value_stream: [<vs-codes>|all]
    fase: [<fase-codes>|all]
    status: <actief|inactief|deprecated>
    doctrine_ref: "<doctrine-bestand>#§<sectienummer>"
```

## Placeholders

| Placeholder | Type | Beschrijving | Verplicht |
|-------------|------|--------------|-----------|
| `<regelset-id>` | string | Unieke identifier voor de regelset (bijv. `RS-BRH-001`) | Ja |
| `<regelset-naam>` | string | Beschrijvende naam (bijv. "Bronhouding regels") | Ja |
| `<versie>` | semver | Versienummer conform semver (bijv. `1.0.0`) | Ja |
| `<doctrine_bron>` | string | Relatief pad naar bron-doctrine | Ja |
| `<regel-id>` | string | Unieke regel-ID met prefix (bijv. `BRH-004`) | Ja |
| `<type>` | enum | Een van: `gebod`, `verbod`, `eis`, `richtlijn`, `aanbeveling` | Ja |
| `<entiteit>` | enum | Een van: `agent`, `artefact`, `proces`, `systeem`, `gebruiker` | Ja |
| `<actie>` | string | Actie in kebab-case (bijv. `exploratieve-output-gebruiken-in-productie`) | Ja |
| `<tekst>` | string | Volledige regelformulering in natuurlijke taal | Ja |
| `<conditie>` | object | Filterbare conditie (optioneel bij onvoorwaardelijke regels) | Nee |
| `<value_stream>` | list | Lijst van value streams of `[all]` | Ja |
| `<fase>` | list | Lijst van fasen of `[all]` | Ja |
| `<status>` | enum | Een van: `actief`, `inactief`, `deprecated` | Ja |
| `<doctrine_ref>` | string | Precieze verwijzing naar doctrine-sectie | Ja |

## Regel-ID conventies

Regel-IDs volgen het patroon `{PREFIX}-{NNN}`:

| Prefix | Doctrine-domein |
|--------|-----------------|
| `BRH` | bronhouding-en-exploratie |
| `TRC` | traceability |
| `HND` | handoff |
| `RET` | retrieval-en-contextselectie |
| `TPL` | templategebruik |
| `CHR` | charter-normering |

## Type-definities

| Type | Modaliteit | Formulering |
|------|------------|-------------|
| `gebod` | MOET/SHALL | "Elke agent MOET..." |
| `verbod` | MAG NIET/SHALL NOT | "Geen agent MAG..." |
| `eis` | VEREIST/REQUIRED | "Het is vereist dat..." |
| `richtlijn` | BEHOORT/SHOULD | "Agents behoren..." |
| `aanbeveling` | KAN/MAY | "Agents kunnen..." |

## Conditie-operatoren

| Operator | Betekenis | Voorbeeld |
|----------|-----------|-----------|
| `eq` | Gelijk aan | `bronhouding eq exploratief` |
| `neq` | Niet gelijk aan | `status neq deprecated` |
| `in` | In lijst | `fase in [aeo.01, aeo.02]` |
| `not_in` | Niet in lijst | `type not_in [aanbeveling]` |
| `contains` | Bevat substring | `naam contains vertaler` |
| `gt`, `lt`, `gte`, `lte` | Numerieke vergelijking | `versie gte 1.0.0` |

## Validatie-criteria

Een valide regelset volgens dit template:
- ✓ Bevat verplichte metadata (`id`, `naam`, `versie`, `doctrine_bron`, `status`)
- ✓ Elke regel heeft een unieke `id` binnen de regelset
- ✓ Elke regel heeft alle verplichte velden ingevuld
- ✓ `type` is een van de toegestane waarden
- ✓ `entiteit` is een van de toegestane waarden
- ✓ `doctrine_ref` verwijst naar bestaande doctrine-sectie
- ✓ `status` is consistent (`actief` regels mogen niet verwijzen naar `deprecated` doctrines)
- ✓ YAML is syntactisch correct en parseert zonder errors

## Voorbeeld-output

```yaml
# Regelset: Bronhouding regels
regelset:
  id: RS-BRH-001
  naam: Bronhouding en exploratie regels
  versie: 1.0.0
  doctrine_bron: doctrine.bronhouding-en-exploratie.md
  gegenereerd: 2026-04-19T10:30:00+02:00
  status: actief

regels:
  - id: BRH-001
    type: gebod
    entiteit: agent
    actie: bronhouding-expliciet-maken
    tekst: >
      Elke agent MOET zijn bronhouding expliciet maken
      in het charter.
    value_stream: [all]
    fase: [all]
    status: actief
    doctrine_ref: "doctrine.bronhouding-en-exploratie.md#§3.1"

  - id: BRH-002
    type: eis
    entiteit: agent
    actie: input-gebonden-output-traceerbaar-houden
    tekst: >
      Input-gebonden agents MOETEN hun output 100% herleidbaar
      houden tot de input.
    conditie:
      veld: bronhouding
      operator: eq
      waarde: input-gebonden
    value_stream: [all]
    fase: [all]
    status: actief
    doctrine_ref: "doctrine.bronhouding-en-exploratie.md#§4.2"

  - id: BRH-003
    type: richtlijn
    entiteit: agent
    actie: canon-consultatie-loggen
    tekst: >
      Canon-gebonden agents BEHOREN elke consultatie te loggen
      in audit/canon-consult.log.md.
    conditie:
      veld: bronhouding
      operator: eq
      waarde: canon-gebonden
    value_stream: [aeo]
    fase: [aeo.01, aeo.02]
    status: actief
    doctrine_ref: "doctrine.bronhouding-en-exploratie.md#§5.3"

  - id: BRH-004
    type: verbod
    entiteit: agent
    actie: exploratieve-output-gebruiken-in-productie
    tekst: >
      Geen agent MAG exploratieve output direct gebruiken
      in productie.
    conditie:
      veld: bronhouding
      operator: eq
      waarde: exploratief
    value_stream: [all]
    fase: [all]
    status: actief
    doctrine_ref: "doctrine.bronhouding-en-exploratie.md#§6.4"
```

## Gebruiksinstructies

Voor agents die dit template gebruiken:

1. **Extraheer regels**: Identificeer normatieve uitspraken in de doctrine (MOET, MAG NIET, BEHOORT, etc.)
2. **Classificeer type**: Bepaal of het een gebod, verbod, eis, richtlijn of aanbeveling is
3. **Identificeer entiteit**: Bepaal op welke entiteit de regel van toepassing is
4. **Formuleer actie**: Beschrijf de actie in kebab-case (werkwoord-object patroon)
5. **Leg conditie vast**: Indien de regel conditioneel is, specificeer de filterbare conditie
6. **Bepaal scope**: Geef aan voor welke value streams en fasen de regel geldt
7. **Voeg referentie toe**: Verwijs exact naar de doctrine-sectie als `doctrine_ref`

## Versiebeheer

| Versie | Datum | Wijziging |
|--------|-------|-----------|
| 1.0.0 | 2026-04-19 | Initiële template voor doctrine-regels-vertaler |

---

**Template-categorie**: Agent-specifiek  
**Gebruikt door intents**: definieer-regels-uit-doctrine, normaliseer-regel, structureer-regelset, publiceer-regelset
