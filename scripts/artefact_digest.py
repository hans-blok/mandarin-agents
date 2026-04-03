#!/usr/bin/env python3
"""
Artefact Digest Tool — Bereken en verifieer content digests voor Mandarin artefacten.

Beheert `digest` (4-karakter MD5 content hash) en `status` (vers/muf/rot) velden
in de YAML frontmatter van boundaries, charters, contracten en templates.

Subcommands:
  init    — Bereken digest voor alle artefacten, voeg toe aan frontmatter
  verify  — Herbereken en vergelijk met opgeslagen digest, rapporteer afwijkingen
  update  — Herbereken digest en schrijf bij (of markeer handmatig als muf/rot)

Conform: doctrine-traceability-digest (concept v0.1.0)
"""
import argparse
import hashlib
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ==============================================================================
# CONSTANTEN
# ==============================================================================

ARTEFACT_GLOBS = {
    "boundary":  "**/*.agent-boundary.md",
    "charter":   "**/*.charter.md",
    "contract":  "**/agent-contracten/*.agent.md",
    "template":  "**/templates/*.template.md",
}

# Minimale frontmatter per type voor bestanden die nog geen frontmatter hebben
MINIMAL_FRONTMATTER = {
    "charter": ["agent", "versie"],
    "contract": ["agent", "intent", "versie"],
    "template": ["agent", "versie"],
    "boundary": ["agent", "versie"],
}


# ==============================================================================
# CORE FUNCTIES
# ==============================================================================

def get_artefacten_root() -> Path:
    """Bepaal de artefacten root (workspace/artefacten)."""
    # Zoek vanuit script locatie naar workspace root
    script_dir = Path(__file__).resolve().parent
    workspace = script_dir.parent  # scripts/ -> workspace root
    artefacten = workspace / "artefacten"
    if artefacten.exists():
        return artefacten
    # Fallback: cwd
    cwd_artefacten = Path.cwd() / "artefacten"
    if cwd_artefacten.exists():
        return cwd_artefacten
    print("ERROR: artefacten/ folder niet gevonden.")
    sys.exit(1)


def split_frontmatter(content: str) -> Tuple[Optional[str], str]:
    """Splits bestandsinhoud in frontmatter en body.

    Returns:
        (frontmatter_text, body) — frontmatter_text is None als er geen frontmatter is.
        frontmatter_text bevat NIET de --- delimiters.
    """
    if not content.startswith("---"):
        return None, content

    # Zoek het afsluitende ---
    end_match = re.search(r"\n---\s*\n", content[3:])
    if not end_match:
        return None, content

    end_pos = 3 + end_match.end()
    fm_text = content[3:3 + end_match.start()].strip()
    body = content[end_pos:]
    return fm_text, body


def compute_digest(body: str) -> str:
    """Bereken 4-karakter MD5 digest van de body content."""
    return hashlib.md5(body.encode("utf-8")).hexdigest()[:4]


def parse_frontmatter_fields(fm_text: str) -> Dict[str, str]:
    """Parse YAML frontmatter naar een simpele key-value dict.
    Ondersteunt alleen scalaire waarden (geen nested YAML).
    """
    fields = {}
    for line in fm_text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = re.match(r"^([a-zA-Z_][a-zA-Z0-9_-]*)\s*:\s*(.*)", line)
        if match:
            key = match.group(1)
            value = match.group(2).strip()
            # Strip quotes
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            fields[key] = value
    return fields


def set_frontmatter_field(fm_text: str, key: str, value: str) -> str:
    """Stel een veld in de frontmatter in (update of voeg toe)."""
    lines = fm_text.split("\n")
    updated = False
    for i, line in enumerate(lines):
        if re.match(rf"^{re.escape(key)}\s*:", line):
            lines[i] = f"{key}: {value}"
            updated = True
            break
    if not updated:
        lines.append(f"{key}: {value}")
    return "\n".join(lines)


def reconstruct_file(fm_text: str, body: str) -> str:
    """Reconstrueer bestandsinhoud uit frontmatter en body."""
    return f"---\n{fm_text}\n---\n{body}"


def infer_artefact_type(file_path: Path) -> Optional[str]:
    """Bepaal het artefacttype op basis van bestandsnaam."""
    name = file_path.name
    if name.endswith(".agent-boundary.md"):
        return "boundary"
    elif name.endswith(".charter.md"):
        return "charter"
    elif name.endswith(".agent.md") and "agent-contracten" in str(file_path):
        return "contract"
    elif name.endswith(".template.md") and "templates" in str(file_path):
        return "template"
    return None


def infer_agent_name(file_path: Path) -> str:
    """Leid agent naam af uit bestandspad."""
    # Zoek in het pad naar een folder met patroon {vs}.{fase}.{agent}
    for part in file_path.parts:
        match = re.match(r"^[a-z]+\.\d+\.(.+)$", part)
        if match:
            return match.group(1)
    # Fallback: eerste deel van bestandsnaam
    return file_path.stem.split(".")[0]


def infer_intent_name(file_path: Path) -> Optional[str]:
    """Leid intent naam af uit contractbestandsnaam."""
    name = file_path.stem  # bijv. agent-curator.valideer-agent-consistentie.agent
    parts = name.split(".")
    if len(parts) >= 2:
        # Verwijder agent naam (eerste deel) en .agent (laatste deel)
        return parts[1] if parts[1] != "agent" else None
    return None


def ensure_frontmatter(file_path: Path, artefact_type: str) -> Tuple[str, str, bool]:
    """Zorg dat een bestand frontmatter heeft. Voeg minimale frontmatter toe indien nodig.

    Returns:
        (fm_text, body, was_created) — was_created is True als frontmatter nieuw is aangemaakt.
    """
    content = file_path.read_text(encoding="utf-8")
    fm_text, body = split_frontmatter(content)

    if fm_text is not None:
        return fm_text, body, False

    # Maak minimale frontmatter aan
    agent_name = infer_agent_name(file_path)
    fields = [f"agent: {agent_name}", "versie: 0.1.0"]

    if artefact_type == "contract":
        intent = infer_intent_name(file_path)
        if intent:
            fields.insert(1, f"intent: {intent}")

    fm_text = "\n".join(fields)
    return fm_text, content, True  # body is de volledige originele content


# ==============================================================================
# DISCOVER
# ==============================================================================

def discover_artefacts(artefacten_root: Path) -> List[Tuple[Path, str]]:
    """Vind alle artefacten in scope.

    Returns:
        Lijst van (file_path, artefact_type) tuples.
    """
    results = []
    for artefact_type, glob_pattern in ARTEFACT_GLOBS.items():
        for file_path in sorted(artefacten_root.rglob(glob_pattern.replace("**/", ""))):
            # Dubbelcheck type via bestandsnaam (rglob kan false positives geven)
            confirmed_type = infer_artefact_type(file_path)
            if confirmed_type == artefact_type:
                results.append((file_path, artefact_type))
    return results


# ==============================================================================
# SUBCOMMANDS
# ==============================================================================

def cmd_init(artefacten_root: Path, dry_run: bool = False) -> int:
    """Initialiseer digest en status voor alle artefacten."""
    artefacts = discover_artefacts(artefacten_root)

    print("=" * 70)
    print(f"ARTEFACT DIGEST — INIT")
    print(f"Scope: {artefacten_root}")
    print(f"Gevonden: {len(artefacts)} artefacten")
    if dry_run:
        print("[DRY-RUN]")
    print("=" * 70)
    print()

    counts = {"boundary": 0, "charter": 0, "contract": 0, "template": 0}
    fm_created = 0
    errors = 0

    for file_path, artefact_type in artefacts:
        try:
            rel_path = file_path.relative_to(artefacten_root)
        except ValueError:
            rel_path = file_path.name

        try:
            fm_text, body, was_created = ensure_frontmatter(file_path, artefact_type)
            digest = compute_digest(body)

            fm_text = set_frontmatter_field(fm_text, "digest", digest)
            fm_text = set_frontmatter_field(fm_text, "status", "vers")

            if was_created:
                fm_created += 1
                tag = "[+FM]"
            else:
                tag = "[UPD]"

            print(f"  {tag} {rel_path}  digest={digest}")

            if not dry_run:
                new_content = reconstruct_file(fm_text, body)
                file_path.write_text(new_content, encoding="utf-8")

            counts[artefact_type] += 1

        except Exception as e:
            print(f"  [ERR] {rel_path}: {e}")
            errors += 1

    print()
    print("-" * 70)
    print(f"Resultaat:")
    for atype, count in counts.items():
        print(f"  {atype:12s}: {count} bestanden")
    print(f"  {'TOTAAL':12s}: {sum(counts.values())} bestanden")
    if fm_created > 0:
        print(f"  Frontmatter aangemaakt: {fm_created} bestanden")
    if errors > 0:
        print(f"  Fouten: {errors}")
    print("-" * 70)

    return 1 if errors > 0 else 0


def cmd_verify(artefacten_root: Path, verbose: bool = False) -> int:
    """Verifieer digests voor alle artefacten."""
    artefacts = discover_artefacts(artefacten_root)

    print("=" * 70)
    print(f"ARTEFACT DIGEST — VERIFY")
    print(f"Scope: {artefacten_root}")
    print(f"Gevonden: {len(artefacts)} artefacten")
    print("=" * 70)
    print()

    vers_count = 0
    mismatch_count = 0
    no_digest_count = 0
    no_fm_count = 0
    errors = 0

    mismatches = []

    for file_path, artefact_type in artefacts:
        try:
            rel_path = file_path.relative_to(artefacten_root)
        except ValueError:
            rel_path = file_path.name

        try:
            content = file_path.read_text(encoding="utf-8")
            fm_text, body = split_frontmatter(content)

            if fm_text is None:
                no_fm_count += 1
                print(f"  [GEEN FM] {rel_path}")
                continue

            fields = parse_frontmatter_fields(fm_text)
            stored_digest = fields.get("digest")

            if not stored_digest:
                no_digest_count += 1
                print(f"  [GEEN DIGEST] {rel_path}")
                continue

            actual_digest = compute_digest(body)
            status = fields.get("status", "?")

            if stored_digest == actual_digest:
                vers_count += 1
                if verbose:
                    print(f"  [VERS]  {rel_path}  digest={actual_digest}  status={status}")
            else:
                mismatch_count += 1
                mismatches.append((rel_path, artefact_type, stored_digest, actual_digest, status))
                print(f"  [MISMATCH] {rel_path}  opgeslagen={stored_digest}  actueel={actual_digest}  status={status}")

        except Exception as e:
            print(f"  [ERR] {rel_path}: {e}")
            errors += 1

    print()
    print("-" * 70)
    print(f"Resultaat:")
    print(f"  Vers:          {vers_count}")
    print(f"  Mismatch:      {mismatch_count}")
    print(f"  Geen digest:   {no_digest_count}")
    print(f"  Geen FM:       {no_fm_count}")
    print(f"  Fouten:        {errors}")
    print(f"  Totaal:        {len(artefacts)}")
    print("-" * 70)

    if mismatches:
        print()
        print("Mismatches die aandacht vereisen:")
        for rel_path, atype, stored, actual, status in mismatches:
            print(f"  [{atype:10s}] {rel_path}")
            print(f"             opgeslagen={stored} → actueel={actual}  status={status}")

    return 1 if mismatch_count > 0 or errors > 0 else 0


def cmd_update(artefacten_root: Path, file_filter: Optional[str] = None,
               force_status: Optional[str] = None, dry_run: bool = False) -> int:
    """Update digest en/of status voor artefacten.

    Args:
        file_filter: Optioneel pad-filter (substring match)
        force_status: Als gezet, markeer met deze status zonder digest te herberekenen
    """
    artefacts = discover_artefacts(artefacten_root)

    if file_filter:
        normalized = file_filter.replace("\\", "/")
        artefacts = [(p, t) for p, t in artefacts if normalized in str(p).replace("\\", "/")]

    print("=" * 70)
    print(f"ARTEFACT DIGEST — UPDATE")
    if file_filter:
        print(f"Filter: {file_filter}")
    if force_status:
        print(f"Status forceren: {force_status}")
    if dry_run:
        print("[DRY-RUN]")
    print(f"Bestanden: {len(artefacts)}")
    print("=" * 70)
    print()

    updated = 0
    errors = 0

    for file_path, artefact_type in artefacts:
        try:
            rel_path = file_path.relative_to(artefacten_root)
        except ValueError:
            rel_path = file_path.name

        try:
            content = file_path.read_text(encoding="utf-8")
            fm_text, body = split_frontmatter(content)

            if fm_text is None:
                fm_text, body, _ = ensure_frontmatter(file_path, artefact_type)

            if force_status:
                # Alleen status wijzigen, geen digest herberekening
                fm_text = set_frontmatter_field(fm_text, "status", force_status)
                print(f"  [STATUS] {rel_path}  status={force_status}")
            else:
                # Herbereken digest en zet status vers
                digest = compute_digest(body)
                fm_text = set_frontmatter_field(fm_text, "digest", digest)
                fm_text = set_frontmatter_field(fm_text, "status", "vers")
                print(f"  [UPD] {rel_path}  digest={digest}")

            if not dry_run:
                new_content = reconstruct_file(fm_text, body)
                file_path.write_text(new_content, encoding="utf-8")

            updated += 1

        except Exception as e:
            print(f"  [ERR] {rel_path}: {e}")
            errors += 1

    print()
    print(f"Bijgewerkt: {updated} bestanden")
    if errors > 0:
        print(f"Fouten: {errors}")

    return 1 if errors > 0 else 0


# ==============================================================================
# CLI
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Artefact Digest Tool — Bereken en verifieer content digests",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--root", type=str, default=None,
        help="Pad naar artefacten/ folder (default: auto-detect)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # init
    p_init = subparsers.add_parser("init", help="Initialiseer digest en status voor alle artefacten")
    p_init.add_argument("--dry-run", action="store_true", help="Toon wat gedaan zou worden")

    # verify
    p_verify = subparsers.add_parser("verify", help="Verifieer digests, rapporteer afwijkingen")
    p_verify.add_argument("--verbose", "-v", action="store_true", help="Toon ook vers-bestanden")

    # update
    p_update = subparsers.add_parser("update", help="Herbereken digest of wijzig status")
    p_update.add_argument("--file", type=str, default=None, help="Filter op bestandspad (substring)")
    p_update.add_argument("--status", type=str, choices=["vers", "muf", "rot"],
                          help="Forceer status zonder digest herberekening")
    p_update.add_argument("--dry-run", action="store_true", help="Toon wat gedaan zou worden")

    args = parser.parse_args()

    if args.root:
        artefacten_root = Path(args.root)
    else:
        artefacten_root = get_artefacten_root()

    if not artefacten_root.exists():
        print(f"ERROR: {artefacten_root} bestaat niet.")
        return 1

    if args.command == "init":
        return cmd_init(artefacten_root, dry_run=args.dry_run)
    elif args.command == "verify":
        return cmd_verify(artefacten_root, verbose=args.verbose)
    elif args.command == "update":
        return cmd_update(artefacten_root, file_filter=args.file,
                          force_status=args.status, dry_run=args.dry_run)

    return 0


if __name__ == "__main__":
    sys.exit(main())
