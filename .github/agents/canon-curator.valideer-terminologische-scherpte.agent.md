---
agent: canon-curator
intent: valideer-terminologische-scherpte
intent-id: aeo.01.canon-curator.01
versie: 1.0.0
digest: 2b9a
status: vers
---
# Canon-curator — Valideer Terminologische Scherpte

## Rolbeschrijving (korte samenvatting)

De Canon-curator toetst grondslag-artefacten op terminologische scherpte door te controleren of termen consistent worden gebruikt conform Artikel 5 en 6 van de constitutie, en levert bij elke bevinding een inhoudelijk verbetervoorstel.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `canon-curator.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- scope: Pad of selectie van te toetsen grondslag-artefacten binnen de canon (type: string of list[string], paden relatief ten opzichte van de canon-workspace root).

**Optionele parameters**:
- termenlijst: Expliciete lijst van termen om specifiek te controleren (type: list[string], default: alle termen die voorkomen in constitutionele definities en Artikel 5/6).
- ernst-filter: Minimaal ernst-niveau om te rapporteren (type: string, waarden: "kritiek", "hoog", "midden", "laag", default: alle niveaus).

**Afgeleide informatie** (automatisch gedetecteerd):
- value_stream_fase: `aeo.01` (vast voor canon-curator)
- canon_ref: Huidige git-hash van de canon-workspace

### Output (wat komt eruit)

De Canon-curator levert:
- **Evaluatierapport** met per bevinding:
  - Locatie: document, sectie en regelnummer waar terminologisch probleem optreedt
  - Gebruikte term: de term zoals aangetroffen in het document
  - Verwachte term: de canoniek vastgelegde term of definitie
  - Type probleem: ongedefinieerd begrip / semantische drift / inconsistent gebruik / schending Artikel 5 of 6
  - Ernst-classificatie: kritiek / hoog / midden / laag
  - Verbetervoorstel: concrete suggestie voor terminologische correctie
- **Samenvattingstabel** met totalen per probleemtype en ernst-categorie
- **Escalatieadvies** voor terminologische problemen die een constitutionele wijziging vereisen

**Deliverable bestand**: `audit/canon-curator-terminologie-{yyyymmdd-HHmm}.rapport.md`

**Formaat-normering**: 
- Default formaat: **Markdown** (.md), conform Principe 9
- Alternatieve formaten alleen op expliciete verzoek

**Contractuele templatebinding**:

```yaml
template: ~
```

### Foutafhandeling

De Canon-curator:
- stopt wanneer de opgegeven scope geen geldige paden bevat of de canon-workspace niet bereikbaar is;
- stopt wanneer geen enkel grondslag-artefact binnen de scope gevonden kan worden;
- stopt wanneer de constitutie (met name Artikel 5 en 6) niet gelezen kan worden als referentienorm;
- vraagt om verduidelijking wanneer een opgegeven term in de termenlijst niet voorkomt in canonieke definities;
- escaleert naar constitutioneel-auteur wanneer een terminologisch probleem wijst op een lacune in de constitutionele definities;
- wijzigt geen grondslag-artefacten; rapporteert uitsluitend bevindingen en verbetervoorstellen.

---

## Werkwijze

### Stappen
1. **Synchroniseer canon**: Haal de meest recente versie van de canon-workspace op via git pull.
2. **Bepaal referentiekader**: Laad constitutie (Artikel 5, 6 en terminologie-sectie) en eventuele aanvullende termenlijsten.
3. **Bepaal scope**: Identificeer alle grondslag-artefacten binnen de opgegeven scope.
4. **Toets terminologie**: Controleer op ongedefinieerde begrippen, semantische drift, inconsistent gebruik en schendingen van Artikel 5 (precisie) en Artikel 6 (taal en terminologie).
5. **Classificeer bevindingen**: Ken probleemtype en ernst-niveau toe aan elke bevinding.
6. **Formuleer verbetervoorstellen**: Geef bij elke bevinding een concrete terminologische correctie.
7. **Stel rapport samen**: Schrijf evaluatierapport met samenvattingstabel en escalatieadvies.

### Kwaliteitsborging
- Elke bevinding verwijst naar het specifieke constitutionele artikel dat geschonden wordt
- Verbetervoorstellen gebruiken uitsluitend canoniek vastgelegde termen
- Onderscheid tussen inconsistent gebruik (auteur-fout) en definitie-lacune (constitutioneel probleem) is expliciet
- Geen bevindingen over termen die bewust uit externe kaders zijn geleend (conform Artikel 6.2)

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract beschrijft extern observeerbaar gedrag
  - Principe 2 (Eenduidige Verantwoordelijkheid): Eén taak — terminologische toetsing van grondslag-artefacten
  - Principe 4 (Scheiding van Wat en Hoe): Contract specificeert input/output, niet implementatie
  - Principe 7 (Transparante Verantwoording): Alle bevindingen herleidbaar naar constitutionele artikelen
  - Principe 9 (Output-formaat Normering): Markdown als default

- **doctrine-templategebruik.md** (v1.0.0):
  - Contractuele templatebinding expliciet opgenomen

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream aeo
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door runner)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: alle grondslag-artefacten binnen scope, constitutie (Artikel 5/6), termenlijsten
- ✓ Aangemaakte bestanden: evaluatierapport
- ✓ Geen gewijzigde bestanden (canon-curator wijzigt niet)
- ✓ Aantal bevindingen per probleemtype en ernst-categorie

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → constitutioneel-auteur: voor definitie-lacunes die een constitutionele aanvulling vereisen
- → agent-curator: wanneer terminologisch probleem doorwerkt in agent-artefacten (buiten grondslag-scope)
- STOP: bij onbereikbare canon-workspace, onleesbare constitutie of lege scope

---

## Metadata

**Intent-ID**: `aeo.01.canon-curator.valideer-terminologische-scherpte`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 01 — Grondslagvorming  
**Classificatie**: 
- Vormingsfase: Toetsing
- Betekeniseffect: Evaluerend
- Werking: Inhoudelijk
- Bronhouding: Canon-gebonden
