---
# IDENTIFICATIE
template-id: "002"
template-naam: ecosysteem-agent-prompt-contracten

# RELATIES
artefact-type-id: "002"
agent-id: aeo.02.agent-curator

# META-DATA
versie: 1.0.0
status: vers
digest: 977c
---
# Template: Ecosysteem-overzicht

## Doel en gebruik

Dit template beschrijft de outputstructuur van het ecosysteem-overzicht dat de agent-curator produceert bij de intent `rapporteer-prompts-overzicht`. Het overzicht geeft een tabellarisch inzicht in de toestand van alle agents en dient als bron voor latere conversie naar YAML conform OpenAPI-achtige agent catalog. 


Gebruikt door intents:
- `rapporteer-prompts-overzicht`

---

# Prompt Contracten Overzicht

Dit is het gegenereerde overzicht voor Agent: **[AGENT_NAAM]**

## Prompt

**naam**  
[PROMPT_NAAM]

**contract-template**  
[CONTRACT_TEMPLATE]

**prompt-template**  
[PROMPT_TEMPLATE]

**template-status**  
[TEMPLATE_STATUS]

**beschrijving**  
[PROMPT_BESCHRIJVING]

---

## Input (parameters)

[VOOR ELKE PARAMETER:]

### [PARAMETER_NAAM]

- **type:** [PARAMETER_TYPE]  
- **verplicht:** [JA/NEE]  
- **beschrijving:**  
  [PARAMETER_BESCHRIJVING]  
- **regels:**  
  - [OPTIONELE_REGEL_1]
  - [OPTIONELE_REGEL_2]

---

## Output

### [OUTPUT_NAAM]

- **type:** [OUTPUT_TYPE]  
- **beschrijving:**  
  [OUTPUT_BESCHRIJVING]

---

## Gedrag van de prompt

Deze prompt:

- [GEDRAGS_STAP_1]
- [GEDRAGS_STAP_2]
- [GEDRAGS_STAP_3]

## Versiebeheer

| Versie | Datum | Wijziging |
|--------|-------|-----------|
| 1.0.0 | [yyyy-mm-dd] | Initiële template voor agent-curator |

---

**Template-categorie**: Agent-specifiek  
**Gebruikt door intents**: beschrijf-agent-contracten, rapporteer-prompts-overzicht
