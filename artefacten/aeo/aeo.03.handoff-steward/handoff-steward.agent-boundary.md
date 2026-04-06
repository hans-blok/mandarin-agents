---
agent: handoff-steward
value_stream: aeo
value_stream_fase: aeo.03
kaderdefinities: geen
versie: 1.0.0
---
# Agent Boundary: Handoff-steward

**agent-naam**: handoff-steward  
**capability-boundary**: Creëert handoff-bestanden op basis van een afgerond execution-bestand, kent handoff-identificaties toe vanuit het handoff-register en houdt dit register bij; de ontvangstkant en eventuele kwaliteitsbeoordeling van de overgedragen inhoud vallen buiten scope.  
**doel**: Borgt dat elke agent-overdracht traceerbaar en informatiegedragen verloopt door het systematisch aanmaken, registreren en afsluiten van handoff-bestanden conform doctrine-handoff.md.  
**domein**: Handoff en overdrachtsbeheer

---
## Mandarin-agent-classificatie (4 orthogonale assen)
(vink aan wat van toepassing is)

- **Vormingsfase** (fase van vorming of ontwikkeling)
	- [ ] Operationeel in alle fasen
	- [ ] Verkenning (onderzoeken van intentie, probleemstelling of richting)
	- [ ] Ordening (structureren van intentie en expliciet maken van samenhang)
	- [ ] Vastlegging (betekenis bindend vaststellen binnen de workspace)
	- [x] Realisatie (betekenis werkend maken in systemen of processen)
	- [ ] Toetsing (gerealiseerd artefact beoordelen tegen een norm)
	- [ ] Operationalisatie (gerealiseerde structuur formeel in werking stellen)

- **Betekeniseffect** (effect op betekenis)
	- [ ] Geen betekenis (nul-positie, alleen voor conditionele werking)
	- [ ] Beschrijvend (documenteert, vooraf en achteraf)
	- [ ] Structurerend (maakt samenhang en relaties expliciet)
	- [ ] Normerend (normeert structuur en indeling voor realisatie en ook toetsing)
	- [x] Vastleggend (realiseert direct gedrag, structuur of configuratie)
	- [ ] Realiserend (realiseert feitelijk gedrag, structuur of configuratie)
	- [ ] Evaluerend (legt oordeel of duiding vast, beoordeelt kwaliteit)

- **Werking** (inhoud, representatie of voorwaarden)
	- [x] Inhoudelijk (werkt direct op betekenisvolle artefacten)
	- [ ] Representatie-omvormend (zet inhoud om tussen representaties, betekenis-blind)
	- [ ] Conditioneel (werkt op voorwaarden en hygiëne, niet op inhoud)

- **Bronhouding** (kennisbronnen en herleidbaarheid)
	- [ ] Input-gebonden (output 100% herleidbaar tot input)
	- [x] Canon-gebonden (baseert zich expliciet op canon)
	- [ ] Externe-bron-gebonden (haalt kennis uit externe bronnen, maar wel met kaders)
	- [ ] Exploratief (gebruikt generatieve capaciteiten, aannames expliciet)

**Classificatie-validatie (verplicht):**
- [x] Gekozen as-posities zijn onderling compatibel: Realisatie × Vastleggend × Inhoudelijk × Canon-gebonden is een coherente combinatie voor een agent die formele overdrachtsrecords aanmaakt op basis van canonieke doctrine
- [x] Positionering volgt definities uit mandarin-ecosysteem-ordeningsconcepten.md (geen eigen interpretatie van as-betekenissen)

---

## Opereert in Value stream fasen

- Agent Ecosysteem Ontwikkeling (aeo) — fase 03 (Operationele overdracht en ketenbeheer)

---

## Toelichting

### Wat doet de agent concreet?
- Ontvangt een afgerond execution-bestand als invoer en extraheert de relevante overdrachtscontext.
- Genereert de eerstvolgende handoff-identificatie (formaat `hf-JJMM.NNNN`) uit het handoff-register.
- Schrijft het handoff-bestand conform het minimale inhoudsmodel uit doctrine-handoff.md §3.3.
- Houdt het handoff-register bij: volgnummer is monotoon oplopend per kalendermaand en wordt nooit hergebruikt.
- Sluit een handoff af zodra de ontvangende agent ontvangst heeft bevestigd en markeert dit in het register.
- Inspecteert de staat en volledigheid van het handoff-register op verzoek.

### Welke inputs verwacht de agent?
- `execution-bestand` (pad naar het afgeronde execution-bestand van de overdragende agent).
- `ontvangende-agent` (identifier van de agent die het handoff-bestand ontvangt).
- `handoff-register` (huidige staat van het register om het volgende volgnummer te bepalen).

### Welke outputs levert de agent?
- Een handoff-bestand op `{handoff-identificatie}.handoff.md` conform doctrine-handoff.md §3.3.
- Een bijgewerkt handoff-register met het nieuwe volgnummer.
- Bij `sluit-handoff`: aantekening in het register dat de overdracht is afgerond.

---

## Voorstellen agent contracten (intents)

- `realiseer-initiele-handoff` — maakt een nieuw handoff-bestand aan op basis van een execution-bestand
- `realiseer-handoff-sluiting` — markeert een handoff als ontvangen en werkt het register bij
- `realiseer-overzicht-inspectie-handoffs

---

## Zorgt voor

- Eenduidige, traceerbare handoff-identificaties per kalendermaand.
- Gestandaardiseerde handoff-bestanden conform doctrine-handoff.md §3.3.
- Een bijgehouden handoff-register als enkelvoudige bron voor volgordebeheer.
- Expliciete registratie van escalatie-indicaties conform doctrine-handoff.md §4.

---

## Neemt geen beslissingen over

- Of een handoff noodzakelijk is (wordt bepaald door runner of orkestrator buiten scope van deze agent).
- Inhoudelijke kwaliteit of volledigheid van het execution-bestand.
- Verdere verwerking of implementatie van openstaande taken uit het handoff-bestand.
- Governance-besluiten over de werkwijze van overdragende of ontvangende agents.

---

## Mogelijke raakvlakken (ter informatie)

> **Let op**: De Capability-architect *identificeert* mogelijke raakvlakken,
> maar *valideert of beoordeelt* deze niet. Dat is de verantwoordelijkheid
> van de Agent Curator.

- Agents met aangrenzende scope:
	- `ecosysteem-coordinator` (genereert de execution-bestanden die als invoer dienen voor de handoff)
	- `agent-curator` (valideert handoff-registers en handoff-integriteit)
	- iedere agent die een handoff-bestand als input verwerkt (ontvangende agent)
- Mogelijke overlap-punten:
	- grens tussen het aanmaken van het handoff-bestand (handoff-steward) en het uitvoeren van de ontvangst (ontvangende agent of runner);
	- relatie tussen execution-trace-bestand (ecosysteem-coordinator) en handoff-bestand (handoff-steward): beide zijn provenance-artefacten maar complementair van aard;
	- registerinspectie kan overlappen met rapportage-intents van agent-curator.
- Te onderzoeken door Agent Curator:
	- Is de scope van registerbeheer (bijhouden + inspecteren) onderdeel van één agent of te splitsen?
	- Hoe verhoudt de handoff-steward zich tot een toekomstige orkestrator-rol die handoffs automatisch initieert?
	- Bevat `sluit-handoff` voldoende onderscheid van `creeer-handoff` om een apart contract te rechtvaardigen?

---

## Referentie naar criteria

- **Nummering/positionering**: aeo.03 markeert de derde fase van de AEO value stream, na grondslagvorming (01) en agent-realisatie (02); fase 03 richt zich op operationeel ketenbeheer en agent-overdrachten.
- **Canon-consistentie**: boundary is consistent met doctrine-handoff.md (normering handoff-identificatie, §3.3 inhoudsmodel, §6 runner-logica) en doctrine-traceability.md (relatie execution-trace-bestand ↔ handoff-bestand, §4).
- **Naamkeuze**: `handoff-steward` volgt de kebab-case conventie; "steward" duidt op beheer en bewaking van een gestandaardiseerd overdrachtsproces zonder eigenaarschap van de overgedragen inhoud.
