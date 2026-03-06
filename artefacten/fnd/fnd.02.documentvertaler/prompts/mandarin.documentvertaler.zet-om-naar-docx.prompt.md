---
agent: mandarin.documentvertaler
intent: zet-om-naar-docx
versie: 1.0.0
input_parameters:
  - markdown_file
  - output_path
  - conversie_opties
value_stream_fase: fnd.02

bootstrap:
  script: scripts/bootstrap_canon_consult.py
---
