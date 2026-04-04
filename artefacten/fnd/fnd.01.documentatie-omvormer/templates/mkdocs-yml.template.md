---
template: mkdocs-yml
versie: 1.0.0
agent: documentatie-omvormer
doel: Template voor genereren van mkdocs.yml configuratiebestanden
digest: 7d3a
status: vers
---
# MkDocs Configuration Template

Dit template wordt gebruikt door de documentatie-omvormer om mkdocs.yml bestanden te genereren.
Alle placeholders tussen `{{` en `}}` moeten worden ingevuld op basis van input.

---

## Placeholders

| Placeholder | Beschrijving | Verplicht | Default |
|-------------|--------------|-----------|---------|
| `{{site_name}}` | Naam van de site | Ja | - |
| `{{site_description}}` | Korte beschrijving van de site | Ja | - |
| `{{site_author}}` | Auteur/team naam | Nee | "Mandarin Team" |
| `{{site_url}}` | Basis-URL van de gepubliceerde site | Nee | - |
| `{{repo_name}}` | Repository naam (optioneel) | Nee | - |
| `{{repo_url}}` | Repository URL (optioneel) | Nee | - |
| `{{docs_dir}}` | Bronmap voor documentatie | Nee | "docs" |
| `{{site_dir}}` | Doelmap voor gegenereerde site | Nee | "site" |
| `{{language}}` | Taalcode (nl, en, etc.) | Nee | "nl" |
| `{{logo_path}}` | Pad naar logo afbeelding | Nee | "assets/mandarin-logo-m.png" |
| `{{favicon_path}}` | Pad naar favicon | Nee | "assets/mandarin-logo-m.png" |
| `{{primary_color}}` | Primaire themakleur | Nee | "deep-orange" |
| `{{accent_color}}` | Accent kleur | Nee | "orange" |
| `{{extra_css}}` | Lijst van extra CSS bestanden | Nee | ["style/mandarin.css"] |
| `{{nav_structure}}` | Navigatiestructuur (YAML) | Ja | - |
| `{{copyright}}` | Copyright tekst | Nee | - |

---

## Template Output

```yaml
# ============================================================
# MkDocs Configuration — {{site_name}}
# Gegenereerd door: documentatie-omvormer
# ============================================================

# ------------------------------------------------------------
# 1. Site Identiteit
# ------------------------------------------------------------
site_name: "{{site_name}}"
site_description: "{{site_description}}"
site_author: "{{site_author}}"
{{#if site_url}}
site_url: "{{site_url}}"
{{/if}}

{{#if repo_name}}
# Repository referentie
repo_name: "{{repo_name}}"
repo_url: "{{repo_url}}"
edit_uri: "edit/main/docs/"
{{/if}}

# ------------------------------------------------------------
# 2. Documentatie Bron
# ------------------------------------------------------------
docs_dir: "{{docs_dir}}"
site_dir: "{{site_dir}}"

# ------------------------------------------------------------
# 3. Theme & Presentatie
# ------------------------------------------------------------
theme:
  name: "material"
  language: "{{language}}"
  features:
    - navigation.instant
    - navigation.sections
    - navigation.expand
    - navigation.top
    - navigation.tabs
    - navigation.tabs.sticky
    - content.code.copy
    - content.code.annotate
    - toc.integrate
    - search.suggest
    - search.highlight
  palette:
    primary: "{{primary_color}}"
    accent: "{{accent_color}}"
  font:
    text: "Segoe UI"
    code: "Consolas"
  logo: "{{logo_path}}"
  favicon: "{{favicon_path}}"

# ------------------------------------------------------------
# 4. Custom Styling
# ------------------------------------------------------------
extra_css:
  - assets/stylesheets/responsive.css
{{#each extra_css}}
  - {{this}}
{{/each}}

extra_javascript: []

# ------------------------------------------------------------
# 5. Plugins
# ------------------------------------------------------------
plugins:
  - search:
      lang: {{language}}

# ------------------------------------------------------------
# 6. Markdown Extensies
# ------------------------------------------------------------
markdown_extensions:
  # Python Markdown
  - abbr
  - admonition
  - attr_list
  - def_list
  - footnotes
  - md_in_html
  - tables
  - toc:
      permalink: true
      toc_depth: 3

  # Python Markdown Extensions
  - pymdownx.arithmatex:
      generic: true
  - pymdownx.betterem:
      smart_enable: all
  - pymdownx.caret
  - pymdownx.details
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.keys
  - pymdownx.mark
  - pymdownx.smartsymbols
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.tasklist:
      custom_checkbox: true
  - pymdownx.tilde

# ------------------------------------------------------------
# 7. Navigatiestructuur
# ------------------------------------------------------------
nav:
{{nav_structure}}

# ------------------------------------------------------------
# 8. Extra Configuratie
# ------------------------------------------------------------
extra:
  social: []
  generator: false

{{#if copyright}}
# ------------------------------------------------------------
# 9. Copyright
# ------------------------------------------------------------
copyright: "{{copyright}}"
{{/if}}
```

---

## Voorbeeld Invulling

**Input parameters:**
```yaml
site_name: "Mandarin Startup"
site_description: "Strategische documentatie voor Product Mandarin"
site_author: "Mandarin Team"
site_url: "https://mandarin-startup.github.io/"
language: "nl"
nav_structure: |
  - Home: index.md
  - Architectuur:
    - Overzicht: architectuur/index.md
    - Componenten: architectuur/componenten.md
  - API: api/index.md
copyright: "Copyright © 2026 Maxia Consultancy"
```

---

## Herkomstverantwoording

- **Template-eigenaar**: documentatie-omvormer
- **Doel**: Genereren van mkdocs.yml zonder inhoudelijke interpretatie
- **Bron**: Mandarin huisstijl en Material theme defaults
