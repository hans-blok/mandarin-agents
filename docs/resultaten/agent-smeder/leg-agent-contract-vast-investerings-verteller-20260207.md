# Agent Smeder - Intent 1: leg-agent-contract-vast
## Agent: investerings-verteller
**Datum**: 2026-02-07  
**Uitgevoerd door**: agent-smeder  
**Intent**: 1.leg-agent-contract-vast

---

## Overzicht

De agent-smeder heeft de agent-contracten en YAML prompt-metadata voor de agent **investerings-verteller** volledig uitgewerkt op basis van de capability boundary en de voorstellen uit de boundary. Beide intents (`schrijf-uitgebreide-pitch`, `schrijf-30-seconden-pitch`) zijn voorzien van volledige contracten met gedetailleerde input, output en foutafhandeling.

---

## Uitgevoerde acties

### 1. Agent-contracten uitgewerkt

Voor elk van de twee intents is een volledig agent-contract opgesteld volgens het template:

#### Intent: `schrijf-uitgebreide-pitch`
**Locatie**: `artefacten/miv/miv.02.investerings-verteller/investerings-verteller.schrijf-uitgebreide-pitch.agent.md`

**Input**:
- Verplicht: strategische-analyse, markt-en-context, risicos-en-aannames
- Optioneel: type-investeerder, tijdshorizon, focus-gebieden

**Output**:
- Uitgebreide investeringspitch: 1.000-1.500 woorden, verhalende logica (probleem → oplossing → waarde → geloofwaardigheid → perspectief)
- Herkomstverantwoording met bronnen, aannames, datum en versie

**Deliverable eigenschappen**:
- Interne consistentie en externe traceerbaarheid
- Begrijpelijk voor investeerders zonder voorkennis
- Geen marketing: zakelijke toon, feitelijk
- Format: Markdown

**Foutafhandeling**:
- Stopt bij onvolledige strategische analyse
- Stopt wanneer nieuwe strategie of aannames gevraagd worden
- Waarschuwt bij ontbrekende risico's/aannames
- Valideert woordlimiet (1.000-1.500)

---

#### Intent: `schrijf-30-seconden-pitch`
**Locatie**: `artefacten/miv/miv.02.investerings-verteller/investerings-verteller.schrijf-30-seconden-pitch.agent.md`

**Input**:
- Verplicht: strategische-analyse
- Optioneel: uitgebreide-pitch (voor consistentie), focus, type-investeerder

**Output**:
- 30-seconden investeringspitch: ±75 woorden, mondeling deelbaar
- Consistentie-notitie (indien uitgebreide pitch beschikbaar)

**Deliverable eigenschappen**:
- Inhoudelijk consistent met uitgebreide pitch en analyse
- Geen samenvatting maar essentie
- Onthoudbaar, helder, rustige toon
- Mondeling testbaar (±30 seconden spreektijd)
- Format: Markdown

**Foutafhandeling**:
- Stopt bij onvolledige strategische analyse
- Stopt wanneer nieuwe strategie gevraagd wordt
- Waarschuwt bij overschrijding woordlimiet (>75 woorden)
- Waarschuwt bij inconsistentie met uitgebreide pitch
- Valideert mondelinge natuurlijkheid

---

### 2. YAML prompt-metadata aangemaakt

Beide prompt-metadata bestanden zijn aangemaakt volgens het YAML-only format:

- `mandarin.investerings-verteller.schrijf-uitgebreide-pitch.prompt.md`
- `mandarin.investerings-verteller.schrijf-30-seconden-pitch.prompt.md`

**Format**:
```yaml
---
agent: investerings-verteller
intent: <intent-naam>
charter_ref: artefacten/miv/miv.02.investerings-verteller/investerings-verteller.charter.md
---
```

---

## Traceerbaarheid

| Artefact | Type | Locatie |
|----------|------|---------|
| Boundary | Input | `artefacten/miv/miv.02.investerings-verteller/agent-boundary-investerings-verteller.md` |
| Contract 1 | Output | `artefacten/miv/miv.02.investerings-verteller/investerings-verteller.schrijf-uitgebreide-pitch.agent.md` |
| Prompt 1 | Output | `artefacten/miv/miv.02.investerings-verteller/mandarin.investerings-verteller.schrijf-uitgebreide-pitch.prompt.md` |
| Contract 2 | Output | `artefacten/miv/miv.02.investerings-verteller/investerings-verteller.schrijf-30-seconden-pitch.agent.md` |
| Prompt 2 | Output | `artefacten/miv/miv.02.investerings-verteller/mandarin.investerings-verteller.schrijf-30-seconden-pitch.prompt.md` |
| Charter (toekomstig) | Volgende stap | `artefacten/miv/miv.02.investerings-verteller/investerings-verteller.charter.md` |

---

## Validatie

✅ **Capability boundary gerespecteerd**: Beide contracten blijven binnen de afbakening (vertaling naar narratief, geen nieuwe strategie)  
✅ **Consistent met boundary**: Input/output aligned met voorstellen uit boundary  
✅ **Geen overlap**: Duidelijk onderscheid met Strategisch Analist (MIV 01), Presentatie-architect en Publisher  
✅ **YAML-only prompt-metadata**: Beide prompt-bestanden volgen het vereiste format  
✅ **Geen marketingtaal**: Contracten benadrukken zakelijke toon en feitelijke benadering  
✅ **Output-formats helder**: Uitgebreide pitch (1.000-1.500 woorden) vs korte pitch (±75 woorden)  

---

## Kernverschillen tussen de twee intents

| Aspect | schrijf-uitgebreide-pitch | schrijf-30-seconden-pitch |
|--------|---------------------------|---------------------------|
| **Lengte** | 1.000-1.500 woorden | ±75 woorden (30 sec spreektijd) |
| **Doel** | Rationeel overtuigen, investeringsmemo | Essentie raken, mondeling deelbaar |
| **Structuur** | Verhalende logica (probleem→oplossing→waarde→geloofwaardigheid→perspectief) | Compacte natuurlijke tekst |
| **Detail** | Volledig onderbouwd | Alleen essentie, geen details |
| **Gebruik** | Voorbereiding gesprek, memo | Hardop uitspreken, elevator pitch |
| **Consistentie-check** | Naar input-analyse | Naar input-analyse + uitgebreide pitch |

---

## Gelezen bestanden

1. `c:\git\mandarin-agents\.github\prompts\mandarin.agent-smeder-1.leg-agent-contract-vast.prompt.md`
2. `c:\git\mandarin-agents\artefacten\miv\miv.02.investerings-verteller\agent-boundary-investerings-verteller.md`
3. `c:\git\mandarin-agents\artefacten\aeo\aeo.02.agent-smeder\agent-smeder-1.leg-agent-contract-vast.agent.md`
4. `c:\git\mandarin-agents\artefacten\aeo\aeo.02.agent-smeder\agent-smeder.charter.md`
5. `c:\git\mandarin-agents\templates\agent-contract.template.md`
6. `c:\git\mandarin-agents\templates\agent-prompt.template.yaml`

---

## Aangemaakte bestanden

1. `c:\git\mandarin-agents\artefacten\miv\miv.02.investerings-verteller\investerings-verteller.schrijf-uitgebreide-pitch.agent.md`
2. `c:\git\mandarin-agents\artefacten\miv\miv.02.investerings-verteller\mandarin.investerings-verteller.schrijf-uitgebreide-pitch.prompt.md`
3. `c:\git\mandarin-agents\artefacten\miv\miv.02.investerings-verteller\investerings-verteller.schrijf-30-seconden-pitch.agent.md`
4. `c:\git\mandarin-agents\artefacten\miv\miv.02.investerings-verteller\mandarin.investerings-verteller.schrijf-30-seconden-pitch.prompt.md`
5. `c:\git\mandarin-agents\docs\resultaten\agent-smeder\leg-agent-contract-vast-investerings-verteller-20260207.md` (dit rapport)

---

## Conclusie

De agent **investerings-verteller** is nu volledig uitgerust met contract-first artefacten voor beide intents. Beide contracten zijn traceerbaar naar de boundary, volgen de governance zoals vastgelegd in `beleid-mandarin-agents.md` en respecteren de capability boundary (geen nieuwe strategie, alleen vertaling naar narratief).

**Volgende stap**: Agent Smeder intent `2.schrijf-charter` om het charter voor investerings-verteller op te stellen.

**Status**: ✅ Gereed voor charter-ontwikkeling en runner-ontwerp
