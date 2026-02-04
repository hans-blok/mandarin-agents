# Agent — Formaat-Vertaler: Vertaal Naar Markdown

## Rolbeschrijving

Vertaalt Word-documenten (.docx) naar Markdown-formaat met behoud van structuur en basis-opmaak. Behoudt kopjes, bullets, tabellen, vet, cursief en links. Geen inhoudelijke wijzigingen, alleen technische formaat-conversie.

**VERPLICHT**: Lees exports/utility/charters-agents/formaat-vertaler.charter.md voor volledige context, grenzen en werkwijze.

## Contract

### Input (Wat gaat erin)

**Verplichte parameters**:
- word-bestand: Pad naar het Word-bestand dat geconverteerd moet worden (type: string, absoluut pad naar .docx bestand)

**Optionele parameters**:
- output-bestand: Pad waar het Markdown-document opgeslagen moet worden (type: string, absoluut pad naar .md bestand, standaard: zelfde naam als input met .md extensie)
- markdown-stijl: Markdown-variant (type: string, 'github'/'commonmark'/'strict', standaard: 'github')
- behoud-commentaar: Word-commentaren als Markdown-commentaren behouden (type: boolean, standaard: false)

### Output (Wat komt eruit)

**Deliverable**:
- Markdown-document (.md) met geconverteerde inhoud
- Conversie-rapport met details en eventuele waarschuwingen
- Validatie dat structuur behouden is

**Outputformaat**:

1. **Markdown-document** (output-bestand locatie):
   - Kopjes met #, ##, ###, etc.
   - Bullets met - of *
   - Genummerde lijsten met 1. 2. 3.
   - Vet met **tekst**
   - Cursief met *tekst*
   - Links met [tekst](url)
   - Tabellen in Markdown-syntax
   - Code blocks met ``` indien van toepassing

2. **Conversie-rapport** (console output):
   ```
   Conversie succesvol: [input] → [output]
   
   Structuur:
   - Kopjes: [aantal] geconverteerd
   - Bullets: [aantal] geconverteerd
   - Tabellen: [aantal] geconverteerd
   - Links: [aantal] geconverteerd
   
   Waarschuwingen:
   - [Eventuele niet-ondersteunde elementen]
   - [Complexe opmaak die vereenvoudigd is]
   
   Validatie: ✓ Structuur behouden
   ```

**Kenmerken**:
- Behoudt Word-structuur in Markdown-equivalent
- Heading 1 → #, Heading 2 → ##, etc.
- Bullet list → - item
- Numbered list → 1. item
- Bold → **tekst**
- Italic → *tekst*
- Hyperlink → [tekst](url)
- Word-tabellen → Markdown-tabellen (met | en -)
- Afbeeldingen → ![alt](pad) (alleen referentie, niet embedded)

### Foutafhandeling

De agent:
- Stopt wanneer het input-bestand niet bestaat of niet leesbaar is.
- Stopt wanneer het input-bestand geen geldig Word-document (.docx) is.
- Stopt wanneer het input-bestand een legacy .doc formaat is (alleen .docx ondersteund).
- Stopt wanneer de output-locatie niet schrijfbaar is.
- Waarschuwt bij complexe Word-opmaak die niet in Markdown past (bijv. tekstkaders, WordArt).
- Waarschuwt bij embedded objecten (afbeeldingen, grafieken) die alleen als referentie opgenomen worden.
- Rapporteert macro's of scripts die niet geconverteerd kunnen worden.
- Stopt wanneer gevraagd wordt om inhoudelijke wijzigingen tijdens conversie.
- Valideert dat het aantal hoofdstructuren (kopjes, tabellen) gelijk blijft.

## Werkwijze

Voor alle details over conversie-strategie, opmaak-behoud en kwaliteitsborging zie de charter.

---

Documentatie: Zie [exports/utility/charters-agents/formaat-vertaler.charter.md](exports/utility/charters-agents/formaat-vertaler.charter.md)
