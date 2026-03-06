---
agent: mandarin.gedragsspecificator
intent: valideer-scenario-consistentie
versie: 1.0.0
input_parameters:
  - feature_files
  - specificatie_document
  - validation_rules
value_stream_fase: sfw.03

bootstrap:
  script: scripts/bootstrap_canon_consult.py
---
