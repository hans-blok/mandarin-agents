---
agent: mandarin.concept-curator
intent: valideer-concept-coherentie
versie: 1.0.0
input_parameters:
  - `artefact_bestand`
  - `domein`
  - `striktheid`
value_stream_fase: fnd.02

bootstrap:
  script: scripts/bootstrap_canon_consult.py
---
