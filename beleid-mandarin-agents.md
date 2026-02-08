
# Beleid voor de MANDARIN-AGENTS workspace

Deze workspace hoort bij de waardestroom **AGENT ECOSYSTEEM ONTWIKKELING (AEO)**.

## Verplichte leesvolgorde van grondslagen

Elke geautomatiseerde rol, agent of runner hanteert bij aanvang van zijn functioneren de volgende verplichte leesvolgorde:

**In de centrale canon repository** (`https://github.com/hans-blok/mandarin-canon.git`):
1. `grondslagen/0.algemeen/constitutie.md`
2. overige algemene grondslagen binnen `grondslagen/0.algemeen/`
3. grondslagen van de expliciet toegewezen value stream

**In deze workspace**:
4. workspace-specifiek beleid (dit bestand)

Het overslaan, herordenen of impliciet toepassen van deze leesvolgorde is niet toegestaan.

**Zonder aantoonbare toepassing van de constitutie is handelen ongeldig.**

## Dit beleid is workspace-specifiek

Dit beleid beschrijft alleen de workspace-specifieke scope. Voor alle regels, uitzonderingen, details en constitutionele bepalingen volgen we volledig de richtlijnen in `hans-blok/mandarin-canon`.

De constitutie, algemene regels en governance voor alle workspaces staan in:
- https://github.com/hans-blok/mandarin-canon.git

## Canon Repository Synchronisatie

In alle geautomatiseerde en handmatige processen wordt de centrale canon repository geraadpleegd. Dit gebeurt altijd eerst met een `git pull` om te waarborgen dat de meest recente grondslagen worden gebruikt.

**Foutmelding**: Wanneer de mandarin-canon-repository niet bereikbaar is of niet kan worden gevonden, wordt een foutmelding gegeven en stopt het proces.

## Scope

### Wat we in deze workspace vastleggen

- **Agent-ontwerp en -implementatie**: Alle artefacten voor het ontwerpen, bouwen en beheren van AI-agents volgens de Mandarin-methodiek
- **Agent boundaries en capabilities**: Definities van wat agents wel en niet doen, inclusief capability boundaries en scope-afbakeningen
- **Agent charters en contracten**: Formele specificaties van agent-rollen, verantwoordelijkheden en interfaces
- **Prompt-engineering en agent-prompts**: YAML-metadata en prompt-structuren voor agent-aanroep
- **Agent runners en orchestratie**: Python-scripts voor het uitvoeren en beheren van agent-lifecycles
- **Templates en standaarden**: Herbruikbare sjablonen voor consistent agent-ontwerp
- **Workspace-governance**: Beleid, procedures en kwaliteitsnormen specifiek voor agent-development
- **Agent-publicatie**: JSON-schemas en overzichten voor het delen van agents tussen workspaces

### Wat niet in deze workspace hoort

Andere domeinen vallen buiten deze workspace en horen in andere repositories. Voorbeelden hiervan zijn:
- **Business domeinlogica**: Specifieke bedrijfsprocessen, domeinkennis en business rules horen in domein-specifieke workspaces
- **Software ontwikkeling**: Applicatie-code, databases, API's en technische implementaties horen in SFW-workspaces (Software-ontwikkeling)
- **Enterprise architectuur**: C4-modellen, ArchiMate-diagrammen en architectuur-artefacten horen in AOD-workspaces (Architectuur- en Oplossingsontwerp)
- **Content en publicaties**: Artikelen, essays, handleidingen en communicatie-materiaal horen in KVL-workspaces (Kennisverwerving en -verspreiding)
- **Strategische analyse**: Marktonderzoek, business cases en investeringsbeslissingen horen in MIV-workspaces (Markt- en Investeringsvorming)
- **Infrastructuur en tooling**: Server-configuratie, deployment-pipelines en basis-tooling horen in FND-workspaces (Foundation)

## Workspace-specifieke aanvullingen

- **Agent-naamgeving**: Alle agents volgen de conventie `{value-stream}.{fase}.{agent-naam}` voor folder-structuur en een lowercase-hyphen-separated naamgeving voor agent-namen
- **Traceerbaarheid**: Elk agent-artefact (charter, contract, prompt) moet traceerbaar zijn naar governance-documenten en canonical bronnen via expliciete verwijzingen
- **JSON Schema conformiteit**: Alle JSON-output (zoals agents-publicatie.json) moet valideren tegen de gedefinieerde schemas in de `/schemas` folder
- **Markdown-kwaliteit**: Alle documentatie gebruikt B1-taalniveau en volgt de Mandarin-stijlgids voor leesbaarheid en consistentie
- **Logging en audit**: Elke handmatige agent-initialisatie wordt gelogd conform Norm 10.4 met paden van gelezen, gewijzigde en aangemaakte bestanden
- **Version control**: Alle agent-wijzigingen worden gedocumenteerd in charter Change Logs met datum, versie, wijziging en auteur
- **Template-usage**: Alle nieuwe agent-artefacten gebruiken de verplichte templates uit de `/templates` folder voor consistentie

---

*Laatste update: 2026-02-08 door Hans Blok*
