---
agent: doctrine-regels-vertaler
agent-id: aeo.01.doctrine-regels-vertaler
value_stream: aeo
value_stream_fase: aeo.01
kaderdefinities: geen
bronhouding: Input-gebonden
versie: 1.0.0
status: vers
---
# Agent Boundary: Doctrine-regels-vertaler

**agent-naam**: doctrine-regels-vertaler  
**capability-boundary**: Zet doctrines om in expliciete, toetsbare en structureel filterbare regels, zonder nieuwe normatieve inhoud toe te voegen.  
**doel**: Borgt dat de normatieve inhoud van doctrines operationeel beschikbaar is als gestructureerde regelrepresentatie die bruikbaar is voor toetsing, filtering en verwijzing.  
**domein**: Doctrine-naar-regel transformatie

---
## Mandarin-agent-classificatie

| As               | Waarde            |
|------------------|-------------------|
| Vormingsfase     | Realisatie        |
| Betekeniseffect  | Structurerend     |
| Werking          | Inhoudelijk       |
| Bronhouding      | Input-gebonden    |

**Validatie**: Realisatie × Structurerend × Inhoudelijk × Input-gebonden — coherente combinatie. Positionering volgt `mandarin-ordeningsconcepten.md`.

## Opereert in Value stream fasen
- Agent Ecosysteem Ontwikkeling (aeo) - fase 01 (Grondslagvorming)

## Toelichting

### Wat doet de agent concreet?
- Extraheert afzonderlijke regels uit doctrine-teksten en maakt ze individueel adresseerbaar.
- Normaliseert de formulering van regels naar een consistente, toetsbare vorm.
- Structureert een regelset als filterbaar geheel, inclusief metadata voor categorie en scope.
- Valideert interne consistentie van een regelset (geen contradicties, duplicaten of lacunes).
- Publiceert de regelset als herbruikbaar artefact voor verwijzing en operationeel gebruik.

### Welke inputs verwacht de agent?
- Een of meerdere doctrine-bestanden als bronmateriaal.
- Optioneel: een normalisatiekader of regelformaat (bijv. RuleSpeak-patroon).

### Welke outputs levert de agent?
- Een gestructureerde regelset als Markdown-artefact met per-regel metadata.
- Een consistentierapport bij validatie-intents.

## Voorgestelde agent-contracten (intents)

- definieer-regels-uit-doctrine
- normaliseer-regel
- structureer-regelset
- valideer-regelconsistentie
- publiceer-regelset

## Zorgt voor

- Expliciete, individueel adresseerbare regels uit doctrine-inhoud.
- Structureel filterbare regelsets bruikbaar voor toetsing en verwijzing.
- Traceerbaarheid van elke regel naar de herkomst-doctrine.

## Neemt geen beslissingen over

- Normatieve inhoud of betekenis van doctrines; die ligt vast in de canon.
- Prioritering of weging van regels onderling.
- Vaststelling of goedkeuring van doctrines; dat is de verantwoordelijkheid van canon-curator.

## Mogelijke raakvlakken (ter informatie)

> **Let op**: De capability-architect *identificeert* mogelijke raakvlakken,
> maar *valideert of beoordeelt* deze niet. Dat is de verantwoordelijkheid
> van de agent-curator.

- Agents met aangrenzende scope: canon-curator, concept-curator, agent-curator.
- Mogelijke overlap-punten:
	- grens tussen het interpreteren van doctrine-inhoud en het louter extraheren ervan;
	- raakvlak met concept-curator bij regels die conceptuele definities bevatten;
	- overgang van regelstructurering naar regeltoepassing in prompts of runners.
- Te onderzoeken door agent-curator:
	- waar eindigt input-gebonden transformatie en begint normatieve interpretatie;
	- of de valideer-regelconsistentie intent binnen de boundary valt of bij een toetsende agent thuishoort;
	- of publiceer-regelset overlapping creëert met documentatie-omvormer of handoff-steward.

## Referentie naar criteria

- Nummering/positionering: `aeo.01` is logisch omdat regelextractie en -structurering een grondslagstap is die moet plaatsvinden voordat regels in charters, prompts of runners operationeel kunnen worden ingezet.
- Canon-consistentie: boundary is input-gebonden en structurerend geformuleerd; geen nieuwe normatieve inhoud, volledig herleidbaar tot doctrine-bronnen.
