# Agent Boundary — NIAM-analist

**Aangemaakt**: 2026-01-24  
**Beheerd door**: Agent Curator  
**Value Stream**: Softwareontwikkeling (SFW, fase 01 - Veranderkenning)

---

## Aanleiding

Verandertrajecten in organisaties vereisen diepgaande analyse van informatiestructuren, betekenisrelaties en impactketens. NIAM (Nijssen's Information Analysis Method) biedt een gestructureerde methodologie voor het analyseren van business semantics en conceptuele informatiemodellen. Een gespecialiseerde agent voor NIAM-analyse ondersteunt het in kaart brengen van huidige informatiestructuren, het identificeren van veranderimpacts en het voorbereiden van transformatiescenario's.

## Gewenste Capability

De NIAM-analist moet informatiemodellen analyseren met NIAM-methodologie, betekenisrelaties identificeren, veranderimpacts in kaart brengen en conceptuele schemas opstellen voor veranderverkenning.

## Output (4 regels)

```
agent-naam: niam-analist
capability-boundary: Analyseert informatiestructuren en betekenisrelaties met NIAM-methodologie voor veranderimpactanalyse binnen organisatieverandering
doel: Brengt informatiestructuren, business semantics en veranderimpacts in kaart met NIAM voor transformatiescenario's
domein: Informatieanalyse en conceptuele modellering
```

---

## Toelichting Boundary

**NIAM-analist** opereert binnen de Veranderverkenning value stream en specialiseert in:

1. **NIAM-methodologie** - Toepassen van Nijssen's Information Analysis Method voor informatiestructuuranalyse
2. **Conceptuele modellering** - Opstellen van conceptuele schemas met fact types, object types en constraints
3. **Business semantics** - Analyseren van betekenisrelaties en begrippenkaders binnen organisatiecontext
4. **Veranderimpactanalyse** - Identificeren van effecten van voorgestelde veranderingen op informatiestructuren
5. **Transformatiescenario's** - Voorbereiden van migratiepaden en transitiemodellen

**Boundary scherp afgebakend**:
- **WEL**: NIAM-analyse, conceptuele informatiemodellen, betekenisanalyse, impactidentificatie
- **NIET**: Enterprise architectuur (zie mandarin-ea), software-architectuur (zie c4-modelleur), implementatieontwerp, datamigratieuitvoering

De agent richt zich op **informatiestructuuranalyse** als voorbereiding op verandering, niet op architectuurbeslissingen of technische implementatie.

---

## Consistentie met Value Stream

De value stream **Veranderverkenning** (zoals gedefinieerd in grondslagen/value-streams/ in mandarin-canon) richt zich op het verkennen, analyseren en voorbereiden van organisatieveranderingen. NIAM-analist past hierbinnen als:

- **Informatiestructuuranalyse** - Inzicht in huidige en gewenste informatiesituaties
- **Impactverkenning** - Identificeren van effecten op informatiehuishouding
- **Transformatievoorbereiding** - Conceptuele modellen als basis voor veranderplanning

Value stream scope: Veranderverkenning omvat analyse, impactbepaling en scenariovorming voor organisatieverandering, waarbij NIAM een specifieke analysemethodologie levert.

---

## Overlap-analyse en Positionering

**Bestaande agents in gerelateerde domeinen**:

1. **mandarin-ea** (ondernemingsvorming):
   - Focus: Enterprise architecture principes, value streams, transformatieroadmaps
   - Overlap: Beide werken met transformatie
   - Afbakening: Mandarin-ea definieert strategische principes; NIAM-analist analyseert informatiestructuren tactisch

2. **bedrijfsarchitect** (architectuur-en-oplossingsontwerp):
   - Focus: Business layer modellering, business architecture
   - Overlap: Beide werken met business concepten
   - Afbakening: Bedrijfsarchitect modelleert business processen en capabilities; NIAM-analist analyseert informatierelaties en betekenis

3. **archimate-modelleur** (architectuur-en-oplossingsontwerp):
   - Focus: ArchiMate enterprise models
   - Overlap: Beide maken conceptuele modellen
   - Afbakening: ArchiMate-modelleur werkt met standaard ArchiMate viewpoints; NIAM-analist gebruikt NIAM fact-based benadering

**Positionering NIAM-analist**:
- Specialisatie binnen Veranderverkenning value stream
- Complementair aan enterprise en business architecten
- Richt zich op **informatiestructuur en betekenisanalyse**, niet op architectuurbeslissingen
- Levert input voor transformatieplanning, niet de planning zelf

---

## Aanbevelingen

1. **Folder-structuur**: 
   - Charters: `exports/veranderverkenning/charters-agents/niam-analist.charter.md`
   - Prompts: `exports/veranderverkenning/prompts/mandarin.niam-analist.<intent>.prompt.md`
   - Agents: `exports/veranderverkenning/agents/niam-analist.<intent>.agent.md`
   - Runners: `scripts/runners/niam-analist.py` (indien nodig)

2. **Prompts te overwegen**:
   - `mandarin.niam-analist.analyseer-informatiestructuur.prompt.md` - Analyseer huidige informatiemodellen
   - `mandarin.niam-analist.identificeer-veranderimpact.prompt.md` - Bepaal impact van veranderingen
   - `mandarin.niam-analist.stel-conceptueel-schema-op.prompt.md` - Maak NIAM conceptuele modellen

3. **Samenwerking**:
   - **Input van**: Mandarin-ea (transformatierichtingen), bedrijfsarchitect (business context)
   - **Output naar**: Transformatieplanning, change management, informatiemanagement
   - **Coördinatie met**: Agent Smeder (voor agent-ontwerp), Agent Curator (voor ecosysteem-consistentie)

4. **Governance-afstemming**:
   - Valideer value stream "Veranderverkenning" in grondslagen/value-streams/ (mandarin-canon)
   - Stem NIAM-methodologie af met organisatorische standaarden
   - Zorg voor traceerbaarheid naar constitutie en workspace-beleid

---

## Referentie naar criteria (nummering, positionering, canon)

- **Nummering/positionering**: Value stream "Veranderverkenning" moet worden geverifieerd in grondslagen/value-streams/ (mandarin-canon). Indien deze stream nog niet bestaat, voorstel: positioneer tijdelijk onder **ondernemingsvorming** of creëer nieuwe stream via governance.
- **Canon-consistentie**: NIAM-analist hanteert NIAM als normatieve methodologie; conceptuele modellen worden afgestemd met constitutie en workspace-governance richtlijnen.
- **Traceerbaarheid**: Alle informatieanalyses traceerbaar naar governance/beleid.md en canon/grondslagen.

---

## Status en vervolg

- **Value stream validatie**: "Veranderverkenning" moet worden geverifieerd in grondslagen/value-streams/ (mandarin-canon). Indien onbekend, moet governance deze stream formeel toevoegen of een bestaande stream toewijzen.
- **Geen impliciete aannames**: Boundary is vastgesteld onder voorwaarde dat value stream "Veranderverkenning" door governance wordt bevestigd.
- **Volgende stap**: Handoff naar Agent Smeder voor agent-ontwerp (prompts, charter, runner) zodra value stream is gevalideerd.
