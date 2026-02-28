# {ecosysteem_naam} — Actieve Structuur Definitie

**Versie**: {versie}  
**Datum**: {datum}  
**Value Stream Fase**: {value_stream_fase}  
**Canon Referentie**: {canon_ref}

## Doel van dit document

Dit document definieert de actieve structuurlagen (active structure) van {ecosysteem_naam}, waarbij expliciet wordt vastgelegd welke actoren, applicatiecomponenten en technische nodes verantwoordelijk zijn voor het realiseren van gedrag.

## Scope

**Gemodelleerde lagen**: {lagen}  
**Focus**: Active elementen (actors, components, nodes) en hun onderlinge relaties

---

## ArchiMate Active Structure Elementen

### Business Layer Active Structure

| Element ID | Type | Naam | Rol/Verantwoordelijkheid | Boundary |
|-----------|------|------|--------------------------|----------|
| {element_id} | Business Actor / Business Role / Business Collaboration | {element_naam} | {verantwoordelijkheid} | {capability_boundary} |

**Rationale**: {waarom_deze_actoren}

### Application Layer Active Structure

| Element ID | Type | Naam | Capability | Interfaces |
|-----------|------|------|------------|-----------|
| {element_id} | Application Component / Application Collaboration | {element_naam} | {welke_functie} | {externe_interfaces} |

**Agents binnen deze laag**:
| Agent ID | Agent Naam | Intent(s) | Component Assignment |
|---------|-----------|-----------|---------------------|
| {agent_id} | {agent_naam} | {intents} | {welke_component_realiseert_agent} |

**Rationale**: {waarom_deze_componenten}

### Technology Layer Active Structure (indien van toepassing)

| Element ID | Type | Naam | Hosting Capability | Communicatie |
|-----------|------|------|-------------------|--------------|
| {element_id} | Node / Device / System Software | {element_naam} | {wat_host_dit} | {protocols} |

**Rationale**: {waarom_deze_nodes}

---

## Hiërarchische Relaties (Composition & Aggregation)

### Compositie binnen lagen

| Parent Element | Relatie Type | Child Element | Rationale |
|----------------|--------------|---------------|-----------|
| {parent_id} | Composition | {child_id} | {waarom_deze_samenstelling} |

### Aggregatie patronen

| Container Element | Relatie Type | Aggregated Elements | Doel |
|-------------------|--------------|---------------------|------|
| {container_id} | Aggregation | {element_ids} | {waarom_gegroepeerd} |

---

## Lagen-overschrijdende Relaties

### Assignment (Active → Behavior)

| Active Element | Relatie Type | Assigned Behavior | Rationale |
|----------------|--------------|-------------------|-----------|
| {active_id} | Assignment | {behavior_id} | {waarom_deze_actor_dit_gedrag_uitvoert} |

### Realization (Component → Service)

| Component | Relatie Type | Gerealiseerde Service | Interface |
|-----------|--------------|----------------------|-----------|
| {component_id} | Realization | {service_id} | {interface_specificatie} |

### Serving (Lower layer → Higher layer)

| Serving Element | Relatie Type | Served Element | Service Type |
|-----------------|--------------|----------------|--------------|
| {lower_layer_id} | Serving | {higher_layer_id} | {welke_service_geleverd} |

---

## Dependencies & Communicatie

### Dependency patronen

| Dependent Element | Relatie Type | Dependency Target | Aard van dependency |
|-------------------|--------------|-------------------|-------------------|
| {dependent_id} | Dependency | {target_id} | {waarom_afhankelijk} |

### Flow tussen active elementen

| Van Element | Relatie Type | Naar Element | Flow Type |
|-------------|--------------|--------------|-----------|
| {van_id} | Flow | {naar_id} | {data/control/message} |

---

## Agent-naar-Component Mapping

Deze sectie legt expliciet vast welke agents (uit het agent-ecosysteem) welke application components realiseren of gebruiken.

| Agent Naam | Agent Boundary | Gerealiseerde Component(en) | Intent(s) | Rationale |
|-----------|----------------|----------------------------|----------|-----------|
| {agent_naam} | {boundary_omschrijving} | {component_id} | {intents} | {waarom_deze_mapping} |

---

## Architectuurbeslissingen (ADRs)

### ADR-{nummer}: {titel_beslissing}

**Status**: {accepted/proposed/deprecated}  
**Context**: {waarom_was_deze_beslissing_nodig}  
**Beslissing**: {wat_is_besloten}  
**Consequenties**: {wat_zijn_de_gevolgen}

---

## Validatie Checklist

- [ ] Alle active elementen hebben een duidelijke verantwoordelijkheid/boundary
- [ ] Hiërarchische relaties (composition/aggregation) zijn consistent
- [ ] Assignment-relaties naar behavior layer zijn compleet
- [ ] Serving-relaties tussen lagen volgen layering principes
- [ ] Dependencies zijn gedocumenteerd en gerechtvaardigd
- [ ] Agent-naar-component mapping is 1-op-1 of expliciet gemotiveerd
- [ ] Naamgeving volgt ArchiMate naming conventions
- [ ] Geen circulaire dependencies binnen dezelfde laag
- [ ] Strategie-consistentie is gevalideerd

---

## Herkomst

**Gebaseerd op**:
- Strategische richting: {strategie_document}
- Agent boundaries: {boundary_documenten}
- ArchiMate metamodel: {archimate_versie}

**Canon SHA**: {canon_ref}  
**Doctrine**: doctrine-agent-charter-normering.md v{doctrine_versie}
