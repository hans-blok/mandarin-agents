---
# IDENTIFICATIE
template-id: "fnd-01-001"
template-naam: ecosysteem-coordinator-genereer-instructies

# RELATIES
artefact-type-id: execution
agent-id: fnd.01.ecosysteem-coordinator
intent: genereer-instructies

# META-DATA
versie: 0.1.0
status: vers
digest: tbd
---
---
execution_id: {4-char-hash}
execution_digest: {12-char-sha256}
timestamp: {ISO-8601}
agent: {agent}
intent: {intent}
value_stream_fase: {vs.fase}
canon_ref: {commit-sha}
bronhouding: {bronhouding-type}
modus: {manual|runner|pipeline}
---

# Instructie

Voer de intent `{intent}` uit voor agent `{agent}`.

{Optionele toelichting op de opdracht — context, aanleiding of specifieke nadruk.}

---

# Parameters

| Parameter | Waarde |
|-----------|--------|
| agent | `{agent}` |
| intent | `{intent}` |
| execution_file | `{execution_file}` |
| method | `{method}` |

{Aanvullende params als key=value-tabel, indien opgegeven:}

| Sleutel | Waarde |
|---------|--------|
| {key} | {value} |

---

# Bronpakket

Overzicht van de bronnen die zijn samengesteld voor de uitvoering van intent `{intent}` door agent `{agent}`.

## Werkbronnen

| Bron | Opname |
|------|--------|
| `{werkbron-bestandsnaam}` | opgenomen |

## Referentiebronnen

| Bron | Opname |
|------|--------|
| `{template-pad}` | opgenomen |

## Kaderbronnen

| Bron | Bronrol | Opname | Opnamevorm |
|------|---------|--------|------------|
| `{agent}.charter.md` | charter | opgenomen | volledig |
| `{doctrine-naam}` | doctrine | opgenomen | bronselectieprofiel `{sleutel}` |
| `{doctrine-naam}` | doctrine | uitgesloten | — |

Canon-referentie: `{commit-sha}`

---

# Template

> Je gebruikt dit template voor je output.

{Volledige inhoud van het template dat hoort bij de intent `{intent}`.
Pad: `{template-pad}`}

{template-inhoud}

---

# Werkbron

{De volledige werkbron die de agent nodig heeft voor uitvoering van `{intent}`.
Bijvoorbeeld: voor `agent-ontwerper.definieer-contract` is dit de `agent-boundary`.
Voor `{agent}.{intent}` is dit: `{werkbron-omschrijving}`.}

## {werkbron-bestandsnaam}

{Volledige inhoud van de werkbron.}

---

# Charter

{Volledige inhoud van het charter van agent `{agent}`.}

{charter-inhoud}

---

# Doctrines

Overzicht van doctrines die van toepassing zijn op intent `{intent}` van agent `{agent}`.
Toegepast bronselectieprofiel: `{sleutel}` (uit `bronselectiebeleid.json`).

## Opgenomen doctrines ({n})

{Voor elke opgenomen doctrine:}

### {doctrine-naam} (`{doctrine-pad}`)

{doctrine-inhoud}

## Uitgesloten doctrines ({m})

| Doctrine | Reden van uitsluiting |
|----------|-----------------------|
| `{doctrine-pad}` | {reden} |

---

# Instructies Hand Off

Na uitvoering van intent `{intent}`:

1. **Schrijf output weg** naar de afgesproken locatie conform het contract van `{agent}.{intent}`.
2. **Log de executie** — append naar `audit/agent-instructions.log.md` met:
   - `execution_id`: `{4-char-hash}`
   - `execution_digest`: `{12-char-sha256}`
   - Agent en intent
   - Tijdstip en methode
3. **Escaleer indien nodig**:
   - → `agent-engineer` indien een prompt- of runner-bestand ontbreekt
   - → `capability-architect` indien het charter ontbreekt
   - STOP bij onoplosbaar conflict of ontbrekende input buiten de capability boundary
4. **Sluit de executie af** — geen verdere actie nodig tenzij het contract een expliciete handoff-stap definieert.
