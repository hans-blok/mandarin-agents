# Beleid voor de mandarin-agents workspace

Deze workspace hoort bij de waardestroom **agent-enablement**.

## Scope

- Deze workspace gaat over het ontwerpen, bouwen en beheren van agents die andere gebruikers helpen om nieuwe agents te maken of te verbeteren ("agent-enablement").
- Andere domeinen (zoals marketing, finance of HR) vallen buiten deze workspace en horen in andere repositories.

**Value Stream**  
Welke waardestroom is primair van toepassing op deze workspace?

- Value stream: `niet van toepassing (boven de value streams)`


## Richtlijnen

**Constitutie (verplicht)**

De constitutie, algemene regels en governance voor alle workspaces staan in:

- https://github.com/hans-blok/mandarin-canon.git

1.  **Canon Repository Synchronisatie**: In alle geautomatiseerde en handmatig processen wordt daarom de centrale canon repository (`https://github.com/hans-blok/mandarin-canon.git`) geraadpleegd. Dit gebeurt altijd eerst met een `git pull`. Dit om te waarborgen dat de meest recente grondslagen worden gebruikt. 

Alleen opgehaald wordt de folder 'grondslagen'

# sparse-checkout blijft actief; working tree blijft beperkt tot deze ene folder
git pull --ff-only


**Grondslagen Lezen**: Van toepassing voor alle geautomatiseerde processen en handmatige processen zijn de grondslagen die als onderdeel van de canon zijn vastgelegd. 

**Vereist**: Bij het starten van deze workspace of bij het raadplegen van beleid moet eerst de constitutie uit `hans-blok/mandarin-canon` worden gelezen en begrepen.

**Foutmelding**: Wanneer de mandarin-canon-repository niet bereikbaar is of niet kan worden gevonden, wordt een foutmelding gegeven en stopt het proces.

## Dit beleid is workspace-specifiek

Dit beleid beschrijft alleen de workspace-specifieke scope. Voor alle regels, uitzonderingen, details en constitutionele bepalingen volgen we volledig de richtlijnen in `hans-blok/mandarin-canon`.