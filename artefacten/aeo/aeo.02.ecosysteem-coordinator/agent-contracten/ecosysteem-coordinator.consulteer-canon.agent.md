---
agent: ecosysteem-coordinator
intent: consulteer-canon
versie: 1.0.0
---

# Ecosysteem-coordinator — Consulteer Canon

## Rolbeschrijving (korte samenvatting)

Raadpleegt de mandarin-canon repository, extraheert relevante grondslagen voor een specifieke value stream, en logt de consultatie met commit SHA voor volledige traceerbaarheid.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `ecosysteem-coordinator.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- agent: Naam van de agent waarvoor canon wordt geraadpleegd (type: string, kebab-case).
- value_stream: Value stream code voor grondslagen-lookup (type: string, bijv. "aeo", "sfw").
- intent: Intent naam voor audit logging (type: string, kebab-case).

**Optionele parameters**:
- canon_path: Lokaal pad naar mandarin-canon repository (type: string, default: "../mandarin-canon").
- canon_github_url: GitHub URL voor clone indien lokaal niet aanwezig (type: string, default uit beleid-workspace.md).
- grondslagen: Comma-separated glob patterns voor grondslagen (type: string, default uit beleid-workspace.md per value stream).
- workspace_file: Pad naar workspace-bestand dat wordt uitgevoerd (type: string, voor audit context).

### Output (wat komt eruit)

De ecosysteem-coordinator levert:
- **Console output**: Samenvatting van geraadpleegde grondslagen met bestandsnamen
- **Environment context**: Commit SHA en branch voor downstream gebruik
- **Audit log entry**: Append naar `audit/canon-consult.log.md`

**Deliverable bestand**: `audit/canon-consult.log.md` (append)

**Outputformaat** (log entry):
```markdown
## Canon Consultatie - {timestamp}

- **Agent**: {agent}
- **Intent**: {intent}
- **Value Stream**: {value_stream}
- **Canon Commit**: {commit_sha}
- **Canon Branch**: {branch}
- **Grondslagen geraadpleegd**:
  - {grondslag-1.md}
  - {grondslag-2.md}
```

**Formaat-normering**: 
- Markdown append-only log conform audit-standaarden
- ISO 8601 timestamps in CET/CEST

### Foutafhandeling

De ecosysteem-coordinator:
- stopt wanneer canon_path niet bestaat EN canon_github_url niet bereikbaar is;
- stopt wanneer geen grondslagen gevonden worden voor opgegeven patterns;
- stopt wanneer git niet beschikbaar is op PATH (voor commit SHA);
- vraagt NIET om verduidelijking (fully deterministic);
- retourneert exit code 1 bij fout, 0 bij succes.

---

## Werkwijze

### Stappen
1. **Bepaal canon locatie**: Check lokaal pad, clone van GitHub indien nodig
2. **Resolve git metadata**: Haal commit SHA en branch op
3. **Match grondslagen**: Glob patterns toepassen op canon directory
4. **Lees grondslagen**: Extraheer content van matched bestanden
5. **Log consultatie**: Append entry naar audit/canon-consult.log.md
6. **Return summary**: Print geraadpleegde bestanden naar stdout

### Kwaliteitsborging
- Commit SHA is altijd 7+ karakters of volledig
- Alle glob patterns worden gelogd, ook als ze 0 matches hebben
- Audit log entry is atomair (geen partial writes)

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Contract is extern observeerbaar
  - Principe 7 (Transparante Verantwoording): Volledige audit trail van raadplegingen

**Canon-consultatie:**
- Dit IS de canon-consultatie functie; raadpleegt zelf geen andere canon-functie
- Broncode: Geïntegreerd in `artefacten/aeo/aeo.02.ecosysteem-coordinator/runner/ecosysteem-coordinator.runner.py`

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gebruikte canon locatie (lokaal pad of GitHub URL)
- ✓ Git commit SHA en branch
- ✓ Alle geraadpleegde grondslagen-bestanden
- ✓ Timestamp van consultatie

Logging-formaat: Markdown append naar `audit/canon-consult.log.md`

**Escalatie-paden:**
- STOP: bij ontbrekende canon repository (geen fallback)
- STOP: bij git fouten (commit SHA vereist voor traceerbaarheid)

---

## Metadata

**Intent-ID**: `aeo.02.ecosysteem-coordinator.consulteer-canon`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 02 — Ecosysteeminrichting  
**Classificatie**: Conditioneel / Input-gebonden
