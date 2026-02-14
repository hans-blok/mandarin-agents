---
agent: agent-smeder
intent: leg-vast-agent-charter
versie: 1.0.0
# Template voor agent charters. Generiek bruikbaar voor alle agents. De vastlegging van het intent hier is een bron voor het goed vastleggen van het agent-contract.
---

# Agent Charter - {agent-naam}

**Agent-ID**: `{value-stream-code}.{fase-nummer}.{agent-naam}`  
**Versie**: 1.0.0  
**Domein**: {hoofddomein van de agent}  
**Value Stream**: {value-stream-naam} (fase {fase-nummer} - {fase-naam})  
**Governance**: Volgt `beleid-workspace.md` (inclusief canon-raadpleging zoals daar vastgelegd) en `doctrine-agent-charter-normering.md`; zie prompt files voor uitvoeringsdetails en grondslagen-patronen.

## Classificatie-assen (vink aan wat van toepassing is)

- **Inhoudelijke as**
	- [ ] Beschrijvend
	- [ ] Structuurrealiserend
	- [ ] Structuur-normerend
	- [ ] Curator
	- [ ] Ecosysteem-normerend
- **Inzet-as**
	- [ ] Value-stream-specifiek
	- [ ] Value-stream-overstijgend
- **Vorm-as**
	- [ ] Vormvast
	- [ ] Representatieomvormend
- **Werkingsas**
	- [ ] Inhoudelijk
	- [ ] Conditioneel

## 1. Doel en bestaansreden

{Beschrijf in 2-4 zinnen waarom deze agent bestaat, welk probleem deze oplost en welke waarde deze toevoegt aan het ecosysteem. Focus op de WHY en het extern observeerbare effect.}

## 2. Capability boundary

{Formuleer in ÉÉN heldere zin wat de agent WEL doet, zonder wat de agent NIET doet. Deze zin moet de kern van de verantwoordelijkheid vastleggen conform Principe 2 (Eenduidige Verantwoordelijkheid) uit doctrine-agent-charter-normering.md.}

## 3. Rol en verantwoordelijkheid

{Beschrijf de rol van de agent binnen het ecosysteem in 2-3 paragrafen:
- Paragraaf 1: Wat is de primaire rol? Wat levert de agent aan het ecosysteem?
- Paragraaf 2: Opsomming van 3-5 concrete verantwoordelijkheden ("Deze agent zorgt ervoor dat...")
- Paragraaf 3: Wat bewaakt de agent specifiek? ("De {agent-naam} bewaakt daarbij...")}

## 4. Kerntaken

{Lijst van 3-7 kerntaken, elk met:
- Korte naam (2-5 woorden, actie-georiënteerd)
- Beschrijving (1-3 zinnen) wat de taak inhoudt
- Link naar intent indien van toepassing

Voorbeeld:
1. **Schrijven van Python-scripts**  
   Ontwerpt en implementeert scripts conform Code Complete standaarden. Past type hints, docstrings en PEP 8 style guide consequent toe.

2. **Reviewen van Python-code**  
   Beoordeelt bestaande code op kwaliteit, leesbaarheid en onderhoudbaarheid. Levert gestructureerde feedback met prioritering.
}

## 5. Grenzen

### Wat de {agent-naam} WEL doet
{Opsomming van 5-10 concrete dingen die binnen de capability boundary vallen. Gebruik actieve werkwoorden en wees specifiek.}

### Wat de {agent-naam} NIET doet
{Opsomming van 5-10 concrete dingen die NIET tot de verantwoordelijkheid behoren. Vermeld expliciet welke andere agents deze taken wel oppakken indien relevant. Dit expliciteert boundaries conform Principe 2.}

## 6. Werkwijze

0. **Canon consultatie (verplicht)**  
   Raadpleegt grondslagen conform `beleid-workspace.md` en logt consultatie via `scripts/bootstrap_canon_consult.py` voordat taken worden uitgevoerd. Deze architectuurkeuze (splitsing tussen proces en regels) zorgt ervoor dat governance centraal beheerd wordt. Specifieke grondslagen per intent staan in de bijbehorende prompt files. Bij handmatige uitvoering moet dit expliciet worden gedaan; bij runners/pipelines gebeurt dit automatisch. Consultaties worden gelogd in `audit/canon-consult.log.md`.

{Voor complexere agents: beschrijf werkwijze per intent-type. Voor simpelere agents: algemene werkwijze in stappen 1-9.

Standaard stappen-structuur:
1. Ontvangt opdracht met parameters
2. Valideert of opdracht binnen boundary valt
3. Verzamelt benodigde context (bestanden, metadata, bronnen)
4. Voert analyse of transformatie uit
5. Valideert output tegen kwaliteitscriteria
6. Documenteert beslissingen, aannames en afwijkingen
7. Schrijft output weg naar afgesproken locaties
8. Legt herkomstverantwoording vast
9. Stopt en escaleert wanneer buiten capability boundary of bij onoplosbare conflicten

Pas aan naar specifieke agent-needs maar behoud deze structuur waar mogelijk.}

## 7. Traceerbaarheid (contract <-> charter)

Dit charter is traceerbaar naar de volgende agent-contracten en prompt-metadata:

{Voor elke intent:}
- Intent: `{intent-kortschrift}`
	- Agent-contract: `artefacten/{vs}/{vs}.{fase}.{agent}/{agent}.{intent}.agent.md`
	- Prompt-metadata: `artefacten/{vs}/{vs}.{fase}.{agent}/mandarin.{agent}.{intent}.prompt.md`
	- Template: {`template-pad` indien van toepassing, anders `-`}

{Herhaal voor alle intents van deze agent}

## 8. Output-locaties

De {agent-naam} legt alle resultaten vast in de workspace als markdown-bestanden:

{Lijst van output-locaties met patronen:}
- `{pad}/{bestandsnaam-patroon}.md` — {beschrijving van wat hier komt}
- `{pad}/{bestandsnaam-patroon}.{ext}` — {beschrijving van wat hier komt}

{Alle output wordt standaard in Markdown (.md) gegenereerd conform Principe 9 (Output-formaat Normering), tenzij expliciet anders gevraagd. Voor inhoudelijke agents op vorm-as "Vormvast" is dit verplicht.}

## 9. Logging bij handmatige initialisatie

Wanneer de **{agent-naam}** handmatig wordt geïnitieerd (dus niet via een geautomatiseerde pipeline of runner), wordt een logbestand weggeschreven naar:

- **Locatie**: `audit/`
- **Bestandsnaam**: `{agent-naam}-{yyyymmdd-HHmm}.log.md`  
  _(agent-naam, datum (ISO 8601 zonder scheidingstekens), 24-uurs tijd)_

Het logbestand bevat ten minste:
1. **Gelezen bestanden**: Lijst met paden van alle bestanden die zijn gelezen tijdens de uitvoering
2. **Aangepaste bestanden**: Lijst met paden van alle bestanden die zijn gewijzigd
3. **Aangemaakte bestanden**: Lijst met paden van alle bestanden die nieuw zijn aangemaakt

Dit voldoet aan **Principe 7 (Transparante Verantwoording)** uit `doctrine-agent-charter-normering.md` v2.1.0 en geldt voor alle mandarin-agents bij handmatige initialisatie.

## 10. Herkomstverantwoording

- Dit charter volgt de structuur uit `artefacten/aeo/aeo.02.agent-smeder/agent-charter.template.md`
- Governance en doctrines: `beleid-workspace.md`, de mandarin-canon repository (constitutie, value streams, doctrine) en `doctrine-agent-charter-normering.md` v2.1.0
- Agent-contracten en prompt-metadata: zie sectie Traceerbaarheid
- Bron-locatie in deze workspace: `artefacten/{vs}.{fase}.{agent}/{agent}.charter.md` (per-agentfolder voor value stream {value-stream-naam}, fase {fase-nummer})
- {Publicatiekopie indien van toepassing: `charters-agents/{agent}.charter.md`}
- {Relevante externe referenties, standaarden of documentatie indien van toepassing}

## 11. Change Log

| Datum | Versie | Wijziging | Auteur |
|------|--------|-----------|--------|
| {YYYY-MM-DD} | 1.0.0 | Initiële charter {agent-naam} volgens agent-charter.template.md | Agent Smeder |

---

## INVULINSTRUCTIES VOOR AGENT-SMEDER

**Verwijder deze sectie na invulling**

### Verplichte placeholders (vervang {...})

**Identificatie:**
- `{agent-naam}`: Kebab-case agent-naam (bijv. "engineer-steward", "hypothese-vormer")
- `{value-stream-code}`: Drieletter code (aeo, sfw, aod, kvl, miv, fnd)
- `{fase-nummer}`: Twee-cijfer fase (01, 02, 03)
- `{value-stream-naam}`: Volledige naam (bijv. "Agent Enablement Orchestration")
- `{fase-naam}`: Volledige fase-naam (bijv. "Ecosysteeminrichting", "Grondslagvorming")

**Inhoudelijk:**
- `{hoofddomein}`: Primair domein van operatie (1-5 woorden)
- Alle tekstblokken tussen `{...}`: Vervang door concrete invulling

**Classificatie (uit boundary.md):**
- Vink correcte boxen aan bij Classificatie-assen
- Gebruik boundary.md als bron voor classificatie

### Structuur-beslisboom

**Altijd verplicht:**
1. ✅ Secties 1-11 (conform template structuur)
2. ✅ Classificatie-assen ingevuld
3. ✅ Canon consultatie workflow (sectie 6.0)
4. ✅ Traceerbaarheid naar alle intents (sectie 7)
5. ✅ Logging bij handmatige initialisatie (sectie 9)

**Optioneel/aanpasbaar:**
6. ⚠️ **Werkwijze per intent-type**: alleen bij grote verschillen tussen intents
7. ⚠️ **Publicatiekopie**: alleen indien agent publiek wordt gepubliceerd
8. ⚠️ **Bootstrap header**: NIET in template zelf, wordt door run_prompt.py toegevoegd

**Altijd weglaten:**
- ❌ Implementatie-details van hoe code werkt
- ❌ Specifieke technologie-keuzes (tenzij architectureel relevant)
- ❌ Tijdelijke of experimentele features

### Doctrine-naleving checklist (doctrine-agent-charter-normering.md v2.1.0)

**Principe 1 — Identiteit vóór Implementatie:**
- [ ] Capability boundary (sectie 2) start bij WAT, niet HOE
- [ ] Charter legitimeert extern observeerbare verwachtingen
- [ ] Ontwerprichting: identiteit → contract → charter → realisatie

**Principe 2 — Eenduidige Verantwoordelijkheid:**
- [ ] Capability boundary is in ÉÉN zin uit te leggen
- [ ] Geen overlap met andere agents (check via boundaries)
- [ ] Volledig: wat WEL én wat NIET (sectie 5)

**Principe 3 — Charter als Ecosysteem-Integrator:**
- [ ] Charter formaliseert identiteit
- [ ] Charter reguleert samenwerking (grenzen expliciet)
- [ ] Charter faciliteert evolutie (versioning, change log)

**Principe 4 — Scheiding van Wat en Hoe:**
- [ ] Capability boundary = WAT (extern observeerbaar gedrag)
- [ ] Werkwijze = HOE (stappen, maar niet implementatie)
- [ ] Geen vermenging van contract en implementatie

**Principe 6 — Ecosysteem-Cohesie:**
- [ ] Grenzen (sectie 5) vermelden afhankelijke agents
- [ ] Escalatiepaden expliciet in werkwijze
- [ ] Impact op samenwerking is doordacht

**Principe 7 — Transparante Verantwoording:**
- [ ] Logging-sectie (9) volledig ingevuld
- [ ] Herkomstverantwoording (10) traceert bronnen
- [ ] Canon consultatie (workflow 0) verplicht aanwezig

**Principe 9 — Output-formaat Normering:**
- [ ] Output-locaties (8) specificeren .md als default
- [ ] Voor inhoudelijke agents, vorm-as "Vormvast": Markdown verplicht
- [ ] Alternatieve formaten alleen op expliciete verzoek

### Kwaliteitsborging

**Voor oplevering:**
1. [ ] Alle `{placeholders}` vervangen
2. [ ] Doctrine-checklist volledig afgevinkt
3. [ ] Classificatie-assen ingevuld uit boundary
4. [ ] Minimaal 3 kerntaken gedefineerd
5. [ ] Grenzen-sectie bevat minimaal 5 WEL + 5 NIET items
6. [ ] Traceerbaarheid verwijst naar alle intents uit boundary
7. [ ] Output-locaties specificeren concrete paden
8. [ ] Bestandsnaam volgt conventie: `{agent}.charter.md`
9. [ ] Change log entry voor versie 1.0.0 aanwezig
10. [ ] Canon consultatie workflow expliciet opgenomen

**Common pitfalls (vermijd):**
- ⚠️ Capability boundary langer dan 2 regels (té complex, refactor agent)
- ⚠️ Geen expliciete "NIET doet" grenzen (Principe 2 violation)
- ⚠️ Implementatie-details in charter (Principe 4 violation)
- ⚠️ Output-formaat niet gespecificeerd (Principe 9 violation)
- ⚠️ Geen verwijzing naar doctrine-agent-charter-normering.md
- ⚠️ Logging-sectie ontbreekt (Principe 7 violation)
- ⚠️ Traceerbaarheid incomplete (intents uit boundary ontbreken)

### Naamgevingsconventie bestand

**Patroon:** `{agent-naam}.charter.md`

**Voorbeelden:**
- `engineer-steward.charter.md`
- `hypothese-vormer.charter.md`
- `agent-curator.charter.md`

**Locatie:** `artefacten/{vs}/{vs}.{fase}.{agent-naam}/{agent-naam}.charter.md`

### Versionering (Semantic Versioning)

- **MAJOR** (1.0.0 → 2.0.0): Fundamentele identiteitswijziging
  - Capability boundary fundamenteel veranderd
  - Intent verwijderd of hernoemd
  - Verantwoordelijkheid verschoven naar andere agent
  - **Vereist ecosysteem-brede herbeoordeling** (Principe 6)
  
- **MINOR** (1.0.0 → 1.1.0): Backward compatible toevoeging
  - Nieuwe intent toegevoegd
  - Kerntaak uitgebreid (bestaande blijven)
  - Werkwijze verduidelijkt/verfijnd
  
- **PATCH** (1.0.0 → 1.0.1): Cosmetische wijziging
  - Typo's in documentatie
  - Verduidelijking zonder gedragswijziging
  - Referentie-updates

**Start altijd bij:** `1.0.0` voor nieuwe agents

### Input-bronnen voor invulling

1. **Boundary** (`{agent}.boundary.md`):
   - Capability boundary (sectie 2)
   - Classificatie-assen
   - Voorgestelde intents (voor sectie 7 Traceerbaarheid)
   - In/Out of scope (voor sectie 5 Grenzen)

2. **Agent-contracten** (`.agent.md` bestanden):
   - Kerntaken afleiden uit contract-beschrijvingen
   - Output-locaties uit deliverables
   - Escalatiepaden uit foutafhandeling

3. **doctrine-agent-charter-normering.md**:
   - Principes voor checklist
   - Output-formaat normering
   - Transparantie-verplichtingen

4. **Beleid-workspace.md**:
   - Value stream metadata
   - Canon URL referentie
   - Grondslagen-patronen

### Workflow voor agent-smeder

1. Lees `{agent}.boundary.md` — extraheer classificatie en capability boundary
2. Lees alle `{agent}.*.agent.md` — extraheer kerntaken en outputs
3. Lees `doctrine-agent-charter-normering.md` — valideer principes
4. Vul template in van boven naar beneden
5. Controleer doctrine-checklist
6. Voer kwaliteitsborging uit
7. Sla op als `{agent}.charter.md` in per-agentfolder
8. Verwijder invulinstructies-sectie

---

**Template-versie**: 1.0.0  
**Laatste update**: 2026-02-14  
**Gebaseerd op**:
- `doctrine-agent-charter-normering.md` v2.1.0 (AEO.DOC.001)
- `agent-smeder.boundary.md` (aeo.02.agent-smeder)
- Bestaande charter voorbeelden: agent-curator, engineer-steward, constitutioneel-auteur

**Changelog:**
- v1.0.0 (2026-02-14): Initiële template met volledige invulinstructies, doctrine-checklist en beslisboom
