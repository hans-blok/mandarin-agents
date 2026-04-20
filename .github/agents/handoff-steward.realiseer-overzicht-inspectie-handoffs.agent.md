---
agent: handoff-steward
intent: realiseer-overzicht-inspectie-handoffs
intent-id: aeo.03.handoff-steward.03
versie: 1.0.0
---
# Handoff-steward — Realiseer Overzicht Inspectie Handoffs

## Rolbeschrijving (korte samenvatting)

De Handoff-steward levert op verzoek een leesbaar overzicht van de staat van het handoff-register: open handoffs, gesloten handoffs, registerintegriteit en eventuele afwijkingen ten opzichte van de verwachte toestand.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `handoff-steward.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- `handoff_register`: Pad naar het handoff-register (type: string, bestandspad).

**Optionele parameters**:
- `filter_status`: Filtert het overzicht op status (type: enum: `open | gesloten | alle`, default: `alle`).
- `filter_maand`: Filtert het overzicht op kalendermaand in formaat `JJMM` (type: string, bijv. `2604`; default: alle maanden).
- `output_bestand`: Pad naar het bestand waar het overzicht wordt geschreven (type: string, bestandspad; default: geen — overzicht wordt uitsluitend in de prompt-respons weergegeven). Wanneer opgegeven, wordt het overzicht ook als bestand weggeschreven.

**Afgeleide informatie** (geëxtraheerd uit het handoff-register):
- Totaalaantal entries, aantal open, aantal gesloten
- Per entry: `handoff_id`, `status`, `execution_id`, `ontvangende_agent`, `aangemaakt`, `gesloten` (indien van toepassing)
- Afwijkingen: handoff-bestanden vermeld in het register maar niet aanwezig op schijf; of handoff-bestanden aanwezig op schijf maar niet in het register

### Output (wat komt eruit)

De Handoff-steward levert:
- **Inspectie-overzicht** van het handoff-register als leesbare samenvatting:
  - Registerstatus: totaal / open / gesloten / afwijkingen
  - Tabel van matching entries (na filters)
  - Lijst van gedetecteerde afwijkingen (registerentry zonder bestand, of bestand zonder entry)
  - Integriteitscontrole: geen dubbele volgnummers per maand, monotone nummering

**Deliverable** (optioneel): `{output_bestand}` (Markdown, indien `output_bestand` is opgegeven)

**VERPLICHT bij afwijkingen**: Afwijkingen worden expliciet gerapporteerd en nooit stilzwijgend gecorrigeerd. Correctie is buiten scope van deze intent.

**Outputformaat** (overzicht als Markdown):
```markdown
# Overzicht Handoff-register — inspectie 2026-04-06

## Registerstatus
- Totaal entries: 3
- Open: 2
- Gesloten: 1
- Afwijkingen: 0

## Entries

| Handoff-ID      | Status   | Execution-ID | Ontvangende agent | Aangemaakt   | Gesloten     |
|-----------------|----------|--------------|-------------------|--------------|--------------|
| hf-2604.0001    | gesloten | 8ff6         | agent-ontwerper   | 2026-04-06   | 2026-04-06   |
| hf-2604.0002    | open     | 8aec         | agent-engineer    | 2026-04-06   | —            |

## Afwijkingen
Geen afwijkingen gedetecteerd.
```

**Formaat-normering**:
- Default: Markdown in de prompt-respons
- Optioneel als bestand weggeschreven naar `output_bestand` (.md), conform Principe 9

**Contractuele templatebinding**:

```yaml
output:
  - type: inspectie-overzicht
    herkomstpositie: initiërend
    template: ~
```

- `template: ~` is expliciet omdat de outputstructuur volledig in dit contract is gespecificeerd en geen afzonderlijk templatebestand vereist

### Foutafhandeling

De Handoff-steward:
- stopt wanneer `handoff_register` niet bestaat of niet leesbaar is;
- stopt wanneer het registerformaat corrupt is en de entries niet kunnen worden gelezen;
- rapporteert expliciet wanneer `filter_maand` een waarde heeft die geen entries oplevert (leeg overzicht, geen fout);
- rapporteert gedetecteerde afwijkingen zonder ze te corrigeren — correctie vereist aparte actie;
- escaleert naar `agent-curator` wanneer afwijkingen systemisch zijn of niet door normaal gebruik verklaard kunnen worden;
- STOP: bij onleesbaar register — een leeg overzicht of onjuist formaat mag niet worden gepresenteerd als een geldig register.

**Niet in scope voor deze intent**:
- Aanmaken, wijzigen of verwijderen van registerentries of handoff-bestanden.
- Beslissingen over hoe afwijkingen hersteld moeten worden.
- Volledige audit-rapportage over de inhoud van handoff-bestanden — alleen de registerstand wordt geïnspecteerd.

---

## Werkwijze

### Stappen
1. **Valideer input**: Controleer aanwezigheid en leesbaarheid van `handoff_register`.
2. **Lees register**: Parseer alle entries; bepaal totaalaantallen.
3. **Pas filters toe**: Filter op `filter_status` en `filter_maand` indien opgegeven.
4. **Integriteitscontrole**:
   - Controleer op dubbele volgnummers per maand.
   - Controleer of handoff-bestanden vermeld in het register ook op schijf bestaan.
   - Controleer of handoff-bestanden op het verwachte schijfpad niet in het register voorkomen.
5. **Stel overzicht samen**: Genereer Markdown-tabel en afwijkings-sectie.
6. **Schrijf bestand** (optioneel): Schrijf overzicht weg indien `output_bestand` is opgegeven.

### Kwaliteitsborging
- Overzicht bevat Registerstatus-sectie met minimaal 4 tellers (totaal, open, gesloten, afwijkingen)
- Tabel bevat minimaal kolommen: Handoff-ID, Status, Execution-ID, Ontvangende agent, Aangemaakt
- Afwijkingen zijn expliciet benoemd (ook wanneer er geen zijn: "Geen afwijkingen gedetecteerd")
- Register en schijf zijn kruiselings gecontroleerd

---

## Governance

**Doctrine-naleving:**
- **doctrine-handoff.md** (v1.0.0):
  - §2.3 Generatie volgnummer: inspectie detecteert afwijkingen in monotone nummering
  - §7.1 Geldigheidsvereisten: overzicht rapporteert ontbrekende of ongeldige entries
  - §7.3 Wijzigingsbeheer: deze intent schrijft niets terug naar het register
- **doctrine-agent-charter-normering.md** (v2.4.0):
  - Principe 7 (Transparante Verantwoording): afwijkingen worden expliciet gerapporteerd
  - Principe 9 (Output-formaat Normering): Markdown als default
- **doctrine-templategebruik.md** (v1.0.0):
  - Output-template is expliciet vastgelegd als `~` in de contractuele templatebinding
  - Prompt-metadata spiegelt de templatekeuze uit het contract

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream aeo
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door runner)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: `handoff_register`
- ✓ Aangemaakte bestanden: `output_bestand` (indien opgegeven)
- ✓ Geen gewijzigde bestanden
- ✓ Aantal gedetecteerde afwijkingen

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → `agent-curator`: bij systemische afwijkingen in het handoff-register die niet door normaal gebruik verklaard kunnen worden
- STOP: bij onleesbaar register

---

## Metadata

**Intent-ID**: `aeo.03.handoff-steward.realiseer-overzicht-inspectie-handoffs`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 03 — Operationele overdracht en ketenbeheer  
**Classificatie**:
- Betekeniseffect: Vastleggend
- Vormingsfase: Realisatie
- Werking: Inhoudelijk
- Bronhouding: Canon-gebonden
