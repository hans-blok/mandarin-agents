---
agent: handoff-steward
intent: realiseer-initiele-handoff
versie: 1.0.0
---
# Handoff-steward — Realiseer Initiële Handoff

## Rolbeschrijving (korte samenvatting)

De Handoff-steward genereert een nieuw handoff-bestand op basis van een afgerond execution-bestand: hij kent de eerstvolgende handoff-identificatie toe uit het handoff-register, vult het minimale inhoudsmodel in conform doctrine-handoff.md §3.3 en werkt het register bij met het nieuwe volgnummer.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `handoff-steward.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- `execution_bestand`: Pad naar het afgeronde execution-bestand van de overdragende agent (type: string, bestandspad, bijv. `executions/8ff6.capability-architect.definieer-agent-boundary.md`). Het bestand moet bestaan en een geldige execution-identiteit bevatten (`execution_id`, `agent`, `intent`, `timestamp`).
- `ontvangende_agent`: Identifier van de agent die het handoff-bestand ontvangt (type: string, kebab-case, bijv. `agent-ontwerper`).
- `handoff_register`: Pad naar het handoff-register (type: string, bestandspad). Het register wordt gelezen om het volgende volgnummer te bepalen.

**Optionele parameters**:
- `overdrachtsnota`: Vrije tekst met aanvullende instructie of context voor de ontvanger (type: string, default: leeg). Wordt opgenomen in het gelijknamige veld van het handoff-bestand.
- `escalatie_indicatie`: Geeft aan of de handoff een escalation van de overdragende agent naar een mens vereist (type: boolean, default: `false`). Wanneer `true`, is `escalatie_reden` verplicht.
- `escalatie_reden`: Beschrijving van de situatie die escalatie vereist (type: string). Verplicht wanneer `escalatie_indicatie: true`.
- `escalatie_urgentie`: Ernst van de escalatie (type: enum: `laag | normaal | hoog`, default: `normaal`). Alleen relevant wanneer `escalatie_indicatie: true`.

**Afgeleide informatie** (geëxtraheerd uit `execution_bestand`):
- `execution_id`: Overgenomen als `execution-identificatie` in het handoff-bestand.
- `overdragende_agent`: Afgeleid van het `agent`-veld in de execution-identiteit.
- `samenvatting_context`: Afgeleid van `agent`, `intent` en `timestamp` als minimale context; optioneel aangevuld vanuit de inhoud van het execution-bestand.

**Afgeleide informatie** (berekend op basis van `handoff_register`):
- `handoff_id`: Gegenereerd als `hf-JJMM.NNNN` — JJMM is de huidige maand, NNNN het volgende vrije volgnummer uit het register.

### Output (wat komt eruit)

De Handoff-steward levert:
- **Handoff-bestand** (`{handoff_id}.handoff.md`) conform het minimale inhoudsmodel van doctrine-handoff.md §3.3:
  - `handoff-identificatie`: gegenereerde `hf-JJMM.NNNN`
  - `execution-identificatie`: overgenomen van het execution-bestand
  - `overdragende-agent`: afgeleid van het execution-bestand
  - `ontvangende-agent`: uit parameter `ontvangende_agent`
  - `overdracht-datum`: datum van aanmaak
  - `samenvatting-context`: beschrijving van wat de overdragende agent heeft uitgevoerd
  - `genomen-beslissingen`: lijst van aantoonbare beslissingen in het execution-bestand (kan leeg zijn)
  - `gesignaleerde-ambiguiteiten`: ambiguïteiten gesignaleerd door de overdragende agent (kan leeg zijn)
  - `openstaande-taken`: taken die nog niet zijn afgerond (kan leeg zijn)
  - `escalatie-indicatie`: `false` standaard, `true` indien escalatie van toepassing
  - `overdrachtsnota`: aanvullende vrije tekst (optioneel)
- **Bijgewerkt handoff-register** met het nieuwe volgnummer voor `hf-JJMM`:

**Deliverable bestand**: `handoffs/{handoff_id}.handoff.md`  
**Registerlocatie**: opgegeven pad in `handoff_register`-parameter

**VERPLICHT**: Beide bestanden MOETEN worden weggeschreven. Het handoff-register MOET worden bijgewerkt vóór het handoff-bestand wordt geschreven om volgordeconsistentie te garanderen.

**Outputformaat** (minimale geldige handoff conform doctrine-handoff.md §3.3):
```yaml
handoff-identificatie: hf-2604.0001
execution-identificatie: 8ff6
overdragende-agent: capability-architect
ontvangende-agent: agent-ontwerper
overdracht-datum: 2026-04-06
samenvatting-context: |
  De capability-architect heeft de agent-boundary voor de handoff-steward (aeo.03)
  gedefinieerd inclusief classificatie, intents en raakvlakken.
genomen-beslissingen:
  - Classificatie: Realisatie × Vastleggend × Inhoudelijk × Canon-gebonden
openstaande-taken:
  - Definieer agent-charter voor handoff-steward
escalatie-indicatie: false
```

**Formaat-normering**:
- Default formaat: **Markdown** (.md) met YAML-frontmatter, conform Principe 9
- Het handoff-bestand bevat de inhoud als YAML-blok conform doctrine-handoff.md §3.3
- Alternatieve formaten alleen op expliciete verzoek

### Foutafhandeling

De Handoff-steward:
- stopt wanneer `execution_bestand` niet bestaat of geen leesbare execution-identiteit bevat (`execution_id`, `agent`, `intent`);
- stopt wanneer `handoff_register` niet bereikbaar is of een corrupt formaat heeft;
- stopt wanneer `escalatie_indicatie: true` is opgegeven zonder `escalatie_reden`;
- stopt wanneer het gegenereerde `handoff_id` reeds bestaat in het register (dubbel volgnummer);
- vraagt om verduidelijking wanneer `ontvangende_agent` niet te herleiden is tot een bekende agent in het ecosysteem;
- escaleert naar `agent-curator` wanneer het handoff-register inconsistenties of lacunes vertoont die niet veilig hersteld kunnen worden;
- STOP: bij een reeds afgesloten execution-bestand waarvan een handoff reeds bestaat in het register — retroactieve creatie is verboden conform doctrine-handoff.md §7.2.

**Niet in scope voor deze intent**:
- Inhoudelijke beoordeling van de output van de overdragende agent.
- Beslissing of een handoff al dan niet noodzakelijk is — dat bepaalt de runner of orkestrator.
- Ophalen of verwerken van reactie van de ontvangende agent.

---

## Werkwijze

### Stappen
1. **Valideer input**: Controleer aanwezigheid en leesbaarheid van `execution_bestand` en `handoff_register`; valideer `escalatie_indicatie`/`escalatie_reden`-combinatie.
2. **Lees execution-identiteit**: Extraheer `execution_id`, `agent`, `intent`, `timestamp` en `value_stream_fase` uit de YAML-frontmatter van het execution-bestand.
3. **Bepaal handoff_id**: Lees het handoff-register, bepaal het volgende vrije volgnummer voor de huidige maand (`hf-JJMM.NNNN`).
4. **Extraheer overdrachtscontext**: Afleid `samenvatting-context` van `agent`, `intent`, `timestamp`; extraheer aantoonbare beslissingen en openstaande taken uit de inhoud van het execution-bestand indien aanwezig.
5. **Blokkeer bij retroactief**: Controleer of het execution-bestand reeds voorkomt als `execution-identificatie` in een bestaand handoff-bestand in het register.
6. **Schrijf handoff-register bij** (vóór het handoff-bestand): Voeg `handoff_id` toe met status `open` en `execution_id`.
7. **Schrijf handoff-bestand**: Genereer `{handoff_id}.handoff.md` met alle verplichte velden conform doctrine-handoff.md §3.3.
8. **Valideer volledigheid**: Controleer aanwezigheid van alle verplichte velden; controleer `escalatie-indicatie`/`escalatie-reden`-coherentie in het bestand.

### Kwaliteitsborging
- `handoff-identificatie` voldoet aan formaat `hf-JJMM.NNNN` (doctrine-handoff.md §2.2)
- `execution-identificatie` verwijst naar een bestaand execution-bestand
- Alle verplichte velden uit doctrine-handoff.md §3.3 zijn aanwezig
- Register is bijgewerkt vóór het handoff-bestand is geschreven
- Geen retroactief gecreëerd handoff-bestand (doctrine-handoff.md §7.2)
- Escalatie-velden coherent (indien `true`, dan `escalatie_reden` aanwezig)

---

## Governance

**Doctrine-naleving:**
- **doctrine-handoff.md** (v1.0.0):
  - §2.2 Formaat-conventie: `hf-JJMM.NNNN`
  - §2.4 Generatie-verantwoordelijkheid: alleen de runner/agent genereert handoff-id's, nooit overgenomen van eerder
  - §3.3 Minimale inhoud: alle verplichte velden aanwezig
  - §4 Escalatie: `escalatie-indicatie` verplicht, `escalatie-reden` conditioneel verplicht
  - §7.2 Verbod op retroactieve creatie
- **doctrine-agent-charter-normering.md** (v2.4.0):
  - Principe 7 (Transparante Verantwoording): handoff-id en register-mutatie gelogd
  - Principe 9 (Output-formaat Normering): Markdown als default
- **doctrine-traceability.md** (v1.2.0):
  - §7 Execution-trace-bestand: handoff is complementair aan execution-trace, niet vervangend

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream aeo
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door runner)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: `execution_bestand`, `handoff_register`
- ✓ Aangemaakte bestanden: `{handoff_id}.handoff.md`
- ✓ Gewijzigde bestanden: `handoff_register` (volgnummer bijgewerkt)
- ✓ Gegenereerde handoff-id en bijbehorend execution-bestand

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → `agent-curator`: bij inconsistente of onherstelbare registerstand
- → menselijk toezicht: wanneer `escalatie-indicatie: true` is opgenomen in het handoff-bestand (doctrine-handoff.md §4.3)
- STOP: bij retroactief handoff-aanmaakrequest; bij ontbrekende verplichte velden in execution-bestand

---

## Metadata

**Intent-ID**: `aeo.03.handoff-steward.realiseer-initiele-handoff`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 03 — Operationele overdracht en ketenbeheer  
**Classificatie**:
- Betekeniseffect: Vastleggend
- Vormingsfase: Realisatie
- Werking: Inhoudelijk
- Bronhouding: Canon-gebonden
