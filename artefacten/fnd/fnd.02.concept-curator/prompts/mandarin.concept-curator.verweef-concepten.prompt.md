---
agent: mandarin.concept-curator
intent: verweef-concepten
versie: 1.0.0
input_parameters:
  - `concept_bestand`
  - *Context*
value_stream_fase: fnd.02

bootstrap:
  script: scripts/bootstrap_canon_consult.py
---
