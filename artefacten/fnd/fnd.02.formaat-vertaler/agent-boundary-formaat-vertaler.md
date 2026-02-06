# Agent Boundary Bepaling — Formaat-Vertaler

**Datum**: 2026-01-27  
**Agent Curator**: Boundary bepaling voor utility value stream  
**Status**: Goedgekeurd voor handoff naar Agent Smeder

---

## 4-Regels Boundary

```
agent-naam: formaat-vertaler
capability-boundary: Vertaalt documenten tussen formaten (Markdown ↔ Word, en uitbreidbaar naar andere formaten) zonder inhoudelijke wijzigingen, waarbij structuur en opmaak behouden blijven.
doel: Technische formaat-conversie mogelijk maken tussen verschillende documentformaten voor hergebruik en uitwisseling.
domein: utility
```

---

## Aanleiding

Er is behoefte aan uitwisseling tussen Markdown (werkformaat binnen ontwikkelomgeving) en Word (stakeholder-formaat voor externe partijen). Markdown wordt gebruikt voor documentatie, beleid en andere werkdocumenten, maar externe stakeholders verwachten vaak Word-documenten. Omgekeerd moeten soms Word-documenten geïmporteerd worden in Markdown-workflows.

---

## Gewenste Capability

Vertalen van documenten tussen Markdown en Word (bidirectioneel) met behoud van structuur en basis-opmaak, zonder inhoudelijke wijzigingen. Later uitbreidbaar naar andere formaten zoals PDF, HTML, plain text.

---

## Value Stream

**utility** - ondersteunende dienst voor alle value streams

---

## Toelichting van de Boundary

### Scope (wat zit erin)
- **Technische conversie**: Formaat A → Formaat B zonder inhoudelijke wijziging
- **Structuurbehoud**: Kopjes, bullets, tabellen, secties blijven intact
- **Basis-opmaak**: Vet, cursief, links worden waar mogelijk behouden
- **Bidirectioneel**: Markdown → Word én Word → Markdown
- **Validatie**: Controle dat structuur behouden is na conversie
- **Uitbreidbaar**: Design voor toekomstige formaten (PDF, HTML, etc.)

### Scope (wat zit er NIET in)
- **Geen inhoudelijke wijzigingen**: Agent herschrijft of optimaliseert tekst niet
- **Geen complexe lay-out**: Alleen basis-opmaak, geen vormgeving of templates
- **Geen advies**: Agent adviseert niet over welk formaat te gebruiken
- **Geen embedded objecten**: Afbeeldingen, macro's, scripts worden niet geconverteerd

### Onderscheid met bestaande agents
- **kort-schrijver**: Herschrijft inhoud voor leesbaarheid; formaat-vertaler doet technische conversie
- **converter-md-to-archimate**: Converteert naar specifiek ArchiMate-model; formaat-vertaler doet algemene formaat-conversie
- **Publisher-agents**: Publiceren naar eindformaten; formaat-vertaler doet technische conversie voor hergebruik

---

## Consistentie-check

### Value stream validatie
✓ **utility** is geldige value stream in mandarin-canon  
✓ Ondersteunt alle andere value streams (kennispublicatie, IT-development, etc.)  
✓ Technische ondersteunende functie zonder strategische beslissingen

### Overlap-detectie
- **Geen overlap** met kort-schrijver (inhoud vs formaat)
- **Geen overlap** met converter-md-to-archimate (algemeen vs domein-specifiek)
- **Geen conflict** met toekomstige Publisher (conversie vs publicatie)

### Governance-check
✓ Binnen scope van utility value stream  
✓ Geen normatieve of strategische beslissingen  
✓ Technisch uitvoerende agent  
✓ Past binnen beleid-mandarin-agents.md

---

## Voorgestelde Intents (prompts)

1. **vertaal-naar-word**: Markdown → Word (.docx)
2. **vertaal-naar-markdown**: Word (.docx) → Markdown
3. **valideer-conversie**: Controle dat structuur behouden is

Toekomstige uitbreidingen (later):
- vertaal-naar-pdf
- vertaal-naar-html
- vertaal-vanaf-html

---

## Aanbevelingen voor Agent Smeder

### Folder structuur
```
exports/utility/
	agents/
		formaat-vertaler.vertaal-naar-word.agent.md
		formaat-vertaler.vertaal-naar-markdown.agent.md
		formaat-vertaler.valideer-conversie.agent.md
	prompts/
		mandarin.formaat-vertaler.vertaal-naar-word.prompt.md
		mandarin.formaat-vertaler.vertaal-naar-markdown.prompt.md
		mandarin.formaat-vertaler.valideer-conversie.prompt.md
	charters-agents/
		formaat-vertaler.charter.md
```

### Technische overwegingen voor runner
- Python libraries: `python-docx` (Word), `markdown` (Markdown)
- Validatie: structuur-vergelijking voor/na conversie
- Foutafhandeling: niet-ondersteunde elementen rapporteren
- Output: geconverteerd document + conversie-rapport

### Charter-aandachtspunten
- WEL/NIET grenzen zeer expliciet (geen inhoudelijke wijzigingen)
- Uitbreidbaarheid naar andere formaten beschrijven
- Validatie-proces beschrijven
- Foutafhandeling voor niet-ondersteunde elementen

---

## Volgende stappen

1. **Handoff naar Agent Smeder**: Deze boundary gebruiken voor agent-ontwerp
2. **Agent Smeder**: Prompts, charter en runner-skelet maken
3. **Testen**: Eerst Markdown ↔ Word, later andere formaten
4. **Documentatie**: Conversie-kwaliteit en beperkingen documenteren

---

**Goedkeuring**: Deze boundary is consistent met governance en utility value stream  
**Handoff**: Klaar voor Agent Smeder om agent te ontwerpen  
**Referentie**: formaat-vertaler.boundary.md

