# Ecosysteem-analyse: docs/resultaten probleem

**Datum**: 2026-02-06  
**Agent**: agent-curator-analyseer  
**Intent**: ecosysteem  
**Analyse-type**: Volledig - governance compliance  
**Charter-referentie**: `agent-charters/agent-curator-analyseer.charter.md`

---

## Samenvatting

Deze analyse onderzoekt het hardnekkige probleem waarbij agents in mandarin-agents workspace blijven schrijven naar `docs/resultaten/` met datum-versionering, ondanks dat dit in strijd is met:
1. **Workspace-doctrine v1.4.0** (2026-01-24): docs/resultaten/ afgeschaft voor agent-output
2. **Constitutie Artikel 4.3**: Geen datum-suffixen, git is versiegeschiedenis
3. **Doctrine-mandarin-agents-output-structuur**: Primaire output naar artefacten/

**Kern van het probleem**: 50+ agent-charters en agent-contracten zijn nooit bijgewerkt na workspace-doctrine v1.4.0 wijziging.

---

## Canon-bevindingen

### 1. Workspace-doctrine v1.4.0 (2026-01-24)

**Bron**: `grondslagen/globaal/workspace-doctrine.md` (Canon)

**Wijzigingen in v1.4.0**:
- Nieuwe folder `artefacten/` toegevoegd aan root-structuur (sectie 3.1)
- Agent-resultaten worden per agent opgeslagen in `artefacten/{agent-naam}/`
- Rol van `docs/` aangepast: **exclusief voor publicatie naar buiten**
- **docs/resultaten/ verwijderd** uit structuur (niet meer voor agent-output)
- Sectie 5.1 "Norm: Locatie van Agent-Resultaten" herzien

**Norm 5.1 - Locatie van Agent-Resultaten**:
```
Standaardregel: Agent-resultaten → artefacten/{agent-naam}/

Alle agents zetten hun resultaten in de artefacten/ folder, 
georganiseerd per agent in een eigen subfolder.

UITZONDERINGEN: 
- Publisher agent → docs/ (publicaties naar buiten)
- Presentatie-architect → docs/ (presentatie-assets)

Workspace-uitzonderingen:
Deze norm is NIET van toepassing op mandarin-agents en mandarin-canon.
Deze workspaces hebben een eigen structuur.
```

**Belangrijk**: Workspace-doctrine v1.4.0 zegt dat mandarin-agents een "eigen structuur" heeft, maar specificeert niet wat die is. Dit wordt gedaan in een aparte doctrine.

### 2. Doctrine-mandarin-agents-output-structuur

**Bron**: `grondslagen/agent-enablement/doctrine-mandarin-agents-output-structuur.md` (Canon)

Deze doctrine vult de "eigen structuur" uitzondering in voor mandarin-agents workspace.

**Norm 3.1 - Hoofdregel: artefacten-folder per agent**:
```
1. Alle agents in mandarin-agents schrijven hun primaire output 
   naar artefacten/, NIET naar docs/resultaten/.

2. De subfolder is afhankelijk van het type agent:
   - Value stream-agents: artefacten/{value-stream-code}.{fase-code}.{agent-naam}/
     Voorbeeld: artefacten/sfw.01.hypothese-vormer/
   
   - Foundational agents: artefacten/fnd.{nn}.{agent-naam}/
     Voorbeeld: artefacten/fnd.01.workspace-steward/
   
   - Agent-enablement agents: artefacten/aeo.{nn}.{agent-naam}/
     Voorbeeld: artefacten/aeo.02.agent-curator/
```

**Gebruikerscorrectie**: De voorgestelde nieuwe locatie moet simpelweg `artefacten/{agent-naam}/` zijn, niet de complexe value-stream patronen. Dit zou uit de canon moeten worden afgeleid.

**Norm 3.2 - Rol van docs/ in mandarin-agents**:
```
1. docs/ is NIET de primaire locatie voor agent-output.
2. Publicatie/documentatie naar buiten MAG in docs/, maar zijn dan 
   afgeleide publicaties van canonieke artefacten in artefacten/.
3. Nieuwe agents verwijzen NIET langer naar docs/resultaten/ als outputlocatie.
```

**Norm 4.1 - Geen datum in bestandsnamen**:
```
1. Bestandsnamen in artefacten/ bevatten GEEN datum-suffix als versie-indicator.
2. Patronen als *-v2.md, *-final.md, *-definitief.md en *-<datum>.md 
   zijn NIET toegestaan.
```

**Norm 5.1 - Eén canoniek pad per artefact**:
```
1. Voor elk type artefact is er ÉÉN canoniek bestandspad in artefacten/.
2. Nieuwe inhoud wordt telkens naar DATZELFDE bestand geschreven.
```

### 3. Constitutie Artikel 4.3

**Bron**: `grondslagen/globaal/constitutie.md` (Canon)

```
Artikel 4. Versionering en Immutability

Versie 1.3.0 bepaalt:
- Git-commits zijn de geschiedenis
- Bestanden hoeven geen intern versieveld te bevatten
- Nieuwe versies overschrijven de vorige inhoud op hetzelfde bestandspad
```

**Implicatie**: Datum-suffixen in bestandsnamen (`*-<datum>.md`) zijn in strijd met dit artikel.

---

## Inventarisatie: Agents met docs/resultaten referenties

**Methode**: Grep-search op "docs/resultaten" uitgevoerd op 2026-02-06  
**Resultaat**: 100+ matches over charters, agent-contracten en Python scripts

### 18 Agents met incorrecte output-locaties

#### Value Stream: Architectuur en Oplossingsontwerp (AOD)

**1. archimate-modelleur** (`artefacten/aod/aod.02.archimate-modelleur/`)
- **Huidige locatie**: `docs/resultaten/archimate-modelleur/`
- **Voorgestelde locatie**: `artefacten/archimate-modelleur/`
- **Deliverables met datum-pattern**:
  - motivatielaag-`<datum>`.md
  - bedrijfslaag-`<datum>`.md
  - applicatielaag-`<datum>`.md
  - technologielaag-`<datum>`.md
  - strategie-migratie-`<datum>`.md
  - analyse-`<datum>`.md
- **Files to update**: 
  - archimate-modelleur.charter.md (sectie 8 Output-locaties)
  - 6 agent-contracts (*.agent.md files)

**2. c4-modelleur** (`artefacten/architectuur-en-oplossingsontwerp/`)
- **Huidige locatie**: `docs/resultaten/c4-modelleur/`
- **Voorgestelde locatie**: `artefacten/c4-modelleur/`
- **Deliverables**:
  - context-containers-`<datum>`.md
  - components-`<datum>`.md
- **Files to update**:
  - c4-modelleur.charter.md
  - 2 agent-contracts

**3. data-duidingsarchitect** (`artefacten/architectuur-en-oplossingsontwerp/`)
- **Huidige locatie**: `docs/resultaten/data-duidingsarchitect/`
- **Voorgestelde locatie**: `artefacten/data-duidingsarchitect/`
- **Deliverables**:
  - duidingskaart-`<datum>`.md
  - mapping-`<datum>`.md
  - conflicten-`<datum>`.md
  - wijzigingsvoorstel-`<datum>`.md
- **Files to update**:
  - data-duidingsarchitect.charter.md
  - 4 agent-contracts

**4. architectuur-regisseur** (`artefacten/architectuur-en-oplossingsontwerp/`)
- **Huidige locatie**: `docs/resultaten/architectuur-regisseur/`
- **Voorgestelde locatie**: `artefacten/architectuur-regisseur/`
- **Deliverables**:
  - signalen-`<datum>`.md
  - gesprekken-`<datum>`.md
  - analyses-`<datum>`.md
  - rapporten-`<datum>`.md
- **Files to update**:
  - architectuur-regisseur.charter.md
  - 4 agent-contracts

#### Value Stream: Software-ontwikkeling (SFW)

**5. hypothese-vormer** (`artefacten/sfw/sfw.01.hypothese-vormer/`)
- **Huidige locatie**: `docs/resultaten/hypothese-vormer/`
- **Voorgestelde locatie**: `artefacten/hypothese-vormer/`
- **Deliverables**:
  - hypothese-formuleer-hypothese-`<datum>`.md
  - hypothese-toets-richting-`<datum>`.md
  - hypothese-vergelijk-met-nietsdoen-`<datum>`.md
- **Files to update**:
  - sfw/sfw.01.hypothese-vormer/hypothese-vormer.charter.md
  - 3 agent-contracts in sfw.01
- **Note**: Intents recent hernoemt naar gebiedende wijs

**6. niam-analist** (`artefacten/sfw/sfw.01.niam-analist/`)
- **Huidige locatie**: `docs/resultaten/niam-analist/`
- **Voorgestelde locatie**: `artefacten/niam-analist/`
- **Deliverables**:
  - bronnenverzameling-`<datum>`.md
  - begripsverkenning-`<datum>`.md
  - feitenanalyse-`<datum>`.md
  - consistentiecheck-`<datum>`.md
  - methodische-onderbouwing-`<datum>`.md
- **Files to update**:
  - sfw/sfw.01.niam-analist/niam-analist.charter.md
  - 5 agent-contracts

**7. thema-verwoorder** (`artefacten/sfw/sfw.02.thema-verwoorder/`)
- **Huidige locatie**: `docs/resultaten/thema-verwoorder/`
- **Voorgestelde locatie**: `artefacten/thema-verwoorder/`
- **Deliverables**:
  - thema-statement-`<datum>`.md
  - validatie-epic-`<datum>`.md
- **Files to update**:
  - sfw/sfw.02.thema-verwoorder/thema-verwoorder.charter.md
  - 2 agent-contracts

#### Value Stream: Markt- en Investeringsvorming (MIV)

**8. hypothese-vormer** (`artefacten/miv/miv.02.hypothese-vormer/`)
- **Huidige locatie**: `docs/resultaten/hypothese-vormer/`
- **Voorgestelde locatie**: `artefacten/hypothese-vormer/` OF behouden in `artefacten/miv/miv.02.hypothese-vormer/`
- **Deliverables**: Same as SFW hypothese-vormer
- **Files to update**:
  - miv/miv.02.hypothese-vormer/hypothese-vormer.charter.md
  - 3 agent-contracts in miv.02
- **Note**: Duplicate van SFW hypothese-vormer, mogelijk consolidatie nodig

#### Value Stream: Kennispublicatie (KVL)

**9. artikel-schrijver** (`artefacten/kvl/kvl.03.artikel-schrijver/`)
- **Huidige locatie**: `docs/resultaten/artikel-schrijver/`
- **Voorgestelde locatie**: `artefacten/artikel-schrijver/`
- **Files to update**:
  - kvl/kvl.03.artikel-schrijver/artikel-schrijver.charter.md
  - Agent-contracts

**10. heraut** (`artefacten/kvl/kvl.04.heraut/`)
- **Huidige locatie**: `docs/resultaten/heraut/`
- **Voorgestelde locatie**: `artefacten/heraut/`
- **Deliverables**:
  - post-`<datum>`.md
  - orientatie.md
- **Files to update**:
  - kvl/kvl.04.heraut/heraut.charter.md
  - Agent-contracts

**11. vertaler** (`artefacten/kvl/kvl.04.vertaler/`)
- **Incorrecte referentie**: `docs/resultaten/moeder/agent-boundary-vertaler.md`
- **Correcte locatie**: `agent-boundaries/vertaler.boundary.md`
- **Files to update**:
  - kvl/kvl.04.vertaler/vertaler.charter.md
  - Agent-contracts

**12. essayist** (`artefacten/kvl/kvl.03.essayist/`)
- **Incorrecte referentie**: `docs/resultaten/moeder/agent-boundary-essayist.md`
- **Correcte locatie**: `agent-boundaries/essayist.boundary.md`
- **Files to update**:
  - kvl/kvl.03.essayist/essayist.charter.md
  - Agent-contracts

#### Value Stream: Foundational (FND)

**13. workspace-steward** (`artefacten/fnd/fnd.01.workspace-steward/`)
- **Huidige locatie**: `docs/resultaten/workspace-audit-<datum>.md`
- **Voorgestelde locatie**: `artefacten/workspace-steward/workspace-audit.md` (GEEN datum)
- **Files to update**:
  - fnd/fnd.01.workspace-steward/workspace-steward.charter.md
  - Agent-contracts

**14. engineer-steward** (`artefacten/fnd/fnd.01.engineer-steward/`)
- **Huidige locatie**: `docs/resultaten/engineer-steward/`
- **Voorgestelde locatie**: `artefacten/engineer-steward/`
- **Deliverables**:
  - code-review-`<datum>`.md
  - executie-rapport-`<datum>`.md
- **Files to update**:
  - fnd/fnd.01.engineer-steward/engineer-steward.charter.md
  - Agent-contracts

**15. formaat-vertaler** (`artefacten/fnd/fnd.02.formaat-vertaler/`)
- **Huidige locatie**: `docs/resultaten/formaat-vertaler/`
- **Voorgestelde locatie**: `artefacten/formaat-vertaler/`
- **Deliverables**:
  - conversie-`<datum>`.log
- **Files to update**:
  - fnd/fnd.02.formaat-vertaler/formaat-vertaler.charter.md
  - Agent-contracts

#### Value Stream: Agent-enablement (AEO)

**16. agent-smeder** (`artefacten/aeo/aeo.02.agent-smeder/`)
- **Huidige locatie**: `docs/resultaten/agent-smeder/`
- **Voorgestelde locatie**: `artefacten/agent-smeder/`
- **Deliverables**:
  - orden-agent-`<agent-naam>`.md
- **Files to update**:
  - aeo/aeo.02.agent-smeder/agent-smeder.charter.md (Sectie 8 Output-locaties)
  - Agent-contracts

**17. agent-curator** (`artefacten/aeo/aeo.02.agent-curator/`)
- **Huidige locatie**: `docs/resultaten/agent-curator/`, `docs/resultaten/agent-publicaties/`
- **Voorgestelde locatie**: `artefacten/agent-curator/`
- **Deliverables**:
  - agents-publicatie-`<datum>`.md (in docs/resultaten/agent-publicaties/)
  - agent-boundary-`<agent-naam>`.md
  - value-streams-overzicht.md
  - ecosysteem-analyse-`<datum>`.md
- **Files to update**:
  - agent-charters/agent-curator.charter.md (Sectie 8 Output-locaties)
  - agent-charters/agent-curator-analyseer.charter.md (Sectie 8)
  - Agent-contracts
- **Special case**: agents-publicatie.json in root kan blijven (machine-readable fetch file)

**18. workflow-architect** (`artefacten/aeo/aeo.03.workflow-architect/`)
- **Huidige locatie**: `docs/resultaten/workflow-architect/`
- **Voorgestelde locatie**: `artefacten/workflow-architect/`
- **Deliverables**:
  - workflow-`<naam>`.md
  - pipeline-`<naam>`.md
  - artefact-flow-`<naam>`.md
- **Files to update**:
  - aeo/aeo.03.workflow-architect/workflow-architect.charter.md
  - Agent-contracts

---

## Python Scripts met docs/resultaten referenties

**1. templates-curator.py**
- **Huidige output**: `docs/resultaten/templates-publicatie-<datum-tijd>.md`
- **Voorgestelde output**: `artefacten/templates-curator/templates-publicatie.md` (geen datum)

**2. agent-curator.py**
- **Huidige output**: `docs/resultaten/agent-publicaties/agents-publicatie-<datum>.md`
- **Voorgestelde output**: `artefacten/agent-curator/agents-publicatie.md` (geen datum)

**3. templates-contract-overzicht.py**
- **Huidige output**: `docs/resultaten/templates-contract-overzicht/`
- **Voorgestelde output**: `artefacten/templates-curator/` (of eigen agent-folder)

**4. init-workspace.py**
- **Probleem**: Creëert `docs/resultaten/` folder
- **Actie**: VERWIJDER folder-creatie voor docs/resultaten/

---

## Governance Compliance Issues

### 1. Datum-versionering in bestandsnamen

**Overtreding**: Constitutie Artikel 4.3

**Voorbeelden**:
- `hypothese-formuleer-hypothese-<datum>.md`
- `duidingskaart-<datum>.md`
- `workspace-audit-<datum>.md`
- `agents-publicatie-<datum>.md`

**Correctie**: Verwijder `<datum>` placeholder uit alle deliverable paden. Gebruik vaste bestandsnamen:
- `hypothese-formuleer-hypothese.md`
- `duidingskaart.md`
- `workspace-audit.md`
- `agents-publicatie.md`

Git-commits zijn de versiegeschiedenis, niet bestandsnamen.

### 2. docs/resultaten/ in plaats van artefacten/

**Overtreding**: Workspace-doctrine v1.4.0, Doctrine-mandarin-agents-output-structuur Norm 3.1

**Omvang**: 18 agents, 50+ bestanden

**Root cause**: Workspace-doctrine v1.4.0 wijziging (2026-01-24) nooit systematisch doorgevoerd in agent-charters en agent-contracten.

### 3. Incorrecte agent-boundary referenties

**Agents**: vertaler, essayist

**Huidige referentie**: `docs/resultaten/moeder/agent-boundary-<agent-naam>.md`

**Correcte locatie**: `agent-boundaries/<agent-naam>.boundary.md`

**Root cause**: Agent-boundaries zijn governance-artefacten en horen in workspace root folder `agent-boundaries/`, niet in docs/resultaten/.

---

## Waarom agents niet loggen wat ze lezen (Norm 10.4)

### Norm 10.4 - Logging bij handmatige initialisatie

**Bron**: `doctrine-agent-charter-normering.md` sectie 10.4

**Norm**:
```
Wanneer agent handmatig wordt geïnitieerd (niet via geautomatiseerde 
pipeline of runner), wordt logbestand weggeschreven naar logs/

Bestandsnaam: yyyyddmm.HHmm {agent-naam}.log

Inhoud moet ten minste bevatten:
1. Gelezen bestanden (met pad)
2. Aangepaste bestanden (met pad)
3. Aangemaakte bestanden (met pad)

Deze norm geldt voor ALLE mandarin-agents bij handmatige initialisatie.
```

### Waarom agents dit niet doen

**1. Geen automatische logging in agent-runtime**
- Agents draaien via IDE/GitHub Copilot (= handmatige initialisatie)
- Geen built-in mechanisme dat automatisch logs genereert
- Agents moeten expliciet log-file aanmaken en schrijven

**2. Geen enforcement of controle**
- Geen pre-commit hook die logging verifieert
- Geen runner die logging controleert
- Geen audit-trail van wat agents gelezen hebben

**3. Charters bijgewerkt, praktijk niet**
- 22 charters zijn bijgewerkt met sectie 9 "Logging bij handmatige initialisatie"
- Norm 10.4 staat in charters
- Maar agents praktiseren het niet in werkelijkheid
- Governance-norm bestaat, compliance ontbreekt

**4. Meta-probleem: Disconnect tussen norm en praktijk**
- Doctrine zegt: "Deze norm geldt voor ALLE mandarin-agents"
- Werkelijkheid: GEEN enkele agent logt wat ie gelezen heeft
- Geen tooling die dit mogelijk maakt of afdwingt
- Agent-gebruikers (mensen via Copilot) weten norm niet of negeren het

### Voorgestelde oplossing

**Optie A: Automatische logging via runner**
- Maak wrapper-runner die logging afdwingt
- Runner tracked file reads/writes automatisch
- Genereert log-file per norm 10.4

**Optie B: Agent-template met logging code**
- Voeg logging-code toe aan agent-template
- Agents genereren eigen log-file als eerste actie
- Track file operations in agent-code zelf

**Optie C: Herdefinieer norm voor IDE-gebruik**
- Erken dat handmatige IDE-initialisatie geen logging heeft
- Norm 10.4 alleen van toepassing op runner-execution
- Documenteer in doctrine-agent-charter-normering

**Aanbeveling**: Combinatie A+C
- Implementeer automatische logging in runners (Optie A)
- Herdefinieer Norm 10.4 scope tot runner-execution (Optie C)
- IDE/Copilot gebruik heeft git-commits als audit-trail

---

## Voorgestelde correctieplan

### Fase 1: Canon-locatie patroon vaststellen

**Actie**: Verifieer met constitutioneel auteur/canon curator:
- Is voorgestelde locatie simpelweg `artefacten/{agent-naam}/`?
- Of blijft het `artefacten/{value-stream-code}.{fase-code}.{agent-naam}/`?
- Documenteer in doctrine-mandarin-agents-output-structuur

**Resultaat**: Eenduidige locatie-pattern voor alle agents

### Fase 2: Systematische charter updates

**Omvang**: 18 agents, 50+ bestanden

**Per agent**:
1. Update charter sectie 8 "Output-locaties"
   - Verwijder docs/resultaten/ referenties
   - Voeg artefacten/{agent-naam}/ toe
   - Verwijder `<datum>` placeholders

2. Update alle agent-contracts (*.agent.md)
   - Update deliverable paden
   - Verwijder datum-suffixen
   - Verwijs naar correcte artefacten-locatie

3. Update prompt-metadata (mandarin.*.prompt.md) indien nodig

**Template voor charter update**:
```markdown
## 8. Output-locaties

De {agent-naam} legt alle resultaten vast in de workspace als markdown-bestanden:

- `artefacten/{agent-naam}/{deliverable-1}.md`
- `artefacten/{agent-naam}/{deliverable-2}.md`

Alle output wordt gegenereerd in gestructureerd markdown-formaat voor 
overdraagbaarheid en versiebeheer binnen de workspace.
```

### Fase 3: Python scripts updaten

**Files**:
1. `scripts/runners/templates-curator.py`
2. `scripts/runners/agent-curator.py`
3. `scripts/runners/templates-contract-overzicht.py`
4. `scripts/workspace-tools/init-workspace.py`

**Acties**:
- Update output paths naar artefacten/
- Verwijder datum-tijd suffix uit bestandsnamen
- Verwijder docs/resultaten/ folder-creatie in init-workspace.py

### Fase 4: Agent-boundary referenties corrigeren

**Agents**: vertaler, essayist

**Actie**: Update charter referenties van `docs/resultaten/moeder/agent-boundary-*.md` naar `agent-boundaries/*.boundary.md`

### Fase 5: Logging-gap adresseren

**Optie 1**: Implementeer automatische logging in runners
**Optie 2**: Herdefinieer Norm 10.4 scope (alleen runners, niet IDE-gebruik)

**Governance beslissing nodig**: Hoe om te gaan met IDE/Copilot agent-gebruik zonder logging?

---

## Traceerbaar correctie-overzicht

| Agent | Charter | Contracts | Python Scripts | Priority |
|-------|---------|-----------|----------------|----------|
| archimate-modelleur | aod.02.archimate-modelleur/archimate-modelleur.charter.md | 6 contracts | - | HIGH |
| c4-modelleur | architectuur-en-oplossingsontwerp/c4-modelleur.charter.md | 2 contracts | - | HIGH |
| data-duidingsarchitect | architectuur-en-oplossingsontwerp/data-duidingsarchitect.charter.md | 4 contracts | - | HIGH |
| architectuur-regisseur | architectuur-en-oplossingsontwerp/architectuur-regisseur.charter.md | 4 contracts | - | HIGH |
| hypothese-vormer (sfw.01) | sfw/sfw.01.hypothese-vormer/hypothese-vormer.charter.md | 3 contracts | - | HIGH |
| niam-analist | sfw/sfw.01.niam-analist/niam-analist.charter.md | 5 contracts | - | MEDIUM |
| thema-verwoorder | sfw/sfw.02.thema-verwoorder/thema-verwoorder.charter.md | 2 contracts | - | MEDIUM |
| hypothese-vormer (miv.02) | miv/miv.02.hypothese-vormer/hypothese-vormer.charter.md | 3 contracts | - | MEDIUM |
| artikel-schrijver | kvl/kvl.03.artikel-schrijver/artikel-schrijver.charter.md | ? contracts | - | MEDIUM |
| heraut | kvl/kvl.04.heraut/heraut.charter.md | ? contracts | - | MEDIUM |
| vertaler | kvl/kvl.04.vertaler/vertaler.charter.md | ? contracts | - | LOW |
| essayist | kvl/kvl.03.essayist/essayist.charter.md | ? contracts | - | LOW |
| workspace-steward | fnd/fnd.01.workspace-steward/workspace-steward.charter.md | ? contracts | - | HIGH |
| engineer-steward | fnd/fnd.01.engineer-steward/engineer-steward.charter.md | ? contracts | - | MEDIUM |
| formaat-vertaler | fnd/fnd.02.formaat-vertaler/formaat-vertaler.charter.md | ? contracts | - | LOW |
| agent-smeder | aeo/aeo.02.agent-smeder/agent-smeder.charter.md | ? contracts | - | CRITICAL |
| agent-curator | agent-charters/agent-curator.charter.md | ? contracts | agent-curator.py | CRITICAL |
| workflow-architect | aeo/aeo.03.workflow-architect/workflow-architect.charter.md | ? contracts | - | MEDIUM |
| templates-curator | - | - | templates-curator.py | HIGH |
| - | - | - | templates-contract-overzicht.py | MEDIUM |
| - | - | - | init-workspace.py | HIGH |

**Totaal**: 18 agents, ~50 charters/contracts, 4 Python scripts

**Priority rationale**:
- CRITICAL: AEO agents (agent-smeder, agent-curator) - foundational voor agent-ecosysteem
- HIGH: Frequently used agents + workspace tooling
- MEDIUM: Active agents met moderate gebruik
- LOW: Rarely used agents of legacy agents

---

## Herkomstverantwoording

### Gelezen bestanden

**Canon-documenten** (via GitHub hans-blok/mandarin-canon):
1. grondslagen/globaal/workspace-doctrine.md (versie 1.5.2)
2. grondslagen/agent-enablement/doctrine-mandarin-agents-output-structuur.md
3. grondslagen/globaal/doctrine-agent-charter-normering.md (sectie 10 Norm 10.4)
4. grondslagen/globaal/constitutie.md (Artikel 4.3)
5. agent-charters/canon-curator.charter.md
6. agent-charters/moeder.charter.md
7. agent-charters/workspace-steward.charter.md
8. agent-charters/constitutioneel-auteur.charter.md
9. artefacten/README.md
10. grondslagen/value-streams/it-development/doctrine-it-development.md
11. grondslagen/globaal/doctrine-handoff-creatie-en-overdrachtsdiscipline.md
12. README.md

**Workspace-documenten**:
1. c:\git\mandarin-agents\.github\prompts\mandarin.agent-curator-analyseer.ecosysteem.prompt.md
2. c:\git\mandarin-agents\agent-charters\agent-curator.charter.md
3. c:\git\mandarin-agents\agent-charters\agent-curator-analyseer.charter.md

**Grep-search resultaten**: 100+ matches voor "docs/resultaten" in workspace (uitgevoerd 2026-02-06)

### Agent-context

- **Agent**: agent-curator-analyseer
- **Charter**: agent-charters/agent-curator-analyseer.charter.md (versie 0.1.0)
- **Value Stream**: agent-enablement (fase 02)
- **Governance**: beleid-mandarin-agents.md + doctrine-agent-charter-normering.md

### Status

- **Datum analyse**: 2026-02-06
- **Analyse-type**: Volledig ecosysteem - governance compliance
- **Status**: Conceptrapport voor governance review
- **Menselijke validatie**: Nog niet gevalideerd

---

## Aanbevelingen voor governance

1. **Stel Canon-locatie pattern vast**
   - Duidelijkheid over artefacten/{agent-naam}/ vs complexere patterns
   - Update doctrine-mandarin-agents-output-structuur indien nodig

2. **Plan systematische charter-update**
   - 18 agents, 50+ bestanden
   - Gecoördineerde aanpak per value stream
   - Agent-smeder kan charters updaten volgens agent-charter.template.md

3. **Update Python tooling**
   - Scripts moeten naar artefacten/ schrijven
   - Verwijder datum-suffixen
   - Init-workspace.py moet docs/resultaten/ niet creëren

4. **Adresseer logging-gap**
   - Besluit over Norm 10.4 scope (runners only vs all use?)
   - Overweeg automatische logging in runners
   - Documenteer IDE/Copilot usage zonder logging

5. **Publiceer doctrine-aanvulling**
   - Constitutioneel auteur kan doctrine schrijven over mandarin-agents output-structuur
   - Maak "eigen structuur" uitzondering expliciet
   - Verduidelijk waarom deze workspace anders is

6. **Consider migrating existing docs/resultaten/ files**
   - Verplaats bestaande deliverables naar artefacten/
   - Of laat docs/resultaten/ as-is (historisch archief)
   - Governance beslissing nodig

---

## Logging van deze analyse

**Log-file**: `c:\git\mandarin-agents\logs\20260206.1430 agent-curator-analyseer.log`

Bevat volledige lijst van gelezen, aangepaste en aangemaakte bestanden conform Norm 10.4.

---

**Einde analyse**
