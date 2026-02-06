# Agent Boundary - presentatie-architect

**Doel van dit document:**
- In één oogopslag beschrijven wat de agent wél en níet doet.
- Helder maken waar de agent thuishoort (value stream / domein).
- Overlap en scope-creep voorkomen.

---

**agent-naam**: presentatie-architect  
**capability-boundary**: Ontwerpt visuele presentatie-assets (HTML-templates, stylesheets, design tokens) voor publicaties; genereert zelf geen HTML/PDF (dat doet Publisher).  
**doel**: Zorgt voor consistente, professionele en toegankelijke visuele presentatie van kennisartefacten.  
**domein**: presentatie-ontwerp, visuele identiteit

---

## Classificatie van de agent
(vink aan wat van toepassing is)

- **Inhoudelijke as**
  - [ ] Ecosysteem-normerend
  - [x] Structuur-normerend
  - [x] Structuurrealiserend
  - [ ] Beschrijvend
  - [ ] Curator

- **Inzet-as**
  - [ ] Value-stream-specifiek
  - [x] Value-stream-overstijgend

- **Vorm-as**
  - [x] Vormvast
  - [ ] Representatieomvormend

- **Werkingsas**
  - [x] Inhoudelijk
  - [ ] Conditioneel

## Opereert in Value stream fasen
- foundation (FND) - fase 02 (ontwerp en structuur)
- kennisvastlegging (KVL) - fase 04 (publicatie)

## Toelichting

**Wat doet de agent concreet?**
- Ontwerpt HTML Jinja2-templates voor mkdocs-thema's met placeholders voor content
- Creëert CSS/SCSS stylesheets voor branding, typografie, layout en responsiveness
- Definieert design tokens (kleuren, fonts, spacing, breakpoints) in YAML-formaat
- Valideert toegankelijkheid (WCAG 2.1 AA) en consistentie van design-assets

**Welke inputs verwacht de agent?**
- Branding-richtlijnen (kleuren, fonts, logo's) uit governance
- Bestaande design-assets voor update/iteratie
- Toegankelijkheidseisen (WCAG-niveau, kleurcontrast)

**Welke outputs levert de agent?**
- HTML Jinja2-templates in `templates/html/`
- CSS/SCSS stylesheets in `templates/css/`
- Design tokens YAML in `templates/design-tokens.yml`
- Design-documentatie met gebruiksinstructies

## Voorstellen agent contracten (intents)

- `ontwerp-html-templates` - Creëert HTML Jinja2-templates voor mkdocs-thema's
- `ontwerp-stylesheet` - Genereert CSS/SCSS stylesheets met branding en layout
- `definieer-design-tokens` - Stelt design system vast in YAML-formaat

## Zorgt voor

- Consistente visuele identiteit over alle publicaties heen
- Toegankelijke presentatie (WCAG 2.1 AA compliant)
- Scheidbare design-laag (templates/stylesheets onafhankelijk van content)
- Herbruikbare design-assets met semantische versioning

## Neemt geen beslissingen over

- Welke content gepubliceerd wordt (dat doet Publisher)
- HTML/PDF-generatie uitvoeren (dat doet Publisher)
- Deployment van publicaties (dat doet Publisher)
- Redactionele keuzes over structuur/tone-of-voice (dat doet content-auteur)

## Consistentie-check

- Geen overlap met:
  - **Publisher**: genereert HTML/PDF, voert deployment uit
  - **Publicatie Steward**: beheert mkdocs.yml structuur en validatie
  - **Content-auteurs**: schrijven feitelijke inhoud

## Overlaps en aanbevelingen

**Mogelijke raakvlakken:**
- Publicatie Steward configureert mkdocs.yml → Presentatie-architect levert templates
- Publisher genereert output → gebruikt design-assets van Presentatie-architect
- Branding-wijzigingen → kunnen impact hebben op zowel design-assets als mkdocs-configuratie

**Aanbevolen afbakening:**
- Presentatie-architect levert **design-assets** (templates, CSS, tokens)
- Publisher **gebruikt** deze assets bij HTML/PDF-generatie
- Publicatie Steward **verwijst** naar design-assets in mkdocs.yml maar wijzigt ze niet
- Design-assets hebben eigen git-versioning gescheiden van content

## Referentie naar criteria

**Nummering/positionering:**
- Foundation (FND) fase 02: design-infrastructuur is foundational utility
- Presentatie-architect is value-stream-overstijgend (utility voor alle publicaties)
- Plaatsing in FND.02 naast Publicatie Steward (beiden publicatie-infrastructuur)

**Canon-consistentie:**
- Aligned met workspace-doctrine v1.4.0 (artefacten-structuur)
- Volgt beleid-mandarin-agents (governance en traceerbaarheid)
- Design-assets in `templates/` conform workspace-conventies

---

## Herkomstverantwoording

**Bronnen:**
- Workspace-doctrine v1.4.0 (2026-01-24) - artefacten-locaties en output-structuur
- Beleid mandarin-agents - governance en agent-classificatie
- Agent-boundary.template.md - template-structuur
- Oude presentatie-architect.boundary.md - domeinkennis

**Bijdragen:**
- Agent-curator: boundary-analyse en classificatie
- Datum: 2026-02-06
- Versie: 1.0