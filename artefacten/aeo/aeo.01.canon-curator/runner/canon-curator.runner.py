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
import json
import os
import re
import subprocess
import sys
from datetime import datetime


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


def infer_scope(rel_path: str) -> str:
    """Leid scope af uit het relatieve pad t.o.v. grondslagen/.

    .algemeen/... -> "algemeen"
    aeo/...       -> "aeo"
    aeo/aeo.03.*/ -> "aeo.03"
    """
    parts = rel_path.replace("\\", "/").split("/")
    if not parts:
        return "algemeen"
    first = parts[0]
    if first == ".algemeen":
        return "algemeen"
    vs = first
    if len(parts) >= 2:
        subfolder = parts[1]
        subparts = subfolder.split(".", 2)
        if len(subparts) >= 2 and subparts[0] == vs:
            return f"{vs}.{subparts[1]}"
    return vs


def infer_type(filename: str) -> str:
    """Leid type af uit bestandsnaam."""
    name = filename.lower()
    if "doctrine" in name:
        return "doctrine"
    if "constitutie" in name:
        return "constitutie"
    if "beleid" in name:
        return "beleid"
    if "normering" in name or "checklist" in name:
        return "normering"
    if "kaderdefinitie" in name:
        return "kaderdefinitie"
    return "concept"


def handle_publiceer_grondslagen() -> int:
    """Programmatische handler voor publiceer-grondslagen intent."""
    try:
        canon_path = find_canon_path()
    except FileNotFoundError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

    grondslagen_dir = canon_path / "grondslagen"
    schema_path = canon_path / "grondslagen.schema.json"
    output_path = canon_path / "grondslagen.json"

    if not grondslagen_dir.exists():
        print(f"[ERROR] grondslagen/ map niet gevonden in {canon_path}", file=sys.stderr)
        return 1
    if not schema_path.exists():
        print(f"[ERROR] grondslagen.schema.json niet gevonden in {canon_path}", file=sys.stderr)
        return 1

    print(f"[INFO] Scannen van {grondslagen_dir} ...")
    entries = []
    for md_file in sorted(grondslagen_dir.rglob("*.md")):
        rel_to_canon = md_file.relative_to(canon_path).as_posix()
        rel_to_grondslagen = md_file.relative_to(grondslagen_dir).as_posix()
        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception as e:
            print(f"  [WARNING] Kan {rel_to_canon} niet lezen: {e}")
            continue
        fields, body = parse_frontmatter(content)
        title = extract_title(body) or md_file.stem.replace("-", " ").title()
        scope = infer_scope(rel_to_grondslagen)
        doc_type = infer_type(md_file.name)
        entry: dict = {
            "bron": rel_to_canon,
            "scope": scope,
            "type": doc_type,
            "titel": title,
            "versie": fields.get("versie", ""),
            "digest": fields.get("digest", ""),
            "status": fields.get("status", ""),
        }
        entries.append(entry)
        print(f"  + {rel_to_canon} [{scope}] [{doc_type}]")

    now = datetime.now()
    publicatie = {
        "metadata": {
            "publicatie_timestamp": now.isoformat(),
            "publicatie_datum": now.strftime("%Y-%m-%d"),
            "versie": "1.0",
            "aantal_grondslagen": len(entries),
            "generator": "canon-curator.runner.py",
            "canon_pad": str(canon_path),
        },
        "grondslagen": entries,
    }

    try:
        import jsonschema  # type: ignore
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        jsonschema.validate(publicatie, schema)
        print("[INFO] JSON valideert succesvol tegen schema")
    except ImportError:
        print("[WARNING] jsonschema niet geïnstalleerd, schema-validatie overgeslagen")
    except Exception as e:
        print(f"[WARNING] Schema-validatie mislukt: {e}")

    output_path.write_text(json.dumps(publicatie, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[INFO] Geschreven: {output_path} ({len(entries)} grondslagen)")
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
