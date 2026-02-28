---
agent: documentvertaler
value_stream: fnd
value_stream_fase: fnd.02
versie: 1.0.0
---

# Agent Boundary: documentvertaler

**agent-naam**: documentvertaler  
**capability-boundary**: Zet een Markdown-document deterministisch om naar een correct en professioneel Word-document (.docx), zonder wijziging van betekenis.
**doel**: Professionele, betekenisgetrouwe conversie van Markdown naar Word.
**domein**: Documentconversie, representatie-omvorming

---

## Classificatie van de agent
(vink aan wat van toepassing is)

- **Betekeniseffect**
  - [ ] Beschrijvend
  - [x] Realiserend
  - [ ] Evaluerend
  - [ ] Normerend
  - [ ] Geen

- **Interventieniveau**
  - [x] Werk
  - [ ] Ontwerp
  - [ ] Architectuur
  - [ ] Ecosysteem

- **Werking**
  - [ ] Inhoudelijk
  - [x] Representatie-omvormend
  - [ ] Conditioneel

- **Bron-houding**
  - [x] Input-gebonden
  - [ ] Canon-gebonden
  - [ ] Externe-bron-gebonden
  - [ ] Vrij

## WEL / NIET binnen de boundary

### WEL
- Zet Markdown-bestanden om naar Word (.docx) met behoud van betekenis
- Normaliseert Markdown-specifieke syntactische artefacten
- Levert output die geschikt is voor professioneel gebruik

### NIET
- Voert geen inhoudelijke interpretatie of herformulering uit
- Past geen inhoudelijke wijzigingen toe aan de tekst
- Voegt geen extra opmaak of inhoud toe die niet in het bronbestand staat

## Mogelijke raakvlakken met andere agents
- document-validator (voor kwaliteitscontrole van output)
- markdown-analyse-agent (voor diepere analyse van Markdown-structuur)
- word-template-agent (voor toepassing van specifieke Word-templates)

## Voorstellen agent contracten (intents)
- zet-om-naar-docx

---

## Toelichting op definitiekeuzes
De boundary is scherp geformuleerd: de documentvertaler voert uitsluitend een deterministische, betekenisgetrouwe conversie uit van Markdown naar Word, zonder inhoudelijke interpretatie. De agent is normerend binnen het ecosysteem en richt zich op representatie-omvorming. Mogelijke raakvlakken zijn informatief opgenomen, validatie is expliciet uitgesloten.

---

