---
agent: agent-smeder
intent: leg-vast-agent-contract
versie: 1.0.0
# Template voor agent charters. Generiek bruikbaar voor alle agents. De vastlegging van het intent hier is een bron voor het goed vastleggen van het agent-contract.
---

# {agent-naam} — {intent-naam}

## Rolbeschrijving (korte samenvatting)

{Beschrijf in 1-2 zinnen wat deze agent doet in de context van deze specifieke intent. Focus op de unieke verantwoordelijkheid binnen de capability boundary.}

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `{agent-naam}.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- {parameter-naam}: {beschrijving van parameter} (type: {datatype}, {constraints/format}).
- {parameter-naam}: {beschrijving van parameter} (type: {datatype}, {constraints/format}).

**Optionele parameters**:
- {parameter-naam}: {beschrijving van parameter} (type: {datatype}, default: {standaardwaarde}).
- {parameter-naam}: {beschrijving van parameter} (type: {datatype}).

### Output (wat komt eruit)

De {agent-naam} levert:
- {primair artefact}: {beschrijving van hoofdoutput}
  - {eigenschap 1}: {toelichting}
  - {eigenschap 2}: {toelichting}
- {secundair artefact indien van toepassing}: {beschrijving}
- {metadata of rapportage indien van toepassing}: {beschrijving}

**Deliverable bestand**: `{pad-naar-output-bestand}/{bestandsnaam-patroon}.md`

{Indien van toepassing: beschrijf outputformaat met voorbeeld structuur}

**Outputformaat** (standaard structuur):
```markdown
# {Voorbeeld van output structuur}

{Toon hier de verwachte structuur van het geleverde artefact}
```

**Formaat-normering**: 
{Voor inhoudelijke agents met vorm-as "Vormvast":}
- Default formaat: **Markdown** (.md), tenzij expliciet anders gevraagd
- Alternatieve formaten (YAML, JSON, etc.) alleen op expliciete verzoek in prompt
- Formatwijziging wordt gedocumenteerd in output

{Conform Principe 9 van doctrine-agent-charter-normering.md}

### Foutafhandeling

De {agent-naam}:
- stopt wanneer {situatie waarin agent niet kan/mag verder};
- stopt wanneer {situatie die buiten capability boundary valt};
- vraagt om verduidelijking wanneer {onduidelijke of onvolledige input};
- escaleert naar {andere-agent} voor {specifieke situaties buiten scope};
- {escalatie-pad 2 indien van toepassing}.

{Beschrijf expliciet wat NIET gebeurt binnen deze intent scope.}

---

## Werkwijze

{Optionele sectie - alleen indien nodig voor complexere intents}

### Stappen
1. {stap 1}: {toelichting}
2. {stap 2}: {toelichting}
3. {stap 3}: {toelichting}

### Kwaliteitsborging
- {check 1}: {criterium}
- {check 2}: {criterium}

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract is extern observeerbaar
  - Principe 2 (Eenduidige Verantwoordelijkheid): Eén heldere taak binnen boundary
  - Principe 7 (Transparante Verantwoording): Traceerbaarheid van beslissingen
  - {Principe 9 (Output-formaat Normering): alleen voor inhoudelijke agents, vorm-as "Vormvast"}
- {Aanvullende doctrine-referenties indien relevant voor deze intent}

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream {value-stream-code}
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Alle gelezen bestanden (met pad en tijdstip)
- ✓ Alle aangemaakte bestanden (met pad en tijdstip)
- ✓ Alle gewijzigde bestanden (met pad en wijzigingsbeschrijving)
- {✓ Intent-specifieke audit-requirements indien van toepassing}

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → {andere-agent-1}: voor {specifieke situatie buiten scope}
- → {andere-agent-2}: voor {specifieke situatie buiten scope}
- STOP: bij {situaties waarin agent definitief stopt zonder escalatie}

---

## Metadata

**Intent-ID**: `{value-stream-code}.{fase-nummer}.{agent-naam}.{intent-kortschrift}`  
**Versie**: 1.0.0  
**Value Stream**: {value-stream-naam} ({value-stream-code})  
**Fase**: {fase-nummer} — {fase-naam}  
**Classificatie**: 
- Inhoudelijk: {ecosysteem-normerend/structuur-normerend/structuurrealiserend/beschrijvend/curator}
- Inzet: {value-stream-specifiek/value-stream-overstijgend}
- Vorm: {vormvast/representatieomvormend}
- Werking: {inhoudelijk/conditioneel}

---

---

## INVULINSTRUCTIES VOOR AGENT-SMEDER

**Verwijder deze sectie na invulling**

### Verplichte placeholders

**Basale identificatie:**
- `{agent-naam}`: Korte kebab-case naam (bijv. "engineer-steward", "hypothese-vormer")
- `{intent-naam}`: Beschrijvende titel (bijv. "Schrijf Script", "Formuleer Hypothese")
- `{intent-kortschrift}`: Kebab-case intent ID (bijv. "schrijf-script", "formuleer-hypothese")

**Locatie-specifiek:**
- `{pad-naar-charter}`: Relatief pad (bijv. `artefacten/fnd/fnd.01.engineer-steward/engineer-steward.charter.md`)
- `{value-stream-code}`: Drieletter code (aeo, sfw, aod, kvl, miv, fnd)
- `{fase-nummer}`: Twee-cijfer fase (01, 02, 03)
- `{value-stream-naam}`: Volledige naam (bijv. "Agent Enablement Orchestration")
- `{fase-naam}`: Volledige fase-naam (bijv. "Ecosysteeminrichting")

**Contract-specifiek:**
- `{parameter-naam}`: Naam van input/output parameter
- `{datatype}`: Type (string, list, dict, Path, etc.)
- `{constraints/format}`: Beperkingen (bijv. "1-3 zinnen", "max 5 items")
- `{pad-naar-output-bestand}`: Uitgangsfolder voor deliverables
- `{bestandsnaam-patroon}`: Naamgevingsconventie output

**Classificatie (uit boundary):**
- Inhoudelijke as: ecosysteem-normerend / structuur-normerend / structuurrealiserend / beschrijvend / curator
- Inzet-as: value-stream-specifiek / value-stream-overstijgend
- Vorm-as: vormvast / representatieomvormend
- Werkingsas: inhoudelijk / conditioneel

### Structuur-beslisboom

**Minimaal vereist:**
1. ✅ Rolbeschrijving (altijd)
2. ✅ Charter-referentie (altijd, **VERPLICHT**)
3. ✅ Input contract (altijd)
4. ✅ Output contract (altijd)
5. ✅ Foutafhandeling (altijd)

**Optioneel toevoegen:**
6. ⚠️ **Werkwijze**: alleen bij multi-step process (>3 stappen)
7. ⚠️ **Outputformaat voorbeeld**: bij gestructureerde outputs (tabellen, YAML, specifieke secties)
8. ⚠️ **Formaat-normering**: alleen voor inhoudelijke agents op vorm-as "Vormvast"

**Altijd weglaten:**
- ❌ Implementatie-details (hoe code werkt)
- ❌ Interne datastructuren
- ❌ Technische constraints die niet extern observeerbaar zijn

### Doctrine-naleving checklist (doctrine-agent-charter-normering.md v2.1.0)

Controleer vóór oplevering:

**Principe 1 — Identiteit vóór Implementatie:**
- [ ] Contract beschrijft extern observeerbaar gedrag (geen interne details)
- [ ] Rolbeschrijving start bij **wat** de agent WEL/NIET doet

**Principe 2 — Eenduidige Verantwoordelijkheid:**
- [ ] Intent heeft precies **één** verantwoordelijkheid (in 1 zin uit te leggen)
- [ ] Geen overlap met andere intents van dezelfde agent

**Principe 4 — Scheiding van Wat en Hoe:**
- [ ] Input/output = **wat** (contract)
- [ ] Foutafhandeling = **wanneer niet** (grenzen)
- [ ] Werkwijze (optioneel) = **hoe** (stappen, maar niet implementatie)

**Principe 7 — Transparante Verantwoording:**
- [ ] Governance-sectie bevat logging-verplichtingen
- [ ] Traceerbaarheid: gelezen/aangemaakte/gewijzigde bestanden

**Principe 9 — Output-formaat Normering (alleen inhoudelijke agents, vorm-as "Vormvast"):**
- [ ] Default formaat = **Markdown** (.md)
- [ ] Alternatieve formaten alleen op expliciete verzoek
- [ ] Formatwijziging = gedocumenteerd in output

### Naamgevingsconventie bestand

**Patroon:** `{agent-naam}.{intent-kortschrift}.agent.md`

**Voorbeelden:**
- `engineer-steward.schrijf-script.agent.md`
- `hypothese-vormer.formuleer-hypothese.agent.md`
- `agent-curator.bepaal-agent-boundary.agent.md`

**Locatie:** `artefacten/{vs}/{vs}.{fase}.{agent-naam}/{agent-naam}.{intent}.agent.md`

### Versionering (Semantic Versioning)

- **MAJOR** (1.0.0 → 2.0.0): Breaking change in contract
  - Input-parameter verwijderd of hernoemd
  - Output-formaat fundamenteel gewijzigd
  - Foutafhandeling-gedrag veranderd (wat eerst werkte, werkt nu niet meer)
  
- **MINOR** (1.0.0 → 1.1.0): Backward compatible toevoeging
  - Nieuwe optionele parameter toegevoegd
  - Extra output-velden toegevoegd (bestaande blijven)
  - Uitgebreidere foutafhandeling
  
- **PATCH** (1.0.0 → 1.0.1): Bugfix of verduidelijking
  - Typo's in documentatie
  - Verduidelijking van bestaande specs (geen gedragswijziging)
  - Voorbeelden toegevoegd

**Start altijd bij:** `1.0.0` voor nieuwe intents

### Kwaliteitsborging

**Voor oplevering:**
1. [ ] Alle `{placeholders}` vervangen
2. [ ] Doctrine-checklist volledig afgevinkt
3. [ ] Minimaal 2 verplichte parameters gedefineerd
4. [ ] Minimaal 1 primair artefact beschreven
5. [ ] Foutafhandeling expliciteert minimaal 3 stop-condities
6. [ ] Charter-referentie is **VERPLICHT** aanwezig
7. [ ] Bestandsnaam volgt conventie: `{agent}.{intent}.agent.md`

**Common pitfalls (vermijd):**
- ⚠️ Te veel parameters (>7 = waarschuwing, >10 = refactor)
- ⚠️ Vage parameter-beschrijvingen ("context", "data", "input")
- ⚠️ Output zonder concreet bestandspad
- ⚠️ Foutafhandeling zonder escalatie-pad
- ⚠️ Geen expliciete stop-condities
- ⚠️ Charter-referentie vergeten (DOCTRINE VIOLATION!)

---

**Template-versie**: 1.1.0  
**Laatste update**: 2026-02-14  
**Gebaseerd op**:
- `doctrine-agent-charter-normering.md` v2.1.0 (AEO.DOC.001)
- `agent-smeder.boundary.md` (aeo.02.agent-smeder)
- Bestaande agent-contract voorbeelden (ecosystem-proven patterns)

**Changelog:**
- v1.1.0 (2026-02-14): Uitgebreide invulinstructies voor agent-smeder, doctrine-checklist, beslisboom
- v1.0.0 (2026-02-14): Initiële template met basis structuur
