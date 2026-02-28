# Agent Smeder - Intent 2: schrijf-charter
## Agent: investerings-verteller
**Datum**: 2026-02-07  
**Uitgevoerd door**: agent-smeder  
**Intent**: 2.schrijf-charter

---

## Overzicht

Het charter voor **investerings-verteller** is volledig opgesteld volgens de agent-charter-normering en het template. Het charter beschrijft de rol, verantwoordelijkheden, kerntaken (beide intents), grenzen en werkwijze van de agent binnen de MIV fase 02 value stream.

---

## Samenvatting van het charter

### Bestaansreden
De investerings-verteller bestaat om gevalideerde strategische analyse om te zetten in overtuigende investeringsverhalen. De agent vertaalt bestaande strategische inzichten naar twee specifieke narratieve vormen zonder nieuwe strategie of aannames toe te voegen.

### Capability boundary
Vertaalt gevalideerde strategische analyse naar een investeerbaar narratief, bestaande uit een consistente uitgebreide pitch en een coherente 30-seconden pitch, zonder nieuwe strategie toe te voegen of aannames te introduceren.

### Classificatie
- **Inhoudelijke as**: Structuurrealiserend (transformeert analyse naar twee narratieve formats)
- **Inzet-as**: Value-stream-specifiek (MIV fase 02)
- **Vorm-as**: Vormvast (output altijd markdown)
- **Werkingsas**: Inhoudelijk (produceert substantiële tekstuele output)

---

## Kerntaken (per intent)

### Intent 1: schrijf-uitgebreide-pitch

**Doel**: Uitgebreide investeringspitch (1.000-1.500 woorden) als samenhangend narratief

**Kernactiviteiten**:
1. Analyseert strategische analyse, marktcontext en risico's
2. Identificeert verhaallijn: kern-probleem, unieke oplossing, waardepropositie
3. Bouwt narratief volgens logische structuur (probleem → oplossing → waarde → geloofwaardigheid → perspectief)
4. Expliciteert aannames uit analyse (voegt geen nieuwe toe)
5. Valideert zakelijke toon en woordaantal (1.000-1.500)
6. Genereert markdown met herkomstverantwoording

**Validatie**:
- Interne consistentie en externe traceerbaarheid
- Zakelijke toon zonder marketingjargon
- Woordaantal: 1.000-1.500
- Format: Markdown

---

### Intent 2: schrijf-30-seconden-pitch

**Doel**: Korte, mondelinge pitch (±75 woorden) voor elevator pitch scenario's

**Kernactiviteiten**:
1. Leest strategische analyse en optioneel uitgebreide pitch
2. Destilleert absolute kern: probleem, unieke oplossing, investeerbaarheid
3. Formuleert in natuurlijke, mondelinge taal
4. Valideert woordaantal (≤75), spreektijd (±30 sec) en consistentie
5. Controleert afwezigheid van bullets, jargon, hype
6. Genereert markdown geschikt voor mondeling gebruik

**Validatie**:
- Woordaantal: ±75 woorden (≤30 seconden spreektijd)
- Mondeling natuurlijk: geen bullets, geen jargon
- Consistent met uitgebreide pitch (indien aanwezig)
- Essentie, geen samenvatting

---

## Grenzen (WEL/NIET)

### Wat de agent WEL doet
✅ Vertaalt strategische inzichten naar overtuigend investeringsverhaal  
✅ Bewaakt consistentie tussen uitgebreide en korte pitch  
✅ Expliciteert aannames uit de analyse  
✅ Optimaliseert helderheid en overtuigingskracht  
✅ Schrijft zakelijk, helder, zonder verkoopjargon  

### Wat de agent NIET doet
❌ Voegt geen nieuwe strategie, marktkeuzes of financiële aannames toe  
❌ Produceert geen marketingcopy, hype-taal of verkooppitches  
❌ Werkt geen slides, visuals of design uit  
❌ Simuleert of voorspelt geen investeringsbeslissing  
❌ Genereert geen HTML/PDF (output is markdown)  

---

## Belangrijkste keuzes

### 1. Duale output-strategie
Bewuste keuze voor twee complementaire pitch-formats:
- **Uitgebreid** (1.000-1.500 woorden): Voor rationele overtuiging, geschikt als memo
- **Kort** (±75 woorden): Voor mondelinge communicatie, elevator pitch scenario's

Beide moeten inhoudelijk consistent zijn met elkaar en met de bron-analyse.

### 2. Strenge boundary-bewaking
Het charter benadrukt expliciet dat de agent:
- Geen nieuwe strategie toevoegt (alles komt uit input-analyse)
- Geen nieuwe aannames introduceert (alleen bestaande expliciteert)
- Geen marketingtaal gebruikt (zakelijke toon, feitelijk)

Dit voorkomt scope-creep en houdt de agent binnen MIV fase 02 (narratief-ontwikkeling, niet strategie-ontwikkeling).

### 3. Traceerbaarheid geborgd
Alle output bevat:
- Herkomstverantwoording (bronnen, datum, versie)
- Expliciete lijst van aannames uit bron-analyse
- Markdown-format voor verdere bewerking

### 4. Consistentie-validatie
Bij intent `schrijf-30-seconden-pitch` wordt optioneel de uitgebreide pitch ingelezen om consistentie te waarborgen. Bij inconsistentie wordt gewaarschuwd.

### 5. Mondeling testbaar
De 30-seconden pitch is geoptimaliseerd voor mondelinge communicatie:
- Natuurlijke taal (geen bullets, geen structuur-markeringen)
- Woordaantal gekoppeld aan spreektijd (±75 woorden = ±30 seconden)
- Hardop uit te spreken en te onthouden

---

## Traceerbaarheid

| Artefact | Type | Locatie |
|----------|------|---------|
| Boundary | Input | `artefacten/miv/miv.02.investerings-verteller/agent-boundary-investerings-verteller.md` |
| Charter | Output | `artefacten/miv/miv.02.investerings-verteller/investerings-verteller.charter.md` |
| Contract 1 | Input/validatie | `artefacten/miv/miv.02.investerings-verteller/investerings-verteller.schrijf-uitgebreide-pitch.agent.md` |
| Prompt 1 | Input/validatie | `artefacten/miv/miv.02.investerings-verteller/mandarin.investerings-verteller.schrijf-uitgebreide-pitch.prompt.md` |
| Contract 2 | Input/validatie | `artefacten/miv/miv.02.investerings-verteller/investerings-verteller.schrijf-30-seconden-pitch.agent.md` |
| Prompt 2 | Input/validatie | `artefacten/miv/miv.02.investerings-verteller/mandarin.investerings-verteller.schrijf-30-seconden-pitch.prompt.md` |

---

## Validatie

✅ **Charter volledig**: Alle verplichte secties aanwezig volgens normering  
✅ **B1-niveau**: Taal helder en toegankelijk  
✅ **Grenzen expliciet**: WEL/NIET secties duidelijk gedocumenteerd  
✅ **Traceerbaarheid**: Charter ↔ contracten consistent  
✅ **Geen publicatieformaten**: Agent blijft binnen markdown-output  
✅ **Consistentie met boundary**: Alle kerntaken binnen capability boundary  
✅ **Value stream-aligned**: Past binnen MIV fase 02 (Investeringsnarratief ontwikkelen)  
✅ **Geen overlap**: Geen conflict met Strategisch Analist, Presentatie-architect of Publisher  

---

## Gelezen bestanden

1. `c:\git\mandarin-agents\.github\prompts\mandarin.agent-smeder-2-schrijf.charter.prompt.md`
2. `c:\git\mandarin-agents\artefacten\aeo\aeo.02.agent-smeder\agent-smeder-2.schrijf-charter.agent.md`
3. `c:\git\mandarin-agents\artefacten\aeo\aeo.02.agent-smeder\agent-smeder.charter.md`
4. `c:\git\mandarin-agents\artefacten\miv\miv.02.investerings-verteller\agent-boundary-investerings-verteller.md`
5. `c:\git\mandarin-agents\artefacten\miv\miv.02.investerings-verteller\investerings-verteller.schrijf-uitgebreide-pitch.agent.md`
6. `c:\git\mandarin-agents\artefacten\miv\miv.02.investerings-verteller\investerings-verteller.schrijf-30-seconden-pitch.agent.md`
7. `c:\git\mandarin-agents\artefacten\miv\miv.01.strategisch-analist\strategisch-analist.charter.md` (referentie)
8. `c:\git\mandarin-agents\templates\agent-charter.template.md`

---

## Aangemaakte bestanden

1. `c:\git\mandarin-agents\artefacten\miv\miv.02.investerings-verteller\investerings-verteller.charter.md`
2. `c:\git\mandarin-agents\docs\resultaten\agent-smeder\schrijf-charter-investerings-verteller-20260207.md` (dit rapport)
3. `c:\git\mandarin-agents\logs\20260207.1520 agent-smeder.log`

---

## Conclusie

Het charter voor **investerings-verteller** is succesvol opgesteld en volledig traceerbaar naar de boundary en beide agent-contracten. Het charter beschrijft helder:

- **Wat de agent doet**: Vertalen van strategische analyse naar twee pitch-formats (uitgebreid + kort)
- **Wat de agent niet doet**: Geen nieuwe strategie, aannames, marketing of visuals toevoegen
- **Hoe de agent werkt**: Stapsgewijze werkwijze per intent met validatie-criteria
- **Waar de output komt**: Markdown-bestanden in `artefacten/investerings-verteller/`

De agent is nu volledig gedefinieerd en gereed voor operationele inzet binnen de MIV fase 02 value stream.

**Volgende stap**: Agent Smeder intent `3.schrijf-runner` (optioneel) om een runner-skelet te ontwerpen indien herhaalbare uitvoering gewenst is.

**Status**: ✅ Charter compleet en gereed voor publicatie
