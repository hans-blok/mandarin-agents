---
workspace: mandarin-agents
value_stream: aeo
value_stream-fasen: ["fnd.01", "aeo.01", "aeo.02", "aeo.03"]
canon_github_url: https://github.com/hans-blok/mandarin-canon.git

# Grondslagen-patronen per value stream voor canon consultatie
grondslagen:
  aeo: "grondslagen/.algemeen/*,grondslagen/aeo/*"
---

# Beleid voor de MANDARIN-AGENTS workspace

Deze workspace hoort bij de waardestroom **AGENT ECOSYSTEEM ONTWIKKELING (AEO)**.

## Verplichte leesvolgorde van grondslagen

Elke geautomatiseerde rol, agent of runner hanteert bij aanvang van zijn functioneren de volgende verplichte leesvolgorde:

**In de centrale canon repository** (`https://github.com/hans-blok/mandarin-canon.git`):
1. `grondslagen/.algemeen/constitutie.md`
2. overige algemene grondslagen binnen `grondslagen/.algemeen/`
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

## Convention over Configuration

Deze workspace hanteert het principe **Convention over Configuration** (*charter-driven self-discovery*):

- **Minimale invoer**: Agents en runners verwachten alleen de strikt noodzakelijke parameters van de gebruiker (typisch alleen `agent_naam`).
- **Automatische ontdekking**: Alle overige artefacten — boundary, charter, templates, intents, referenties — worden automatisch afgeleid uit de folder-structuur en naamconventies.
- **Charter als beleidsbron**: Het charter van een agent bepaalt welke artefacten relevant zijn voor die agent. De boundary bepaalt welke intents bestaan.
- **Geen redundante invoer**: Parameters die uit conventie of charter af te leiden zijn, worden niet aan de gebruiker gevraagd.

## Workspace-specifieke aanvullingen

- **Agent-naamgeving**: Alle agents volgen de conventie `{value-stream}.{fase}.{agent-naam}` voor folder-structuur en een lowercase-hyphen-separated naamgeving voor agent-namen
- **Agent-artefacten organisatie**: Normerende artefacten die agents beschrijven worden gestructureerd vastgelegd in de `/artefacten` folder volgens de volgende conventie:
  - **Parent folder** (`artefacten/{vs}/{vs}.{fase}.{agent-naam}/`): Bevat charter (`.charter.md`), boundary (`.boundary.md`), doctrine en runner-scripts (`.runner.py`)
  - **Subfolder `/templates`**: Bevat herbruikbare templates voor prompt, contract, charter en runner
  - **Subfolder `/agent-contracten`**: Bevat alle agent-contract beschrijvingen (`.agent.md`) per intent
  - **Subfolder `/prompts`**: Bevat alle prompt-bestanden (`.prompt.md`) per intent
  - **Voorbeeld**: `artefacten/aeo/aeo.02.agent-ontwerper/` met subfolders `templates/`, `agent-contracten/` en `prompts/`
  - Deze structuur zorgt ervoor dat gelijksoortige artefact-types bij elkaar staan en de parent folder overzichtelijk blijft
- **Traceerbaarheid**: Elk agent-artefact (charter, contract, prompt) moet traceerbaar zijn naar governance-documenten en canonical bronnen via expliciete verwijzingen
- **JSON Schema conformiteit**: Alle JSON-output (zoals agents-publicatie.json) moet valideren tegen de gedefinieerde schemas in de `/schemas` folder
- **Markdown-kwaliteit**: Alle documentatie gebruikt B1-taalniveau en volgt de Mandarin-stijlgids voor leesbaarheid en consistentie
- **Prompt-frontmatter werkbronnen en afnemers**: Prompt-bestanden declareren zowel hun inputs als hun downstream consumers in de YAML frontmatter:
  - `werkbronnen`: bestanden die de runner ophaalt als input (zie CLAUDE.md voor lookup-strategieën)
  - `afnemers`: downstream agents die de output van deze intent consumeren — de spiegelstructuur van `werkbronnen`. Schema per entry:
    ```yaml
    afnemers:
      - agent: {agent-naam}          # kebab-case agent-id van de ontvanger
        intent: {intent-naam}        # specifieke intent; "*" = alle intents
        consumes:
          type: {artefact-type}      # matcht output[].type in het contract van deze agent
          required: true             # is de ontvanger geblokkeerd zonder dit artefact
    ```
  - De `type`-waarde in `afnemers[].consumes` MOET overeenkomen met een `type` in de `output`-specificatie van het bijbehorende agent-contract
  - `afnemers` hoort in de **prompt** (uitvoeringsbedrading), niet in het contract (stabiele capability)
- **Logging en audit**: Elke handmatige agent-initialisatie wordt gelogd conform Norm 10.4 met paden van gelezen, gewijzigde en aangemaakte bestanden
- **Version control**: Alle agent-wijzigingen worden gedocumenteerd in charter Change Logs met datum, versie, wijziging en auteur
- **Template-usage**: Alle nieuwe agent-artefacten gebruiken de verplichte templates uit de `/templates` folder voor consistentie

---

*Laatste update: 2026-03-29 door GitHub Copilot*
