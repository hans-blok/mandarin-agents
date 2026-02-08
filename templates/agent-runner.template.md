# Runner Template — <Runner Naam> (Execution Runner)

> **Doel**: dit template beschrijft een *deterministische uitvoerder* (runner) in een agentic systeem.  
> Een runner is geen “intelligentie”, maar **uitvoering onder governance**.  
> De runner hoort bij één capability boundary en heeft één of meer **front doors** (interfaces) die fungeren als **contracts**.

---

## 0. Metadata

- **Identifier**: `<namespace>.runner.<naam>`  
- **Status**: Draft | Active | Deprecated  
- **Versie**: `0.1.0`
- **Owner**: `<rol/team>`
- **Value Stream**: `<value-stream>`
- **Primary Boundary**: `<één zin: wat doet deze runner wel>`
- **Repo/Locatie**: `<pad naar script/runner>`
- **Laatste wijziging**: `YYYY-MM-DD`

---

## 1. Purpose

### Bestaansreden
Beschrijf in 2–5 zinnen:
- welk concreet probleem de runner oplost,
- welke herhaalbare uitvoering hij levert,
- welke waarde dit oplevert (tijd, kwaliteit, compliance, voorspelbaarheid).

### Niet-doel
Noem expliciet wat deze runner **niet** is/doet (max 5 bullets), bijv.:
- geen interpretatie van ambigue input,
- geen autonoom “besluit” buiten de contractregels,
- geen domeinstrategie.

---

## 2. Capability Boundary

### Binnen scope (DOES)
- `<actie 1, concreet en toetsbaar>`
- `<actie 2>`
- `<actie 3>`

### Buiten scope (DOES NOT)
- `<uitgesloten actie 1>`
- `<uitgesloten actie 2>`
- `<uitgesloten actie 3>`

> **Norm**: één runner = één verantwoordelijkheid.  
> Als je “en” moet gebruiken, is splitsen waarschijnlijk beter.

---

## 3. Front Doors (Contracts)

> **Front door** = het formele contract waarmee de runner wordt aangeroepen.  
> Dit is het equivalent van “agent contracts”, maar dan voor deterministische uitvoering.

Beschrijf elke front door als een apart contract.

### Front Door A — CLI
- **Command**: `<voorbeeld: runner-name --arg value>`
- **Verplichte parameters**:
  - `<naam>`: `<type/format>` — `<betekenis>`
- **Optionele parameters**:
  - `<naam>`: `<type/format>` — `<betekenis>`
- **Exit codes**:
  - `0`: success
  - `1`: validation error
  - `2`: execution error
  - `3`: dependency unavailable
- **Output kanaal**:
  - stdout: `<wat komt hier>`
  - stderr: `<wat komt hier>`

### Front Door B — Config file (optioneel)
- **Config format**: `YAML | JSON | ENV`
- **Schema**: `<link/pad naar schema of beschrijving>`
- **Validatieregels**:
  - `<regel 1>`
  - `<regel 2>`

### Front Door C — API call / webhook (optioneel)
- **Endpoint**: `<pad>`
- **Auth**: `<mechanisme>`
- **Request schema**: `<beschrijving>`
- **Response schema**: `<beschrijving>`

---

## 4. Inputs

### Vereiste inputs
| Input | Bron | Formaat | Validatieregel | Opmerking |
|------|------|---------|----------------|-----------|
| `<input-1>` | `<bron>` | `<format>` | `<regel>` | `<…>` |

### Input-kwaliteitspoort (Input Quality Gate)
De runner start **alleen** als:
- ☐ alle verplichte inputs aanwezig zijn
- ☐ formats valide zijn
- ☐ referenties/paden bestaan
- ☐ expliciete aannames ≤ 3

---

## 5. Outputs

### Geleverde outputs
| Output | Doel/locatie | Formaat | Voorbeeldnaam | Traceerbaarheid |
|--------|--------------|---------|---------------|-----------------|
| `<output-1>` | `<pad>` | `<format>` | `<naam>` | `<link naar run-id>` |

### Output-kwaliteitspoort (Exit Criteria)
De run is pas “Success” wanneer:
- ☐ outputs compleet zijn
- ☐ outputs intern consistent zijn
- ☐ traceerbaarheid is vastgelegd
- ☐ geen stille degradatie (warnings expliciet)

---

## 6. Determinisme en Idempotency

### Determinisme
- **Deterministisch gedrag**: ja/nee  
  Toelichting: `<wat maakt de run deterministisch?>`

### Idempotency
- **Idempotent**: ja/nee  
- **Idempotency key**: `<run-id / input hash / timestamp policy>`
- **Gedrag bij herhaalde run**:
  - `<overschrijven | skip | versioned output>`

---

## 7. Processing Rules (Execution Contract)

> Beschrijf WAT er gebeurt, in stappen die toetsbaar zijn.

1. **Validate input**  
   - `<validatiestap>`
2. **Load dependencies**  
   - `<dependency stap>`
3. **Execute transformation / action**  
   - `<kernactie>`
4. **Write outputs**  
   - `<output stap>`
5. **Write trace log**  
   - `<trace stap>`
6. **Return status**  
   - `<exit code + samenvatting>`

### Invarianten (altijd waar)
- `<invariant 1>`
- `<invariant 2>`
- `<invariant 3>`

---

## 8. Observability en Audit Trail

### Logging (minimumnorm)
- **Run ID**: altijd vastleggen
- **Start/stop timestamp**: altijd
- **Input fingerprint**: hash/summary (geen gevoelige data)
- **Output references**: paden/ids
- **Warnings & errors**: expliciet en machineleesbaar

### Audit trail
- Waar staat het run-log? `<pad/locatie>`
- Hoe link je output ↔ run ↔ input? `<mechanisme>`

---

## 9. Security, Privacy en Compliance

### Data handling
- **Gevoelige data**: ja/nee  
- **Masking/redaction**: `<regels>`
- **Retention**: `<termijn>`

### Toegang
- **Minimale rechten**: `<beschrijving>`
- **Secrets**: nooit hardcoded; bron: `<secret store/env>`

### Verboden gedrag
- geen exfiltratie,
- geen “best effort” op privacyregels,
- geen silent fallback naar onbetrouwbare bronnen.

---

## 10. Failure Modes en Escalatie

### Verwachte fouten (met gedrag)
| Fouttype | Detectie | Gedrag | Exit code | Escalatie |
|---------|----------|--------|----------|----------|
| Validation error | `<rule>` | stop | `1` | `<naar wie>` |

### Escalatie-triggers
Escaleren naar mens wanneer:
- meer dan 3 aannames nodig zijn,
- input conflictueus is,
- compliance-regels niet aantoonbaar gehaald worden,
- afhankelijkheden instabiel zijn (herhaald).

---

## 11. Dependencies

### Interne dependencies
- `<lib/tooling>`
- `<shared assets>`

### Externe dependencies
- `<ERP/CRM/DB/API>`
- **Beschikbaarheidseis**: `<SLA/assumption>`
- **Fallback policy**: `<none | degraded mode | stop>`

---

## 12. Orkestratie (Workflow Position)

### Plaats in de keten
- **Upstream**: `<wat moet er eerst gebeurd zijn>`
- **Downstream**: `<wat volgt hierna>`

### Triggering
- **Event**: `<event>`
- **Schedule**: `<cron>` (optioneel)
- **Manual**: `<wie mag dit starten>`

### Concurrency
- **Parallel runs toegestaan**: ja/nee  
- **Locking strategy**: `<none | file lock | distributed lock>`

---

## 13. Testbaarheid

### Contract tests (minimumnorm)
- Input-validatie tests
- Determinisme test (zelfde input → zelfde output)
- Error-path test (bekende failure → juiste exit code)
- Golden file / snapshot tests (optioneel)

### Voorbeeld testcases
- `<case 1>`
- `<case 2>`

---

## 14. Versiebeheer en Change Policy

- **Breaking changes**: alleen via major version bump
- **Backward compatibility**: `<beleid>`
- **Deprecation window**: `<termijn>`
- **Changelog**: `<pad>`

---

## 15. Traceerbaarheid naar Canon en Contracts

- **Boundary bron**: `<charter/boundary document>`
- **Front doors (contracts) gekoppeld aan**:
  - `<contract-id A>`
  - `<contract-id B>`
- **Artefacten geproduceerd in**: `<standaard outputlocatie>`

---

## 16. Anti-patterns

De runner mag nooit:
- “stil” doorgaan bij fouten,
- output genereren zonder trace,
- ongedocumenteerde aannames gebruiken,
- scope uitbreiden (“even dit ook”) zonder nieuw contract.

---

# Bijlage A — Minimale Run Summary (output)

Na elke run produceert de runner een klein machineleesbaar summary-object:

- `run_id`
- `status` (success/fail)
- `exit_code`
- `inputs_fingerprint`
- `outputs` (paden/ids)
- `warnings[]`
- `errors[]`
- `duration_ms`
