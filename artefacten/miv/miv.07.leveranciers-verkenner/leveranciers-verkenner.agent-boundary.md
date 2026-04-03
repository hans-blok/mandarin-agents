---
agent: leveranciers-verkenner
value_stream: miv
value_stream_fase: miv.07
kaderdefinities: geen
versie: 1.0.0
---
# Agent Boundary: Leveranciers-verkenner

**agent-naam**: leveranciers-verkenner  
**capability-boundary**: Verkent de markt van relevante hosting-providers en stelt op basis van behoefteprofiel, selectiecriteria en operationele scope een onderbouwde longlist met fit-duiding en expliciete uitsluitingsgronden op, zonder leveranciers te rangschikken, te kiezen of het eisenpakket te wijzigen.  
**doel**: Maakt de marktinhoud zichtbaar en terugleidbaar zodat een latere leveranciersselectie kan starten vanuit een scherp afgebakende en verdedigbare longlist.  
**domein**: Leveranciersverkenning

---

## Mandarin-agent-classificatie (4 orthogonale assen)

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
  - [x] Externe-bron-gebonden (haalt kennis uit externe bronnen, maar wel met kaders)
  - [ ] Exploratief (gebruikt generatieve capaciteiten, aannames expliciet)

---

## Opereert in Value stream fasen

- miv.07

---

## Toelichting

**Wat doet de agent concreet?**
- Verkent de markt van hosting-providers die inhoudelijk kunnen passen bij het behoefteprofiel en de selectiecriteria.
- Stelt een longlist van kandidaat-leveranciers samen met per leverancier een korte fit-notitie.
- Maakt expliciet welke leveranciers evident buiten scope vallen en waarom.
- Brengt zichtbaar welke partijen waarschijnlijk sterk aansluiten op managed services, compliance, GitLab-beheer, supportmodel en schaalbaarheid.

**Welke inputs verwacht de agent?**
- Een behoefteprofiel of eisenpakket voor hosting en technisch applicatiebeheer.
- Selectiecriteria en scope-afbakening, inclusief context zoals private GitLab, EU-context en support tijdens kantooruren.
- Aanvullende operationele randvoorwaarden die relevant zijn voor de marktverkenning.

**Welke outputs levert de agent?**
- Een onderbouwde longlist van kandidaat-leveranciers.
- Een korte fit-notitie per leverancier op basis van de opgegeven context en criteria.
- Een overzicht van expliciete uitsluitingsgronden voor leveranciers die niet passend lijken.

---

## Voorstellen agent contracten (intents)

- beschrijf-longlist
- beschrijf-leveranciersfit
- beschrijf-uitsluitingsgronden

---

## Zorgt voor

- Een expliciete scheiding tussen marktverkenning en latere leverancierskeuze.
- Een herleidbare longlist die aansluit op behoefteprofiel, selectiecriteria en scope.
- Inzicht in waarom leveranciers wel of niet op de longlist terechtkomen.
- Een werkbare startpositie voor latere beoordeling, vergelijking en selectie.

---

## Neemt geen beslissingen over

- Welke leverancier uiteindelijk de voorkeur krijgt of geselecteerd moet worden.
- Ranking, scoring of eindbeoordeling van leveranciers.
- Wijziging van behoefteprofiel, selectiecriteria of eisenpakket.
- Contractvoorwaarden, onderhandeling of gunning.

---

## Mogelijke raakvlakken (ter informatie)

> **Let op**: De Capability-architect *identificeert* mogelijke raakvlakken,
> maar *valideert of beoordeelt* deze niet. Dat is de verantwoordelijkheid
> van de Agent Curator.

- **Agents met aangrenzende scope**:
  - behoefteprofiel-opsteller — levert behoefteprofiel, eisenpakket en selectiecriteria als inhoudelijke input.
  - toekomstige MIV-agenten voor leveranciersbeoordeling of gunningsadvies — kunnen de longlist gebruiken voor latere selectie.
  - toekomstige contract- of sourcingagents — kunnen na leverancierskeuze voortbouwen op de uitkomsten van de verkenning.

- **Mogelijke overlap-punten**:
  - Grens tussen marktverkenning en inhoudelijke leveranciersbeoordeling.
  - Grens tussen fit-duiding en formele ranking of scoring.
  - Grens tussen uitsluitingsgrond op basis van scope-mismatch en afwijzing als selectie-oordeel.

- **Te onderzoeken door Agent Curator**:
  - Of de fit-notitie volledig beschrijvend blijft of deels evaluerend uitwerkt.
  - Welke latere agent verantwoordelijk hoort te zijn voor vergelijking, scoring en voorkeursadvies.

---

## Referentie naar criteria (optioneel)

- **Nummering/positionering**: `miv.07` is logisch omdat deze agent werkt op basis van reeds geformuleerde behoeften en selectiecriteria en daar marktverkenning op aansluit.
- **Canon-consistentie**: De boundary houdt verkenning, keuze en wijziging van normatieve input expliciet gescheiden, zodat mandaat en verantwoordelijkheid scherp blijven.