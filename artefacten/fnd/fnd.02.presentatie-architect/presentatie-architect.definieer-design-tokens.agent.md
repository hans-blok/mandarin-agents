# presentatie-architect — definieer-design-tokens (contract)

**Template**: -

## Rolbeschrijving

De presentatie-architect ontwerpt visuele presentatie-assets voor publicaties. Bij intent `definieer-design-tokens` stelt de agent een design system vast in YAML-formaat met kleuren, typografie, spacing, breakpoints en andere design-primitieven die de basis vormen voor alle stylesheets en templates.

**VERPLICHT**: Lees artefacten/fnd.02.presentatie-architect/presentatie-architect.charter.md voor volledige context, grenzen en werkwijze.

## Contract

### Input (Wat gaat erin)

**Verplichte parameters**:
- branding-richtlijnen: Huisstijlhandboek met kleuren (hex/RGB), fonts (families, weights), logo-specificaties (type: referentie naar bestand of inline specificatie)
- toegankelijkheidseisen: WCAG-niveau, minimale contrastratios, minimum font-groottes (type: string of gestructureerd object)

**Optionele parameters**:
- bestaande-tokens: Pad naar bestaande design-tokens voor update/iteratie (type: bestandspad, default: geen)
- custom-breakpoints: Afwijkende responsive breakpoints (type: lijst van pixel-waarden, default: standaard mobile/tablet/desktop)
- uitbreidingen: Extra token-categorieën (bijv. animations, z-index-lagen) (type: lijst, default: geen)

### Output (Wat komt eruit)

Bij een geldige opdracht levert de presentatie-architect altijd op:

- **Design tokens YAML**: Bestand `templates/design-tokens.yml` met:
  
  **Verplichte secties**:
  - `colors`: Primary, secondary, neutral palette + semantische kleuren (success, warning, error, info)
  - `typography`: Font-families (primair, secundair, monospace), groottes (scale), line-heights, weights
  - `spacing`: Marges en paddings (scale van sm tot xl)
  - `breakpoints`: Responsive breakpoints (mobile, tablet, desktop, wide)
  - `shadows`: Box-shadows voor elevatie (levels 1-5)
  - `borders`: Border-widths en border-radii
  
  **Optionele secties**:
  - `animations`: Duration en easing-functies
  - `z-index`: Gelaagdheid voor UI-componenten
  - `opacity`: Standaard opacity-waarden

- **Design tokens documentatie**: Markdown-bestand met:
  - Uitleg per token-categorie en gebruik
  - Toegankelijkheidsvalidatie (welke kleurcombinaties WCAG-compliant zijn)
  - Voorbeelden van token-gebruik in CSS/SCSS
  - Semantische versioning van tokens (breaking changes bij kleurwijzigingen)

**Deliverable eigenschappen:**
- YAML is syntactisch correct en bevat alle verplichte secties
- Alle kleurcombinaties (tekst op achtergrond) voldoen aan WCAG 2.1 AA (minimaal 4.5:1 contrast)
- Font-groottes zijn toegankelijk (minimaal 16px voor body-tekst)
- Tokens zijn semantisch benoemd (geen `color1`, `color2`, maar `primary`, `secondary`)
- Breakpoints volgen mobile-first principe (kleinste eerst)

### Foutafhandeling

De presentatie-architect:
- Stopt wanneer branding-richtlijnen ontbreken of onvolledige kleurspecificaties bevatten
- Waarschuwt wanneer kleurcombinaties niet voldoen aan WCAG 2.1 AA en stelt aangepaste kleuren voor
- Vraagt om verduidelijking als font-families niet beschikbaar zijn (web-fonts vs system-fonts)
- Valideert dat tokens geen implementatie-specifieke waarden bevatten (tokens zijn platform-agnostisch)

## Verwijzing
- Boundary: presentatie-architect.boundary.md
- Charter: artefacten/fnd.02.presentatie-architect/presentatie-architect.charter.md
- Template: -

## Versiehistorie
| Datum       | Versie | Wijziging                           | Auteur            |
|-------------|--------|-------------------------------------|-------------------|
| 2026-02-06  | 1.0    | Volledig uitgewerkt contract        | agent-smeder      |
| 2026-02-06  | 0.1.0  | Initiële skeleton                   | agent-smeder      |
