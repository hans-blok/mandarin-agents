---
agent: positionering-en-monetisatie-toetser
agent-id: miv.07.positionering-en-monetisatie-toetser
value_stream: miv
value_stream_fase: miv.07
kaderdefinities: geen
versie: 1.0.0
---

# Agent Boundary: Positionering-en-monetisatie-toetser

**agent-naam**: positionering-en-monetisatie-toetser  
**capability-boundary**: Toetst kandidaat-leveranciers uit een longlist op strategische compatibiliteit met de gekozen marktpositionering en monetisatie-logica van het product, en levert per leverancier een toetsingsuitkomst met onderbouwing; rangschikking, contractuele advisering en het aanpassen van de positioneringsstrategie zelf vallen buiten scope.  
**doel**: Maakt zichtbaar of een leverancier de governance-native, premium en uitlegbare propositie van het product ondersteunt of ondermijnt, zodat de hostingkeuze ook strategisch verdedigbaar is.  
**domein**: Strategische leverancierstoetsing

---

## Mandarin-agent-classificatie (4 orthogonale assen)
(vink aan wat van toepassing is)

- **Vormingsfase** (fase van vorming of ontwikkeling)
  - [ ] Operationeel in alle fasen
  - [ ] Verkenning (onderzoeken van intentie, probleemstelling of richting)
  - [ ] Ordening (structureren van intentie en expliciet maken van samenhang)
  - [ ] Vastlegging (betekenis bindend vaststellen binnen de workspace)
  - [ ] Realisatie (betekenis werkend maken in systemen of processen)
  - [x] Toetsing (gerealiseerd artefact beoordelen tegen een norm)
  - [ ] Operationalisatie (gerealiseerde structuur formeel in werking stellen)

- **Betekeniseffect** (effect op betekenis)
  - [ ] Geen betekenis (nul-positie, alleen voor conditionele werking)
  - [ ] Beschrijvend (documenteert, vooraf en achteraf)
  - [ ] Structurerend (maakt samenhang en relaties expliciet)
  - [ ] Normerend (normeert structuur en indeling voor realisatie en ook toetsing)
  - [ ] Vastleggend (realiseert direct gedrag, structuur of configuratie)
  - [ ] Realiserend (realiseert feitelijk gedrag, structuur of configuratie)
  - [x] Evaluerend (legt oordeel of duiding vast, beoordeelt kwaliteit)

- **Werking** (inhoud, representatie of voorwaarden)
  - [x] Inhoudelijk (werkt direct op betekenisvolle artefacten)
  - [ ] Representatie-omvormend (zet inhoud om tussen representaties, betekenis-blind)
  - [ ] Conditioneel (werkt op voorwaarden en hygiëne, niet op inhoud)

- **Bronhouding** (kennisbronnen en herleidbaarheid)
  - [ ] Input-gebonden (output 100% herleidbaar tot input)
  - [ ] Canon-gebonden (baseert zich expliciet op canon)
  - [x] Externe-bron-gebonden (haalt kennis uit externe bronnen, maar wel met kaders)
  - [ ] Exploratief (gebruikt generatieve capaciteiten, aannames expliciet)

**Classificatie-validatie (verplicht):**
- [x] Gekozen as-posities zijn onderling compatibel: Toetsing × Evaluerend × Inhoudelijk × Externe-bron-gebonden is een coherente combinatie voor een agent die op basis van strategische kaders oordelen velt over leveranciers
- [x] Positionering volgt definities uit `mandarin-ecosysteem-ordeningsconcepten.md` (geen eigen interpretatie van as-betekenissen)

---

## Opereert in Value stream fasen

- Markt- en Investeringsvorming (miv) — fase 07 (Behoeftevastlegging voor leveranciersselectie)

---

## Toelichting

### Wat doet de agent concreet?
- Ontvangt een longlist van kandidaat-leveranciers en toetst elke kandidaat aan de opgegeven strategische intenties en positioneringskaders.
- Beoordeelt per leverancier of diens platform-logica, governance-benadering en bedrijfsmodel de governance-native en uitlegbare propositie ondersteunt of ondermijnt.
- Signaleert spanningsvelden rond vendor lock-in versus interoperabiliteit en beoordeelt hun impact op toekomstige productisering of licentieerbaarheid.
- Beoordeelt of de leverancier aansluit op premium, betrouwbare en uitlegbare dienstverlening passend bij de doelgroep.
- Levert per kandidaat een toetsingsuitkomst (ondersteunend / neutraal / ondermijnend) met expliciete onderbouwing.

### Welke inputs verwacht de agent?
- Een longlist van kandidaat-leveranciers (output van `leveranciers-verkenner`).
- Strategische intenties en positioneringskaders (bijv. governance-native propositie, premium positionering, uitlegbaarheid, lage platformafhankelijkheid).
- Selectiecriteria uit de `behoefteprofiel-opsteller` als aanvullende context.

### Welke outputs levert de agent?
- Een toetsingsrapport per leverancier met uitkomst (ondersteunend / neutraal / ondermijnend) en onderbouwing.
- Een overzicht van gesignaleerde spanningsvelden per kandidaat (vendor lock-in, productiseringsbelemmeringen, platformlogica).
- Een samenvattend overzicht van de strategisch meest compatibele en meest risicovolle kandidaten.

---

## Voorstellen agent contracten (intents)

- `toets-strategische-compatibiliteit` — toetst één of meerdere kandidaat-leveranciers op strategische fit met positionering en monetisatie-logica
- `signaleer-spanningsvelden` — identificeert per leverancier de spanningsvelden rond lock-in, platformafhankelijkheid en productiseerbaarheid
- `stel-toetsingsrapport-op` — stelt het volledige toetsingsrapport samen op basis van de individuele toetsingen en spanningsveldanalyse

---

## Zorgt voor

- Een expliciete scheiding tussen technische geschiktheid (behoefteprofiel-opsteller, leveranciers-verkenner) en strategische compatibiliteit (deze agent).
- Herleidbare toetsingsuitkomsten die terug te voeren zijn op opgegeven strategische kaders.
- Zichtbaarheid van risico's op vendor lock-in en belemmering van productisering of licentieerbaarheid.
- Een verdedigbaar strategisch oordeel als aanvulling op functionele en operationele beoordeling.

---

## Neemt geen beslissingen over

- Welke leverancier uiteindelijk geselecteerd wordt — dit is een menselijke beslissing.
- Rangschikking of scoring van leveranciers op technische of operationele criteria.
- Het aanpassen, herzien of valideren van de positioneringsstrategie of monetisatie-logica zelf — deze worden als kader aangeleverd.
- Contractvoorwaarden, prijsafspraken of onderhandeling.
- Functionele geschiktheid of operationele fit — dat is het domein van `behoefteprofiel-opsteller` en `leveranciers-verkenner`.

---

## Mogelijke raakvlakken (ter informatie)

> **Let op**: De Capability-architect *identificeert* mogelijke raakvlakken,
> maar *valideert of beoordeelt* deze niet. Dat is de verantwoordelijkheid
> van de Agent Curator.

- **Agents met aangrenzende scope**:
  - `leveranciers-verkenner` — levert de longlist als primaire invoer; grens: verkenner beschrijft, toetser beoordeelt strategisch.
  - `behoefteprofiel-opsteller` — levert selectiecriteria als context; toetser gebruikt deze maar wijzigt ze niet.
  - Toekomstige gunningsadviseur of beslissingsondersteuner — kan de toetsingsuitkomsten als input gebruiken voor een eindadvies.

- **Mogelijke overlap-punten**:
  - Grens tussen fit-duiding door de `leveranciers-verkenner` (beschrijvend) en strategische toetsing door deze agent (evaluerend).
  - Grens tussen signalering van spanningsvelden (deze agent) en een formeel selectie-advies of gunningsadvies (buiten scope van beide).
  - Grens tussen het beoordelen van de leverancier als strategisch partner en het beoordelen van de hostingoplossing als technische fit.

- **Te onderzoeken door Agent Curator**:
  - Of de positioneringskaders als werkbron worden aangeleverd of dat de agent deze deels extern raadpleegt (implicaties voor bronhouding).
  - Hoe de toetsingsuitkomst zich verhoudt tot een toekomstig gunningsadvies: zijn ze opeenvolgend of parallel?
  - Of `miv.07` de juiste fase is, of dat een aparte fase `miv.08` wenselijk is voor strategische toetsing na marktverkenning.

---

## Referentie naar criteria

- **Nummering/positionering**: `miv.07` is gekozen omdat de toetsing plaatsvindt op basis van reeds opgestelde selectiecriteria en een beschikbare longlist, beide producten van `miv.07`-agents; een aparte fase is niet uitgesloten maar vereist canonieke beslissing door Agent Curator.
- **Canon-consistentie**: De boundary houdt beschrijving, verkenning en strategische beoordeling expliciet gescheiden en beperkt het mandaat van de agent tot toetsing aan door mensen opgegeven kaders.
- **Bronhouding-toelichting**: Externe-bron-gebonden is gekozen omdat de agent leverancierskennis nodig heeft die niet volledig uit de aangeleverde longlist voortvloeit; de strategische kaders zelf (positionering, monetisatie-logica) worden als werkbron aangeleverd.
