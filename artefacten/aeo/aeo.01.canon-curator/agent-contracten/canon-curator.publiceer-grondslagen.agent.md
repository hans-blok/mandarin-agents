---
agent: canon-curator
intent: publiceer-grondslagen
versie: 1.0.0
digest: 5278
status: vers
---
# Canon-curator — Publiceer Grondslagen

## Rolbeschrijving (korte samenvatting)

De Canon-curator scant de volledige `grondslagen/` map van de canon-workspace en genereert een machineleesbaar register als `grondslagen.json`, gevalideerd tegen `grondslagen.schema.json`. De uitvoering is volledig programmatisch — zonder LLM-consultatie.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `canon-curator.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**: geen — de intent werkt volledig automatisch op basis van de canon-structuur.

**Afgeleide informatie** (automatisch bepaald door runner):
- `canon_pad`: Pad naar mandarin-canon workspace (resolved als sibling van repo-root)
- `grondslagen_dir`: `{canon_pad}/grondslagen/`
- `schema_pad`: `{canon_pad}/grondslagen.schema.json`
- `output_pad`: `{canon_pad}/grondslagen.json`

### Output (wat komt eruit)

De Canon-curator levert:
- **`grondslagen.json`** in de canon-workspace root, conform `grondslagen.schema.json`:
  - `metadata`: publicatie_timestamp, publicatie_datum, versie, aantal_grondslagen, generator, canon_pad
  - `grondslagen`: gesorteerde array van entries, elk met:
    - `bron`: relatief pad t.o.v. canon-root (bijv. `grondslagen/.algemeen/doctrine-traceability.md`)
    - `scope`: `algemeen` | `{vs}` | `{vs}.{fase}` (afgeleid uit mapstructuur)
    - `type`: `doctrine` | `constitutie` | `beleid` | `normering` | `kaderdefinitie` | `concept`
    - `titel`: eerste `# H1` header uit het bestand (fallback: bestandsnaam, getiteld)
    - `versie`: uit YAML frontmatter van het bestand (leeg indien absent)
    - `digest`: 4-karakter MD5-digest uit YAML frontmatter (leeg indien absent)
    - `status`: `vers` | `muf` | `rot` uit YAML frontmatter (leeg indien absent)

**Scope-afleiding** (op basis van relatief pad t.o.v. `grondslagen/`):

| Pad-patroon | Scope |
|---|---|
| `.algemeen/...` | `algemeen` |
| `{vs}/...` (geen subfase-subfolder) | `{vs}` (bijv. `aeo`) |
| `{vs}/{vs}.{nr}.*/...` | `{vs}.{nr}` (bijv. `aeo.03`) |

**Type-afleiding** (op basis van bestandsnaam):

| Patroon | Type |
|---|---|
| `*doctrine*` | `doctrine` |
| `*constitutie*` | `constitutie` |
| `*beleid*` | `beleid` |
| `*normering*` of `*checklist*` | `normering` |
| `*kaderdefinitie*` | `kaderdefinitie` |
| overig | `concept` |

**Deliverable bestand**: `{canon_pad}/grondslagen.json`

**VERPLICHT**: Het bestand wordt programmatisch gegenereerd door de runner en weggeschreven naar de canon-workspace root. Een bestaand `grondslagen.json` wordt overschreven zonder bevestiging.

**Formaat-normering**:
- JSON, conform `grondslagen.schema.json`
- Geïndenteerd met 2 spaties, UTF-8 encoding, `ensure_ascii=False`

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
