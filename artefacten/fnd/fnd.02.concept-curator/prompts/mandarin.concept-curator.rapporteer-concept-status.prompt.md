---
agent: mandarin.concept-curator
intent: rapporteer-concept-status
versie: 1.0.0
input_parameters:
  - domein
  - formaat
  - status_filter
value_stream_fase: fnd.02

bootstrap:
  script: scripts/bootstrap_canon_consult.py
---
