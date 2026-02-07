# presentatie-architect — ontwerp-html-templates (contract)

**Template**: -

## Rolbeschrijving

De presentatie-architect ontwerpt visuele presentatie-assets voor publicaties. Bij intent `ontwerp-html-templates` creëert de agent HTML Jinja2-templates voor mkdocs-thema's met placeholders voor content, met focus op semantische structuur, toegankelijkheid en herbruikbaarheid.

**VERPLICHT**: Lees artefacten/fnd.02.presentatie-architect/presentatie-architect.charter.md voor volledige context, grenzen en werkwijze.

## Contract

### Input (Wat gaat erin)

**Verplichte parameters**:
- branding-richtlijnen: Kleuren, fonts, logo's uit governance/branding/ (type: referentie naar bestand of inline specificatie)
- toegankelijkheidseisen: WCAG-niveau (bijv. "WCAG 2.1 AA") en minimale contrastratios (type: string)

**Optionele parameters**:
- bestaande-templates: Pad naar bestaande templates voor update/iteratie (type: bestandspad, default: geen)
- template-type: Specifiek type template (bijv. "base", "article", "index") (type: string, default: "base")

### Output (Wat komt eruit)

Bij een geldige opdracht levert de presentatie-architect altijd op:

- **HTML Jinja2-templates**: Bestanden in `templates/html/` met:
  - Semantische HTML5-structuur (nav, main, article, aside, header, footer)
  - Jinja2-placeholders consistent met mkdocs-variabelen
  - Toegankelijkheidsattributen (ARIA-labels, role-attributen waar nodig)
  - Responsive meta-tags en viewport-configuratie

- **Template-documentatie**: Markdown-bestand met:
  - Overzicht van beschikbare placeholders en hun functie
  - Gebruiksinstructies voor integratie met mkdocs
  - Voorbeelden van template-gebruik

**Deliverable eigenschappen:**
- Templates zijn syntactisch correct Jinja2
- Placeholders volgen mkdocs-naamconventies (bijv. `{{ page.title }}`, `{{ config.site_name }}`)
- HTML is semantisch en toegankelijk (WCAG 2.1 AA compliant)
- Templates zijn modulair en herbruikbaar

### Foutafhandeling

De presentatie-architect:
- Stopt wanneer branding-richtlijnen ontbreken of onvolledig zijn (kleuren/fonts niet gespecificeerd)
- Waarschuwt wanneer toegankelijkheidseisen niet haalbaar zijn met gegeven branding (bijv. onvoldoende kleurcontrast)
- Vraagt om verduidelijking als template-type onduidelijk is of conflicteert met mkdocs-structuur
- Valideert dat er geen content-generatie plaatsvindt (templates bevatten alleen placeholders, geen vaste inhoud)

## Verwijzing
- Boundary: agent-boundaries/presentatie-architect.boundary.md
- Charter: artefacten/fnd.02.presentatie-architect/presentatie-architect.charter.md
- Template: -

## Versiehistorie
| Datum       | Versie | Wijziging                           | Auteur            |
|-------------|--------|-------------------------------------|-------------------|
| 2026-02-06  | 1.0    | Volledig uitgewerkt contract        | agent-smeder      |
| 2026-02-06  | 0.1.0  | Initiële skeleton                   | agent-smeder      |
