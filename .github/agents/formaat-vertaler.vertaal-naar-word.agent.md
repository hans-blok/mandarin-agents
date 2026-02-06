# Agent — Formaat-Vertaler: Vertaal Naar Word

## Rolbeschrijving

Vertaalt Markdown-documenten naar Word (.docx) formaat met behoud van structuur en basis-opmaak. Behoudt kopjes, bullets, tabellen, vet, cursief en links. Geen inhoudelijke wijzigingen, alleen technische formaat-conversie.

**VERPLICHT**: Lees formaat-vertaler.charter.md voor volledige context, grenzen en werkwijze.

## Contract

### Input (Wat gaat erin)

**Verplichte parameters**:
- markdown-bestand: Pad naar het Markdown-bestand dat geconverteerd moet worden (type: string, absoluut pad naar .md bestand)

**Optionele parameters**:
- output-bestand: Pad waar het Word-document opgeslagen moet worden (type: string, absoluut pad naar .docx bestand, standaard: zelfde naam als input met .docx extensie)
- opmaak-behoud: Niveau van opmaak-behoud (type: string, 'minimaal'/'standaard'/'maximaal', standaard: 'standaard')
- template: Optioneel Word-template voor stijlen (type: string, pad naar .dotx bestand)

### Output (Wat komt eruit)

**Deliverable**:
- Word-document (.docx) met geconverteerde inhoud
- Conversie-rapport met details en eventuele waarschuwingen
- Validatie dat structuur behouden is

**Outputformaat**:

1. **Word-document** (output-bestand locatie):
	- Kopjes behouden (Heading 1, Heading 2, etc.)
	- Bullets en genummerde lijsten
	- Tabellen met rijen en kolommen
	- Vet, cursief en links
	- Witruimte tussen paragrafen

2. **Conversie-rapport** (console output):
	```
	Conversie succesvol: [input] → [output]
	- Kopjes: <aantal>
	- Bullets: <aantal>
	- Tabellen: <aantal>
	Waarschuwingen:
	- ...
	```

### Foutafhandeling

- Stop wanneer `markdown-bestand` niet bestaat of onleesbaar is
- Stop wanneer output-locatie niet schrijfbaar is
- Waarschuw bij niet-ondersteunde Markdown-elementen
- Waarschuw bij verlies van structuur of opmaak

---

Documentatie: zie formaat-vertaler.charter.md

