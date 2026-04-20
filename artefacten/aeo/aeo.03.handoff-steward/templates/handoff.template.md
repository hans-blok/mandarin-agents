---
# IDENTIFICATIE
template-id: "013"
template-naam: handoff

# RELATIES
artefact-type-id: "013"
agent-id: aeo.03.handoff-steward

# META-DATA
versie: 0.1.0
status: vers
digest: 0314
---
# Template voor handoff-steward

Gebruik dit bestand als invultemplate voor `handoff-steward.realiseer-initiele-handoff`.
Het eerste blok bevat de parameters voor de runner. Het tweede blok laat zien welke
handoff-inhoud daar normaliter uit voortkomt.

## Runner-input

```yaml
execution-bestand: executions/<yyyymmddHHMMSS-agent.intent>.md
ontvangende-agent: <ontvangende-agent-in-kebab-case>
handoff-register: handoffs/handoff-register.yaml
overdrachtsnota: |
  <korte instructie of overdrachtscontext voor de ontvanger>
escalatie-indicatie: false
escalatie-reden: ""
escalatie-urgentie: normaal
```

## Verwachte handoff-inhoud

```yaml
handoff-identificatie: hf-<JJMM>.<NNNN>
execution-identificatie: exec-<JJMM>.<xxxx>
overdragende-agent: <bron-agent>
ontvangende-agent: <ontvangende-agent-in-kebab-case>
overdracht-datum: <YYYY-MM-DD>

samenvatting-context: |
  <beschrijf in 2-4 regels wat is afgerond en waarom overdracht nodig is>

genomen-beslissingen:
  - <beslissing 1>
  - <beslissing 2>

gesignaleerde-ambiguiteiten:
  - <ambiguiteit of risico 1>
  - <ambiguiteit of risico 2>

openstaande-taken:
  - <taak 1 voor ontvangende agent>
  - <taak 2 voor ontvangende agent>

escalatie-indicatie: false

overdrachtsnota: |
  <extra instructie, deadline, aandachtspunt of verzoek aan ontvanger>
```

## Invulhulp

- `execution-bestand`: pad naar het afgeronde execution-bestand van de overdragende agent.
- `ontvangende-agent`: moet aansluiten op een bekende agentnaam in deze repo.
- `handoff-register`: centraal register waarin de handoff-steward het volgende vrije nummer bepaalt.
- `escalatie-indicatie`: zet op `true` als menselijke tussenkomst nodig is.
- `escalatie-reden`: verplicht zodra `escalatie-indicatie: true` is.
- `escalatie-urgentie`: gebruik `laag`, `normaal` of `hoog`.

## Minimale variant

```yaml
execution-bestand: executions/<bestand>.md
ontvangende-agent: <agent>
handoff-register: handoffs/handoff-register.yaml
overdrachtsnota: |
  <korte overdrachtstekst>
escalatie-indicatie: false
```