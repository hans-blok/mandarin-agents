# Beleid voor de <workspace-naam> workspace

Deze workspace hoort bij de waardestroom **<value-stream-naam>**.

## Scope

- Deze workspace gaat over <korte beschrijving van de scope en doelen van deze workspace>.
- Andere domeinen (zoals <voorbeelden van zaken die niet in deze workspace horen>) vallen buiten deze workspace en horen in andere repositories.

**Value Stream**  
Deze workspace hoort bij de waardestroom **<value-stream-naam>**.

## Richtlijnen

**Constitutie (verplicht)**

De constitutie, algemene regels en governance voor alle workspaces staan in:

- https://github.com/hans-blok/mandarin-canon.git

1. **Canon Repository Synchronisatie**: In alle geautomatiseerde en handmatig processen wordt daarom de centrale canon repository (`https://github.com/hans-blok/mandarin-canon.git`) geraadpleegd. Dit gebeurt altijd eerst met een `git pull`. Dit om te waarborgen dat de meest recente grondslagen worden gebruikt.

**Foutmelding**: Wanneer de mandarin-canon-repository niet bereikbaar is of niet kan worden gevonden, wordt een foutmelding gegeven en stopt het proces.

## Dit beleid is workspace-specifiek

Dit beleid beschrijft alleen de workspace-specifieke scope. Voor alle regels, uitzonderingen, details en constitutionele bepalingen volgen we volledig de richtlijnen in `hans-blok/mandarin-canon`.

<Optionele workspace-specifieke aanvullingen zoals:
- Specifieke werkwijzen voor deze workspace
- Bijzondere afhankelijkheden of integraties
- Workspace-specifieke automatiseringen
- etc.>

---

## Instructies voor gebruik van dit template

1. Vervang `<workspace-naam>` met de naam van je workspace (bijvoorbeeld: "kennispublicatie", "architectuur-ontwerp")
2. Vervang `<value-stream-naam>` met de juiste value stream naam (bijvoorbeeld: "agent-enablement", "markt-en-investeringsvorming", "kennisverwerving-en-verspreiding")
3. Vervang `<korte beschrijving van de scope en doelen van deze workspace>` met een concrete beschrijving van wat deze workspace wel en niet doet
4. Vervang `<voorbeelden van zaken die niet in deze workspace horen>` met specifieke voorbeelden
5. Voeg eventuele workspace-specifieke aanvullingen toe in de laatste sectie
6. Verwijder deze instructiesectie na het invullen

### Value Stream Opties

Bekende value streams:
- **AEO** (Agent Enablement & Orchestratie): Het ontwerpen, bouwen en beheren van agents
- **SFW** (Software-ontwikkeling): Software architectuur, development, testen
- **AOD** (Architectuur- en Oplossingsontwerp): Enterprise architectuur, C4-modellen, ArchiMate
- **KVL** (Kennisverwerving en -verspreiding): Publicaties, artikelen, essays, communicatie
- **MIV** (Markt- en Investeringsvorming): Strategie, marktverkenning, business cases
- **FND** (Foundation): Basis tooling, workspace management, engineering support
