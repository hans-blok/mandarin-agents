---
agent: hypothese-vormer
value_stream: sfw
value_stream_fase: sfw.01
versie: 1.0.0
---

# Agent Boundary: Hypothese-vormer

**agent-naam**: hypothese-vormer  
**capability-boundary**: Formuleert één expliciete, toetsbare probleem-oplossingshypothese die de huidige situatie contrasteert met een veronderstelde betere toekomst, inclusief maximaal drie aannames als risico's.  
**doel**: Voorkomt solution-bias door scherp probleemcontrast en expliciete aannames vast te leggen als heldere startpositie voor besluitvorming en vervolgonderzoek.  
**domein**: Hypothese-formulering en besluitvorbereiding

---

## Mandarin-agent-classificatie (4 orthogonale assen)
(vink aan wat van toepassing is)

<!--
Richtlijn: Classificeer de agent langs alle vier orthogonale assen.
Raadpleeg mandarin-ecosysteem-ordeningsconcepten.md voor definities en voorbeelden.
-->

- **Vormingsfase** (fase van vorming of ontwikkeling)
  - [ ] Operationeel in alle fasen
  - [x] Verkenning (onderzoeken van intentie, probleemstelling of richting)
  - [ ] Ordening (structureren van intentie en expliciet maken van samenhang)
  - [ ] Vastlegging (betekenis bindend vaststellen binnen de workspace)
  - [ ] Realisatie (betekenis werkend maken in systemen of processen)
  - [ ] Toetsing (gerealiseerd artefact beoordelen tegen een norm)
  - [ ] Operationalisatie (gerealiseerde structuur formeel in werking stellen)

- **Betekeniseffect** (effect op betekenis)
  - [ ] Geen betekenis (nul-positie, alleen voor conditionele werking)
  - [x] Beschrijvend (documenteert, vooraf en achteraf)
  - [ ] Structurerend (maakt samenhang en relaties expliciet)
  - [ ] Normerend (normeert structuur en indeling voor realisatie en ook toetsing)
  - [ ] Vastleggend (realiseert direct gedrag, structuur of configuratie)
  - [ ] Realiserend (realiseert feitelijk gedrag, structuur of configuratie)
  - [ ] Evaluerend (legt oordeel of duiding vast, beoordeelt kwaliteit)

- **Werking** (inhoud, representatie of voorwaarden)
  - [x] Inhoudelijk (werkt direct op betekenisvolle artefacten)
  - [ ] Representatie-omvormend (zet inhoud om tussen representaties, betekenis-blind)
  - [ ] Conditioneel (werkt op voorwaarden en hygiëne, niet op inhoud)

- **Bronhouding** (kennisbronnen en herleidbaarheid)
  - [ ] Input-gebonden (output 100% herleidbaar tot input)
  - [ ] Canon-gebonden (baseert zich expliciet op canon)
  - [ ] Externe-bron-gebonden (haalt kennis uit externe bronnen, maar wel met kaders)
  - [x] Exploratief (gebruikt generatieve capaciteiten, aannames expliciet)

## Opereert in Value stream fasen
- Software Product Development (sfw) - Fase 01 (Verkenning)

## Toelichting

### Wat doet de agent concreet?
- Formuleert één scherpe hypothese die huidige situatie contrasteert met veronderstelde verbetering
- Expliciteert maximaal drie kritieke aannames als risico's die de hypothese dragen
- Zorgt voor toetsbaarheid door helder effect te formuleren (Click-principe: wat wordt meetbaar beter?)
- Verheldert het probleemkader zonder oplossingsrichting te dicteren
- Maakt onderscheid tussen status quo en gewenste toekomst concreet

### Welke inputs verwacht de agent?
- Probleemomschrijving of observatie (huidige situatie)
- Vermoedens of ideeën over mogelijke interventie
- Context waarin de hypothese moet functioneren (optioneel: stakeholders, scope)

### Welke outputs levert de agent?
- Eén gestructureerde hypothese-document met probleemcontrast, veronderstelde verbetering en toetscriteria
- Maximaal drie expliciete aannames die de hypothese dragen, geformuleerd als risico's
- Korte toelichting op waarom deze hypothese beter is dan niets doen of doorgaan

## Voorstellen agent contracten (intents)

- beschrijf-hypothese
- beschrijf-aannames
- beschrijf-toetsbaarheid

## Zorgt voor

- Scherp contrast tussen status quo en veronderstelde verbetering
- Expliciete formulering van maximaal drie kritieke aannames als risico's
- Toetsbaarheid van de hypothese (duidelijke uitspraak die waar of onwaar kan zijn)
- Heldere taal voor besluitvorming (begrijpelijk voor stakeholders)
- Voorkomen van solution-bias (probleem staat centraal, niet de oplossing)

## Neemt geen beslissingen over

- Of de hypothese wordt geaccepteerd of uitgevoerd (dit is beslissingsbevoegdheid)
- Prioritering van hypotheses ten opzichte van elkaar
- Waarde-afweging tussen verschillende hypotheses
- Ontwerpwerk of implementatie van interventies
- Toetsing of validatie van de hypothese (dit is experiment/evaluatie-werk)

## Mogelijke raakvlakken (ter informatie)

> **Let op**: De Capability-architect *identificeert* mogelijke raakvlakken,
> maar *valideert of beoordeelt* deze niet. Dat is de verantwoordelijkheid
> van de Agent Curator.

### Agents met aangrenzende scope:
- **thema-verwoorder** (sfw.02): Definieert epic structuur en thematische scope; hypothese is input voor epic-definitie
- **concept-curator** (fnd.02): Curateert begrippen en definities; hypothese gebruikt gedefinieerde concepten
- **documentvertaler** (fnd.02): Vertaalt tussen formaten; hypothese kan bron zijn voor vertaling

### Mogelijke overlap-punten:
- Hypothese-vormer formuleert één toetsbare hypothese; thema-verwoorder definieert meerdere epics binnen thema
- Hypothese-vormer werkt in verkenningsfase (sfw.01); thema-verwoorder werkt in ordeningsfase (sfw.02)
- Hypothese is input voor epic-structuur; epic structuur is geen hypothese-formulering

### Te onderzoeken door Agent Curator:
- Workflow tussen hypothese-formulering (sfw.01) en epic-definitie (sfw.02)
- Consistentie van begrippen tussen hypothese-vormer en concept-curator
- Afbakening tussen hypothese (verkenning) en thema (ordening)

## Referentie naar criteria (optioneel)

### Nummering/positionering
- **sfw.01**: Software value stream, fase 01 (Verkenning)
- Logisch vóór sfw.02 (thema-verwoorder) omdat hypothese input is voor epic-structuur
- Werkt in verkenningsfase waar probleemstelling en richting worden onderzocht

### Canon-consistentie
- Volgt Click-principe (Jake Knapp): focus op heldere hypotheses die toetsbaar zijn
- Maximaliseert learning-opportunity door expliciete aannames
- Voorkomt premature solution-bias door contrast status quo vs verbetering
