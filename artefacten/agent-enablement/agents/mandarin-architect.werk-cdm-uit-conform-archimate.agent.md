# Agent-contract — mandarin-architect.werk-cdm-uit-conform-archimate

---
agent: mandarin-architect
intent: werk-cdm-uit-conform-archimate
charter_ref: @main:exports/agent-enablement/charters-agents/mandarin-architect.charter.md
input-parameters:
- domein (string, verplicht)
- archimate-scope (string, optioneel)
output-afspraken:
- Markdown-bestand met minimaal ArchiMate-model (elementen, relaties, toelichting)
foutafhandeling:
- Stopt bij onduidelijke scope of ontbrekende input
- Vraagt verduidelijking bij onvolledige opdracht
---