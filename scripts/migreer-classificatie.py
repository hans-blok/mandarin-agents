#!/usr/bin/env python3
"""Eenmalig migratiescript: zet checkbox-classificatie om naar Markdown-tabel.

Werkt op alle *.charter.md en *.agent-boundary.md in artefacten/.
Voegt bronhouding toe aan de YAML frontmatter van boundary-bestanden.

Vereisten: git add . is gedaan vóór uitvoering (restore-punt).
"""
import re
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).parent.parent

AXES = [
    ('Vormingsfase', r'Vormingsfase'),
    ('Betekeniseffect', r'Betekeniseffect'),
    ('Werking', r'Werking'),
    ('Bronhouding', r'Bron-?houding'),
]


def extract_checkbox_value(block_text: str, heading_re: str) -> str | None:
    """Extraheer de [x]-waarde onder een as-heading."""
    in_section = False
    for line in block_text.splitlines():
        stripped = line.strip()
        if re.match(rf'-\s+\*\*{heading_re}', stripped):
            in_section = True
            continue
        if in_section:
            if re.match(r'-\s+\*\*', stripped):
                break
            m = re.match(r'-\s+\[x\]\s+(.+?)(?:\s*\(|$)', stripped, re.IGNORECASE)
            if m:
                return m.group(1).strip()
    return None


def find_classification_block(lines: list[str]) -> tuple[int, int] | None:
    """Geef (start, end) regel-indices van het classificatie-blok."""
    start = None
    for i, line in enumerate(lines):
        if re.match(r'##\s+Mandarin-agent-classificatie', line.strip()):
            start = i
            break
    if start is None:
        return None

    for i in range(start + 2, len(lines)):
        if re.match(r'##\s+', lines[i].strip()) and i > start + 2:
            return start, i

    return start, len(lines)


def build_table_block(values: dict[str, str]) -> str:
    v1 = values.get('Vormingsfase', '?')
    v2 = values.get('Betekeniseffect', '?')
    v3 = values.get('Werking', '?')
    v4 = values.get('Bronhouding', '?')
    table = (
        "## Mandarin-agent-classificatie\n\n"
        "| As               | Waarde            |\n"
        "|------------------|-------------------|\n"
        f"| Vormingsfase     | {v1:<17} |\n"
        f"| Betekeniseffect  | {v2:<17} |\n"
        f"| Werking          | {v3:<17} |\n"
        f"| Bronhouding      | {v4:<17} |\n"
        "\n"
        f"**Validatie**: {v1} \u00d7 {v2} \u00d7 {v3} \u00d7 {v4}"
        " \u2014 coherente combinatie. Positionering volgt `mandarin-ordeningsconcepten.md`.\n"
    )
    return table


def add_bronhouding_to_frontmatter(text: str, value: str) -> str:
    """Voeg bronhouding toe aan YAML frontmatter (als nog niet aanwezig)."""
    if not text.startswith('---'):
        return text

    parts = text.split('---', 2)
    if len(parts) < 3:
        return text

    fm = parts[1]
    body = parts[2]

    if re.search(r'^bronhouding\s*:', fm, re.MULTILINE):
        return text

    insert_line = f'bronhouding: {value}\n'

    if re.search(r'^versie\s*:', fm, re.MULTILINE):
        fm = re.sub(r'^(versie\s*:.+)$', rf'{insert_line}\1', fm, count=1, flags=re.MULTILINE)
    else:
        fm = fm.rstrip('\n') + '\n' + insert_line

    return f'---{fm}---{body}'


def migrate_file(path: Path, is_boundary: bool) -> bool:
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines(keepends=True)

    result = find_classification_block(lines)
    if result is None:
        print(f'  SKIP (geen classificatie-blok): {path.name}')
        return False

    start, end = result
    block_text = ''.join(lines[start:end])

    if '| Bronhouding' in block_text or '| bronhouding' in block_text.lower():
        print(f'  SKIP (al tabelformaat): {path.name}')
        return False

    values: dict[str, str] = {}
    for label, heading_re in AXES:
        val = extract_checkbox_value(block_text, heading_re)
        if val:
            values[label] = val
        else:
            print(f'  WAARSCHUWING: geen [x] gevonden voor {label} in {path.name}')
            values[label] = '?'

    table = build_table_block(values)
    table_lines = table.splitlines(keepends=True)
    if table_lines and not table_lines[-1].endswith('\n'):
        table_lines[-1] += '\n'
    table_lines.append('\n')

    new_lines = lines[:start] + table_lines + lines[end:]
    new_text = ''.join(new_lines)

    if is_boundary and values.get('Bronhouding') and values['Bronhouding'] != '?':
        new_text = add_bronhouding_to_frontmatter(new_text, values['Bronhouding'])

    path.write_text(new_text, encoding='utf-8')
    print(f'  OK: {path.relative_to(WORKSPACE_ROOT)}')
    return True


def main() -> int:
    artefacten = WORKSPACE_ROOT / 'artefacten'
    if not artefacten.exists():
        print(f'ERROR: artefacten-folder niet gevonden: {artefacten}')
        return 1

    changed = 0
    skipped = 0
    warned = 0

    print('=== Charters ===')
    for path in sorted(artefacten.rglob('*.charter.md')):
        ok = migrate_file(path, is_boundary=False)
        if ok:
            changed += 1
        else:
            skipped += 1

    print()
    print('=== Boundaries ===')
    for path in sorted(artefacten.rglob('*.agent-boundary.md')):
        ok = migrate_file(path, is_boundary=True)
        if ok:
            changed += 1
        else:
            skipped += 1

    print()
    print(f'Klaar. Gewijzigd: {changed}, overgeslagen: {skipped}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
