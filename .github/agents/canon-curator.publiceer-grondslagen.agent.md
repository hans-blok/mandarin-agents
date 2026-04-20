---
agent: canon-curator
intent: publiceer-grondslagen
intent-id: aeo.01.canon-curator.04
versie: 1.0.0
digest: 98c3
status: vers
---
# Canon-curator — Publiceer Grondslagen

## Rolbeschrijving (korte samenvatting)

De Canon-curator scant de volledige `grondslagen/` map van de canon-workspace en genereert een machineleesbaar register als `grondslagen/grondslagen.json`, gevalideerd tegen `grondslagen.schema.json`. De uitvoering is volledig deterministisch en programmatisch — zonder LLM-consultatie of inferentie.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `canon-curator.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**: geen — de intent werkt volledig automatisch op basis van de canon-structuur.

**Afgeleide informatie** (automatisch bepaald door runner):
- `canon_pad`: Pad naar mandarin-canon workspace (resolved als sibling van repo-root)
- `grondslagen_dir`: `{canon_pad}/grondslagen/`
- `schema_pad`: `{canon_pad}/grondslagen.schema.json`
- `output_pad`: `{canon_pad}/grondslagen/grondslagen.json`

### Output (wat komt eruit)

De Canon-curator levert:
- **`grondslagen/grondslagen.json`** in de canon-workspace, conform `grondslagen.schema.json`, met een genormaliseerde structuur:
  - `versie`: Versienummer van de publicatie
  - `gegenereerd`: ISO 8601 timestamp (UTC) van het moment van generatie
  - `algemeen`: Grondslagen die ecosysteem-breed gelden (`.algemeen/`, `value-streams/`, `kaderdefinities/`, e.d.)
  - `value_streams`: Object per value stream (sleutel = VS-code in hoofdletters, bijv. `AEO`), elk met:
    - `code`: VS-code
    - `naam`: Volledige naam (voor bekende VS-codes)
    - `grondslagen`: Bestanden direct in `{vs}/` (zonder fase-subfolder)
    - `fasen`: Object per fasecode (`01`, `02`, ...), elk met `code` en `grondslagen[]`

  Elk grondslag-entry bevat:
  - `naam`: Bestandsnaam (bijv. `doctrine-traceability.md`)
  - `pad`: Relatief pad t.o.v. `grondslagen/` (bijv. `.algemeen/doctrine-traceability.md`)
  - `type`: Zie type-afleiding tabel hieronder
  - `titel`: Eerste `# H1` header uit het bestand (fallback: bestandsnaam, getiteld)
  - `digest_header`: Digest zoals opgeslagen in de YAML frontmatter (`"0000"` als absent)
  - `digest_berekend`: Live berekende MD5-digest van de body op moment van publicatie
  - `status_header`: Status zoals vermeld in de YAML frontmatter — dit is een feitelijke rapportage van wat het bestand claimt, geen oordeel over inhoudelijke kwaliteit

> **Let op**: `publiceer-grondslagen` rapporteert feiten — geen oordelen. Wanneer `digest_header ≠ digest_berekend` spreekt men van *drift*: het bestand is gewijzigd na de laatste digest-registratie. Het oordeel of dit een inconsistentie of probleem vormt is de verantwoordelijkheid van de `valideer-grondslag-consistentie` intent.

**Classificatie-regels**:

| Pad-patroon (t.o.v. `grondslagen/`) | Bucket in JSON |
|---|---|
| `.algemeen/...` | `algemeen[]` |
| `value-streams/...` | `algemeen[]` |
| `kaderdefinities/...` | `algemeen[]` |
| `{vs}/bestand.md` (geen fase-subfolder) | `value_streams[VS].grondslagen[]` |
| `{vs}/{vs}.{NN}.*/bestand.md` | `value_streams[VS].fasen[NN].grondslagen[]` |

VS-herkenning: eerste padsegment matcht `^[a-z]{2,5}$` (geen punt, geen koppelteken).

**Type-afleiding** (op basis van pad en bestandsnaam):

| Patroon | Type |
|---|---|
| pad begint met `value-streams/` of naam bevat `value-stream` | `value-stream` |
| pad begint met `kaderdefinities/` of naam bevat `kaderdefinitie` | `kaderdefinitie` |
| naam bevat `doctrine` | `doctrine` |
| naam bevat `constitutie` | `constitutie` |
| naam bevat `concepten` | `concepten` |
| naam bevat `checklist` | `checklist` |
| overig | `grondslag` |

**Digest-semantiek**:

| Situatie | `digest_header` | `status_header` |
|---|---|---|
| Frontmatter `digest` aanwezig | waarde uit frontmatter | waarde uit frontmatter `status` |
| Frontmatter `digest` absent of leeg | `0000` (sentinel) | `rot` (fallback) |

Wanneer `digest_header ≠ digest_berekend` is er sprake van *drift*: het bestand is gewijzigd na de laatste digest-registratie. Dit is een signaalgegeven voor `valideer-grondslag-consistentie` — geen oordeel.

**Deliverable bestand**: `{canon_pad}/grondslagen/grondslagen.json`

**VERPLICHT**: Het bestand wordt deterministisch gegenereerd door de runner (geen LLM, geen inferentie) en weggeschreven naar `grondslagen/grondslagen.json` in de canon-workspace. Een bestaand bestand wordt overschreven zonder bevestiging.

**Formaat-normering**:
- JSON, conform `grondslagen.schema.json`
- Geïndenteerd met 2 spaties, UTF-8 encoding, `ensure_ascii=False`

**Contractuele templatebinding**:

```yaml
template: ~
```

### Foutafhandeling

De Canon-curator:
- stopt wanneer de canon-workspace niet gevonden kan worden als sibling van de repo-root;
- stopt wanneer `grondslagen/` map niet bestaat in de canon-workspace;
- stopt wanneer `grondslagen.schema.json` niet aanwezig is in de canon-workspace root;
- logt een waarschuwing bij afzonderlijke bestanden die niet gelezen kunnen worden, maar stopt niet;
- logt een waarschuwing wanneer JSON-schema-validatie mislukt (bijv. `jsonschema` niet geïnstalleerd), maar schrijft het bestand toch;
- overschrijft een bestaand `grondslagen.json` zonder bevestiging.

---

## Werkwijze

### Stappen
1. **Bepaal canon-pad**: Resolve canon-workspace als `{repo_root.parent}/mandarin-canon`.
2. **Valideer paden**: Controleer aanwezigheid van `grondslagen/` map en `grondslagen.schema.json`.
3. **Scan grondslagen**: Doorloop alle `*.md` bestanden in `grondslagen/` recursief, gesorteerd op pad.
4. **Extraheer metadata per bestand**: Lees YAML frontmatter (versie, digest, status) en eerste `# H1` als titel.
5. **Leid scope af**: Op basis van relatief pad t.o.v. `grondslagen/` map.
6. **Leid type af**: Op basis van bestandsnaam-patronen.
7. **Bouw JSON**: Assembleer metadata-object en grondslagen-array.
8. **Valideer tegen schema**: Controleer output conform `grondslagen.schema.json` (soft fail bij ontbrekend `jsonschema` package).
9. **Schrijf output**: Sla `grondslagen.json` op in canon-workspace root.

### Kwaliteitsborging
- Alle entries hebben minimaal `bron`, `scope`, `type` en `titel`
- Scope wordt deterministisch afgeleid uit mapstructuur
- Type-afleiding dekt alle bekende bestandsnaampatronen in de huidige canon
- JSON is valide UTF-8 en valideert optioneel tegen schema

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0):
  - Principe 2 (Eenduidige Verantwoordelijkheid): Eén taak — publiceren van grondslagen-register
  - Principe 4 (Scheiding van Wat en Hoe): Contract specificeert input/output; runner implementeert scanning
  - Principe 7 (Transparante Verantwoording): Alle entries herleidbaar tot bestandspaden in canon
  - Principe 9 (Output-formaat Normering): JSON conform schema als primair artefact

- **doctrine-templategebruik.md** (v1.0.0):
  - Contractuele templatebinding expliciet opgenomen

**Canon-consultatie:**
- Geen LLM-consultatie; volledig programmatische uitvoering door runner.

**Transparantie-verplichtingen:**

Bij uitvoering logt de runner:
- ✓ Gelezen bestanden: alle `.md` bestanden in `grondslagen/` (pad per entry in console)
- ✓ Aangemaakte/gewijzigde bestanden: `grondslagen.json`
- ✓ Aantal verwerkte grondslagen en eventuele waarschuwingen

**Escalatie-paden:**
- STOP: bij ontbrekende canon-workspace of `grondslagen.schema.json`
- → workspace-steward: bij JSON-schema-validatiefouten (schema vereist mogelijk update)

---

## Metadata

**Intent-ID**: `aeo.01.canon-curator.publiceer-grondslagen`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 01 — Grondslagvorming  
**Classificatie**:
- Vormingsfase: Realisatie
- Betekeniseffect: Vastleggend
- Werking: Inhoudelijk
- Bronhouding: Canon-gebonden
