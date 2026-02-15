# {ecosysteem_naam} — Gedragslaag Definitie

**Versie**: {versie}  
**Datum**: {datum}  
**Value Stream Fase**: {value_stream_fase}  
**Canon Referentie**: {canon_ref}

## Doel van dit document

Dit document definieert de gedragslaag (behavior layer) van {ecosysteem_naam}, waarbij expliciet wordt vastgelegd welke processen, functies en interacties plaatsvinden binnen het ecosysteem.

## Scope

**Gemodelleerde lagen**: {lagen}  
**Focus**: Behavior elementen en hun relaties tot active/passive structuur

---

## ArchiMate Behavior Elementen

### Business Layer Behavior

| Element ID | Type | Naam | Beschrijving | Getriggerd door |
|-----------|------|------|--------------|-----------------|
| {element_id} | Business Process / Business Function / Business Interaction / Business Event | {element_naam} | {beschrijving} | {trigger} |

**Rationale**: {waarom_deze_processen}

### Application Layer Behavior

| Element ID | Type | Naam | Beschrijving | Gebruikt door |
|-----------|------|------|--------------|---------------|
| {element_id} | Application Process / Application Function / Application Interaction / Application Event | {element_naam} | {beschrijving} | {gebruiker} |

**Rationale**: {waarom_deze_functies}

### Technology Layer Behavior (indien van toepassing)

| Element ID | Type | Naam | Beschrijving | Ondersteunt |
|-----------|------|------|--------------|-------------|
| {element_id} | Technology Process / Technology Function / Technology Interaction / Technology Event | {element_naam} | {beschrijving} | {ondersteund_gedrag} |

**Rationale**: {waarom_deze_technologie_processen}

---

## Relaties tussen Behavior Elementen

### Flow Relaties

| Van Element | Relatie Type | Naar Element | Rationale |
|-------------|--------------|--------------|-----------|
| {van_element_id} | Flow | {naar_element_id} | {waarom_deze_flow} |

### Triggering Relaties

| Trigger Element | Relatie Type | Getriggerd Element | Conditie |
|-----------------|--------------|-------------------|----------|
| {trigger_element_id} | Triggering | {target_element_id} | {conditie} |

### Serving Relaties

| Behavior Element | Relatie Type | Served Active Element | Doel |
|------------------|--------------|----------------------|------|
| {behavior_id} | Serving | {active_element_id} | {welke_capability_ondersteunt} |

---

## Koppeling naar Active Structuur

| Behavior Element | Gerealiseerd door (Active Element) | Assignment Rationale |
|------------------|-----------------------------------|----------------------|
| {behavior_id} | {active_element_id} (bijv. Application Component, Business Actor) | {waarom_deze_assignment} |

---

## Koppeling naar Passive Structuur

| Behavior Element | Gebruikt/Produceert (Passive Element) | Access Type | Rationale |
|------------------|--------------------------------------|-------------|-----------|
| {behavior_id} | {passive_element_id} (bijv. Data Object, Business Object) | Access / Write / Read | {waarom_deze_data_relatie} |

---

## Architectuurbeslissingen (ADRs)

### ADR-{nummer}: {titel_beslissing}

**Status**: {accepted/proposed/deprecated}  
**Context**: {waarom_was_deze_beslissing_nodig}  
**Beslissing**: {wat_is_besloten}  
**Consequenties**: {wat_zijn_de_gevolgen}

---

## Validatie Checklist

- [ ] Alle behavior elementen hebben een duidelijke trigger of initiator
- [ ] Flow-relaties tussen behavior elementen zijn compleet
- [ ] Elk behavior element is gekoppeld aan minimaal één active element (assignment)
- [ ] Serving-relaties naar active structuur zijn gevalideerd
- [ ] Access-relaties naar passive structuur (data) zijn gedocumenteerd
- [ ] ADRs zijn gedocumenteerd voor niet-triviale keuzes
- [ ] Naamgeving volgt ArchiMate naming conventions
- [ ] Strategie-consistentie is gevalideerd

---

## Herkomst

**Gebaseerd op**:
- Strategische richting: {strategie_document}
- Scope-definitie: {scope_document}
- ArchiMate metamodel: {archimate_versie}

**Canon SHA**: {canon_ref}  
**Doctrine**: doctrine-agent-charter-normering.md v{doctrine_versie}
