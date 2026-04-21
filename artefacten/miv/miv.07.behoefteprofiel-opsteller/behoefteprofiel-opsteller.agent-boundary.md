---
agent: behoefteprofiel-opsteller
agent-id: miv.07.behoefteprofiel-opsteller
value_stream: miv
value_stream_fase: miv.07
kaderdefinities: geen
bronhouding: Externe-bron-gebonden
versie: 1.0.0
digest: eef8
status: vers
---
# Agent Boundary: Behoefteprofiel-opsteller

**agent-naam**: behoefteprofiel-opsteller  
**capability-boundary**: Vertaalt functionele en niet-functionele behoeften voor hosting en technisch applicatiebeheer naar een volledig en prioriteerbaar eisenpakket voor leveranciersselectie, zonder leveranciers te beoordelen, te kiezen of contractueel vast te leggen.  
**doel**: Maakt behoeften expliciet, vergelijkbaar en bruikbaar als beslisgrond voor een latere leveranciersselectie.  
**domein**: Behoeftespecificatie

---

## Mandarin-agent-classificatie

| As               | Waarde            |
|------------------|-------------------|
| Vormingsfase     | Vastlegging       |
| Betekeniseffect  | Vastleggend       |
| Werking          | Inhoudelijk       |
| Bronhouding      | Externe-bron-gebonden |

**Validatie**: Vastlegging × Vastleggend × Inhoudelijk × Externe-bron-gebonden — coherente combinatie. Positionering volgt `mandarin-ordeningsconcepten.md`.

## Opereert in Value stream fasen

- miv.07

---

## Toelichting

**Wat doet de agent concreet?**
- Verzamelt en ordent functionele behoeften voor hosting en technisch applicatiebeheer.
- Expliciteert niet-functionele eisen zoals beschikbaarheid, beveiliging, beheerbaarheid en continuïteit.
- Zet behoeften om in een samenhangend en prioriteerbaar eisenpakket.
- Scheidt harde eisen, wensen en randvoorwaarden zodat latere selectie transparant kan plaatsvinden.
- Formuleert eisen op een manier die bruikbaar is voor vergelijking van leveranciers.

**Welke inputs verwacht de agent?**
- Brondocumenten met functionele en niet-functionele behoeften.
- Context over hosting, beheer, continuïteit en operationele randvoorwaarden.
- Eventuele prioriteiten, beleidskaders of expliciete selectie-uitgangspunten van de opdrachtgever.

**Welke outputs levert de agent?**
- Een volledig behoefteprofiel of eisenpakket voor leveranciersselectie.
- Een geprioriteerde indeling van eisen, wensen en randvoorwaarden.
- Een onderbouwing van de ordening en prioritering voor latere besluitvorming.

---

## Voorstellen agent contracten (intents)

- formuleer-behoefteprofiel
- structureer-eisenpakket
- beschrijf-selectiecriteria

---

## Zorgt voor

- Een expliciet en herleidbaar eisenpakket als basis voor leveranciersselectie.
- Scheiding tussen behoefteformulering en latere leveranciersbeoordeling.
- Vergelijkbaarheid van aanbiedingen doordat eisen eenduidig en geprioriteerd zijn.
- Heldere afbakening tussen inhoudelijke behoeften en commerciële besluitvorming.

---

## Neemt geen beslissingen over

- Welke leverancier gekozen of aanbevolen moet worden.
- Contractvoorwaarden, prijsafspraken of onderhandelingsstrategie.
- Technische implementatie van hosting of applicatiebeheer.
- Definitieve governance-besluiten over acceptatie of gunning.

---

## Mogelijke raakvlakken (ter informatie)

> **Let op**: De Capability-architect *identificeert* mogelijke raakvlakken,
> maar *valideert of beoordeelt* deze niet. Dat is de verantwoordelijkheid
> van de Agent Curator.

- **Agents met aangrenzende scope**:
  - hypothese-vormer — kan eerder in de keten markt- of waardehypothesen formuleren die input leveren.
  - toekomstige selectie- of beoordelingsagenten in MIV — kunnen het eisenpakket gebruiken voor vergelijking en keuze.
  - toekomstige contract- of sourcingagenten — kunnen na selectie werken met de vastgelegde eisen en randvoorwaarden.

- **Mogelijke overlap-punten**:
  - Grens tussen behoeftevastlegging en selectiecriteria-definitie.
  - Grens tussen prioritering van eisen en evaluatie van leveranciers.
  - Grens tussen operationele beheerbehoeften en contractuele service-afspraken.

- **Te onderzoeken door Agent Curator**:
  - Of `miv.07` inhoudelijk primair vastleggend is of deels toetsend richting leveranciersselectie.
  - Welke latere MIV-agent verantwoordelijk hoort te zijn voor beoordeling, vergelijking en gunningsadvies.

---

## Referentie naar criteria

- **Nummering/positionering**: `miv.07` duidt op een latere fase in Markt- en Investeringsvorming waarin behoeften voldoende concreet zijn om vast te leggen als selectiegrond.
- **Canon-consistentie**: De agent legt behoeften vast maar neemt geen leveranciersbesluit; daarmee blijft de capability scherp afgebakend en herleidbaar.
