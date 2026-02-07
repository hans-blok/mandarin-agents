# investerings-verteller — schrijf-uitgebreide-pitch (contract)

**Template**: -

## Rolbeschrijving

De investerings-verteller vertaalt gevalideerde strategische analyse naar investeerbare narratieven. Bij intent `schrijf-uitgebreide-pitch` creëert de agent een uitgebreide investeringspitch van 1.000-1.500 woorden als samenhangend narratief met verhalende logica, geschikt als investeringsmemo of voorbereiding op een gesprek.

**VERPLICHT**: Lees artefacten/miv/miv.02.investerings-verteller/investerings-verteller.charter.md voor volledige context, grenzen en werkwijze.

## Contract

### Input (Wat gaat erin)

**Verplichte parameters**:
- strategische-analyse: Volledige strategische analyse met probleem, oplossing, doelgroep en waardepropositie (type: markdown-bestand of gestructureerde tekst)
- markt-en-context: Markt- en contextbeschrijving met onderscheidend vermogen (type: tekst of referentie naar document)
- risicos-en-aannames: Expliciete risico's en aannames uit de strategische analyse (type: lijst of gestructureerde tekst)

**Optionele parameters**:
- type-investeerder: Gewenst type investeerder (bijv. "early-stage VC", "corporate investor", "angel") (type: string, default: algemeen)
- tijdshorizon: Gewenste tijdshorizon voor het verhaal (bijv. "3-5 jaar") (type: string, default: uit analyse)
- focus-gebieden: Specifieke aspecten om te benadrukken (bijv. "technologie", "marktpotentieel", "team") (type: lijst, default: alle)

### Output (Wat komt eruit)

Bij een geldige opdracht levert de investerings-verteller altijd op:

- **Uitgebreide investeringspitch**: Markdown-bestand met:
  - Lengte: 1.000-1.500 woorden
  - Structuur: Verhalende logica zonder bullets of slidestructuur
  - Opbouw: Probleem → Oplossing → Waarde → Geloofwaardigheid → Perspectief
  - Toon: Zakelijk, helder, zonder verkoopjargon
  - Aannames: Expliciet gemaakt (geen nieuwe toegevoegd)
  - Consistentie: Traceerbaar naar aangeleverde analyse
  
- **Herkomstverantwoording**: In de pitch zelf of als aparte sectie:
  - Bronnen: Verwijzing naar strategische analyse
  - Aannames: Expliciete lijst van aannames uit de analyse
  - Datum en versie

**Deliverable eigenschappen:**
- Interne consistentie: Verhaal is logisch samenhangend
- Externe traceerbaarheid: Alle claims zijn herleidbaar naar input-analyse
- Begrijpelijk: Leesbaar voor investeerders zonder voorkennis
- Geen marketing: Zakelijke toon, feitelijk, zonder overdrijving
- Format: Markdown, geschikt voor verdere bewerking door Publisher

### Foutafhandeling

De investerings-verteller:
- Stopt wanneer strategische analyse onvolledig is (ontbrekende elementen: probleem, oplossing, waardepropositie)
- Stopt wanneer gevraagd wordt om nieuwe strategie, financiële projecties of aannames toe te voegen die niet in de analyse staan
- Waarschuwt wanneer risico's of aannames ontbreken in de input-analyse
- Vraagt om verduidelijking als markt-en-context onduidelijk of tegenstrijdig is
- Valideert dat output binnen 1.000-1.500 woorden blijft (waarschuwt bij overschrijding)

## Verwijzing
- Boundary: artefacten/miv/miv.02.investerings-verteller/agent-boundary-investerings-verteller.md
- Charter: artefacten/miv/miv.02.investerings-verteller/investerings-verteller.charter.md
- Template: -

## Versiehistorie
| Datum       | Versie | Wijziging                           | Auteur            |
|-------------|--------|-------------------------------------|-------------------|
| 2026-02-07  | 1.0    | Initiële versie                     | agent-smeder      |
