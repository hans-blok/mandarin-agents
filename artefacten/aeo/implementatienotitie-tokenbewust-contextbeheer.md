# Implementatienotitie — Tokenbewust Contextbeheer in mandarin-agents

## 1. Doel

Deze notitie beschrijft hoe `mandarin-agents` het nieuwe normatieve kader voor tokenbewust werken technisch kan implementeren.

De notitie sluit aan op:

- `doctrine.bronhouding-en-exploratie.md`;
- `doctrine.traceability.md`;
- `rules.bronhouding.yaml`;
- `rules.traceability.yaml`;
- `execution-trace-bestand.schema.json`.

Het doel is drieledig:

1. de gebruiker vooraf waarschuwen bij waarschijnlijke contextoverschrijding;
2. tokenmetingen en contextdruk traceerbaar vastleggen;
3. aantoonbaar of vermoed contextverlies eerlijk communiceren.

---

## 2. Ontwerpuitgangspunten

### 2.1 Geen schijnnauwkeurigheid

`mandarin-agents` mag alleen een exacte tokenwaarde communiceren wanneer de gebruikte provider of runtime die waarde expliciet teruggeeft.

Er zijn daarom drie toegestane meetstatussen:

- `exact`;
- `schatting`;
- `onbekend`.

Alle componenten moeten deze driedeling expliciet ondersteunen. Een booleaanse vlag zoals `is_exact` is te arm. Gebruik een canonieke enumeratie.

### 2.2 Eén centrale meetketen

Tokenmetingen en contextdruk mogen niet verspreid in losse runners of agents ontstaan. De logica moet centraal liggen in één gedeelde service in `mandarin-agents`.

Werknaam:

- `context_budget_service`

Deze service wordt de enige plek voor:

- preflight-raming;
- normalisatie van provider-usage;
- drempelbepaling;
- genereren van context-events;
- opmaak van gebruikersmeldingen.

### 2.3 Runner is bron van waarheid voor trace

De agent communiceert met de gebruiker, maar de runner blijft de bron van waarheid voor:

- vastlegging van context-events;
- meetwijze (`exact`, `schatting`, `onbekend`);
- bron van het signaal;
- relatie met execution en tracebestand.

---

## 3. Functioneel doelbeeld

Per uitvoering krijgt `mandarin-agents` vier vaste momenten.

### 3.1 Moment A — Preflight bij invoer

Doel:

- schatten of de aangeleverde invoer al een risico vormt.

Resultaat:

- een `context_status` object;
- optioneel een `preflight_warning` event;
- een korte gebruikersmelding vóór modelaanroep.

### 3.2 Moment B — Preflight na bronassemblage

Doel:

- bepalen of de volledige samengestelde context nog binnen veilige marge ligt.

Resultaat:

- herziene tokenraming;
- geactualiseerde risicoklasse;
- eventueel escalatie van `laag` naar `hoog` of `kritiek`.

### 3.3 Moment C — Tijdens en na modelaanroep

Doel:

- provider-usage uitlezen wanneer beschikbaar;
- signalen over truncatie, summarization of andere compressie registreren.

Resultaat:

- `token_measurement` event;
- `compression_event`, `context_loss_known` of `context_loss_suspected` waar van toepassing.

### 3.4 Moment D — Trace schrijven

Doel:

- alle context-events vastleggen in `execution-trace-bestand`.

Resultaat:

- `context_events[]` gevuld conform schema;
- alle events gelabeld met bron, meetwijze en detail.

---

## 4. Technische architectuur

### 4.1 Nieuw kernobject: context_status

Introduceer een centraal object dat door runner, model-adapter en trace-writer wordt gedeeld.

Voorstel:

```python
class ContextStatus:
    model_name: str
    provider_name: str
    context_window_tokens: int | None
    context_window_meetwijze: Literal["exact", "schatting", "onbekend"]
    input_tokens: int | None
    input_tokens_meetwijze: Literal["exact", "schatting", "onbekend"]
    output_tokens: int | None
    output_tokens_meetwijze: Literal["exact", "schatting", "onbekend"]
    context_pressure_level: Literal["laag", "middel", "hoog", "kritiek"]
    exacte_meetbron_beschikbaar: bool
    hard_signaal_contextverlies: bool
    contextverlies_bekend: bool
    vermoed_contextverlies: bool
    events: list[ContextEvent]
```

Dit object voorkomt dat elk onderdeel eigen velden of eigen taal gebruikt.

### 4.2 Nieuw kernobject: context_event

Voorstel:

```python
class ContextEvent:
    event_type: Literal[
        "preflight_warning",
        "context_loss_known",
        "context_loss_suspected",
        "compression_event",
        "token_measurement",
    ]
    timestamp: datetime
    meetwijze: Literal["exact", "schatting", "onbekend"]
    bron: str
    detail: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    context_window_tokens: int | None = None
```

### 4.3 Nieuwe service: context_budget_service

Verantwoordelijkheden:

- tokenizer-selectie per model;
- schatting van promptonderdelen vóór provider-call;
- drempelwaardes bepalen;
- provider-responses normaliseren;
- events genereren;
- gebruikersmeldingen formatteren.

Niet in deze service:

- schrijven naar disk;
- tonen van UI;
- businesslogica van één specifieke agent.

### 4.4 Model-adapterlaag uitbreiden

Elke provider-adapter moet een uniforme interface opleveren voor:

- `usage` metadata;
- bekende limiet van context-window;
- signalen over truncatie of samenvatting;
- eventuele ontbrekende meetvelden.

Voorbeeld uniforme adapter-output:

```python
class ProviderUsageSnapshot:
    input_tokens: int | None
    output_tokens: int | None
    context_window_tokens: int | None
    meetwijze: Literal["exact", "schatting", "onbekend"]
    hard_signaal_contextverlies: bool
    compression_detected: bool
    raw_signal_source: str
```

---

## 5. Implementatie per component

### 5.1 Prompt assembler of bronassembler

Aanpassen:

- tel tokens per bouwblok waar mogelijk;
- label elk blok als `exact` of `schatting`;
- lever een samengesteld preflight-beeld aan de runner.

Belangrijk:

- hidden system prompts of platforminterne packing mogen niet als exact worden behandeld als die niet observeerbaar zijn.

### 5.2 Runner orchestration

Aanpassen:

- roep `context_budget_service` aan vóór modelaanroep;
- laat runner bij `hoog` of `kritiek` een waarschuwing uitsturen;
- registreer elk event in geheugen tot het tracebestand wordt geschreven;
- blokkeer niet direct, tenzij later bewust geconfigureerd.

### 5.3 Gebruikerscommunicatie

Voeg twee standaardmeldingen toe.

Preflight-waarschuwing:

```text
Waarschuwing: de samengestelde context nadert waarschijnlijk de limiet van het context-window.
Meetwijze: schatting.
Bron: runner-tokenizer.
```

Runtime-contextverlies:

```text
Let op: eerdere context is mogelijk niet meer volledig actief.
Meetwijze: onbekend.
Bron: provider-signaal ontbreekt, runner ziet verhoogde contextdruk.
```

Bij hard signaal:

```text
Let op: eerdere context is aantoonbaar gecomprimeerd of weggevallen.
Meetwijze: exact.
Bron: provider usage / runner event.
```

### 5.4 Trace writer

Aanpassen:

- schrijf `context_events` naar het execution-trace-bestand;
- valideer verplichte velden;
- weiger een event zonder `meetwijze`, `bron` of `detail`.

### 5.5 Validatie

Aanpassen:

- voeg validatieregels toe voor `context_events[]`;
- keur af wanneer `context_loss_known` zonder hard signaal wordt geschreven;
- keur af wanneer exacte meting wordt geclaimd zonder expliciete meetbron.

---

## 6. Drempelmodel

Gebruik geen harde claim “past wel” of “past niet”. Gebruik vier risiconiveaus.

Voorstel:

- `laag`: minder dan 60% van bekende of geschatte limiet;
- `middel`: 60% tot 80%;
- `hoog`: 80% tot 95%;
- `kritiek`: boven 95%.

Als `context_window_tokens` onbekend is:

- gebruik modelspecifieke configuratie als schatting;
- label de uitkomst als `schatting`;
- maak dit expliciet in melding en trace.

---

## 7. Wat exact kan en wat niet

### 7.1 Vaak exact mogelijk

- input- en outputtokenaantallen wanneer provider usage dit teruggeeft;
- bekende modelconfiguratie als de runtime deze zelf beheert;
- hard compressiesignaal wanneer provider of runner dit expliciet meldt.

### 7.2 Vaak alleen geschat mogelijk

- totaal van samengestelde prompt vóór verzending;
- context-window-vulling inclusief verborgen systeemlagen;
- effect van platforminterne packing;
- ruimte die nog beschikbaar blijft na tool- of schema-injectie.

### 7.3 Vaak niet betrouwbaar observeerbaar

- volledige werkelijke inhoud van het actieve context-window in gesloten platformen;
- exacte oorzaak van stil gedrag van een model zonder provider-signaal;
- automatische samenvatting als het platform daar geen event voor afgeeft.

Gevolg:

- de implementatie moet sturen op `transparantie van meetbaarheid`, niet op absolute schijnzekerheid.

---

## 8. Voorstel voor configuratie

Voeg een centrale configuratie toe, bijvoorbeeld:

```yaml
context_budget:
  enabled: true
  warn_threshold: 0.80
  critical_threshold: 0.95
  block_on_critical: false
  default_measurement_mode: schatting
  providers:
    anthropic:
      supports_exact_usage: true
      supports_hard_context_loss_signal: false
    openai:
      supports_exact_usage: true
      supports_hard_context_loss_signal: afhankelijk-van-model
```

Doel:

- geen providerlogica hard coderen in agents;
- gedrag per platform configureerbaar houden.

---

## 9. Implementatiefasen

### Fase 1 — Infrastructuur

- bouw `context_budget_service`;
- voeg `ContextStatus` en `ContextEvent` toe;
- breid provider-adapters uit met genormaliseerde usage-output.

### Fase 2 — Runner-integratie

- roep preflight in alle relevante runners aan;
- voeg gebruikerswaarschuwingen toe;
- verzamel events in execution-context.

### Fase 3 — Trace-integratie

- schrijf `context_events` naar execution-trace-bestanden;
- valideer schema en verplichte velden.

### Fase 4 — Curator- en testlaag

- voeg validatieregels toe;
- maak regressietests voor `exact`, `schatting` en `onbekend`;
- test foutscenario’s rond ontbrekende usage.

### Fase 5 — Adoptie

- eerst alleen waarschuwen en loggen;
- daarna strengere validatie;
- pas daarna eventueel hard blokkeren bij `kritiek`.

---

## 10. Teststrategie

Minimaal testen:

### 10.1 Normale kleine invoer

Verwacht:

- geen waarschuwing;
- wel een `token_measurement` event;
- meetwijze correct gelabeld.

### 10.2 Grote invoer met hoge contextdruk

Verwacht:

- preflight-waarschuwing;
- `preflight_warning` event;
- geen claim van exacte meting als provider die niet geeft.

### 10.3 Provider met usage maar zonder compressiesignaal

Verwacht:

- `token_measurement` event;
- geen `context_loss_known`;
- alleen `context_loss_suspected` als runner daarvoor onderbouwde indicatie heeft.

### 10.4 Hard compressiesignaal

Verwacht:

- `compression_event`;
- `context_loss_known`;
- gebruikersmelding met label `exact`.

### 10.5 Ontbrekende provider-usage

Verwacht:

- meetwijze `onbekend` of `schatting`;
- geen foutieve exacte claims;
- tracebestand blijft geldig.

---

## 11. Belangrijkste risico’s

### 11.1 Te veel verspreide logica

Risico:

- elke runner gaat zelf tokens schatten.

Maatregel:

- alle metingen via één centrale service laten lopen.

### 11.2 Verwarring tussen provider en runner

Risico:

- agenttekst zegt “exact”, terwijl de runner slechts heeft geraamd.

Maatregel:

- agenttekst altijd laten genereren uit `ContextStatus`.

### 11.3 Verleiding tot hard blokkeren

Risico:

- gebruikersflow breekt te vroeg op schattingen.

Maatregel:

- eerst waarschuwen, loggen en meten; pas later blokkeren.

### 11.4 Onzichtbare platformlagen

Risico:

- systeemprompt, toolschema’s en vendor-packing worden abusievelijk meegerekend als exacte context.

Maatregel:

- deze standaard als `schatting` of `onbekend` labelen tenzij het platform anders bewijst.

---

## 12. Concreet advies voor start in mandarin-agents

Eerst bouwen:

1. `ContextStatus` en `ContextEvent` datamodel.
2. `context_budget_service`.
3. provider usage normalisatie.
4. trace-writer uitbreiding voor `context_events`.

Eerst valideren:

1. dat geen exacte claims meer uit de runners komen zonder expliciete meetbron;
2. dat elk tracebestand context-events correct kan opslaan;
3. dat gebruikersmeldingen onderscheid maken tussen bekend en vermoed contextverlies.

Niet als eerste doen:

- hard blokkeren op geschatte overschrijding;
- model-onafhankelijke exacte tokenclaims invoeren;
- UI-teksten per agent handmatig laten formuleren.

---

## 13. Samenvatting

De kern van de implementatie is eenvoudig:

- één centrale service voor contextbudget en tokenmeting;
- één gedeeld statusmodel;
- één traceformaat voor context-events;
- strikte scheiding tussen exact, schatting en onbekend.

Als `mandarin-agents` dit centraal oplost, blijft de nieuwe governance uitvoerbaar, toetsbaar en technisch eerlijk.