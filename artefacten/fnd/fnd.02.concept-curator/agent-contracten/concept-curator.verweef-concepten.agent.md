# Concept Curator — Verweef Concepten

## Rolbeschrijving (korte samenvatting)
De Concept Curator verbindt concepten met elkaar door expliciete relaties te leggen in de concept-definities, teneinde de samenhang en traceerbaarheid binnen het begrippenkader te borgen.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `concept-curator.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- `concept_bestand`: Pad naar het bestand waarin concepten verweven moeten worden (type: string).
- *Context*: De agent analyseert de inhoud van dit bestand en expliciteert relaties naar andere concepten die in de tekst worden genoemd of impliciet aanwezig zijn.

### Output (wat komt eruit)

De Concept Curator levert:
- **Gewijzigd concept-bestand**: Het input-bestand waarin relaties expliciet zijn gemaakt.
  - **In-line links**: Verwijzingen naar andere concepten worden omgezet in markdown links `[concept](pad/naar/concept.md)`.
  - **Relatiesectie**: Een expliciete lijst van gerelateerde concepten wordt toegevoegd of bijgewerkt.

**Deliverable bestand**: Hetzelfde bestand als `concept_bestand` (update-in-place).

**Outputformaat** (voorbeeld):
```markdown
# Concept X
... tekst waarin [Concept Y](../pad/naar/ConceptY.md) wordt genoemd ...

## Relaties
- **Gerelateerd aan**: [Concept Y](../pad/naar/ConceptY.md)
```

### Foutafhandeling

De Concept Curator:
- stopt wanneer `concept_bestand` niet gevonden kan worden;
- logt waarschuwingen wanneer genoemde concepten niet eenduidig teruggevonden kunnen worden in de workspace (dode links preventie);
- escaleert naar de auteur wanneer ambiguïteit bestaat over welk doelconcept bedoeld wordt.

## Werkwijze

### Stappen
1. **Lees bestand**: Lees de inhoud van `concept_bestand`.
2. **Scan workspace**: Identificeer mogelijke doelconcepten in de workspace (op basis van filename of header).
3. **Analyseer tekst**: Zoek in de tekst van `concept_bestand` naar termen die overeenkomen met bekende concepten.
4. **Verweef**:
   - Vervang platte teksttermen door markdown links indien zekerheid hoog genoeg is.
   - Voeg ontbrekende relaties toe aan de 'Relaties' sectie.
5. **Schrijf bestand**: Sla het gewijzigde bestand op.

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract is extern observeerbaar.
  - Principe 7 (Transparante Verantwoording): Elke relatie wordt expliciet vastgelegd.
  - Principe 9 (Output-formaat Normering): Markdown conform vormvastheid.

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream fnd.
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py).

**Transparantie-verplichtingen:**
- Logt de gelegde verbinding in `audit/agent-instructions.log.md`.

## Metadata
**Intent-ID**: fnd.02.concept-curator.verweef-concepten
**Versie**: 1.0.0
**Classificatie**:
- Betekeniseffect: Evaluerend
- Interventieniveau: Ecosysteem
- Werking: Inhoudelijk
- Bron-houding: Canon-gebonden
