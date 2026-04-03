---
agent: hypothese-vormer
intent: beschrijf-toetsbaarheid
versie: 1.0.0
digest: 1c04
status: vers
---
# Hypothese-vormer — Beschrijf Toetsbaarheid

## Rolbeschrijving (korte samenvatting)

De Hypothese-vormer expliciteert de toetsbaarheid van een hypothese door concrete criteria te definiëren voor wanneer de hypothese klopt, wanneer niet klopt, en wat de eerste toetsstap zou zijn. Deze intent zorgt dat hypotheses observeerbaar en valideerbaar worden.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `hypothese-vormer.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- hypothese_statement: De hypothese-formulering die toetsbaar moet worden gemaakt (type: string, minimaal 30 karakters). Format: "[Interventie] is beter dan [status quo] omdat [effect]".
- auteur: Naam van degene die toetsbaarheid expliceert (type: string).

**Optionele parameters**:
- hypothese_bestand: Pad naar bestaand hypothese-document indien verfijning van bestaande hypothese (type: string, relatief pad).
- toetsingscontext: Context waarin getoetst zou worden (type: string, bijv. "pilotgroep van 10 gebruikers gedurende 2 weken").
- beschikbare_metrics: Lijst van beschikbare meetinstrumenten of observatie-mogelijkheden (type: list[string]).
- acceptatie_drempel: Minimale verbetering die als succes gezien wordt (type: string, bijv. "20% sneller", "0 fouten in eerste week").

**Afgeleide informatie** (gegenereerd door agent):
- datum: Aanmaakdatum of update-datum (format: yyyy-mm-dd)
- toetsbaarheids_score: Indicatie of hypothese voldoende concreet is om te toetsen (hoog/medium/laag)

### Output (wat komt eruit)

De Hypothese-vormer levert:
- **Toetsbaarheids-sectie** (.md fragment) met concrete validatie-criteria:
  - "Wat zou betekenen dat deze hypothese klopt?": Concrete, observeerbare criteria voor succes
  - "Wat zou betekenen dat deze hypothese niet klopt?": Concrete deal-breakers of falsificatie-criteria
  - "Eerste stap om te toetsen": Kleinst mogelijke experiment of observatie om hypothese te testen

**Deliverable bestand**: 
- Bij nieuwe hypothese: standalone `toetsbaarheid-{datum}.md` in output folder
- Bij verfijning bestaande hypothese: update van Sectie 5 in bestaand hypothese-document

**VERPLICHT**: Het bestand MOET worden weggeschreven naar de workspace (niet alleen voorgesteld).

**Outputformaat**:
```markdown
## 5. Toetsbaarheid

### Wat zou betekenen dat deze hypothese klopt?

{Concrete, observeerbare criteria:}
- {Criterium 1: wat zou je moeten zien, meten of observeren?}
- {Criterium 2: bij welke uitkomst concludeer je dat effect optreedt?}
- {Criterium 3: welke gedragsverandering of resultaat duidt op succes?}

**Acceptatie-drempel**: {minimale verbetering die als succes geldt}

### Wat zou betekenen dat deze hypothese niet klopt?

{Concrete deal-breakers:}
- {Deal-breaker 1: bij welke uitkomst verwerp je hypothese?}
- {Deal-breaker 2: welk gebrek aan effect zou fataal zijn?}
- {Deal-breaker 3: welke negatieve bijwerking zou interventie diskwalificeren?}

**Verwerp-criteria**: {harde grens waarbij hypothese verworpen moet worden}

### Eerste stap om te toetsen

**Experiment**: {Beschrijf kleinst mogelijke eerste stap}
- **Wat**: {Wat doe je concreet?}
- **Met wie**: {Wie zijn betrokken/benaderd?}
- **Hoelang**: {Tijdsduur van toets}
- **Meet**: {Wat observeer/meet je?}
- **Besluit na**: {Wanneer besluit je over volgende stap?}

---

**Herkomstverantwoording toetsbaarheid**:
- Auteur: {auteur}
- Datum: {yyyy-mm-dd}
- Context: {toetsingscontext indien opgegeven}
```

**Formaat-normering**: 
- Default formaat: **Markdown** (.md), conform Principe 9
- Minimaal 2 succes-criteria en 2 verwerp-criteria
- Eerste toetsstap maximaal 1 week uitvoeringstijd, minimale investering
- Criteria zijn concreet en observeerbaar (niet vaag of subjectief)

### Foutafhandeling

De Hypothese-vormer:
- stopt wanneer hypothese_statement ontbreekt of te vaag is (<30 karakters);
- stopt wanneer auteur ontbreekt;
- stopt wanneer hypothese_statement geen meetbaar effect bevat (niet toetsbaar te maken);
- stopt wanneer hypothese_bestand wordt opgegeven maar niet bestaat of niet leesbaar is;
- vraagt om verduidelijking wanneer hypothese_statement alleen qualitatieve claims bevat zonder observeerbare indicatoren;
- vraagt om verduidelijking wanneer acceptatie_drempel te vaag is (bijv. "beter" zonder maat);
- escaleert naar thema-verwoorder wanneer toetsing meerdere epics/features vereist (buiten scope van één hypothese);
- escaleert naar concept-curator voor metrics of begrippen die niet gedefinieerd zijn;
- STOP: bij ontbrekende input-parameters, bij fundamenteel niet-toetsbare hypothese, bij eerste toetsstap >1 week of >€1000 investering.

**Contract is extern observeerbaar**: bevat GEEN implementatie-details, alleen wat agent ontvangt, levert en wanneer stopt.

---

## Werkwijze

### Stappen
1. **Valideer input**: Check of hypothese_statement en auteur aanwezig zijn.
2. **Lees context**: Bij hypothese_bestand opgegeven: lees bestaand document voor volledige context.
3. **Analyseer hypothese**: Extraheer interventie, status quo en verondersteld effect uit statement.
4. **Bepaal observeerbare indicatoren**: Welke uitkomsten duiden op succes van het veronderstelde effect?
5. **Formuleer succes-criteria**: Minimaal 2 concrete, meetbare of observeerbare criteria voor "klopt".
6. **Formuleer verwerp-criteria**: Minimaal 2 concrete deal-breakers voor "klopt niet".
7. **Definieer acceptatie-drempel**: Bij welke minimale verbetering geldt hypothese als bevestigd?
8. **Definieer verwerp-grens**: Bij welke uitkomst wordt hypothese definitief verworpen?
9. **Ontwerp eerste toetsstap**: Kleinst mogelijke experiment (max 1 week, minimale investering).
10. **Check Click-principe**: Toetsbaarheid moet helder zijn (niet vaag), eerste stap minimaal (niet zwaar).
11. **Genereer output**: Sectie 5 format volgens template.
12. **Schrijf weg**: Update bestaand document OF creëer standalone toetsbaarheid-bestand.
13. **Valideer concreetheid**: Criteria zijn observeerbaar, niet vaag; eerste stap is uitvoerbaar binnen 1 week.

### Kwaliteitsborging
- Minimaal 2 succes-criteria, elk concreet en observeerbaar
- Minimaal 2 verwerp-criteria (deal-breakers)
- Acceptatie-drempel is kwantitatief (niet "beetje beter" maar "20% sneller")
- Verwerp-grens is expliciet (niet "als het niet werkt" maar "bij <5% verbetering na 1 week")
- Eerste toetsstap:
  - Maximaal 1 week uitvoeringstijd
  - Minimale investering (<€1000 of <40 uur)
  - Concreet beschreven: wat/wie/hoelang/meet/besluit
  - Geen ontwerpwerk of implementatie (observatie/gesprek/kleine pilot)
- Criteria zijn toetsbaar zonder grote infrastructuur of systemen
- Bij bestaand hypothese-bestand: referentie correct, update traceerbaar
- Herkomstverantwoording compleet: auteur, datum, context

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract is extern observeerbaar
  - Principe 2 (Eenduidige Verantwoordelijkheid): Focus op toetsbaarheid, niet op uitvoering
  - Principe 7 (Transparante Verantwoording): Herkomst toetsbaarheid gedocumenteerd
  - Principe 9 (Output-formaat Normering): Markdown als default

**Canon-consultatie:**
- Raadpleegt `audit/canon-consult.log.md` voor grondslagen uit value stream sfw
- Bootstrap via `scripts/bootstrap_canon_consult.py` (automatisch door run_prompt.py)
- Raadpleegt Click-principe (Jake Knapp) voor minimale eerste toetsstap

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen bestanden: hypothese_bestand (indien opgegeven), hypothese-template.md
- ✓ Aangemaakte bestanden: toetsbaarheid-{datum}.md OF bijgewerkt hypothese-bestand
- ✓ Toetsbaarheids-analyse: succes-criteria gedefinieerd, verwerp-criteria gedefinieerd, eerste toetsstap ontworpen
- ✓ Click-principe check: eerste stap minimaal (max 1 week, minimale investering)

Logging-formaat: Markdown append naar `audit/agent-instructions.log.md`

**Escalatie-paden:**
- → thema-verwoorder: wanneer toetsing meerdere epics/features vereist (buiten scope van één hypothese)
- → concept-curator: voor metrics of begrippen in toetscriteria die niet gedefinieerd zijn
- → capability-architect: wanneer hypothese fundamenteel niet toetsbaar blijkt (boundary-issue)
- STOP: bij fundamenteel niet-toetsbare hypothese, bij eerste toetsstap >1 week of >€1000, bij vage criteria

---

## Metadata

**Intent-ID**: `sfw.01.hypothese-vormer.beschrijf-toetsbaarheid`  
**Versie**: 1.0.0  
**Value Stream**: Software Product Development (sfw)  
**Fase**: 01 — Verkenning  
**Classificatie**: 
- Vormingsfase: Verkenning
- Betekeniseffect: Beschrijvend
- Werking: Inhoudelijk
- Bronhouding: Exploratief
