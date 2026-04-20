---
agent: handoff-steward
intent: realiseer-handoff-sluiting
intent-id: aeo.03.handoff-steward.02
versie: 1.0.0
---
# Handoff-steward — Realiseer Handoff-sluiting

## Rolbeschrijving (korte samenvatting)

De Handoff-steward markeert een bestaande, open handoff als afgesloten in het handoff-register nadat de ontvangende agent ontvangst heeft bevestigd, en legt de sluitingsdatum en eventuele ontvangstbevestiging vast.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `handoff-steward.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- `handoff_id`: De handoff-identificatie van de te sluiten handoff (type: string, formaat `hf-JJMM.NNNN`, bijv. `hf-2604.0001`). Moet voorkomen in het handoff-register met status `open`.
- `handoff_register`: Pad naar het handoff-register dat wordt bijgewerkt (type: string, bestandspad).

**Optionele parameters**:
- `ontvangstbevestiging`: Beschrijving of referentie van de bevestiging van ontvangst door de ontvangende agent (type: string, default: leeg). Wordt opgenomen als annotatie bij de registerEntry.
- `sluitings_datum`: Datum van sluiting (type: string, formaat `JJJJ-MM-DD`, default: huidige datum). Gebruik standaard huidige datum tenzij expliciet anders opgegeven.

**Afgeleide informatie** (geëxtraheerd uit het handoff-register op basis van `handoff_id`):
- `handoff_bestand`: pad naar het bijbehorende handoff-bestand, voor verificatie dat het bestand bestaat.
- `execution_id`: referentie-execution voor audit-doeleinden.
- `ontvangende_agent`: ter verificatie dat de sluiting door de juiste agent is geïnitieerd.

### Output (wat komt eruit)

De Handoff-steward levert:
- **Bijgewerkt handoff-register**: de registerentry voor `handoff_id` wordt bijgewerkt van status `open` naar `gesloten`, met:
  - `sluitings_datum`
  - `ontvangstbevestiging` (indien opgegeven)

**Registerlocatie**: opgegeven pad in `handoff_register`-parameter

**VERPLICHT**: Het handoff-register MOET worden bijgewerkt. Het handoff-bestand zelf wordt NIET gewijzigd — het is na uitgifte onveranderlijk conform doctrine-handoff.md §7.3.

**Registerformaat** (voorbeeld na sluiting):
```yaml
hf-2604.0001:
  status: gesloten
  execution_id: 8ff6
  ontvangende_agent: agent-ontwerper
  aangemaakt: 2026-04-06
  gesloten: 2026-04-06
  ontvangstbevestiging: "Bevestigd via execution 9df1"
```

**Formaat-normering**:
- Het handoff-register is een YAML-bestand; updates volgen het bestaande registerformaat
- Geen overschrijving van eerder vastgelegde registergegevens anders dan statuswijziging en toevoeging van sluitingsvelden

**Contractuele templatebinding**:

```yaml
output:
  - type: register-update
    herkomstpositie: muterend
    template: ~
```

- `template: ~` is expliciet omdat de output een registerupdate betreft waarvan het formaat in het register zelf is bepaald, niet in een afzonderlijk templatebestand

### Foutafhandeling

De Handoff-steward:
- stopt wanneer `handoff_id` niet voorkomt in het handoff-register;
- stopt wanneer de registerentry voor `handoff_id` al de status `gesloten` heeft (dubbele sluiting is niet toegestaan);
- stopt wanneer `handoff_register` niet bereikbaar is of een corrupt formaat heeft;
- stopt wanneer het handoff-bestand dat hoort bij `handoff_id` niet (meer) bestaat — sluiting zonder bestaand handoff-bestand is ongeldig;
- vraagt om verduidelijking wanneer `handoff_id` niet voldoet aan het formaat `hf-JJMM.NNNN`;
- escaleert naar `agent-curator` wanneer het register inconsistenties vertoont die niet veilig hersteld kunnen worden;
- STOP: bij poging tot wijziging van het handoff-bestand zelf — dit is verboden conform doctrine-handoff.md §7.3.

**Niet in scope voor deze intent**:
- Beoordeling of de ontvangende agent correct heeft gehandeld op basis van het handoff-bestand.
- Aanmaken van nieuwe handoff-bestanden — dat is in scope van `realiseer-initiele-handoff`.
- Correctie van een reeds gesloten handoff — hiervoor dient een nieuwe handoff aangemaakt te worden met expliciete verwijzing naar de vorige (doctrine-handoff.md §7.3).

---

## Werkwijze

### Stappen
1. **Valideer input**: Controleer aanwezigheid van `handoff_id` met formaat `hf-JJMM.NNNN` en leesbaarheid van `handoff_register`.
2. **Zoek registerentry**: Controleer of `handoff_id` voorkomt in het register met status `open`.
3. **Verificeer handoff-bestand**: Controleer dat het bijbehorende handoff-bestand nog bestaat op het verwachte pad.
4. **Schrijf registerupdate**: Zet status op `gesloten`; voeg `sluitings_datum` en `ontvangstbevestiging` toe aan de registerentry.
5. **Valideer register**: Controleer integriteit van het register na de write (geen andere entries gewijzigd, formaat intact).

### Kwaliteitsborging
- `handoff_id` had status `open` vóór sluiting
- Registerentry bevat na sluiting minimaal `status: gesloten` en `gesloten: {datum}`
- Het bijbehorende handoff-bestand is onaangeroerd gebleven
- Geen andere registerentries zijn gewijzigd

---

## Governance

**Doctrine-naleving:**
- **doctrine-handoff.md** (v1.0.0):
  - §7.3 Wijzigingsbeheer: handoff-bestand is na uitgifte onveranderlijk; correcties vereisen nieuw bestand
  - §3.1 Definitie: handoff-bestand is geldig tot ontvanger heeft gehandeld — sluiting markeert dit moment
- **doctrine-agent-charter-normering.md** (v2.4.0):
  - Principe 7 (Transparante Verantwoording): registerwijziging gelogd met sluitingsdatum en bevestiging
- **doctrine-templategebruik.md** (v1.0.0):
  - Output-template is expliciet vastgelegd als `~` in de contractuele templatebinding
  - Prompt-metadata spiegelt de templatekeuze uit het contract

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream aeo
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door runner)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: `handoff_register`
- ✓ Gewijzigde bestanden: `handoff_register` (status `open` → `gesloten`)
- ✓ Geen aangemaakte bestanden
- ✓ Gesloten handoff-id en bijbehorend execution-bestand (ter audit)

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → `agent-curator`: bij inconsistente of beschadigde registerstand
- → `handoff-steward (realiseer-initiele-handoff)`: wanneer een correctie van de afgesloten handoff vereist is — maak nieuw handoff-bestand aan met verwijzing naar het vorige
- STOP: bij poging tot sluiting van een al gesloten handoff; bij ontbrekend handoff-bestand

---

## Metadata

**Intent-ID**: `aeo.03.handoff-steward.realiseer-handoff-sluiting`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 03 — Operationele overdracht en ketenbeheer  
**Classificatie**:
- Betekeniseffect: Vastleggend
- Vormingsfase: Realisatie
- Werking: Inhoudelijk
- Bronhouding: Canon-gebonden
