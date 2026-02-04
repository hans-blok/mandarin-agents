## 1. Samenvatting ordentaak

- **Agent-naam**: niam-analist  
- **Oorspronkelijke value stream** (charter + boundary): "veranderverkenning" (niet canoniek in mandarin-value-streams-en-fasen)  
- **Gekozen canonieke value stream/fase**: Softwareontwikkeling (SFW), fase 01  Veranderkenning  
- **Bron-artefactlocatie**: `artefacten/veranderverkenning/...` en agent-boundary in `agent-boundaries/`  
- **Nieuwe per-agentfolder**: `artefacten/sfw.01.niam-analist/`

Deze notitie beschrijft de **uitgevoerde ordening** voor niam-analist: alle agent-specifieke artefacten zijn ondergebracht in een per-agentfolder onder `artefacten/` en de value stream is gealigneerd op de canon `Softwareontwikkeling (SFW, fase 01 - Veranderkenning)`.

## 2. Gevonden artefacten (bronsituatie)

### 2.1 Contracts

Bronpaden in `artefacten/veranderverkenning/agents/`:

| Type      | Huidig pad                                                                                          |
|-----------|-----------------------------------------------------------------------------------------------------|
| contract  | artefacten/veranderverkenning/agents/niam-analist.verzamel-bronnen.agent.md                        |
| contract  | artefacten/veranderverkenning/agents/niam-analist.verken-begrippen.agent.md                        |
| contract  | artefacten/veranderverkenning/agents/niam-analist.analyseer-feiten.agent.md                        |
| contract  | artefacten/veranderverkenning/agents/niam-analist.valideer-consistentie.agent.md                   |
| contract  | artefacten/veranderverkenning/agents/niam-analist.onderbouw-methodiek.agent.md                     |

### 2.2 Prompts

Bronpaden in `artefacten/veranderverkenning/prompts/`:

| Type    | Huidig pad                                                                                                |
|---------|-----------------------------------------------------------------------------------------------------------|
| prompt  | artefacten/veranderverkenning/prompts/mandarin.niam-analist.verzamel-bronnen.prompt.md                  |
| prompt  | artefacten/veranderverkenning/prompts/mandarin.niam-analist.verken-begrippen.prompt.md                  |
| prompt  | artefacten/veranderverkenning/prompts/mandarin.niam-analist.analyseer-feiten.prompt.md                  |
| prompt  | artefacten/veranderverkenning/prompts/mandarin.niam-analist.valideer-consistentie.prompt.md             |
| prompt  | artefacten/veranderverkenning/prompts/mandarin.niam-analist.onderbouw-methodiek.prompt.md               |

### 2.3 Charter

Bronpad in `artefacten/veranderverkenning/charters-agents/`:

| Type    | Huidig pad                                                                                     |
|---------|------------------------------------------------------------------------------------------------|
| charter | artefacten/veranderverkenning/charters-agents/niam-analist.charter.md                          |

### 2.4 Boundary

Boundary-document:

- [agent-boundaries/agent-boundary-niam-analist.md](agent-boundaries/agent-boundary-niam-analist.md)

Samenvattend gaf de boundary als value stream "Veranderverkenning" en vroeg expliciet om governance-validatie van deze positionering.

## 3. Canon-context (value streams en fasen)

Volgens [temp/mandarin-value-streams-en-fasen.md](temp/mandarin-value-streams-en-fasen.md):

- Canonieke value stream voor "Veranderkenning" is **Softwareontwikkeling (SFW)**, fase **01 Veranderkenning**.
- Er bestaat geen zelfstandige value stream "veranderverkenning"; dit is een fase in SFW.

De ordening vertaalt daarom de historische aanduiding "veranderverkenning" naar de canonieke SFW-fase 01 Veranderkenning.

## 4. Nieuwe doelstructuur (per-agentfolder)

Gekozen is voor positionering als **SFW fase 01 agent (Veranderkenning)**.

- **Per-agentfolder**: `artefacten/sfw.01.niam-analist/`

Kernartefacten in de nieuwe structuur:

| Artefacttype | Canoniek pad                                                                                 |
|--------------|----------------------------------------------------------------------------------------------|
| contract     | artefacten/sfw.01.niam-analist/niam-analist.verzamel-bronnen.agent.md                        |
| contract     | artefacten/sfw.01.niam-analist/niam-analist.verken-begrippen.agent.md                        |
| contract     | artefacten/sfw.01.niam-analist/niam-analist.analyseer-feiten.agent.md                        |
| contract     | artefacten/sfw.01.niam-analist/niam-analist.valideer-consistentie.agent.md                   |
| contract     | artefacten/sfw.01.niam-analist/niam-analist.onderbouw-methodiek.agent.md                     |
| prompt       | artefacten/sfw.01.niam-analist/mandarin.niam-analist.verzamel-bronnen.prompt.md              |
| prompt       | artefacten/sfw.01.niam-analist/mandarin.niam-analist.verken-begrippen.prompt.md              |
| prompt       | artefacten/sfw.01.niam-analist/mandarin.niam-analist.analyseer-feiten.prompt.md              |
| prompt       | artefacten/sfw.01.niam-analist/mandarin.niam-analist.valideer-consistentie.prompt.md         |
| prompt       | artefacten/sfw.01.niam-analist/mandarin.niam-analist.onderbouw-methodiek.prompt.md           |
| charter      | artefacten/sfw.01.niam-analist/niam-analist.charter.md                                       |

## 5. Uitgevoerde verplaatsingen en aanpassingen

### 5.1 Bestandsverplaatsingen (van veranderverkenning naar SFW.01)

Van  Naar:

- artefacten/veranderverkenning/agents/niam-analist.verzamel-bronnen.agent.md  
   artefacten/sfw.01.niam-analist/niam-analist.verzamel-bronnen.agent.md
- artefacten/veranderverkenning/agents/niam-analist.verken-begrippen.agent.md  
   artefacten/sfw.01.niam-analist/niam-analist.verken-begrippen.agent.md
- artefacten/veranderverkenning/agents/niam-analist.analyseer-feiten.agent.md  
   artefacten/sfw.01.niam-analist/niam-analist.analyseer-feiten.agent.md
- artefacten/veranderverkenning/agents/niam-analist.valideer-consistentie.agent.md  
   artefacten/sfw.01.niam-analist/niam-analist.valideer-consistentie.agent.md
- artefacten/veranderverkenning/agents/niam-analist.onderbouw-methodiek.agent.md  
   artefacten/sfw.01.niam-analist/niam-analist.onderbouw-methodiek.agent.md

- artefacten/veranderverkenning/prompts/mandarin.niam-analist.verzamel-bronnen.prompt.md  
   artefacten/sfw.01.niam-analist/mandarin.niam-analist.verzamel-bronnen.prompt.md
- artefacten/veranderverkenning/prompts/mandarin.niam-analist.verken-begrippen.prompt.md  
   artefacten/sfw.01.niam-analist/mandarin.niam-analist.verken-begrippen.prompt.md
- artefacten/veranderverkenning/prompts/mandarin.niam-analist.analyseer-feiten.prompt.md  
   artefacten/sfw.01.niam-analist/mandarin.niam-analist.analyseer-feiten.prompt.md
- artefacten/veranderverkenning/prompts/mandarin.niam-analist.valideer-consistentie.prompt.md  
   artefacten/sfw.01.niam-analist/mandarin.niam-analist.valideer-consistentie.prompt.md
- artefacten/veranderverkenning/prompts/mandarin.niam-analist.onderbouw-methodiek.prompt.md  
   artefacten/sfw.01.niam-analist/mandarin.niam-analist.onderbouw-methodiek.prompt.md

- artefacten/veranderverkenning/charters-agents/niam-analist.charter.md  
   artefacten/sfw.01.niam-analist/niam-analist.charter.md

De bronbestanden onder `artefacten/veranderverkenning/...` zijn na succesvolle kopie verwijderd.

### 5.2 Charter-aanpassingen

In de nieuwe charter [artefacten/sfw.01.niam-analist/niam-analist.charter.md](artefacten/sfw.01.niam-analist/niam-analist.charter.md):

- Value Stream gewijzigd van "veranderverkenning" naar:  
  `softwareontwikkeling (SFW, fase 01 - Veranderkenning)`.
- Traceerbaarheid bijgewerkt naar paden onder `artefacten/sfw.01.niam-analist/` voor alle intents en prompts.
- Historische verwijzingen naar `exports/veranderverkenning/...` zijn vervangen door de nieuwe artefactpaden.
- Change Log uitgebreid met een nieuwe entry (2026-02-04, versie 0.3.0) die de ordening en padaanpassing beschrijft.

### 5.3 Prompt- en contract-aanpassingen

- Voor alle prompts is een nieuw frontmatter-bestand aangemaakt in de per-agentfolder met:
  - `agent: niam-analist`
  - `intent: <intent>`
  - `charter_ref: @main:artefacten/sfw.01.niam-analist/niam-analist.charter.md`
- De contracten zijn - overgenomen qua semantiek, maar verwijzen in documentatie en traceerbaarheid nu naar de charter in `artefacten/sfw.01.niam-analist/`.

### 5.4 Boundary-aanpassing

In [agent-boundaries/agent-boundary-niam-analist.md](agent-boundaries/agent-boundary-niam-analist.md) is:

- De waarde voor **Value Stream** aangepast van "Veranderverkenning" naar:  
  `Softwareontwikkeling (SFW, fase 01 - Veranderkenning)`.
- Overige boundary-tekst (capability-boundary, toelichting, overlap-analyse) inhoudelijk ongewijzigd gelaten.

## 6. Aannames en resterende aandachtspunten

Belangrijkste aannames bij deze ordening:

- De oorspronkelijke aanduiding "veranderverkenning" in boundary en charter wordt geïnterpreteerd als de canonieke SFW-fase **01 Veranderkenning**.
- NIAM-analist wordt gezien als uitvoerende analyse-agent binnen SFW.01 (Veranderkenning), niet als AOD-agent; architectonische beslissingen blijven bij architectuur-agents.
- Historische resultaten onder `docs/resultaten/niam-analist/` blijven op die locatie; de ordening richt zich op contracten/prompts/charter, niet op bestaande resultaatbestanden.

Openstaande punten (niet blokkerend voor ordening):

- Optioneel kan een korte README in `docs/resultaten/niam-analist/` worden toegevoegd die verwijst naar de nieuwe per-agentfolder `artefacten/sfw.01.niam-analist/`.

---

_Dit verslag is opgesteld door agent-smeder (intent `4.orden-agent`) en beschrijft de **feitelijk uitgevoerde** migratie van niam-analist naar de canonieke value stream Softwareontwikkeling (SFW, fase 01 Veranderkenning)._ 
