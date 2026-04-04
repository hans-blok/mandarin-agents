#!/usr/bin/env python3
"""
Runner voor agent: canon-curator

Beschikbare intents:
- adviseer-grondslag-verbeteringen
- publiceer-grondslagen
- valideer-grondslag-consistentie
- valideer-terminologische-scherpte

Architectuur: One Agent, One Runner.
Deze runner delegeert execution-file generatie aan ecosysteem-coordinator.runner.py.
"""

from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone


TARGET_AGENT = 'canon-curator'


def find_ecosysteem_coordinator_runner() -> Path:
    """Zoek de ecosysteem-coordinator runner."""
    this_file = Path(__file__).resolve()
    # runner/ -> aeo.01.canon-curator/ -> aeo/ -> artefacten/ -> repo-root
    repo_root = this_file.parent.parent.parent.parent.parent

    candidate = repo_root / "artefacten" / "fnd" / "fnd.01.ecosysteem-coordinator" / "runner" / "ecosysteem-coordinator.runner.py"
    if candidate.exists():
        return candidate

    cwd_candidate = Path.cwd() / "artefacten" / "fnd" / "fnd.01.ecosysteem-coordinator" / "runner" / "ecosysteem-coordinator.runner.py"
    if cwd_candidate.exists():
        return cwd_candidate

    raise FileNotFoundError("ecosysteem-coordinator.runner.py niet gevonden")


def run_intent(intent: str, params: dict[str, str]) -> int:
    """Delegeer intent-uitvoering naar de ecosysteem-coordinator."""
    coordinator = find_ecosysteem_coordinator_runner()
    cmd = [
        sys.executable,
        str(coordinator),
        "genereer-instructies",
        "--agent",
        TARGET_AGENT,
        "--intent",
        intent,
    ]

    for key, value in params.items():
        if value is None or value == "":
            continue
        cmd.extend(["-p", f"{key}={value}"])

    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(cmd, env=env).returncode


def find_canon_path() -> Path:
    """Zoek de canon-workspace als sibling van de repo-root."""
    this_file = Path(__file__).resolve()
    # runner/ -> aeo.01.canon-curator/ -> aeo/ -> artefacten/ -> repo-root
    repo_root = this_file.parent.parent.parent.parent.parent
    candidate = repo_root.parent / "mandarin-canon"
    if candidate.exists():
        return candidate
    cwd_candidate = Path.cwd().parent / "mandarin-canon"
    if cwd_candidate.exists():
        return cwd_candidate
    raise FileNotFoundError("mandarin-canon niet gevonden naast de huidige workspace")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parseer YAML frontmatter uit markdown tekst. Geeft (fields, body) terug."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_text = text[3:end].strip()
    body = text[end + 4:].strip()
    fields: dict = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r'^([a-zA-Z_][a-zA-Z0-9_-]*)\s*:\s*(.*)', line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            fields[key] = val
    return fields, body


def extract_title(body: str) -> str:
    """Extraheer eerste H1 header uit markdown body."""
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return ""


# Bekende value stream codes en namen
_VS_NAMEN: dict[str, str] = {
    "AEO": "Agent Ecosysteem Ontwikkeling",
    "AOD": "Architectuur Ontwerp & Documentatie",
    "FND": "Fundament",
    "MIV": "Markt en Inkoop Verkenning",
    "SFW": "Software",
}


def classify_path(rel_to_grondslagen: str) -> tuple:
    """Classificeer een pad t.o.v. grondslagen/ in een van drie buckets.

    Returns:
        ('algemeen',)              — algemeen[] array
        ('vs', 'AEO')              — value_streams[VS].grondslagen[]
        ('fase', 'AEO', '03')      — value_streams[VS].fasen[NN].grondslagen[]
    """
    parts = rel_to_grondslagen.replace("\\", "/").split("/")
    first = parts[0]

    # .algemeen/ of thematische mappen zonder VS-code (value-streams/, kaderdefinities/, ...)
    if first.startswith(".") or not re.match(r'^[a-z]{2,5}$', first):
        return ("algemeen",)

    vs_code = first.upper()

    # Fase-submap: aeo/aeo.03.automatisering-en-pipeline/...
    if len(parts) >= 3:
        second = parts[1]
        m = re.match(rf'^{re.escape(first)}\.([0-9]{{2}})\.',  second)
        if m:
            return ("fase", vs_code, m.group(1))

    return ("vs", vs_code)


def infer_type(rel_to_grondslagen: str, filename: str) -> str:
    """Leid type af, conform schema enum: constitutie | doctrine | concepten |
    kaderdefinitie | checklist | value-stream | grondslag."""
    rel = rel_to_grondslagen.replace("\\", "/")
    name = filename.lower()
    if rel.startswith("value-streams/") or "value-stream" in name:
        return "value-stream"
    if rel.startswith("kaderdefinities/") or "kaderdefinitie" in name:
        return "kaderdefinitie"
    if "doctrine" in name:
        return "doctrine"
    if "constitutie" in name:
        return "constitutie"
    if "concepten" in name:
        return "concepten"
    if "checklist" in name:
        return "checklist"
    return "grondslag"


def _make_entry(md_file: Path, grondslagen_dir: Path) -> dict:
    """Bouw een grondslag-entry van een markdown bestand. Volledig deterministisch.

    Bevat twee digest-velden als ruwe data:
    - digest_header: zoals opgeslagen in de YAML frontmatter (wat het bestand claimt)
    - digest_berekend: live berekend op moment van publicatie (wat het bestand werkelijk is)
    - status_header: de status zoals vermeld in de YAML frontmatter — geen oordeel, alleen feitrapportage

    Het oordeel over inhoudelijke kwaliteit of consistentie is niet de taak van publiceer-grondslagen;
    dat is de verantwoordelijkheid van valideer-grondslag-consistentie.
    """
    rel = md_file.relative_to(grondslagen_dir).as_posix()
    content = md_file.read_text(encoding="utf-8")
    fields, body = parse_frontmatter(content)

    naam = md_file.name
    titel = extract_title(body) or md_file.stem.replace("-", " ").title()
    doc_type = infer_type(rel, naam)

    digest_header = fields.get("digest", "0000")
    digest_berekend = hashlib.md5(body.encode("utf-8")).hexdigest()[:4]
    status_header = fields.get("status", "rot")

    return {
        "naam": naam,
        "pad": rel,
        "type": doc_type,
        "titel": titel,
        "digest_header": digest_header,
        "digest_berekend": digest_berekend,
        "status_header": status_header,
    }


def handle_publiceer_grondslagen() -> int:
    """Programmatische handler voor publiceer-grondslagen intent.

    Volledig deterministisch. Geen LLM of inferentie.
    Berekent dual-digest (digest_header uit frontmatter + digest_berekend live)
    en genereert een genormaliseerde JSON-structuur per value stream en fase.
    Output: {canon}/grondslagen/grondslagen.json
    """
    try:
        canon_path = find_canon_path()
    except FileNotFoundError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

    grondslagen_dir = canon_path / "grondslagen"
    schema_path = canon_path / "grondslagen.schema.json"
    output_path = grondslagen_dir / "grondslagen.json"  # inside grondslagen/

    if not grondslagen_dir.exists():
        print(f"[ERROR] grondslagen/ map niet gevonden in {canon_path}", file=sys.stderr)
        return 1
    if not schema_path.exists():
        print(f"[ERROR] grondslagen.schema.json niet gevonden in {canon_path}", file=sys.stderr)
        return 1

    print(f"[INFO] Scannen van {grondslagen_dir} ...")

    algemeen: list = []
    value_streams: dict = {}

    for md_file in sorted(grondslagen_dir.rglob("*.md")):
        rel = md_file.relative_to(grondslagen_dir).as_posix()
        try:
            entry = _make_entry(md_file, grondslagen_dir)
        except Exception as e:
            print(f"  [WARNING] Kan {rel} niet verwerken: {e}")
            continue

        bucket = classify_path(rel)
        label = f"[{entry['status_header']}] {'match' if entry['digest_header'] == entry['digest_berekend'] else 'DRIFT'}"
        print(f"  + {rel}  {bucket[0]}  {entry['type']}  {label}")

        if bucket[0] == "algemeen":
            algemeen.append(entry)
        elif bucket[0] == "vs":
            vs = bucket[1]
            value_streams.setdefault(vs, {"code": vs, "grondslagen": [], "fasen": {}})
            if vs in _VS_NAMEN:
                value_streams[vs]["naam"] = _VS_NAMEN[vs]
            value_streams[vs]["grondslagen"].append(entry)
        elif bucket[0] == "fase":
            vs, fase_code = bucket[1], bucket[2]
            value_streams.setdefault(vs, {"code": vs, "grondslagen": [], "fasen": {}})
            if vs in _VS_NAMEN:
                value_streams[vs]["naam"] = _VS_NAMEN[vs]
            value_streams[vs]["fasen"].setdefault(fase_code, {"code": fase_code, "grondslagen": []})
            value_streams[vs]["fasen"][fase_code]["grondslagen"].append(entry)

    now = datetime.now(timezone.utc)
    publicatie = {
        "versie": "1.0.0",
        "gegenereerd": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "algemeen": algemeen,
        "value_streams": value_streams,
    }

    # Schema-validatie (soft fail)
    try:
        import jsonschema  # type: ignore
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        jsonschema.validate(publicatie, schema)
        print("[INFO] JSON valideert succesvol tegen schema")
    except ImportError:
        print("[WARNING] jsonschema niet geïnstalleerd, schema-validatie overgeslagen")
    except Exception as e:
        print(f"[WARNING] Schema-validatie mislukt: {e}")

    total = len(algemeen) + sum(
        len(vs["grondslagen"]) + sum(len(f["grondslagen"]) for f in vs["fasen"].values())
        for vs in value_streams.values()
    )
    output_path.write_text(json.dumps(publicatie, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[INFO] Geschreven: {output_path} ({total} grondslagen, {len(value_streams)} value streams)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=f"Runner voor agent: {TARGET_AGENT}",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="intent", required=True, help="Beschikbare intents")

    p_adviseer_grondslag_verbeteringen = subparsers.add_parser('adviseer-grondslag-verbeteringen', help='Intent: adviseer-grondslag-verbeteringen')
    p_adviseer_grondslag_verbeteringen.add_argument('--scope', required=True, help='Pad of selectie van grondslag-artefacten waarvoor verbeteradvies wordt gevraagd')
    p_adviseer_grondslag_verbeteringen.add_argument('--focus', required=False, help='Specifiek verbeterdomein om op te richten')

    p_valideer_grondslag_consistentie = subparsers.add_parser('valideer-grondslag-consistentie', help='Intent: valideer-grondslag-consistentie')
    p_valideer_grondslag_consistentie.add_argument('--scope', required=True, help='Pad of selectie van te toetsen grondslag-artefacten binnen de canon')

    p_valideer_terminologische_scherpte = subparsers.add_parser('valideer-terminologische-scherpte', help='Intent: valideer-terminologische-scherpte')
    p_valideer_terminologische_scherpte.add_argument('--scope', required=True, help='Pad of selectie van te toetsen grondslag-artefacten binnen de canon')
    p_valideer_terminologische_scherpte.add_argument('--termenlijst', required=False, help='Expliciete lijst van termen om specifiek te controleren')

    subparsers.add_parser('publiceer-grondslagen', help='Intent: publiceer-grondslagen (programmatisch, geen parameters vereist)')

    args = parser.parse_args()

    if args.intent == "publiceer-grondslagen":
        return handle_publiceer_grondslagen()

    params = {
        key: value
        for key, value in vars(args).items()
        if key != "intent" and value is not None
    }
    return run_intent(args.intent, params)


if __name__ == "__main__":
    sys.exit(main())
