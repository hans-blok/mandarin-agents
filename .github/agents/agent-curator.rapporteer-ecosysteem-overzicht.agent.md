---
agent: agent-curator
intent: rapporteer-ecosysteem-overzicht
intent-id: aeo.02.agent-curator.04
versie: 1.0.0
digest: b4b8
status: vers
---
# Agent-curator — Rapporteer Ecosysteem Overzicht

## Rolbeschrijving (korte samenvatting)

De agent-curator genereert een tabellarisch overzicht van alle agents in een value stream fase, met de status van hun artefacten en canonieke consistentie, zodat de human-in-the-loop de toestand van het ecosysteem in één oogopslag kan beoordelen.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `agent-curator.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)
**Verplichte parameters**: Geen — overzicht wordt altijd gegenereerd voor alle agents in de workspace.


**Afgeleide informatie** (geëxtraheerd uit artefacten-structuur):
- agent-lijst: Alle agent-mappen onder `artefacten/{vs}/{vs}.{fase}.*/`
- artefact-aanwezigheid: Per agent bepaald via mapstructuur

### Output (wat komt eruit)

De agent-curator levert:
- **Ecosysteem-overzicht document** met:
  - Samenvatting-tabel (totalen per statuscategorie)
  - Agents-tabel per value stream fase (✓/✗/⚠ per artefact-type)
  - Gesignaleerde aandachtspunten met prioritering
  - Ecosysteem-lacunes (capabilities zonder agent)
  - Aanbevolen vervolgactie voor human-in-the-loop
- Het overzicht vervangt het vorige overzicht (fixed filename, overschrijft bij elke run)

**Deliverable bestand**: `docs/agents-overzicht.md`

**Contractuele templatebinding**:
```yaml
output:
  - type: ecosysteem-overzicht
    herkomstpositie: initiërend
    template: templates/ecosysteem-overzicht.template.md
```

**VERPLICHT**: Het bestand MOET worden weggeschreven naar de workspace.

**Outputformaat**: Volgt `artefacten/aeo/aeo.02.agent-curator/templates/ecosysteem-overzicht.template.md`.

**Formaat-normering**:
- Default formaat: **Markdown** (.md), conform Principe 9
- Statuswaarden: ✓ (aanwezig + compliant) / ✗ (ontbreekt) / ⚠ (aanwezig, afwijking)
- Eindstatus per agent: COMPLIANT / DEELS-COMPLIANT / NON-COMPLIANT / — (niet getoetst)

### Foutafhandeling

De agent-curator:
- stopt wanneer value_stream_fase niet het format `{vs}.{fase}` heeft (tenzij "alles");
- stopt wanneer de `artefacten/` map niet leesbaar is of niet bestaat;
- neemt agents zonder artefacten-map op als "— (map niet gevonden)" in plaats van fout te geven;
- corrigeert geen artefacten — vermeldt status en signaleert uitsluitend;
- escaleert geen bevindingen automatisch — overzicht is ter informatie voor human-in-the-loop;
- STOP: wanneer `docs/` map niet bestaat of niet schrijfbaar is.

---

## Werkwijze

### Stappen
1. **Inventariseer agents**: Scan `artefacten/{vs}/{vs}.{fase}.*/` en extraheer agent-namen.
2. **Bepaal artefact-aanwezigheid**: Controleer per agent of boundary, charter, agent-contracten/, prompts/, tasks/ aanwezig zijn.
3. **Stel basisstatus vast**: ✓ indien aanwezig en basisvolledigheid ok, ✗ indien ontbreekt, ⚠ indien aanwezig maar eerder bevinding bekend.
4. **Afleiden eindstatus**: Op basis van statuspatroon per agent (zie template).
5. **Identificeer lacunes**: Capabilities die ontbreken in het ecosysteem op basis van verwachte coverage binnen de value stream.
6. **Formuleer aanbeveling**: Één zin gericht aan human-in-the-loop over meest urgente vervolgactie.
7. **Schrijf overzicht**: Genereer conform template en schrijf weg naar `docs/agents-overzicht.md`.

### Kwaliteitsborging
- Overzicht bevat YAML frontmatter met agent, intent, value_stream_fase, datum, canon_ref
- Samenvatting-tabel klopt met de individuele agent-regels
- Eindigt met concrete "Volgende aanbevolen actie" gericht aan human-in-the-loop
- Geen oordelen over artefact-inhoud opgenomen (alleen aanwezigheid/volledigheid)

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 7 (Transparante Verantwoording): Overzicht maakt ecosysteemstatus observeerbaar
  - Principe 9 (Output-formaat Normering): Markdown als default
- **doctrine-templategebruik.md** (v1.0.0):
  - contract legt expliciet vast welk template voor dit overzicht geldt
  - prompt-YAML moet dezelfde templatekeuze spiegelen

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen
- Bootstrap via `scripts/bootstrap_canon_consult.py`

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: mapstructuur onder `artefacten/`
- ✓ Aangemaakte/overschreven bestanden: `docs/agents-overzicht.md`
- ✓ Geen gewijzigde artefacten (curator leest alleen, corrigeert niet)
- ✓ Aantal agents in scope vermeld

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → human-in-the-loop: overzicht is primair bedoeld als stuurinformatie voor mens
- → agent-curator zelf (`valideer-agent-consistentie`): voor gedetailleerd rapport per agent
- STOP: wanneer `artefacten/` of `docs/` map niet beschikbaar is

---

## Metadata

**Intent-ID**: `aeo.02.agent-curator.rapporteer-ecosysteem-overzicht`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 02 — Ecosysteeminrichting  
**Classificatie**:
- Betekeniseffect: Evaluerend
- Interventieniveau: Ecosysteem
- Werking: Inhoudelijk
- Bron-houding: Canon-gebonden
