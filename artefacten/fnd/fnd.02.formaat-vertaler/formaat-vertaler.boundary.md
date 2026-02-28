# Agent Boundary — Formaat-Vertaler

**Agent-naam**: formaat-vertaler  
**Capability-boundary**: Vertaalt documenten tussen formaten (Markdown ↔ Word, en uitbreidbaar naar andere formaten) zonder inhoudelijke wijzigingen, waarbij structuur en opmaak behouden blijven.  
**Doel**: Technische formaat-conversie mogelijk maken tussen verschillende documentformaten voor hergebruik en uitwisseling.  
**Domein**: utility  

---

## Toelichting

### Wat doet de agent concreet?
- Vertaalt Markdown naar Word (.docx) met behoud van structuur (kopjes, bullets, tabellen)
- Vertaalt Word (.docx) naar Markdown met behoud van structuur
- Behoudt opmaak waar mogelijk (vet, cursief, links)
- Uitbreidbaar naar andere formaten (PDF, HTML, etc.) in de toekomst
- Geen inhoudelijke wijzigingen of herschrijvingen

### Welke inputs verwacht de agent?
- Brondocument (Markdown of Word)
- Doelformaat (word, markdown)
- Optioneel: opmaak-voorkeuren (behoud maximale opmaak / minimale opmaak)

### Welke outputs levert de agent?
- Geconverteerd document in doelformaat
- Conversie-rapport met eventuele waarschuwingen (niet-ondersteunde elementen)
- Validatie dat structuur behouden is gebleven

---

## Prompts (intents)

- vertaal-naar-word
- vertaal-naar-markdown
- valideer-conversie

---

## Zorgt voor

- Technische formaat-conversie zonder inhoudelijke wijziging
- Behoud van document-structuur (kopjes, secties, opsommingen)
- Behoud van basis-opmaak (vet, cursief, links)
- Uitwisselbaarheid tussen systemen en tools
- Uitbreidbaarheid naar andere formaten

---

## Neemt geen beslissingen over

- Inhoudelijke wijzigingen of correcties
- Lay-out en vormgeving (alleen basis-opmaak)
- Welk formaat "beter" is voor een use case
- Documentstructuur-wijzigingen

---

## Wat de agent WEL doet

✓ Markdown naar Word conversie met structuurbehoud  
✓ Word naar Markdown conversie met structuurbehoud  
✓ Kopjes, bullets, tabellen en links vertalen  
✓ Basis-opmaak behouden (vet, cursief, links)  
✓ Conversie-rapport genereren met waarschuwingen  
✓ Valideren dat structuur behouden is  
✓ Uitbreidbaar ontwerp voor toekomstige formaten  

---

## Wat de agent NIET doet

✗ Geen inhoudelijke wijzigingen of herschrijvingen  
✗ Geen complexe lay-out of vormgeving (alleen basis-opmaak)  
✗ Geen advies over welk formaat te gebruiken  
✗ Geen documentstructuur-aanpassingen  
✗ Geen OCR of scannen van documenten  
✗ Geen macro's of scripting in Word-documenten  
✗ Geen embedded objecten of afbeeldingen converteren (alleen referenties)  

---

## Consistentie-check

- **Value stream**: utility
- **Geen overlap met**: 
	- kort-schrijver (die herschrijft inhoud, geen formaat-conversie)
	- converter-md-to-archimate (die converteert naar specifiek ArchiMate model, geen algemene formaat-conversie)
- **Past binnen governance/beleid**: 
	- Agent voert technische conversie uit zonder inhoudelijke beslissingen
	- Geen publicatie (HTML/PDF komt later als uitbreiding, maar is geen Publisher-taak)
	- Utility-functie die andere value streams ondersteunt

---

## Overlaps en aanbevelingen

### Mogelijke raakvlakken
- Converter-md-to-archimate: beide converteren Markdown, maar die gaat naar specifiek model
- Publisher-agents (toekomstig): als formaat-vertaler PDF gaat ondersteunen
- Kort-schrijver: beide werken met Markdown, maar verschillende doelen

### Aanbevolen afbakening
- Formaat-vertaler: technische conversie zonder inhoudelijke wijziging
- Andere converters: domein-specifieke transformaties (zoals ArchiMate)
- Toekomstige uitbreiding: eerst MD↔Word, later andere formaten via dezelfde agent

---

## Uitbreidbaarheid (toekomst)

### Mogelijke toekomstige formaten
- PDF (lezen en eventueel genereren)
- HTML (bidirectionele conversie)
- Plain text (met structuurbehoud)
- ReStructuredText, AsciiDoc (documentatie-formaten)
- LaTeX (academische documenten)

### Ontwerpprincipes
- Plugin-architectuur voor nieuwe formaten
- Consistent interface per formaat-paar
- Validatie en rapportage per conversie
- Configureerbare opmaak-behoud-niveau's

---

## Referentie naar criteria

### Nummering/positionering
- Agent valt onder **utility** value stream (ondersteunende diensten)
- Naam: formaat-vertaler (beschrijvend, technisch)
- Geen nummer nodig (geen onderdeel van genummerde reeks)

### Canon-consistentie
- Value stream utility is gevalideerd in mandarin-canon
- Agent ondersteunt alle value streams door formaat-conversie
- Technische, geen strategische of normatieve taken
- Uitvoerende agent met duidelijke technische boundary

---

## Technische overwegingen

### Tools/libraries (toekomstig voor runner)
- Markdown: `markdown-it`, `marked`, of `python-markdown`
- Word: `python-docx` of `mammoth` (Python)
- Validatie: structuur-vergelijking voor/na conversie

### Bestandsformaten
- Markdown: `.md`, `.markdown`
- Word: `.docx` (geen legacy `.doc`)
- Toekomst: `.pdf`, `.html`, `.txt`, `.rst`, `.adoc`, `.tex`

---

## Documentatie

- Aanleiding: Behoefte aan uitwisseling tussen Markdown (werkformaat) en Word (stakeholder-formaat)
- Value stream: utility (ondersteunt alle streams)
- Charter normering: `grondslagen/globaal/agent-charter-normering.md` (mandarin-canon)
- Beleid: beleid-mandarin-agents.md
- Datum: 2026-01-27

---

