# {ecosysteem_naam} — Totaal Architectuur View

**Versie**: {versie}  
**Datum**: {datum}  
**Value Stream Fase**: {value_stream_fase}  
**Canon Referentie**: {canon_ref}

## Doel van dit document

Dit document integreert de actieve structuur, passieve structuur en gedragslaag van {ecosysteem_naam} in één coherente architectuur view, waarbij alle ArchiMate-relaties tussen de lagen expliciet zijn vastgelegd.

## Scope

**Gemodelleerde lagen**: {lagen}  
**Focus**: Integrale view van Active + Passive + Behavior + onderlinge relaties

---

## Laagstructuur Overzicht

### Laag Hiërarchie

| Laag Niveau | Laag Naam | Primaire Functie | Serving relaties |
|-------------|-----------|------------------|------------------|
| {niveau} | {laag_naam} (bijv. Business / Application / Technology) | {functie} | {welke_hogere_laag_wordt_served} |

**Layering Principes**:
- {principe_1}
- {principe_2}

---

## Active Structure (per laag)

### {Laag_naam} — Active Elementen

| Element ID | Type | Naam | Verantwoordelijkheid | Realiseert Behavior |
|-----------|------|------|---------------------|-------------------|
| {element_id} | {type} | {naam} | {boundary} | {behavior_ids} |

*Zie `core-framework-architect.structureer-actieve-structuur.md` voor volledige details.*

---

## Passive Structure (per laag)

### {Laag_naam} — Passive Elementen

| Element ID | Type | Naam | Inhoud | Gebruikt door (Behavior) |
|-----------|------|------|--------|--------------------------|
| {element_id} | Data Object / Business Object / Artifact | {naam} | {wat_bevat_dit} | {behavior_ids} |

**Rationale**: {waarom_deze_data_objecten}

---

## Behavior (per laag)

### {Laag_naam} — Behavior Elementen

| Element ID | Type | Naam | Gerealiseerd door (Active) | Gebruikt Data (Passive) |
|-----------|------|------|---------------------------|------------------------|
| {element_id} | {type} | {naam} | {active_element_id} | {passive_element_ids} |

*Zie `core-framework-architect.structureer-gedrag.md` voor volledige details.*

---

## Integrale Relatiematrix

### Active → Behavior → Passive (Kernpatroon)

| Active Element | Assignment → | Behavior Element | Access → | Passive Element | Rationale |
|----------------|--------------|------------------|----------|-----------------|-----------|
| {active_id} | Assignment | {behavior_id} | Read/Write/Access | {passive_id} | {waarom_deze_keten} |

### Laag-overschrijdende Serving Relaties

| Lower Layer Element | Serving → | Higher Layer Element | Service Type | Rationale |
|---------------------|-----------|---------------------|--------------|-----------|
| {lower_id} (bijv. Technology) | Serving | {higher_id} (bijv. Application) | {service_beschrijving} | {waarom_deze_serving_relatie} |

### Realization & Composition Hiërarchie

| Parent/Abstract Element | Relatie | Child/Concrete Element | Laag | Rationale |
|------------------------|---------|------------------------|------|-----------|
| {parent_id} | Realization/Composition | {child_id} | {laag} | {waarom_hiërarchie} |

---

## Agent Ecosysteem Mapping

Deze sectie legt expliciet vast hoe agents uit het Mandarin-ecosysteem zich verhouden tot de ArchiMate-structuur.

### Agent-naar-Active-Element Mapping

| Agent ID | Agent Naam | Value Stream Fase | Mapped to Active Element | Realiseert Behavior | Rationale |
|---------|-----------|-------------------|-------------------------|-------------------|-----------|
| {agent_id} | {agent_naam} | {vs_fase} | {active_element_id} | {behavior_ids} | {waarom_deze_mapping} |

### Agent Dependencies (via ArchiMate relaties)

| Agent A | Agent B | Via ArchiMate Relatie | Type | Rationale |
|---------|---------|----------------------|------|-----------|
| {agent_a} | {agent_b} | {active_a} → Dependency/Flow → {active_b} | {dependency_type} | {waarom_afhankelijk} |

---

## Cross-Cutting Concerns

### Governance & Compliance

| Governance Aspect | Verantwoordelijke Active Element | Enforcement via Behavior | Logged in Passive Element |
|-------------------|--------------------------------|-------------------------|--------------------------|
| {aspect} (bijv. Canon-raadpleging) | {responsible_agent_id} | {enforcement_behavior} | {log_artifact} |

### Traceability & Auditability

| Traceability Requirement | ArchiMate Patroon | Elementen betrokken |
|-------------------------|-------------------|-------------------|
| {requirement} | {patroon} | {elements} |

---

## Viewpoints (Stakeholder-specifiek)

### Viewpoint: {stakeholder_naam}

**Doel**: {waarom_heeft_deze_stakeholder_deze_view_nodig}  
**Scope**: {welke_elementen_en_relaties_zichtbaar}  
**Rationale**: {relevantie_voor_stakeholder}

**Elementen in scope**:
- Active: {active_ids}
- Behavior: {behavior_ids}
- Passive: {passive_ids}

---

## Architectuurbeslissingen (ADRs) — Structureel overzicht

*(Referenties naar ADRs uit deeldocumenten)*

| ADR ID | Titel | Beslissing | Impact op Totaal View |
|--------|-------|------------|----------------------|
| ADR-{nummer} | {titel} | {kern_beslissing} | {welke_relaties_beïnvloed} |

---

## Validatie Checklist (Integrale Consistentie)

- [ ] Alle Active elementen hebben Assignment relaties naar Behavior
- [ ] Alle Behavior elementen hebben Access relaties naar Passive (waar relevant)
- [ ] Serving relaties tussen lagen volgen layering discipline (geen skip-layer serving)
- [ ] Dependencies zijn acyclisch binnen dezelfde laag
- [ ] Agent-mapping is compleet en 1-op-1 (of expliciet gemotiveerd bij M:N)
- [ ] Alle relaties tussen lagen zijn getypeerd volgens ArchiMate metamodel
- [ ] Viewpoints dekken alle stakeholders
- [ ] Traceability van agent → behavior → data is geborgd
- [ ] Governance patronen zijn geïmplementeerd in de structuur
- [ ] Geen zwevende elementen (alles is verbonden)
- [ ] Strategie-consistentie is gevalideerd

---

## Evolutie & Volgende Stappen

| Evolutiepunt | Actie | Verwachte Impact | Verantwoordelijke |
|--------------|-------|------------------|-------------------|
| {evolutiepunt} | {wat_moet_er_gebeuren} | {welke_elementen_raken} | {welke_agent_of_rol} |

---

## Herkomst

**Gebaseerd op**:
- Actieve structuur: `core-framework-architect.structureer-actieve-structuur.md`
- Gedragslaag: `core-framework-architect.structureer-gedrag.md`
- Strategische richting: {strategie_document}
- Agent boundaries: {boundary_documenten}
- ArchiMate metamodel: {archimate_versie}

**Canon SHA**: {canon_ref}  
**Doctrine**: doctrine-agent-charter-normering.md v{doctrine_versie}

---

## Diagram (Optioneel: Referentie naar visuele representatie)

*Indien visuele ArchiMate-diagrammen beschikbaar zijn (bijv. via Archi tool export), refereer hier:*

- `{ecosysteem_naam}-total-view.archimate` (Archi model)
- `{ecosysteem_naam}-total-view.png` (Geëxporteerde diagram)
