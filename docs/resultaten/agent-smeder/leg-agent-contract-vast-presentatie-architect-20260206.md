# Agent Smeder - Intent 1: leg-agent-contract-vast
## Agent: presentatie-architect
**Datum**: 2026-02-06  
**Uitgevoerd door**: agent-smeder  
**Intent**: 1.leg-agent-contract-vast

---

## Overzicht

De agent-smeder heeft de agent-contracten en YAML prompt-metadata voor de agent **presentatie-architect** volledig uitgewerkt op basis van de capability boundary en charter. Alle drie de intents (`ontwerp-html-templates`, `ontwerp-stylesheet`, `definieer-design-tokens`) zijn voorzien van volledige contracten met gedetailleerde input, output en foutafhandeling.

---

## Uitgevoerde acties

### 1. Agent-contracten uitgewerkt

Voor elk van de drie intents is een volledig agent-contract opgesteld volgens het template:

#### Intent: `ontwerp-html-templates`
**Locatie**: `artefacten/fnd.02.presentatie-architect/presentatie-architect.ontwerp-html-templates.agent.md`

**Input**:
- Verplicht: branding-richtlijnen, toegankelijkheidseisen (WCAG-niveau)
- Optioneel: bestaande-templates, template-type

**Output**:
- HTML Jinja2-templates in `templates/html/` met semantische structuur
- Template-documentatie met placeholder-uitleg

**Foutafhandeling**:
- Stopt bij ontbrekende/onvolledige branding-richtlijnen
- Waarschuwt bij onhaalbare toegankelijkheidseisen
- Valideert geen content-generatie (alleen placeholders)

---

#### Intent: `ontwerp-stylesheet`
**Locatie**: `artefacten/fnd.02.presentatie-architect/presentatie-architect.ontwerp-stylesheet.agent.md`

**Input**:
- Verplicht: design-tokens (YAML-pad), branding-richtlijnen
- Optioneel: stylesheet-type, breakpoint-specificaties, bestaande-stylesheet

**Output**:
- CSS/SCSS bestanden in `templates/css/` met responsive design
- Stylesheet-documentatie met class-conventies en toegankelijkheidschecks

**Foutafhandeling**:
- Stopt bij ontbrekende/ongeldige design tokens
- Waarschuwt bij WCAG 2.1 AA contrastverstoring
- Valideert geen JavaScript-afhankelijkheden

---

#### Intent: `definieer-design-tokens`
**Locatie**: `artefacten/fnd.02.presentatie-architect/presentatie-architect.definieer-design-tokens.agent.md`

**Input**:
- Verplicht: branding-richtlijnen (huisstijl), toegankelijkheidseisen
- Optioneel: bestaande-tokens, custom-breakpoints, uitbreidingen

**Output**:
- `templates/design-tokens.yml` met verplichte secties (colors, typography, spacing, breakpoints, shadows, borders)
- Design tokens documentatie met toegankelijkheidsvalidatie

**Foutafhandeling**:
- Stopt bij onvolledige kleurspecificaties
- Waarschuwt bij WCAG 2.1 AA niet-compliant kleuren
- Valideert platform-agnostische tokens

---

### 2. YAML prompt-metadata bijgewerkt

Alle drie de prompt-metadata bestanden zijn gestandaardiseerd naar het YAML-only format:

- `mandarin.presentatie-architect.ontwerp-html-templates.prompt.md`
- `mandarin.presentatie-architect.ontwerp-stylesheet.prompt.md`
- `mandarin.presentatie-architect.definieer-design-tokens.prompt.md`

**Format**:
```yaml
---
agent: presentatie-architect
intent: <intent-naam>
charter_ref: artefacten/fnd.02.presentatie-architect/presentatie-architect.charter.md
---
```

---

## Traceerbaarheid

| Artefact | Type | Locatie |
|----------|------|---------|
| Boundary | Input | `agent-boundaries/presentatie-architect.boundary.md` |
| Charter | Input | `artefacten/fnd.02.presentatie-architect/presentatie-architect.charter.md` |
| Contract 1 | Output | `artefacten/fnd.02.presentatie-architect/presentatie-architect.ontwerp-html-templates.agent.md` |
| Prompt 1 | Output | `artefacten/fnd.02.presentatie-architect/mandarin.presentatie-architect.ontwerp-html-templates.prompt.md` |
| Contract 2 | Output | `artefacten/fnd.02.presentatie-architect/presentatie-architect.ontwerp-stylesheet.agent.md` |
| Prompt 2 | Output | `artefacten/fnd.02.presentatie-architect/mandarin.presentatie-architect.ontwerp-stylesheet.prompt.md` |
| Contract 3 | Output | `artefacten/fnd.02.presentatie-architect/presentatie-architect.definieer-design-tokens.agent.md` |
| Prompt 3 | Output | `artefacten/fnd.02.presentatie-architect/mandarin.presentatie-architect.definieer-design-tokens.prompt.md` |

---

## Validatie

✅ **Capability boundary gerespecteerd**: Alle contracten blijven binnen de afbakening (ontwerp van design-assets, geen HTML/PDF-generatie)  
✅ **Consistent met charter**: Input/output aligned met kerntaken in charter  
✅ **WCAG 2.1 AA compliant**: Toegankelijkheid expliciet geborgd in alle contracten  
✅ **YAML-only prompt-metadata**: Alle prompt-bestanden volgen het vereiste format  
✅ **Geen overlap met Publisher**: Contracten maken duidelijk dat generatie bij Publisher ligt  

---

## Gelezen bestanden

1. `c:\git\mandarin-agents\.github\prompts\mandarin.agent-smeder-1.leg-agent-contract-vast.prompt.md`
2. `c:\git\mandarin-agents\agent-boundaries\presentatie-architect.boundary.md`
3. `c:\git\mandarin-agents\artefacten\aeo\aeo.02.agent-smeder\agent-smeder.charter.md`
4. `c:\git\mandarin-agents\artefacten\fnd\fnd.02.presentatie-architect\presentatie-architect.charter.md`
5. `c:\git\mandarin-agents\templates\agent-contract.template.md`
6. `c:\git\mandarin-agents\templates\agent-prompt.template.yaml`

---

## Aangepaste bestanden

1. `c:\git\mandarin-agents\artefacten\fnd\fnd.02.presentatie-architect\presentatie-architect.ontwerp-html-templates.agent.md` (versie 0.1.0 → 1.0)
2. `c:\git\mandarin-agents\artefacten\fnd\fnd.02.presentatie-architect\presentatie-architect.ontwerp-stylesheet.agent.md` (versie 0.1.0 → 1.0)
3. `c:\git\mandarin-agents\artefacten\fnd\fnd.02.presentatie-architect\presentatie-architect.definieer-design-tokens.agent.md` (versie 0.1.0 → 1.0)
4. `c:\git\mandarin-agents\artefacten\fnd\fnd.02.presentatie-architect\mandarin.presentatie-architect.ontwerp-html-templates.prompt.md` (YAML-format gestandaardiseerd)
5. `c:\git\mandarin-agents\artefacten\fnd\fnd.02.presentatie-architect\mandarin.presentatie-architect.ontwerp-stylesheet.prompt.md` (YAML-format gestandaardiseerd)
6. `c:\git\mandarin-agents\artefacten\fnd\fnd.02.presentatie-architect\mandarin.presentatie-architect.definieer-design-tokens.prompt.md` (YAML-format gestandaardiseerd)

---

## Aangemaakte bestanden

1. `c:\git\mandarin-agents\docs\resultaten\agent-smeder\leg-agent-contract-vast-presentatie-architect-20260206.md` (dit rapport)

---

## Conclusie

De agent **presentatie-architect** is nu volledig uitgerust met contract-first artefacten voor alle drie de intents. Alle contracten zijn traceerbaar naar de boundary en charter, en volgen de governance zoals vastgelegd in `beleid-mandarin-agents.md`. De agent kan nu operationeel worden ingezet binnen de Foundation value stream (FND fase 02) voor het ontwerpen van toegankelijke, consistente presentatie-assets.

**Status**: ✅ Gereed voor overdracht aan Publisher of uitvoerende runners
