# Agent Execution History

Deze folder bevat vorige versies van gegenereerde execution files.

Wanneer een nieuw execution file wordt aangemaakt door `generate_instructions.py`, worden alle bestaande .md bestanden in `agent-execution/` automatisch verplaatst naar deze history subfolder. Dit zorgt ervoor dat de parent folder altijd alleen het meest recente execution file bevat, zodat je gemakkelijk het juiste bestand kunt vinden.

**Automatische rotatie**: Bij elke nieuwe generatie worden oude bestanden hierheen verplaatst  
**Bestandsnamen**: Originele execution ID en timestamp blijven behouden  
**Duplicaten**: Als een bestand met dezelfde naam al bestaat, wordt een timestamp toegevoegd

## Gebruik

De bestanden in deze folder zijn volledig bruikbaar als referentie of voor hergebruik. Ze bevatten:
- Execution metadata (ID, timestamp, canon reference)
- Volledige agent instructies (charter + contract)
- Parameters die zijn gebruikt bij generatie

## Onderhoud

Deze folder wordt automatisch beheerd door het script. Je kunt oude bestanden handmatig verwijderen indien gewenst.
