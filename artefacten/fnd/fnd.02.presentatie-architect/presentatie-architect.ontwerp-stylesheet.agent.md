# presentatie-architect — ontwerp-stylesheet (contract)

**Template**: -

## Rolbeschrijving

De presentatie-architect ontwerpt visuele presentatie-assets voor publicaties. Bij intent `ontwerp-stylesheet` genereert de agent CSS/SCSS stylesheets met branding, layout, responsiveness en toegankelijkheid, gebouwd op design tokens voor consistentie.

**VERPLICHT**: Lees artefacten/fnd.02.presentatie-architect/presentatie-architect.charter.md voor volledige context, grenzen en werkwijze.

## Contract

### Input (Wat gaat erin)

**Verplichte parameters**:
- design-tokens: Pad naar YAML-bestand met kleuren, fonts, spacing, breakpoints (type: bestandspad, bijv. `templates/design-tokens.yml`)
- branding-richtlijnen: Aanvullende visuele richtlijnen (logo-plaatsing, typografie-hiërarchie) (type: referentie of inline specificatie)

**Optionele parameters**:
- stylesheet-type: Type stylesheet (bijv. "main", "print", "theme-dark") (type: string, default: "main")
- breakpoint-specificaties: Custom responsive breakpoints (type: lijst, default: uit design-tokens)
- bestaande-stylesheet: Pad naar bestaande stylesheet voor update/iteratie (type: bestandspad, default: geen)

### Output (Wat komt eruit)

Bij een geldige opdracht levert de presentatie-architect altijd op:

- **CSS/SCSS bestanden**: In `docs/styles/` met:
  - Import van design tokens als CSS custom properties (variabelen)
  - Typografie-regels (font-families, groottes, line-heights, weights)
  - Kleurenschema (primary, secondary, neutral, semantic kleuren)
  - Layout-regels (grid, flexbox, spacing)
  - Responsive media queries (mobile-first approach)
  - Toegankelijkheidsoptimalisaties (focus states, high contrast mode)
  - Print-stylesheet (indien van toepassing)

- **Stylesheet-documentatie**: Markdown-bestand met:
  - Overzicht van CSS-klassen en hun gebruik
  - Naamconventies (bijv. BEM-methodologie)
  - Responsive breakpoints en mobile-first strategie
  - Toegankelijkheidschecks (contrastratios, focus indicators)

**Deliverable eigenschappen:**
- CSS/SCSS is syntactisch correct en valideert
- Kleurcontrasten voldoen aan WCAG 2.1 AA (minimaal 4.5:1 voor normale tekst, 3:1 voor grote tekst)
- Responsive design werkt op mobile, tablet en desktop
- Design tokens worden consistent gebruikt (geen hardcoded waarden)
- Print-stylesheet aanwezig voor papieren output

### Foutafhandeling

De presentatie-architect:
- Stopt wanneer design-tokens ontbreken of ongeldig YAML bevatten
- Waarschuwt wanneer kleurcontrasten niet voldoen aan WCAG 2.1 AA en stelt alternatieven voor
- Vraagt om verduidelijking als breakpoint-specificaties conflicteren met design tokens
- Valideert dat stylesheet geen JavaScript-afhankelijkheden introduceert (pure CSS/SCSS)

## Verwijzing
- Boundary: agent-boundaries/presentatie-architect.boundary.md
- Charter: artefacten/fnd.02.presentatie-architect/presentatie-architect.charter.md
- Template: -

## Versiehistorie
| Datum       | Versie | Wijziging                           | Auteur            |
|-------------|--------|-------------------------------------|-------------------|
| 2026-02-06  | 1.1    | Output-locatie gewijzigd naar docs/styles/ | agent-smeder      |
| 2026-02-06  | 1.0    | Volledig uitgewerkt contract        | agent-smeder      |
| 2026-02-06  | 0.1.0  | Initiële skeleton                   | agent-smeder      |
