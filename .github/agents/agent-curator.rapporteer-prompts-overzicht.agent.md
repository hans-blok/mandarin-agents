---
agent: agent-curator
intent: rapporteer-prompts-overzicht
versie: 1.0.0
---

# Agent-curator — Rapporteer Prompts Overzicht

## Rolbeschrijving (korte samenvatting)

De agent-curator genereert een gestructureerd overzicht per agent uit alle aanwezige prompt-contracten, inclusief hun invoerparameters (en of ze verplicht/optioneel zijn), definities en beschrijvingen, zodat we een overkoepelend "catalogus"-inzicht krijgen in de interactie met agents.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.
**Conventie**: Charter bevindt zich in `agent-curator.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)
**Verplichte parameters**: Geen — overzicht wordt altijd gegenereerd voor alle beschikbare prompt-contracten in de workspace.

**Afgeleide informatie** (geëxtraheerd uit artefacten-structuur):
- agent-lijst: Alle agent-mappen onder `artefacten/{vs}/{vs}.{fase}.*/`
- agent-contracten: Alle bestanden die in `agent-contracten/` mappen staan.

### Output (wat komt eruit)

De agent-curator levert:
- **Ecosysteem Prompt Contracten overzicht-document** met per agent:
  - De beschrijving van het contract (prompt).
  - Lijsten met parameters onderverdeeld in Invoer en/of Optioneel.
  - Eventuele definities of output regels.
- Bevat documentversie en overzicht generatie datum.

**Deliverable bestand**: `docs/agents-prompts-overzicht.md`

**VERPLICHT**: Het bestand MOET worden weggeschreven naar de workspace.

**Outputformaat**: Volgt `artefacten/aeo/aeo.02.agent-curator/templates/ecosysteem-agent-prompt-contracten.template.md`.

**Formaat-normering**:
- Default formaat: **Markdown** (.md), conform Principe 9
- Inhoud iteratief geproduceerd over *alle* actieve value streams
- Elk agent parameter contract heeft geneste structuur conform de template.

### Foutafhandeling

De agent-curator:
- stopt wanneer de `artefacten/` map niet leesbaar is of niet bestaat;
- negeert agents zonder `.agent.md` bestanden stilletjes in the rapportage;
- corrigeert geen parameters of fouten in het contract — parseert domweg textueel;
- escaleert geen bevindingen automatisch — overzicht is ter informatie voor human-in-the-loop;
- STOP: wanneer `docs/` map niet bestaat of niet schrijfbaar is.

---

## Werkwijze

### Stappen
1. **Inventariseer agents**: Scan `artefacten/{vs}/{vs}.{fase}.*/` en extraheer agent-namen.
2. **Scan contracten**: Zoek naar `*.agent.md` in de map `agent-contracten/` per agent.
3. **Parse details**: Lees intent beschrijving en haal input_parameters op.
4. **Bouw structuur**: Loop over het `ecosysteem-agent-prompt-contracten.template.md` document per parameter die geparsed kon worden.
5. **Schrijf overzicht**: Genereer totale markdown opmaak en schrijf weg naar `docs/agents-prompts-overzicht.md`.

### Kwaliteitsborging
- Overzicht bevat per contract een duidelijke weergave van verplichte en optionele parameters
- Output bestand volgt template nesting strict.

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 7 (Transparante Verantwoording): Overzicht maakt parameters transparant
  - Principe 9 (Output-formaat Normering): Markdown als default

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen
- Bootstrap via `scripts/bootstrap_canon_consult.py`

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: mapstructuur onder `artefacten/` en specifieke `.agent.md` files
- ✓ Aangemaakte/overschreven bestanden: `docs/agents-prompts-overzicht.md`
- ✓ Geen gewijzigde artefacten (curator leest alleen contracten)

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → human-in-the-loop: overzicht catalogus ter observatie.
- STOP: wanneer `artefacten/` of `docs/` map niet beschikbaar is

---

## Metadata

**Intent-ID**: `aeo.02.agent-curator.rapporteer-prompts-overzicht`
**Versie**: 1.0.0
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)
**Fase**: 02 — Ecosysteeminrichting
**Classificatie**:
- Betekeniseffect: Evaluerend
- Interventieniveau: Ecosysteem
- Werking: Inhoudelijk
- Bron-houding: Canon-gebonden