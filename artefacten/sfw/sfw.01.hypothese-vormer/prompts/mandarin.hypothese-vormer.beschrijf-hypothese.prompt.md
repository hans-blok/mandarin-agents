---
agent: mandarin.hypothese-vormer
intent: beschrijf-hypothese
versie: 1.0.0
input_parameters:
  - probleemomschrijving
  - interventie_vermoeden
  - auteur
  - bron_referenties
  - context
  - stakeholders
value_stream_fase: sfw.01

bootstrap:
  script: scripts/bootstrap_canon_consult.py
---
