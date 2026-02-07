# investerings-verteller — schrijf-30-seconden-pitch (contract)

**Template**: -

## Rolbeschrijving

De investerings-verteller vertaalt gevalideerde strategische analyse naar investeerbare narratieven. Bij intent `schrijf-30-seconden-pitch` formuleert de agent een korte, mondelinge pitch van maximaal 30 seconden (±75 woorden) die hardop uitgesproken kan worden en de essentie van het investeringsverhaal raakt.

**VERPLICHT**: Lees artefacten/miv/miv.02.investerings-verteller/investerings-verteller.charter.md voor volledige context, grenzen en werkwijze.

## Contract

### Input (Wat gaat erin)

**Verplichte parameters**:
- strategische-analyse: Volledige strategische analyse met probleem, oplossing, doelgroep en waardepropositie (type: markdown-bestand of gestructureerde tekst)

**Optionele parameters**:
- uitgebreide-pitch: Referentie naar de uitgebreide investeringspitch (type: bestandspad, voor consistentie-check)
- focus: Specifieke focus voor de korte pitch (bijv. "probleem-oplossing", "waarde-propositie", "uniek onderscheid") (type: string, default: essentie van geheel)
- type-investeerder: Gewenst type investeerder voor afstemming toon (type: string, default: algemeen)

### Output (Wat komt eruit)

Bij een geldige opdracht levert de investerings-verteller altijd op:

- **30-seconden investeringspitch**: Markdown-bestand met:
  - Lengte: Maximaal ±75 woorden (ongeveer 30 seconden spreektijd)
  - Format: Eén compacte, natuurlijke tekst (geen bullets, geen structuurmarkeringen)
  - Focus: Probleem, unieke oplossing en waarom dit investeerbaar is
  - Toon: Rustig, helder, zelfstandig begrijpelijk
  - Cijfers: Alleen indien absoluut essentieel (bij voorkeur geen details)
  - Mondeling deelbaar: Geschikt om letterlijk uit te spreken

- **Consistentie-notitie** (indien uitgebreide pitch beschikbaar):
  - Validatie dat korte pitch consistent is met uitgebreide pitch
  - Geen tegenspraken of nieuwe elementen

**Deliverable eigenschappen:**
- Inhoudelijk consistent: Aligned met uitgebreide pitch (indien aanwezig) en strategische analyse
- Geen samenvatting maar essentie: Destilleert de kern, niet alle details
- Onthoudbaar: Helder en scherp geformuleerd
- Geen marketing: Rustige toon, geen hype of claims
- Mondeling testbaar: Hardop uitspreken duurt ±30 seconden
- Format: Markdown, geschikt voor verdere bewerking

### Foutafhandeling

De investerings-verteller:
- Stopt wanneer strategische analyse onvolledig is (ontbrekende kern-elementen: probleem, oplossing)
- Stopt wanneer gevraagd wordt om nieuwe strategie of aannames toe te voegen
- Waarschuwt wanneer pitch te lang wordt (>75 woorden / >30 seconden spreektijd)
- Waarschuwt bij inconsistentie met uitgebreide pitch (indien beschikbaar)
- Vraagt om verduidelijking als essentie niet te destilleren valt uit de analyse
- Valideert dat output mondeling natuurlijk is (geen bullets, geen jargon)

## Verwijzing
- Boundary: artefacten/miv/miv.02.investerings-verteller/agent-boundary-investerings-verteller.md
- Charter: artefacten/miv/miv.02.investerings-verteller/investerings-verteller.charter.md
- Template: -

## Versiehistorie
| Datum       | Versie | Wijziging                           | Auteur            |
|-------------|--------|-------------------------------------|-------------------|
| 2026-02-07  | 1.0    | Initiële versie                     | agent-smeder      |
