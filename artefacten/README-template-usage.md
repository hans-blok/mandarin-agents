# Template Usage Guide voor Agent Smeder

**Doel:** Constitutional compliance borging door template-driven agent creation.

## Charter Template (`agent-charter.template.md`)

### Bootstrap-Header Placeholders

| Placeholder | Invulling | Voorbeeld |
|-------------|-----------|-----------|
| `<value-stream-code>` | 3-letter code | `aeo`, `kvl`, `sfw`, `miv`, `aod`, `fnd` |
| `<agent-naam>` | Kebab-case agent identifier | `hypothese-vormer`, `agent-curator` |
| `<actor-versie>` | SemVer voor agent implementatie | `1.0.0` (start), `1.1.0` (features), `2.0.0` (breaking) |
| `<charter-versie>` | Governance document versie | `1.0` (start), `1.1` (additions), `2.0` (structure change) |
| `<charter-evidence-phrase>` | WEL-statement uit capability boundary | "Agent X ontwerpt **wél** [core capability]" |
| `<ISO-8601-timestamp>` | Bootstrapping moment | `2026-02-08T16:30:00Z` |

### Charter-Evidence Generation

**Formaat:** "[Agent naam] ontwerpt **wél** [kernactiviteit]"  
**Basis:** Neem capability boundary sectie, pak hoofdwerkwoord en maak bevestigend  
**Voorbeelden:**
- "Agent Smeder ontwerpt **wél** hoe een agent consistent, contract-first en uitvoerbaar wordt vormgegeven"
- "Workflow Architect ontwerpt **wél** hoe agents samenwerken, wanneer ze draaien, met welke gates"

## Prompt Template (`agent-prompt.template.yaml`)

### Charter-Acknowledgement Placeholders

| Placeholder | Invulling | Bron |
|-------------|-----------|------|
| `<agent-naam>` | Zonder "mandarin." prefix | Charter Bootstrap-Header |
| `<charter-versie>` | Exacte match charter | Charter Bootstrap-Header |
| `<value-stream-code>` | Korte code | Charter Bootstrap-Header |
| `<pad-naar-charter.md>` | Relatief pad | Locatie van charter bestand |
| `<letterlijke tekst uit capability boundary sectie van charter>` | Exacte text copy | Charter sectie 2 |
| `<letterlijke tekst uit belangrijkste WEL-grens van charter>` | Exacte text copy | Charter sectie 5 - eerste WEL item |
| `<Charter-Evidence phrase uit Bootstrap-Header van charter>` | Exacte text copy | Charter Bootstrap-Header |

### Kritieke Grens Extractie

1. Zoek in charter: `## 2. Capability boundary`
2. Neem eerste complete zin na sectie header
3. Kopieer letterlijk inclusief markdown formatting

### Kritieke Output-Eis Extractie

1. Zoek in charter: `### Wat de [agent-naam] WEL doet`
2. Neem eerste bullet point
3. Kopieer letterlijk zonder "- " prefix

## Runtime Resolution

**Na agent execution:**
1. Resolve `Branch: main` naar werkelijke commit hash
2. Update beide bestanden:
   - Charter: `resolved_ref: <wordt-achteraf-gevuld>` → `resolved_ref: a1c1997`
   - Prompt: `canon-resolved-ref: <wordt-achteraf-gevuld>` → `canon-resolved-ref: a1c1997`

## Validation Checklist

### Charter Bootstrap-Header ✅
- [ ] Constitutie pad correct: `grondslagen/.algemeen/constitutie.md`
- [ ] Branch reference: `Branch: main`
- [ ] Canon placeholder: `resolved_ref: <wordt-achteraf-gevuld>`
- [ ] Value stream code: 3 letters, lowercase
- [ ] Geraadpleegde grondslagen: paths match value stream
- [ ] Actor versie: SemVer format
- [ ] Charter versie: separate from actor versie
- [ ] Charter-Evidence: WEL-statement format
- [ ] Timestamp: ISO-8601 format

### Prompt Charter-Acknowledgement ✅
- [ ] Agent naam: matches charter Bootstrap-Header
- [ ] Charter versie: matches charter Bootstrap-Header
- [ ] Value stream: matches charter Bootstrap-Header
- [ ] Canon placeholder: `<wordt-achteraf-gevuld>`
- [ ] Kritieke grens: literal copy from charter capability boundary
- [ ] Kritieke output-eis: literal copy from charter WEL-grens
- [ ] Charter-evidence: literal copy from charter Bootstrap-Header

### Constitutional Consistency ✅
- [ ] Charter en prompt refereren dezelfde charter versie
- [ ] Value stream codes consistent tussen charter en prompt
- [ ] Charter_ref pad klopt met werkelijke charter locatie
- [ ] Alle placeholders zijn ingevuld (geen `<...>` patterns remaining)

---

**Herkomst:** Agent Smeder constitutional compliance system v2.3  
**Laatst bijgewerkt:** 2026-02-08T16:35:00Z