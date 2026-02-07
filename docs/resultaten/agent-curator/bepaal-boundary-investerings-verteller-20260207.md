# Agent Curator - Boundary Bepaling: investerings-verteller

**Datum**: 2026-02-07  
**Uitgevoerd door**: agent-curator  
**Intent**: bepaal-agent.boundary  
**Target agent**: investerings-verteller  
**Value stream**: MIV (Markt- en Investeringsvorming), fase 02

---

## Verplichte 4-regel output

```
agent-naam: investerings-verteller
capability-boundary: De Investerings-verteller vertaalt gevalideerde strategische analyse naar een investeerbaar narratief, bestaande uit een consistente uitgebreide pitch en een coherente 30-seconden pitch, zonder nieuwe strategie toe te voegen of aannames te introduceren.
doel: Strategische analyse omzetten in overtuigende, coherente investeringsverhalen die investeerders rationeel en inhoudelijk overtuigen.
domein: markt- en investeringsvorming (MIV)
```

---

## Voorgestelde intents (agent contracten)

1. **`schrijf-uitgebreide-pitch`**  
   Creeërt een uitgebreide investeringspitch (1.000-1.500 woorden) als samenhangend narratief met verhalende logica (probleem → oplossing → waarde → geloofwaardigheid → perspectief).

2. **`schrijf-30-seconden-pitch`**  
   Formuleert een korte, mondelinge pitch (±75 woorden) die hardop uitgesproken kan worden en de essentie van het investeringsverhaal raakt.

---

## Toelichting op de boundary

### Kernkarakter
De **investerings-verteller** is een **vertaalagens**: het neemt gevalideerde strategische analyse uit eerdere MIV-fasen (bijvoorbeeld van de Strategisch Analist uit MIV 01) en transformeert deze naar twee specifieke narratieve vormen:
1. Een uitgebreide, rationele investeringspitch (geschikt als memo of voorbereiding op gesprek)
2. Een compacte 30-seconden pitch (mondeling deelbaar, essentie-gericht)

**Cruciaal**: De agent voegt **geen nieuwe strategie, aannames of financiële projecties** toe. Het expliciteert alleen wat al in de analyse aanwezig is en optimaliseert voor helderheid, coherentie en overtuigingskracht.

### Classificatie
- **Inhoudelijke as**: Structuurrealiserend (vertaalt bestaande analyse naar twee narratieve formats)
- **Inzet-as**: Value-stream-specifiek (MIV fase 02)
- **Vorm-as**: Vormvast (output altijd markdown-tekst, geen visuals)
- **Werkingsas**: Inhoudelijk (produceert substantiële tekstuele output)

### Grenzen (wat de agent WEL doet)
✅ Vertaalt strategische inzichten naar overtuigend investeringsverhaal  
✅ Bewaakt consistentie tussen lange en korte pitch  
✅ Expliciteert aannames die al in de analyse aanwezig zijn  
✅ Optimaliseert helderheid, structuur en overtuigingskracht  
✅ Schrijft zakelijk, helder, zonder verkoopjargon  

### Grenzen (wat de agent NIET doet)
❌ Voegt geen nieuwe strategie, marktkeuzes of financiële aannames toe  
❌ Produceert geen marketingcopy, hype-taal of verkooppitches  
❌ Werkt geen slides, visuals of design uit (dat is Presentatie-architect)  
❌ Simuleert of voorspelt geen investeringsbeslissing  

---

## Consistentie-check

### Positionering in MIV value stream
- **MIV 01** (Strategische intentie expliciteren): **Strategisch Analist** expliciteert intenties, spanning en aannames
- **MIV 02** (Investeringsnarratief ontwikkelen): **Investerings-verteller** vertaalt deze analyse naar investeerbare verhalen
- Geen overlap: Strategisch Analist levert feitenbasis, Investerings-verteller construeert overtuigend narratief

### Geen overlap met andere agents
| Agent | Boundary verschil |
|-------|-------------------|
| **Strategisch Analist** (MIV 01) | Expliciteert strategie; Investerings-verteller vertaalt deze maar voegt niets toe |
| **Presentatie-architect** (FND 02) | Ontwerpt visuals/templates; Investerings-verteller levert alleen tekst |
| **Publisher** (KVL 04) | Genereert HTML/PDF; Investerings-verteller levert markdown |
| **Marketing-agents** | Produceren klantgerichte copy; Investerings-verteller richt zich op investeerders met zakelijke toon |

### Canon-consistentie
✅ Naam "investerings-verteller" is beschrijvend voor de rol: een verhaal vertellen aan investeerders  
✅ Past binnen MIV fase 02 "Investeringsnarratief ontwikkelen"  
✅ Volgt mandarin-principe: geen nieuwe strategie toevoegen, alleen bestaande vertalen  
✅ Output blijft markdown (geen publicatieformaten)  

---

## Uitgevoerde acties

1. **Per-agentfolder aangemaakt**:  
   `artefacten/miv/miv.02.investerings-verteller/`  
   (volgens namingconventie: 3-letter value-streamcode + 2-cijferige fase + agent-naam)

2. **Boundary-artefact geplaatst in per-agentfolder**:  
   `artefacten/miv/miv.02.investerings-verteller/agent-boundary-investerings-verteller.md`  
   Dit is de bronlocatie voor Agent Smeder om contracten, charter en prompt-metadata te genereren.

3. **Publicatiekopie gemaakt**:  
   `docs/resultaten/agent-curator/agent-boundary-investerings-verteller.md`  
   Voor overdracht aan Agent Smeder en documentatie-doeleinden.

---

## Aanbevelingen voor Agent Smeder

De boundary is nu gereed voor handoff naar **Agent Smeder** (intent: `1.leg-agent-contract-vast` en `2.schrijf-charter`).

**Aandachtspunten bij contract-ontwikkeling**:
1. **Twee intents** met sterk verschillende output-lengtes (1.000-1.500 woorden vs ±75 woorden)
2. **Kwaliteitscriteria**: Beide pitches moeten inhoudelijk consistent zijn; geen nieuwe aannames
3. **Input-validatie**: Strategische analyse moet volledig zijn (probleem, oplossing, waarde, risico's)
4. **Foutafhandeling**: Stopt wanneer nieuwe strategie of aannames gevraagd worden
5. **Output-format**: Altijd markdown, geschikt voor verdere bewerking door Publisher

**Voorgestelde runner-structuur**:
- Leest strategische analyse (markdown)
- Valideert volledigheid van analyse
- Genereert beide pitches in één run (voor consistentie)
- Schrijft output naar `docs/resultaten/investerings-verteller/pitch-<datum>.md`

---

## Traceerbaarheid

| Artefact | Type | Locatie |
|----------|------|---------|
| Boundary (bron) | Per-agentfolder | `artefacten/miv/miv.02.investerings-verteller/agent-boundary-investerings-verteller.md` |
| Boundary (publicatie) | Resultaat-documentatie | `docs/resultaten/agent-curator/agent-boundary-investerings-verteller.md` |
| Charter (toekomstig) | Agent Smeder output | `artefacten/miv/miv.02.investerings-verteller/investerings-verteller.charter.md` |
| Contracten (toekomstig) | Agent Smeder output | `artefacten/miv/miv.02.investerings-verteller/investerings-verteller.*.agent.md` |

---

## Gelezen bestanden

1. `c:\git\mandarin-agents\.github\prompts\mandarin.agent-curator.bepaal-agent.boundary.prompt.md`
2. `c:\git\mandarin-agents\artefacten\aeo\aeo.02.agent-curator\agent-curator.bepaal-agent.boundary.agent.md`
3. `c:\git\mandarin-agents\artefacten\aeo\aeo.02.agent-curator\agent-curator.charter.md`
4. `c:\git\mandarin-agents\templates\agent-boundary.template.md`
5. `c:\git\mandarin-agents\artefacten\miv\miv.01.strategisch-analist\agent-boundary-strategisch-analist.md` (referentie)

---

## Aangemaakte bestanden

1. `c:\git\mandarin-agents\artefacten\miv\miv.02.investerings-verteller\agent-boundary-investerings-verteller.md` (bron)
2. `c:\git\mandarin-agents\docs\resultaten\agent-curator\agent-boundary-investerings-verteller.md` (publicatie)
3. `c:\git\mandarin-agents\docs\resultaten\agent-curator\bepaal-boundary-investerings-verteller-20260207.md` (dit rapport)
4. `c:\git\mandarin-agents\logs\20260207.1500 agent-curator.log` (logging conform Norm 10.4)

---

## Validatie

✅ **Capability boundary scherp**: Vertaling zonder toevoeging, twee output-formats  
✅ **Geen overlap**: Geen conflict met Strategisch Analist, Presentatie-architect of Publisher  
✅ **Value stream-consistent**: Past binnen MIV 02  
✅ **Canon-aligned**: Naam en scope volgen mandarin-principes  
✅ **Governance-compliant**: Volgt beleid-mandarin-agents.md en normering  
✅ **Per-agentfolder aangemaakt**: `artefacten/miv/miv.02.investerings-verteller/` bestaat  
✅ **Boundary-artefact geplaatst**: Gereed voor Agent Smeder handoff  

---

## Status

✅ **Boundary-bepaling voltooid**  
🔄 **Klaar voor handoff naar Agent Smeder** voor contracten, charter en prompt-metadata  

De agent **investerings-verteller** is nu gedefinieerd binnen het mandarin-agents ecosysteem en gereed voor verdere uitwerking.
