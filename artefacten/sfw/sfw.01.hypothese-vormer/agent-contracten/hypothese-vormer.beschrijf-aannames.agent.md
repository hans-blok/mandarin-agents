---
agent: hypothese-vormer
intent: beschrijf-aannames
versie: 1.1.0
---

# Hypothese-vormer — Beschrijf Aannames

## Rolbeschrijving (korte samenvatting)

De Hypothese-vormer expliciteert maximaal drie kritieke aannames als risico's die een hypothese dragen. Deze intent zoekt het hypothese-document op basis van de titel en beschrijft aannames met structuur wat/waarom/hoe-toetsen.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `hypothese-vormer.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- hypothese_titel: Titel van de hypothese waarvoor aannames worden geëxpliciteerd (type: string).

**Afgeleide informatie** (gegenereerd door agent):
- hypothese_bestand: Agent zoekt hypothese-document op basis van titel
- hypothese_context: Agent extraheert context uit gevonden hypothese-document
- auteur: Wordt overgenomen uit hypothese-document (of 'onbekend' indien niet aanwezig)
- datum: Aanmaakdatum of update-datum (format: yyyy-mm-dd)
- aanname_codes: Unieke identifiers per aanname (format: "AAN-{seq}")

### Output (wat komt eruit)

De Hypothese-vormer levert:
- **Aannames-sectie** (.md fragment) met maximaal 3 gestructureerde aannames:
  - Per aanname:
    - Korte naam/titel van de aanname
    - "Wat nemen we aan?": Expliciete formulering van de aanname
    - "Waarom is dit een risico?": Toelichting waarom het een aanname is (niet vaststaand feit)
    - "Hoe kunnen we dit toetsen?": Concrete mogelijkheden om aanname te valideren

**Deliverable bestand**: 
- Update van Sectie 3 in bestaand hypothese-document (gezocht op basis van hypothese_titel)

**VERPLICHT**: Het bestand MOET worden weggeschreven naar de workspace (niet alleen voorgesteld).

**Outputformaat**:
```markdown
## 3. Aannames (maximaal 3 risico's)

### Aanname 1: {Korte naam}
- **Wat nemen we aan?**: {Expliciete formulering van aanname}
- **Waarom is dit een risico?**: {Toelichting waarom dit geen vaststaand feit is}
- **Hoe kunnen we dit toetsen?**: {Concrete validatie-mogelijkheden}

### Aanname 2: {Korte naam}
- **Wat nemen we aan?**: ...
- **Waarom is dit een risico?**: ...
- **Hoe kunnen we dit toetsen?**: ...

### Aanname 3: {Korte naam}
- **Wat nemen we aan?**: ...
- **Waarom is dit een risico?**: ...
- **Hoe kunnen we dit toetsen?**: ...

---

**Herkomstverantwoording aannames**:
- Hypothese: {hypothese_titel}
- Datum: {yyyy-mm-dd}
- Bestand: {pad naar hypothese-document}
```

**Formaat-normering**: 
- Default formaat: **Markdown** (.md), conform Principe 9
- Maximaal 3 aannames (nooit meer)
- Elke aanname heeft exact 3 sub-secties: wat/waarom/hoe
- Aannames zijn geformuleerd als risico's, niet als zekerheden

### Foutafhandeling

De Hypothese-vormer:
- stopt wanneer hypothese_titel ontbreekt;
- stopt wanneer geen hypothese-document gevonden wordt met opgegeven titel;
- stopt wanneer gevonden hypothese-document niet leesbaar is;
- stopt wanneer hypothese_titel meerdere hypothese-documenten oplevert (ambiguïteit);
- escaleert naar capability-architect wanneer meer dan 3 aannames nodig lijken (boundary-issue);
- escaleert naar concept-curator voor begrippen in aannames die niet gedefinieerd zijn;
- STOP: bij ontbrekende hypothese_titel, bij niet-gevonden hypothese, bij ambigue titel.

**Contract is extern observeerbaar**: bevat GEEN implementatie-details, alleen wat agent ontvangt, levert en wanneer stopt.

---

## Werkwijze

### Stappen
1. **Valideer input**: Check of hypothese_titel aanwezig is.
2. **Zoek hypothese-document**: Zoek in workspace naar hypothese-document met opgegeven titel.
3. **Valideer unieke match**: Check dat precies 1 hypothese-document gevonden is (niet 0, niet meerdere).
4. **Lees hypothese**: Lees volledig hypothese-document voor context.
5. **Analyseer hypothese**: Identificeer kritieke onderdelen die op aannames berusten.
6. **Selecteer max 3 aannames**: Prioriteer meest kritieke aannames voor hypothese-validatie.
7. **Formuleer per aanname**:
   - Geef korte, heldere naam
   - Expliciteer wat wordt aangenomen (positieve formulering)
   - Leg uit waarom het een aanname is (geen feit)
   - Beschrijf concrete validatie-mogelijkheden
8. **Check overlap**: Zorg dat aannames niet overlappen en elk uniek risico adresseren.
9. **Check kritikaliteit**: Elke aanname moet kritiek zijn voor hypothese (niet nice-to-have).
10. **Genereer output**: Sectie 3 format volgens template.
11. **Update hypothese-document**: Schrijf Sectie 3 weg naar gevonden hypothese-bestand.
12. **Valideer compleetheid**: Max 3 aannames, elk met 3 sub-secties, als risico's geformuleerd.

### Kwaliteitsborging
- Maximaal 3 aannames (boundary-eis)
- Elke aanname heeft korte, heldere naam (max 80 karakters)
- "Wat nemen we aan?" is positief geformuleerd (niet: "we nemen aan dat X NIET...")
- "Waarom is dit een risico?" legt expliciet uit waarom het geen vaststaand feit is
- "Hoe kunnen we dit toetsen?" bevat concrete, uitvoerbare validatie-optie's
- Geen overlap tussen aannames (elk uniek risico)
- Alleen kritieke aannames (geen randvoorwaarden of nice-to-haves)
- Aannames zijn geformuleerd als risico's die hypothese ondermijnen als ze niet kloppen
- Hypothese-document correct gevonden via titel-match
- Sectie 3 update traceerbaar in hypothese-document
- Herkomstverantwoording compleet: hypothese-titel, datum, bestandspad

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract is extern observeerbaar
  - Principe 2 (Eenduidige Verantwoordelijkheid): Maximaal 3 aannames per uitvoering
  - Principe 7 (Transparante Verantwoording): Herkomst aannames gedocumenteerd
  - Principe 9 (Output-formaat Normering): Markdown als default

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream sfw
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)
- Raadpleegt Click-principe (Jake Knapp) voor aanname-formulering als risico's

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: hypothese-document (gezocht via titel), hypothese-template.md
- ✓ Bijgewerkte bestanden: hypothese-document (Sectie 3 aannames)
- ✓ Zoek-operatie: hypothese_titel → gevonden bestand
- ✓ Aanname-analyse: kritieke aannames geïdentificeerd, overlap gecheckt, kritikaliteit beoordeeld
- ✓ Boundary-check: max 3 aannames, als risico's geformuleerd

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → capability-architect: wanneer meer dan 3 aannames nodig lijken (boundary-issue)
- → concept-curator: voor begrippen in aannames die niet gedefinieerd zijn
- → thema-verwoorder: wanneer aannames zo breed zijn dat ze meerdere epics raken
- STOP: bij niet-gevonden hypothese, bij ambigue titel (meerdere matches), bij >3 aannames, bij overlappende aannames

---

## Metadata

**Intent-ID**: `sfw.01.hypothese-vormer.beschrijf-aannames`  
**Versie**: 1.1.0  
**Value Stream**: Software Product Development (sfw)  
**Fase**: 01 — Verkenning  
**Classificatie**: 
- Vormingsfase: Verkenning
- Betekeniseffect: Beschrijvend
- Werking: Inhoudelijk
- Bronhouding: Exploratief
