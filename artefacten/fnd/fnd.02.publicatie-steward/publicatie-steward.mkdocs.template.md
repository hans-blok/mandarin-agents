# ============================================================
# MkDocs Configuration — Publicatie Steward Template
# Owner: Publicatie Steward
# Doel: Gestandaardiseerde, traceerbare publicatie van expliciete kennis
# ============================================================

# ------------------------------------------------------------
# 1. Site Identiteit
# Vul in: project- of workspace-naam, beschrijving en eigenaar
# ------------------------------------------------------------
site_name: "{{workspace_name}}"
site_description: "{{workspace_description}}"
site_author: "{{workspace_author}}"
site_url: "{{site_url}}"

# Optioneel maar aanbevolen voor version control referentie
repo_name: "{{repo_name}}"
repo_url: "{{repo_url}}"
edit_uri: "edit/main/docs/"

# ------------------------------------------------------------
# 2. Documentatie Bron
# Standaard locaties (pas alleen aan bij afwijking)
# ------------------------------------------------------------
docs_dir: "docs"
site_dir: "site"

# ------------------------------------------------------------
# 3. Theme & Presentatie
# Standaard Material theme met core features
# (Presentatie Architect verantwoordelijk voor advanced styling)
# ------------------------------------------------------------
theme:
  name: "material"
  language: "nl"
  features:
    - navigation.instant
    - navigation.sections
    - navigation.expand
    - navigation.top
    - navigation.tabs
    - content.code.copy
    - toc.integrate
  palette:
    primary: "blue"
    accent: "light-blue"

# ------------------------------------------------------------
# 4. Custom Styling
# (Optioneel; eigendom van Presentatie Architect)
# ------------------------------------------------------------
extra_css:
  - css/custom.css

extra_javascript: []

# ------------------------------------------------------------
# 5. Navigatiestructuur
# Primaire verantwoordelijkheid van Publicatie Steward
# Gegenereerd op basis van workspace content-structuur
# ------------------------------------------------------------
nav:
  - Home: index.md

  # Governance documentatie
  - Governance:
      - Overzicht: governance/index.md
      - Beleid: governance/beleid.md
      - Gedragscode: governance/gedragscode.md

  # Canon en concepten (indien aanwezig)
  - Canon:
      - Introductie: canon/index.md
      - Principes: canon/principes.md
      - Concepten: canon/concepten.md

  # Value Streams (aanpassen per workspace)
  {{#value_streams}}
  - {{value_stream_name}}:
      - Overzicht: value-streams/{{value_stream_code}}/index.md
      {{#fases}}
      - {{fase_name}}:
          {{#agents}}
          - {{agent_name}}: value-streams/{{value_stream_code}}/{{fase_code}}/{{agent_slug}}.md
          {{/agents}}
      {{/fases}}
  {{/value_streams}}

  # Agents overzicht
  - Agents:
      - Overzicht: agents/index.md
      {{#agent_categories}}
      - {{category_name}}:
          {{#agents}}
          - {{agent_name}}: agents/{{category_slug}}/{{agent_slug}}.md
          {{/agents}}
      {{/agent_categories}}

  # Artefacten en resultaten
  - Artefacten:
      - Overzicht: artefacten/index.md
      - Per Value Stream: artefacten/value-streams.md

  # Status tracking (indien gebruikt)
  - Status:
      - Drafts: status/drafts.md
      - Gepubliceerd: status/gepubliceerd.md

# ------------------------------------------------------------
# 6. Plugins
# Alleen goedgekeurde, expliciete plugins toegestaan
# ------------------------------------------------------------
plugins:
  - search:
      lang: nl
  # - git-revision-date:
  #     enabled_if_env: CI
  # - tags

# ------------------------------------------------------------
# 7. Markdown Extensions
# Standaard set voor code, admonitions, tabellen en syntax highlighting
# ------------------------------------------------------------
markdown_extensions:
  - admonition
  - toc:
      permalink: true
      toc_depth: 3
  - footnotes
  - tables
  - attr_list
  - def_list
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.tabbed:
      alternate_style: true

# ------------------------------------------------------------
# 8. Extra Configuratie
# Metadata en custom variabelen
# ------------------------------------------------------------
extra:
  generator: false
  status_labels:
    draft: "Concept"
    review: "In Review"
    published: "Gepubliceerd"
  version:
    provider: mike  # Voor versioning (optioneel)

# ------------------------------------------------------------
# 9. Build & Validatie Settings
# Strenge validatie voor productie-kwaliteit
# ------------------------------------------------------------
strict: true              # Fail build bij warnings
use_directory_urls: true  # Clean URLs (zonder .html)

# ------------------------------------------------------------
# 10. Governance Richtlijnen
# ------------------------------------------------------------
# BELANGRIJK:
# - Wijzigingen aan navigatie (nav) vereisen expliciete review
# - Content status moet consistent in nav worden weergegeven
# - mkdocs.yml is een governed artefact, geen convenience bestand
# - Broken links worden gedetecteerd in validatie-fase
# - Gevoelige content (credentials, API keys) NOOIT in docs/
#
# BEHEER:
# - Eigenaar: Publicatie Steward
# - Update-frequentie: Bij toevoegen/verwijderen content
# - Validatie: Via publicatie-steward.valideer-publicatiestructuur
# - Actualisatie: Via publicatie-steward.actualiseer-mkdocs-configuratie
# ============================================================
