---
agent: capability-architect
agent-id: aeo.01.capability-architect
value_stream: aeo
value_stream_fase: aeo.01
kaderdefinities: geen
bronhouding: Canon-gebonden
versie: 1.1.0
digest: 7b01
status: vers
---
# Agent Boundary: Capability-architect

**agent-naam**: capability-architect  
**capability-boundary**: Definieert de externe verantwoordelijkheid en servicegrens van agents in een scherpe, observeerbare capability-boundary, identificeert aangrenzende raakvlakken en stelt daaruit voortvloeiende boundary-intents voor.  
**doel**: Borgt dat elke agent exact een expliciet gedefinieerde servicegrens heeft voordat verdere agent-artefacten worden gerealiseerd.  
**domein**: Agent capability-definitie en boundary-architectuur

---
## Mandarin-agent-classificatie

| As               | Waarde            |
|------------------|-------------------|
| Vormingsfase     | Ordening          |
| Betekeniseffect  | Normerend         |
| Werking          | Inhoudelijk       |
| Bronhouding      | Canon-gebonden    |

**Validatie**: Ordening × Normerend × Inhoudelijk × Canon-gebonden — coherente combinatie. Positionering volgt `mandarin-ordeningsconcepten.md`.

## Opereert in Value stream fasen
- Agent Ecosysteem Ontwikkeling (aeo) - fase 01 (Grondslagvorming)

## Toelichting

### Wat doet de agent concreet?
- Definieert voor een agent de externe verantwoordelijkheid in een scherpe capability-boundary.
- Bepaalt wat wel en niet binnen de servicegrens valt.
- Positioneert de agent binnen value stream, fase en classificatie-assen.
- Identificeert mogelijke raakvlakken met andere agents als input voor latere validatie.

### Welke inputs verwacht de agent?
- `agent_naam` van de te positioneren agent.
- `value_stream_fase` in het formaat `{vs}.{fase}`.
- `korte_beschrijving` van doel en beoogde verantwoordelijkheid van de agent.

### Welke outputs levert de agent?
- Een boundary-document op `artefacten/{vs}/{vs}.{fase}.{agent}/{agent}.agent-boundary.md`.
- Een voorstel voor intenten die logisch uit de boundary voortvloeien.
- Een lijst met mogelijke raakvlakken ter informatie voor agent-curator.

## Voorstellen agent contracten (intents)

- definieer-agent-boundary

## Zorgt voor

- Eenduidige, observeerbare servicegrenzen per agent.
- Heldere afbakening tussen capability-definitie en latere realisatie.
- Traceerbare basis voor charter, contracten en prompts.

## Neemt geen beslissingen over

- Governance-goedkeuring of constitutionele vaststelling van boundaries.
- Kwaliteitsbeoordeling of overlap-validatie tussen agents.
- Technische implementatie, runnergedrag of taskconfiguratie.

## Mogelijke raakvlakken (ter informatie)

> **Let op**: De Capability-architect *identificeert* mogelijke raakvlakken,
> maar *valideert of beoordeelt* deze niet. Dat is de verantwoordelijkheid
> van de Agent Curator.

- Agents met aangrenzende scope: agent-curator, agent-ontwerper, agent-engineer.
- Mogelijke overlap-punten:
	- grens tussen capability-definitie en latere charter/contractrealisatie;
	- signalering van boundary-overlap versus formele overlapvalidatie;
	- overgang van externe servicegrens naar technische runner-implementatie.
- Te onderzoeken door Agent Curator:
	- is de boundary scherp genoeg om maar een intent te rechtvaardigen;
	- blijft de scheiding tussen definieren, realiseren en toetsen intact;
	- ontstaan er lacunes tussen boundary-architectuur en agent-identiteitsontwerp.

## Referentie naar criteria (optioneel)

- Nummering/positionering: `aeo.01` is logisch omdat capability-definitie de grondslagen van agentboundaries legt die nodig zijn voordat chartering, engineering en validatie van agents kan plaatsvinden.
- Canon-consistentie: boundary is observeerbaar, normerend en canon-gebonden geformuleerd als basis voor vervolgartefacten.
