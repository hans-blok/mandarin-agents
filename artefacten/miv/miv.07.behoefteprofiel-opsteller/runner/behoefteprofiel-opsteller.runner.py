#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Iterable


WORKSPACE_ROOT = Path.cwd()
OUTPUT_DIR = WORKSPACE_ROOT / "artefacten" / "miv" / "miv.07.behoefteprofiel-opsteller" / "output"
AUDIT_DIR = WORKSPACE_ROOT / "audit"


def slugify(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", normalized.lower()).strip("-")
    return slug or "output"


def split_source_paths(raw_value: str) -> list[Path]:
    candidate = Path(raw_value.strip())
    if candidate.exists():
        return [candidate]

    parts = [part.strip() for part in re.split(r"[;\n]+", raw_value) if part.strip()]
    if len(parts) == 1 and "," in parts[0]:
        comma_parts = [part.strip() for part in parts[0].split(",") if part.strip()]
        if len(comma_parts) > 1:
            parts = comma_parts

    return [Path(part) for part in parts]


def read_text_file(path: Path) -> str:
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Bestand niet gevonden: {path}")
    return path.read_text(encoding="utf-8")


def extract_functional_requirements(content: str) -> list[tuple[str, str]]:
    requirements: list[tuple[str, str]] = []
    for line in content.splitlines():
        match = re.match(r"^\|\s*(F-\d+)\s*\|\s*(.*?)\s*\|$", line.strip())
        if match:
            requirements.append((match.group(1), match.group(2)))
    return requirements


def extract_nonfunctional_sections(content: str) -> list[tuple[str, list[str]]]:
    sections: list[tuple[str, list[str]]] = []
    current_title: str | None = None
    current_items: list[str] = []

    for line in content.splitlines():
        heading = re.match(r"^###\s+(.+)$", line.strip())
        bullet = re.match(r"^-\s+(N-\d+:\s+.+)$", line.strip())

        if heading:
            if current_title:
                sections.append((current_title, current_items))
            current_title = heading.group(1).strip()
            current_items = []
            continue

        if bullet and current_title:
            current_items.append(bullet.group(1).strip())

    if current_title:
        sections.append((current_title, current_items))

    return sections


def infer_system_name(operationele_context: str, source_paths: Iterable[Path]) -> str:
    upper_tokens = re.findall(r"\b[A-Z]{2,}\b", operationele_context)
    if upper_tokens:
        return upper_tokens[0]

    for source_path in source_paths:
        stem = source_path.stem
        if stem.lower() not in {"fennf", "requirements", "hosting"}:
            return stem.upper()

    return "DOELSYSTEEM"


def infer_profile_slug(system_name: str, operationele_context: str) -> str:
    if "hosting" in operationele_context.lower():
        return slugify(f"{system_name} hosting")
    return slugify(system_name)


def write_output(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_audit_log(agent_name: str, gelezen: list[str], aangemaakt: list[str]) -> None:
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    log_path = AUDIT_DIR / f"{agent_name}-{timestamp}.log.md"
    lines = [
        f"# Handmatige start log — {agent_name}\n\n",
        f"**Datum/tijd**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n",
        "## Bestanden gelezen\n",
    ]
    if gelezen:
        lines.extend(f"- {item}\n" for item in gelezen)
    else:
        lines.append("(geen)\n")
    lines.extend(["\n## Bestanden aangemaakt\n"])
    if aangemaakt:
        lines.extend(f"- {item}\n" for item in aangemaakt)
    else:
        lines.append("(geen)\n")
    log_path.write_text("".join(lines), encoding="utf-8")


def formuleer_behoefteprofiel(args: argparse.Namespace) -> int:
    source_paths = split_source_paths(args.bronbestanden)
    if not source_paths:
        raise ValueError("Geen bronbestanden opgegeven")
    if len(args.operationele_context.strip()) < 50:
        raise ValueError("operationele_context is te kort")
    if len(args.selectiedoel.strip()) < 20:
        raise ValueError("selectiedoel is te kort")

    contents = [(path, read_text_file(path)) for path in source_paths]
    functional = extract_functional_requirements(contents[0][1])
    nonfunctional = extract_nonfunctional_sections(contents[0][1])

    if not functional and not nonfunctional:
        raise ValueError("Bronbestand bevat geen bruikbare behoefte-inhoud")

    system_name = infer_system_name(args.operationele_context, source_paths)
    profile_slug = slugify(args.output_naam) if getattr(args, "output_naam", "") else infer_profile_slug(system_name, args.operationele_context)
    title = f"{system_name} hosting en technisch applicatiebeheer"

    assumptions: list[str] = []
    if re.search(r"\b30 gebruikers\b", args.operationele_context, re.IGNORECASE) and re.search(r"20 gelijktijdige gebruikers", contents[0][1], re.IGNORECASE):
        assumptions.append("De operationele context met 30 gebruikers is leidend voor de huidige behoeftebepaling en scherpt de eerdere referentie van 20 gelijktijdige gebruikers aan.")
    if re.search(r"BaseTide", args.selectiedoel, re.IGNORECASE):
        assumptions.append("Het selectiedoel noemt BaseTide als latere beoordelingscontext, maar dit document bevat geen leveranciersoordeel.")

    functional_lines = "\n".join(f"- **{ref}**: {description}" for ref, description in functional)
    nonfunctional_chunks: list[str] = []
    for section_title, items in nonfunctional:
        if not items:
            continue
        nonfunctional_chunks.append(f"### {section_title}\n")
        nonfunctional_chunks.extend(f"- {item}" for item in items)
        nonfunctional_chunks.append("")
    nonfunctional_text = "\n".join(nonfunctional_chunks).strip()

    source_list = "\n".join(f"- `{path.as_posix()}`" for path in source_paths)
    assumptions_text = "\n".join(f"- {item}" for item in assumptions) if assumptions else "- Geen aanvullende aannames buiten bron en context."

    content = f"""# Behoefteprofiel: {title}

## 1. Doel en scope

Dit behoefteprofiel legt de functionele en niet-functionele behoeften vast voor hosting en technisch applicatiebeheer van {system_name}.

Het profiel dient als objectieve basis voor latere leveranciersselectie. Het selectiedoel in deze opdracht is: {args.selectiedoel.strip()}

## 2. Context

{args.operationele_context.strip()}

De leverancier moet hosting en technisch applicatiebeheer als samenhangende dienst kunnen uitvoeren, met nadruk op operationele continuiteit en snelle ondersteuning bij toegangsproblemen.

## 3. Functionele behoeften

{functional_lines}

## 4. Niet-functionele eisen

{nonfunctional_text}

## 5. Randvoorwaarden

- Ondersteuning is minimaal nodig tijdens kantooruren.
- Chauffeurs die geen toegang hebben, moeten snel worden geholpen.
- Private GitLab en technisch applicatiebeheer vallen binnen de gevraagde dienstverlening.
- Het profiel is bedoeld voor leveranciersvergelijking en niet voor contractuele eindredactie.

## 6. Afbakening

- Geen leveranciersbeoordeling, rangorde of keuze.
- Geen contractonderhandeling of prijsbeoordeling.
- Geen implementatie- of migratieplan.
- Geen operationele inrichting buiten de vastgelegde behoeften.

## 7. Herkomstverantwoording

### Gebruikte bronnen

{source_list}

### Operationele context

- {args.operationele_context.strip()}

### Expliciete aannames

{assumptions_text}
"""

    output_path = OUTPUT_DIR / f"behoefteprofiel-{profile_slug}.md"
    write_output(output_path, content)
    write_audit_log("behoefteprofiel-opsteller", [str(path) for path in source_paths], [str(output_path)])
    print(f"[OK] Behoefteprofiel geschreven: {output_path}")
    return 0


def structureer_eisenpakket(args: argparse.Namespace) -> int:
    source_path = Path(args.behoefteprofiel_bron)
    source_content = read_text_file(source_path)
    if len(args.ordeningskader.strip()) < 30:
        raise ValueError("ordeningskader is te kort")
    if len(args.prioriteringsgrondslag.strip()) < 20:
        raise ValueError("prioriteringsgrondslag is te kort")

    hard_requirements = re.findall(r"^- \*\*(F-\d+)\*\*: (.+)$", source_content, re.MULTILINE)
    nonfunctional = re.findall(r"^- (N-\d+: .+)$", source_content, re.MULTILINE)
    output_slug = slugify(args.output_naam) if args.output_naam else slugify(source_path.stem.replace("behoefteprofiel-", ""))

    hard_text = "\n".join(f"- **{ref}**: {desc}" for ref, desc in hard_requirements) or "- Geen expliciete harde eisen afleidbaar uit bronbestand."
    wishes_text = "\n".join(f"- {item}" for item in nonfunctional[:8]) or "- Geen wensen expliciet afleidbaar uit bronbestand."
    constraints: list[str] = [
        "- Leverancier moet aantoonbaar hosting en technisch applicatiebeheer gecombineerd kunnen leveren.",
        "- Structuur moet vergelijking van aanbiedingen ondersteunen zonder al scoring toe te passen.",
    ]
    if args.aanvullende_toelichting.strip():
        constraints.append(f"- Aanvullende toelichting: {args.aanvullende_toelichting.strip()}")

    content = f"""# Eisenpakket: {output_slug.replace('-', ' ').title()}

## 1. Scope en bron

- Bronbestand: `{source_path.as_posix()}`
- Ordeningskader: {args.ordeningskader.strip()}
- Prioriteringsgrondslag: {args.prioriteringsgrondslag.strip()}

## 2. Harde eisen

{hard_text}

## 3. Wensen

{wishes_text}

## 4. Randvoorwaarden

{"\n".join(constraints)}

## 5. Prioritering

- Harde eisen zijn eisen die direct bepalen of een leverancier in scope blijft.
- Wensen vergroten geschiktheid maar zijn niet per definitie uitsluitingsgrond.
- Randvoorwaarden bepalen bestuurlijke, operationele en vergelijkingscontext.

## 6. Toelichting voor latere vergelijking

Dit eisenpakket structureert behoeften zodanig dat latere leveranciersvergelijking mogelijk wordt, zonder scoremodel, ranking of gunningsadvies toe te voegen.

## 7. Herkomstverantwoording

- Gebaseerd op: `{source_path.as_posix()}`
- Aanvullende toelichting: {args.aanvullende_toelichting.strip() or 'geen'}
"""

    output_path = OUTPUT_DIR / f"eisenpakket-{output_slug}.md"
    write_output(output_path, content)
    write_audit_log("behoefteprofiel-opsteller", [str(source_path)], [str(output_path)])
    print(f"[OK] Eisenpakket geschreven: {output_path}")
    return 0


def beschrijf_selectiecriteria(args: argparse.Namespace) -> int:
    source_path = Path(args.eisenpakket_bron)
    source_content = read_text_file(source_path)
    if len(args.selectiecontext.strip()) < 30:
        raise ValueError("selectiecontext is te kort")

    hard_requirements = re.findall(r"^- \*\*(F-\d+)\*\*: (.+)$", source_content, re.MULTILINE)
    nonfunctional = re.findall(r"^- (N-\d+: .+)$", source_content, re.MULTILINE)
    output_slug = slugify(args.output_naam) if args.output_naam else slugify(source_path.stem.replace("eisenpakket-", "").replace("behoefteprofiel-", ""))

    hard_text = "\n".join(f"- **{ref}**: {desc}" for ref, desc in hard_requirements[:6]) or "- Geen harde criteria expliciet afleidbaar uit bronbestand."
    other_text = "\n".join(f"- {item}" for item in nonfunctional[:10]) or "- Geen overige criteria expliciet afleidbaar uit bronbestand."

    content = f"""# Selectiecriteria: {output_slug.replace('-', ' ').title()}

## 1. Scope en bron

- Bronbestand: `{source_path.as_posix()}`
- Selectiecontext: {args.selectiecontext.strip()}

## 2. Harde criteria

{hard_text}

## 3. Overige selectiecriteria

{other_text}

## 4. Relatie met eisenpakket

De criteria zijn rechtstreeks afgeleid uit functionele behoeften, niet-functionele eisen en randvoorwaarden in het bronartefact.

## 5. Afbakening

- Geen leveranciersscore of ranking.
- Geen gunningsadvies.
- Geen prijsweging als beslismodel.
- Geen contractuele keuze.

## 6. Herkomstverantwoording

- Gebaseerd op: `{source_path.as_posix()}`
- Toelichting op prioriteit: {args.toelichting_op_prioriteit.strip() or 'geen aanvullende toelichting'}
"""

    output_path = OUTPUT_DIR / f"selectiecriteria-{output_slug}.md"
    write_output(output_path, content)
    write_audit_log("behoefteprofiel-opsteller", [str(source_path)], [str(output_path)])
    print(f"[OK] Selectiecriteria geschreven: {output_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Runner voor behoefteprofiel-opsteller")
    subparsers = parser.add_subparsers(dest="intent", required=True)

    formuleer = subparsers.add_parser("formuleer-behoefteprofiel")
    formuleer.add_argument("--bronbestanden", required=True)
    formuleer.add_argument("--operationele-context", required=True)
    formuleer.add_argument("--selectiedoel", required=True)
    formuleer.add_argument("--output-naam", default="")
    formuleer.set_defaults(func=formuleer_behoefteprofiel)

    structureer = subparsers.add_parser("structureer-eisenpakket")
    structureer.add_argument("--behoefteprofiel-bron", required=True)
    structureer.add_argument("--ordeningskader", required=True)
    structureer.add_argument("--prioriteringsgrondslag", required=True)
    structureer.add_argument("--aanvullende-toelichting", default="")
    structureer.add_argument("--output-naam", default="")
    structureer.set_defaults(func=structureer_eisenpakket)

    beschrijf = subparsers.add_parser("beschrijf-selectiecriteria")
    beschrijf.add_argument("--eisenpakket-bron", required=True)
    beschrijf.add_argument("--selectiecontext", required=True)
    beschrijf.add_argument("--output-naam", default="")
    beschrijf.add_argument("--toelichting-op-prioriteit", default="")
    beschrijf.set_defaults(func=beschrijf_selectiecriteria)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())