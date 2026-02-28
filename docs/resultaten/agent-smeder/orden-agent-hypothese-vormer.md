# Ordeningsvoorstel agent **hypothese-vormer** (SFW fase 01 - Veranderkenning)

## 1. Samenvatting ordentaak

- **Agent-naam**: hypothese-vormer  
- **Huidige value stream** (volgens charter): veranderverkenning  
- **Canonieke value stream/fase**: Softwareontwikkeling (SFW) – fase 01 Veranderkenning  
- **Doel-locatie** (per-agentfolder): `artefacten/sfw.01.hypothese-vormer/`  

Doel van deze ordentaak is om alle bestaande artefacten van hypothese-vormer (charter, contracts, prompts, resultaten) te herleiden, en een voorstel te doen om ze volgens de mandarin-conventies onder te brengen in één per-agentfolder voor SFW fase 01, zonder inhoudelijke semantiek te wijzigen.

## 2. Gevonden artefacten

### 2.1 Contracts

Gevonden in `artefacten/veranderverkenning/agents/`:

| Type      | Huidig pad                                                                                           |
|-----------|------------------------------------------------------------------------------------------------------|
| contract  | artefacten/veranderverkenning/agents/hypothese-vormer.probleemkader-hypothese.agent.md             |
| contract  | artefacten/veranderverkenning/agents/hypothese-vormer.richting-toetsen.agent.md                    |
| contract  | artefacten/veranderverkenning/agents/hypothese-vormer.interventie-versus-nietsdoen.agent.md        |

### 2.2 Prompts

Gevonden in `artefacten/veranderverkenning/prompts/`:

| Type    | Huidig pad                                                                                                  |
|---------|-------------------------------------------------------------------------------------------------------------|
| prompt  | artefacten/veranderverkenning/prompts/mandarin.hypothese-vormer.probleemkader-hypothese.prompt.md         |
| prompt  | artefacten/veranderverkenning/prompts/mandarin.hypothese-vormer.richting-toetsen.prompt.md                |
| prompt  | artefacten/veranderverkenning/prompts/mandarin.hypothese-vormer.interventie-versus-nietsdoen.prompt.md    |

### 2.3 Charter

Gevonden in `artefacten/veranderverkenning/charters-agents/`:

| Type    | Huidig pad                                                                                      |
|---------|-------------------------------------------------------------------------------------------------|
| charter | artefacten/veranderverkenning/charters-agents/hypothese-vormer.charter.md                      |

### 2.4 Resultaten

Volgens de huidige charter hoort output onder `docs/resultaten/hypothese-vormer/`. Deze ordentaak verandert die historische resultaten niet, maar neemt de locatie als gegeven.

## 3. Voorgestelde doelstructuur (per-agentfolder)

Nieuwe per-agentfolder voor hypothese-vormer als SFW fase 01 agent:

- **Folder**: `artefacten/sfw.01.hypothese-vormer/`

Binnen deze folder worden de kernartefacten als volgt geordend:

| Artefacttype | Doelpad                                                                                           |
|--------------|---------------------------------------------------------------------------------------------------|
| contract     | artefacten/sfw.01.hypothese-vormer/hypothese-vormer.probleemkader-hypothese.agent.md             |
| contract     | artefacten/sfw.01.hypothese-vormer/hypothese-vormer.richting-toetsen.agent.md                    |
| contract     | artefacten/sfw.01.hypothese-vormer/hypothese-vormer.interventie-versus-nietsdoen.agent.md        |
| prompt       | artefacten/sfw.01.hypothese-vormer/mandarin.hypothese-vormer.probleemkader-hypothese.prompt.md   |
| prompt       | artefacten/sfw.01.hypothese-vormer/mandarin.hypothese-vormer.richting-toetsen.prompt.md          |
| prompt       | artefacten/sfw.01.hypothese-vormer/mandarin.hypothese-vormer.interventie-versus-nietsdoen.prompt.md |
| charter      | artefacten/sfw.01.hypothese-vormer/hypothese-vormer.charter.md                                    |

De waarde stream-header in de charter dient bij deze ordening te worden bijgewerkt van **veranderverkenning** naar:

- `**Value Stream**: softwareontwikkeling (SFW, fase 01 - Veranderkenning)`

De inhoudelijke secties van de charter blijven gelijk; alleen de positionering in de canon wordt gecorrigeerd.

## 4. Voorgestelde verplaats- en hernoemoperaties

**Let op**: dit is een voorstel (dry-run); er zijn nog geen bestanden fysiek verplaatst.

### 4.1 Aanmaken per-agentfolder

- Maak de folder aan: `artefacten/sfw.01.hypothese-vormer/`.

### 4.2 Contracts

| Actie      | Bron                                                                                           | Doel                                                                                           |
|-----------|-------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
| verplaatsen | artefacten/veranderverkenning/agents/hypothese-vormer.probleemkader-hypothese.agent.md      | artefacten/sfw.01.hypothese-vormer/hypothese-vormer.probleemkader-hypothese.agent.md          |
| verplaatsen | artefacten/veranderverkenning/agents/hypothese-vormer.richting-toetsen.agent.md             | artefacten/sfw.01.hypothese-vormer/hypothese-vormer.richting-toetsen.agent.md                 |
| verplaatsen | artefacten/veranderverkenning/agents/hypothese-vormer.interventie-versus-nietsdoen.agent.md | artefacten/sfw.01.hypothese-vormer/hypothese-vormer.interventie-versus-nietsdoen.agent.md     |

### 4.3 Prompts

| Actie      | Bron                                                                                                  | Doel                                                                                                  |
|-----------|--------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| verplaatsen | artefacten/veranderverkenning/prompts/mandarin.hypothese-vormer.probleemkader-hypothese.prompt.md  | artefacten/sfw.01.hypothese-vormer/mandarin.hypothese-vormer.probleemkader-hypothese.prompt.md       |
| verplaatsen | artefacten/veranderverkenning/prompts/mandarin.hypothese-vormer.richting-toetsen.prompt.md         | artefacten/sfw.01.hypothese-vormer/mandarin.hypothese-vormer.richting-toetsen.prompt.md              |
| verplaatsen | artefacten/veranderverkenning/prompts/mandarin.hypothese-vormer.interventie-versus-nietsdoen.prompt.md | artefacten/sfw.01.hypothese-vormer/mandarin.hypothese-vormer.interventie-versus-nietsdoen.prompt.md |

### 4.4 Charter

| Actie      | Bron                                                                                      | Doel                                                                                      |
|-----------|--------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| verplaatsen | artefacten/veranderverkenning/charters-agents/hypothese-vormer.charter.md              | artefacten/sfw.01.hypothese-vormer/hypothese-vormer.charter.md                            |

Na verplaatsing van de charter:
- Header updaten naar de standaardvorm van het agent-chartertemplate (inclusief Template-veld en classificatie-assen).
- Value Stream-header aanpassen naar SFW fase 01 Veranderkenning, conform `temp/mandarin-value-streams-en-fasen.md`.

## 5. Openstaande vragen en aandachtspunten

- **Bevestiging value stream**: dit voorstel positioneert hypothese-vormer expliciet als SFW fase 01 (Veranderkenning) agent. Dit sluit aan bij de huidige chartertekst (probleemkader, hypothesevorming, veranderbehoefte), maar vraagt formele bevestiging in de canon.
- **Historische paden**: de verwijzingen in de charter naar `exports/veranderverkenning/...` dienen te worden bijgewerkt naar het nieuwe `artefacten/sfw.01.hypothese-vormer/`-patroon zodra de feitelijke verplaatsing is gedaan.
- **Resultatenmap**: `docs/resultaten/hypothese-vormer/` kan als historische locatie gehandhaafd worden; optioneel kan een korte toelichting worden toegevoegd in een README in die map om de nieuwe agentfolder te duiden.

---

_Dit document is opgesteld door agent-smeder (intent `4.orden-agent`) als dry-run ordeningsvoorstel. Er zijn nog geen bestanden fysiek verplaatst; dit voorstel dient als basis voor een expliciete migratiestap._
