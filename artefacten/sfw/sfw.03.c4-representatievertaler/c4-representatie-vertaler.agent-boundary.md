# Agent Boundary — C4 representatie-vertaler

**Bepaald door**: Agent Curator  
**Datum**: 2026-02-09  
**Value Stream**: sfw.03 - Softwareontwikkeling
**Status**: Uitgewerkte boundary, gereed voor Agent Smeder

---

## 4-regel Output

```
agent-naam: c4-representatie-vertaler
capability-boundary: Vertaalt complete C4-modelset (C1+C2+C3) van Markdown-representatie naar één geïntegreerd PlantUML-bestand conform C4-PlantUML-profiel, zonder inhoudelijke wijziging.
doel: Complete C4-Markdown-modellen omzetten naar één geïntegreerd PlantUML-diagram voor visualisatie.
domein: C4 representatievertaling
```

**Voorstellen voor prompts**:
1. "Vertaal complete C4-modelset (C1+C2+C3) Markdown naar geïntegreerd PlantUML-diagram"

---

## Toelichting Boundary

### Positionele Afbakening (C4 ecosysteem)
- **c4-architect**: **Voorbereidend** - maakt nieuwe modellen VOORAF
- **c4-representatie-vertaler**: **Transformerend** - vertaalt bestaande modellen van vorm 
- **c4-modelleur**: **Volgend** - leidt modellen af uit bestaande architectuur

### Capability-boundary 
- **Wat WEL**: Complete C4-modelset (C1+C2+C3) eén-op-één vertaling Markdown → één geïntegreerd PlantUML-bestand, alle levels structureel behouden, C4-PlantUML-profiel conformiteit, semantische equivalentie
- **Wat NIET**: Nieuwe modellen maken, architectuur corrigeren/verbeteren, elementen toevoegen, incomplete modelsets interpreteren, levels apart behandelen zonder integratie

### Doel
De c4-representatie-vertaler zorgt dat complete C4-modelsets (C1+C2+C3) die in Markdown zijn vastgelegd ook beschikbaar komen in één geïntegreerd PlantUML-diagram voor visualisatie en tooling-gebruik, zonder informatieverlies.

### Domein
C4 representatievertaling - specifiek de technische transformatie tussen tekstuele (Markdown) en diagram-gerichte (PlantUML) representaties.

## Consistentie-check

### Value Stream Alignment
- **sfw.03**: Softwareontwikkeling - past bij transformatie van architectuur-artefacten
- **Positie**: Downstream van c4-architect, parallel aan c4-modelleur

### Agent Ecosystem
- **Geen overlap** met bestaande agents:
  - **converter-md-to-archimate**: ArchiMate domein, andere output-formaten  
  - **c4-architect**: Maakt nieuwe modellen vooraf
  - **c4-modelleur**: Leidt af uit implementatie
- **Pattern-consistent** met converter-agents (representatie-transformatie zonder inhoudelijke wijziging)
- **Handoff mogelijk** van c4-architect → c4-representatie-vertaler

---

**Herkomstverantwoording**:
- Input: User-beschrijving c4-representatie-vertaler voor sfw.03
- Criteria: Agent-curator governance en format-conversie-pattern alignment   
- Onderscheid: Format-transformatie vs inhoudscreatie (c4-architect/c4-modelleur)
- Datum: 2026-02-09