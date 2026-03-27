# Hypothese: E-facturatie Klantportaal

**Hypothese-code**: HYP-20260327-01  
**Datum**: 2026-03-27  
**Bron**: EU-wetgeving e-facturatie verplichting

---

## 1. Probleemkader

### De huidige situatie (status quo)

TLX verstuurt facturen aan klanten (particulieren en grote klanten zoals aannemers in de bouw) via traditionele kanalen. De factureringsprocessen zijn ingericht voor de afvalverwerkingssector (levering containers). Er is geen centrale locatie waar klanten hun facturen digitaal kunnen raadplegen of downloaden in een gestandaardiseerd e-factuurformaat.

### De frictie

De EU heeft verplichte e-facturatie voor B2B-transacties aangekondigd. Dit betekent dat TLX facturen moet kunnen versturen én ontvangen in een gestandaardiseerd elektronisch formaat (zoals Peppol/UBL). De huidige factureringsprocessen voldoen niet aan deze wettelijke vereisten, wat risico's oplevert:
- Boetes bij niet-naleving van EU-wetgeving
- Verstoring van bedrijfsvoering wanneer facturen niet worden geaccepteerd
- Klanten die zelf ook moeten voldoen aan e-facturatie kunnen TLX-facturen niet verwerken

### Waarom blijft dit probleem bestaan?

- De deadline voor verplichte e-facturatie ligt in de toekomst, waardoor urgentie ontbreekt
- Investering in nieuwe factureringsinfrastructuur wordt uitgesteld
- De impact op verschillende klantgroepen (particulieren vs. B2B) is nog niet helder in kaart gebracht
- Er is geen centrale voorziening waar klanten zelf facturen kunnen ophalen

---

## 2. Hypothese

**De hypothese luidt:**

> "Een klantportaal met downloadfunctionaliteit voor facturen en notificaties is beter dan het huidige factureringsproces zonder centrale toegang, omdat dit TLX in staat stelt te voldoen aan EU e-facturatie wetgeving terwijl klanten eenvoudig toegang krijgen tot hun facturen."

**Interventie**: Implementatie van een klantportaal waar klanten hun facturen kunnen downloaden, met notificaties bij nieuwe facturen.

**Contrasteert met**: Het huidige proces waarbij facturen via traditionele kanalen (post, losse e-mail) worden verstuurd zonder centrale digitale toegang voor klanten.

**Verondersteld effect**: 
1. TLX voldoet aan EU e-facturatie wetgeving en vermijdt boetes
2. Klanten (particulieren en grote aannemers) hebben eenvoudige toegang tot hun facturen
3. Bedrijfsvoering kan worden voortgezet zonder onderbreking door compliance-issues

---

## 3. Aannames (maximaal 3 risico's)

### Aanname 1: Klanten willen een portaal gebruiken

- **Wat nemen we aan?**: Klanten (zowel particulieren als grote aannemers in de bouw) zijn bereid en in staat om een digitaal portaal te gebruiken voor factuurtoegang.
- **Waarom is dit een risico?**: Particulieren kunnen digitaal minder vaardig zijn of de voorkeur geven aan papieren facturen. Grote klanten hebben mogelijk eigen systemen en processen die niet aansluiten op een portaal.
- **Hoe kunnen we dit toetsen?**: Interview 5 particuliere klanten en 3 grote klanten over hun huidige factuurverwerking en bereidheid tot portaalgebruik (binnen 1 week, kosten: interviews ~8 uur).

### Aanname 2: Een portaal volstaat voor EU e-facturatie compliance

- **Wat nemen we aan?**: Een downloadfunctionaliteit via een klantportaal voldoet aan de technische en juridische vereisten van EU e-facturatie wetgeving.
- **Waarom is dit een risico?**: EU-regelgeving kan specifieke formaten (UBL, Peppol) en uitwisselingsprotocollen vereisen die verder gaan dan "downloadbaar maken". Een portaal is mogelijk niet voldoende.
- **Hoe kunnen we dit toetsen?**: Raadpleeg de specifieke EU-regelgeving en/of een compliance-expert om te bepalen welke technische eisen gelden voor de afvalverwerkingssector (binnen 1 week, kosten: ~€500 voor juridisch advies of 16 uur eigen onderzoek).

### Aanname 3: Notificaties leiden tot tijdige factuurverwerking

- **Wat nemen we aan?**: Het versturen van notificaties (e-mail/push) zorgt ervoor dat klanten hun facturen tijdig ophalen en verwerken.
- **Waarom is dit een risico?**: Notificaties kunnen worden genegeerd, in spam belanden, of niet aansluiten bij de werkprocessen van grote klanten die geautomatiseerde factuurverwerking gebruiken.
- **Hoe kunnen we dit toetsen?**: Pilot met 10 klanten waarbij notificaties worden verstuurd en we meten: openratio, tijd tot download, en feedback over bruikbaarheid (binnen 1 week met bestaande e-mailinfrastructuur, kosten: ~8 uur).

---

## 4. Context en afbakening

### Ontstaan

Deze hypothese komt voort uit de aanstaande EU-wetgeving die e-facturatie verplicht stelt voor B2B-transacties. TLX opereert in de afvalverwerkingssector en levert containers aan zowel particulieren als grote klanten (aannemers in de bouw). De noodzaak om te voldoen aan wetgeving dwingt tot een herbezinning op het factureringsproces.

### Doelgroep

- **Primair**: Grote klanten (B2B) zoals aannemers in de bouwsector — voor hen geldt de wetgeving direct
- **Secundair**: Particuliere klanten — profiteren van eenvoudiger factuurtoegang

### Scope

**Binnen scope:**
- Centrale plek voor factuurdownload
- Notificatiemechanisme voor nieuwe facturen
- Ondersteuning van e-factuurformaten conform wetgeving

**Buiten scope:**
- Volledige klantportal met selfservice voor contractbeheer, bestellingen etc.
- Integratie met klant-ERP-systemen (kan vervolgstap zijn)
- Wijzigingen aan het primaire facturatiesysteem (alleen output-kant)

---

## 5. Toetsbaarheid

### Wat zou betekenen dat deze hypothese klopt?

1. **Juridische bevestiging**: Een portaal met downloadfunctionaliteit (in juist formaat) voldoet aan EU e-facturatie eisen voor de afvalverwerkingssector
2. **Klantacceptatie**: Minimaal 60% van de geïnterviewde klanten geeft aan een portaal te willen gebruiken voor factuurtoegang
3. **Technische haalbaarheid**: Het is mogelijk om facturen in het vereiste e-formaat (UBL/Peppol) beschikbaar te stellen via een portaal

### Wat zou betekenen dat deze hypothese niet klopt?

1. **Juridische afwijzing**: EU-wetgeving vereist actieve verzending via Peppol-netwerk, niet passieve download via portaal
2. **Klantafwijzing**: Minder dan 30% van klanten is bereid een portaal te gebruiken; grote klanten eisen directe systeemintegratie
3. **Technische blokkade**: Huidige facturatiesystemen kunnen niet worden aangepast om e-factuurformaten te genereren

### Eerste stap om te toetsen

**Actie**: Valideer juridische compliance-eisen  
**Wat**: Onderzoek of een downloadportaal voldoet aan EU e-facturatie wetgeving, of dat actieve verzending via Peppol-netwerk vereist is  
**Hoe**: Raadpleeg de bron (EY-artikel) en eventueel aanvullend juridisch advies  
**Doorlooptijd**: Max 1 week  
**Kosten**: <€1000 (eigen onderzoek 16 uur + eventueel kort juridisch advies)  
**Acceptatiedrempel**: Als portaal-download juridisch volstaat, ga door naar klantvalidatie. Zo niet, herformuleer hypothese naar Peppol-integratie.

---

## 6. Relatie met andere hypotheses

_(Nog niet van toepassing — dit is eerste hypothese over dit thema)_

---

## 7. Herkomstverantwoording

**Bronnen**: 
- https://www.dutchitchannel.nl/news/727447/ey-adviseert-verplichte-e-facturatie-voor-alle-b2b-transacties

**Bijdragen**: dalm

**Laatste update**: 2026-03-27

**Gegenereerd door**: hypothese-vormer (sfw.01)  
**Template**: hypothese-template.md  
**Click-principe check**: ✓ Scherp probleemcontrast, ✓ Toetsbaarheid concreet, ✓ Geen solution-bias (probleem centraal)
