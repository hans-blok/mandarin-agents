#!/usr/bin/env python3

"""
Publicatie Steward Runner

Deze runner beheert mkdocs.yml en publicatiestructuur voor consistente content-ontsluiting.
De runner ondersteunt 4 intents:
1. schrijf-publicatiestructuur: Genereer nieuwe mkdocs.yml uit workspace-content
2. valideer-publicatiestructuur: Valideer bestaande mkdocs.yml op correctheid
3. actualiseer-mkdocs-configuratie: Update bestaande mkdocs.yml met nieuwe content
4. rapporteer-publicatiestatus: Genereer overzicht van gepubliceerde vs niet-gepubliceerde content

Usage:
    python scripts/runners/publicatie-steward.py

Input:
    - input/input.md (verplicht): Bevat intent en parameters in YAML frontmatter

Output locaties:
    - mkdocs.yml (root): Gegenereerde of geactualiseerde mkdocs configuratie
    - artefacten/publicatie-steward/publicatiestructuur-rapport-<datum>.md
    - artefacten/publicatie-steward/validatie-rapport-<datum>.md
    - artefacten/publicatie-steward/actualisatie-rapport-<datum>.md
    - artefacten/publicatie-steward/publicatiestatus-rapport-<datum>.md

Traceability:
    Charter: artefacten/fnd/fnd.02.publicatie-steward/publicatie-steward.charter.md
    Contracts: artefacten/fnd/fnd.02.publicatie-steward/publicatie-steward.<intent>.agent.md
    Prompts: artefacten/fnd/fnd.02.publicatie-steward/mandarin.publicatie-steward.<intent>.prompt.md
"""

import argparse
import re
import subprocess
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


def log_agent_action(agent_naam: str, gelezen: Optional[List[str]] = None, 
                     aangepast: Optional[List[str]] = None, 
                     aangemaakt: Optional[List[str]] = None) -> None:
    """Log agent actions conform Norm 10.4 via mandarin_agent_runner.
    
    Args:
        agent_naam: Naam van de agent (publicatie-steward)
        gelezen: Lijst van gelezen bestandspaden
        aangepast: Lijst van aangepaste bestandspaden
        aangemaakt: Lijst van aangemaakte bestandspaden
    """
    cmd = [
        "python", "scripts/runners/mandarin_agent_runner.py", agent_naam,
        "--gelezen", *(gelezen or []),
        "--aangepast", *(aangepast or []),
        "--aangemaakt", *(aangemaakt or [])
    ]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[WARN] Logging failed: {e}", file=sys.stderr)


def read_input_file(input_path: Path) -> Dict:
    """Leest input/input.md en extraheert YAML frontmatter.
    
    Args:
        input_path: Pad naar input.md bestand
        
    Returns:
        Dictionary met parsed YAML frontmatter
        
    Raises:
        FileNotFoundError: Als input.md niet bestaat
        ValueError: Als YAML frontmatter niet gevonden of invalid
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input file niet gevonden: {input_path}")
    
    content = input_path.read_text(encoding="utf-8")
    
    # Extract YAML frontmatter (between --- ... ---)
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
    
    if not match:
        raise ValueError("Geen YAML frontmatter gevonden in input.md")
    
    yaml_content = match.group(1)
    
    try:
        data = yaml.safe_load(yaml_content)
        if not isinstance(data, dict):
            raise ValueError("YAML frontmatter is geen valid dictionary")
        return data
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in frontmatter: {e}")


def scan_workspace_content(workspace_root: Path, 
                          include_folders: List[str],
                          exclude_patterns: List[str]) -> List[Path]:
    """Scant workspace voor Markdown bestanden in gegeven folders.
    
    Args:
        workspace_root: Root van de workspace
        include_folders: Lijst van folders om te scannen
        exclude_patterns: Patronen van paden om uit te sluiten
        
    Returns:
        Gesorteerde lijst van Path objecten naar Markdown bestanden
    """
    markdown_files = []
    
    for folder in include_folders:
        folder_path = workspace_root / folder
        if not folder_path.exists():
            print(f"[WARN] Folder niet gevonden: {folder_path}", file=sys.stderr)
            continue
        
        # Recursief scannen voor .md bestanden
        for md_file in folder_path.rglob("*.md"):
            # Check exclusion patterns
            rel_path = md_file.relative_to(workspace_root)
            excluded = any(
                re.search(pattern.replace("*", ".*").replace("**", ".*"), str(rel_path))
                for pattern in exclude_patterns
            )
            
            if not excluded:
                markdown_files.append(md_file)
    
    return sorted(markdown_files)


def build_nav_structure(files: List[Path], workspace_root: Path, nav_depth: int = 3) -> List:
    """Bouwt navigatiestructuur voor mkdocs.yml uit lijst van bestanden.
    
    Args:
        files: Lijst van Markdown bestanden
        workspace_root: Root van workspace
        nav_depth: Maximale diepte van navigatie
        
    Returns:
        Geneste lijst/dict structuur voor mkdocs nav sectie
    """
    # Groepeer bestanden per folder hiërarchie
    nav_tree = {}
    
    for file_path in files:
        rel_path = file_path.relative_to(workspace_root)
        parts = rel_path.parts
        
        # Limiteer diepte
        if len(parts) > nav_depth + 1:  # +1 voor bestandsnaam
            parts = parts[:nav_depth] + (parts[-1],)
        
        # Bouw boom
        current = nav_tree
        for i, part in enumerate(parts[:-1]):  # Alle folders
            if part not in current:
                current[part] = {}
            current = current[part]
        
        # Voeg bestand toe
        filename = parts[-1]
        title = extract_title_from_md(file_path)
        current[title] = str(rel_path.as_posix())
    
    return convert_tree_to_nav(nav_tree)


def extract_title_from_md(file_path: Path) -> str:
    """Extraheert titel uit Markdown bestand (eerste # heading of bestandsnaam).
    
    Args:
        file_path: Path naar Markdown bestand
        
    Returns:
        Titel string
    """
    try:
        content = file_path.read_text(encoding="utf-8")
        # Zoek eerste # heading
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
    except Exception:
        pass
    
    # Fallback: gebruik bestandsnaam zonder .md
    return file_path.stem.replace("-", " ").replace("_", " ").title()


def convert_tree_to_nav(tree: Dict, level: int = 0) -> List:
    """Converteert folder-boom naar mkdocs nav structuur.
    
    Args:
        tree: Dictionary met folder/file structuur
        level: Huidige diepte (voor recursie)
        
    Returns:
        Lijst van nav items (str of dict)
    """
    nav = []
    
    for key, value in sorted(tree.items()):
        if isinstance(value, dict):
            # Folder met substructuur
            subnav = convert_tree_to_nav(value, level + 1)
            nav.append({key: subnav})
        else:
            # File
            nav.append({key: value})
    
    return nav


def generate_mkdocs_yml(workspace_root: Path, nav: List, output_path: Path) -> None:
    """Genereert mkdocs.yml configuratiebestand.
    
    Args:
        workspace_root: Root van workspace
        nav: Navigatiestructuur
        output_path: Waar mkdocs.yml moet worden geschreven
    """
    config = {
        "site_name": workspace_root.name.replace("-", " ").title(),
        "site_url": "https://example.com",  # Placeholder
        "site_description": "Gegenereerd door publicatie-steward",
        "theme": {
            "name": "material",
            "palette": {
                "primary": "blue",
                "accent": "light-blue"
            },
            "features": [
                "navigation.tabs",
                "navigation.sections",
                "toc.integrate"
            ]
        },
        "plugins": [
            "search",
            {"git-revision-date": {"enabled_if_env": "CI"}}
        ],
        "nav": nav
    }
    
    # Schrijf YAML
    with output_path.open("w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def validate_mkdocs_yml(mkdocs_path: Path, workspace_root: Path, 
                       check_broken_links: bool = True,
                       check_governance: bool = True) -> Tuple[str, List[Dict]]:
    """Valideert mkdocs.yml op correctheid.
    
    Args:
        mkdocs_path: Pad naar mkdocs.yml
        workspace_root: Root van workspace
        check_broken_links: Controleer of alle paden bestaan
        check_governance: Check voor gevoelige content
        
    Returns:
        Tuple van (status, issues lijst)
        status: "PASS", "WARNINGS", "FAIL"
        issues: Lijst van dicts met {severity, location, description}
    """
    issues = []
    
    # Check bestand bestaat
    if not mkdocs_path.exists():
        return "FAIL", [{"severity": "kritiek", "location": str(mkdocs_path), 
                        "description": "mkdocs.yml niet gevonden"}]
    
    # Parse YAML
    try:
        with mkdocs_path.open("r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return "FAIL", [{"severity": "kritiek", "location": str(mkdocs_path),
                        "description": f"Invalid YAML syntax: {e}"}]
    
    # Check nav sectie
    if "nav" not in config:
        issues.append({"severity": "waarschuwing", "location": "mkdocs.yml",
                      "description": "Geen nav sectie gevonden"})
    else:
        # Check broken links
        if check_broken_links:
            nav_paths = extract_paths_from_nav(config["nav"])
            for path_str in nav_paths:
                path = workspace_root / path_str
                if not path.exists():
                    issues.append({"severity": "kritiek", "location": path_str,
                                  "description": "Bestand niet gevonden (broken link)"})
    
    # Check gevoelige content
    if check_governance:
        sensitive_patterns = [
            r"password\s*[:=]",
            r"api[_-]?key\s*[:=]",
            r"secret\s*[:=]",
            r"token\s*[:=]"
        ]
        
        for path_str in nav_paths if check_broken_links and "nav" in config else []:
            path = workspace_root / path_str
            if path.exists():
                try:
                    content = path.read_text(encoding="utf-8")
                    for pattern in sensitive_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            issues.append({
                                "severity": "kritiek",
                                "location": path_str,
                                "description": f"Mogelijk gevoelige content gedetecteerd: {pattern}"
                            })
                except Exception:
                    pass
    
    # Bepaal status
    if any(issue["severity"] == "kritiek" for issue in issues):
        status = "FAIL"
    elif issues:
        status = "WARNINGS"
    else:
        status = "PASS"
    
    return status, issues


def extract_paths_from_nav(nav: List) -> Set[str]:
    """Extraheert alle bestandspaden uit nav structuur.
    
    Args:
        nav: mkdocs nav structuur
        
    Returns:
        Set van alle paden als strings
    """
    paths = set()
    
    for item in nav:
        if isinstance(item, dict):
            for key, value in item.items():
                if isinstance(value, str):
                    paths.add(value)
                elif isinstance(value, list):
                    paths.update(extract_paths_from_nav(value))
    
    return paths


def write_report(report_path: Path, title: str, content: str) -> None:
    """Schrijft een Markdown rapport bestand.
    
    Args:
        report_path: Waar het rapport moet worden geschreven
        title: Titel van het rapport
        content: Markdown content van het rapport
    """
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with report_path.open("w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"**Datum**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**Agent**: publicatie-steward\n\n")
        f.write("---\n\n")
        f.write(content)


def intent_schrijf_publicatiestructuur(workspace_root: Path, params: Dict) -> int:
    """Implementeert intent: schrijf-publicatiestructuur.
    
    Args:
        workspace_root: Root van workspace
        params: Parameters uit input.md
        
    Returns:
        Exit code (0 = success)
    """
    print("[INFO] Intent: schrijf-publicatiestructuur")
    
    # Extract parameters
    include_folders = params.get("include-folders", ["docs/", "governance/"])
    exclude_patterns = params.get("exclude-patterns", ["**/temp/", "**/.git/"])
    nav_depth = params.get("nav-depth", 3)
    
    # Scan workspace
    print(f"[INFO] Scannen van folders: {', '.join(include_folders)}")
    files = scan_workspace_content(workspace_root, include_folders, exclude_patterns)
    print(f"[INFO] {len(files)} Markdown bestanden gevonden")
    
    # Log gelezen bestanden
    log_agent_action("publicatie-steward", gelezen=[str(f) for f in files[:10]])  # Sample
    
    # Bouw navigatie
    print("[INFO] Bouwen van navigatiestructuur...")
    nav = build_nav_structure(files, workspace_root, nav_depth)
    
    # Genereer mkdocs.yml
    mkdocs_path = workspace_root / "mkdocs.yml"
    print(f"[INFO] Genereren van {mkdocs_path}")
    generate_mkdocs_yml(workspace_root, nav, mkdocs_path)
    
    # Schrijf rapport
    datum = datetime.now().strftime("%Y%m%d-%H%M")
    report_path = workspace_root / "artefacten" / "publicatie-steward" / f"publicatiestructuur-rapport-{datum}.md"
    
    report_content = f"## Overzicht\n\n"
    report_content += f"- **Gescande folders**: {', '.join(include_folders)}\n"
    report_content += f"- **Aantal bestanden**: {len(files)}\n"
    report_content += f"- **Navigatie-diepte**: {nav_depth}\n\n"
    report_content += f"## Gegenereerde navigatiestructuur\n\n"
    report_content += f"Zie `mkdocs.yml` voor volledige structuur.\n"
    
    write_report(report_path, "Publicatiestructuur Rapport", report_content)
    
    # Log output
    log_agent_action("publicatie-steward", 
                    aangemaakt=[str(mkdocs_path), str(report_path)])
    
    print(f"[SUCCESS] mkdocs.yml gegenereerd: {mkdocs_path}")
    print(f"[SUCCESS] Rapport geschreven: {report_path}")
    
    return 0


def intent_valideer_publicatiestructuur(workspace_root: Path, params: Dict) -> int:
    """Implementeert intent: valideer-publicatiestructuur.
    
    Args:
        workspace_root: Root van workspace
        params: Parameters uit input.md
        
    Returns:
        Exit code (0 = success, 1 = validation failed)
    """
    print("[INFO] Intent: valideer-publicatiestructuur")
    
    # Extract parameters
    mkdocs_path_str = params.get("mkdocs-yml-path", "mkdocs.yml")
    mkdocs_path = workspace_root / mkdocs_path_str
    check_broken_links = params.get("check-broken-links", True)
    check_governance = params.get("check-governance", True)
    strict_mode = params.get("strict-mode", False)
    
    # Log gelezen bestand
    log_agent_action("publicatie-steward", gelezen=[str(mkdocs_path)])
    
    # Valideer
    print(f"[INFO] Valideren van {mkdocs_path}")
    status, issues = validate_mkdocs_yml(mkdocs_path, workspace_root, 
                                        check_broken_links, check_governance)
    
    # Schrijf rapport
    datum = datetime.now().strftime("%Y%m%d-%H%M")
    report_path = workspace_root / "artefacten" / "publicatie-steward" / f"validatie-rapport-{datum}.md"
    
    report_content = f"## Status: **{status}**\n\n"
    
    if issues:
        report_content += f"### Gevonden issues ({len(issues)})\n\n"
        
        for issue in sorted(issues, key=lambda x: {"kritiek": 0, "waarschuwing": 1, "info": 2}[x["severity"]]):
            report_content += f"- **{issue['severity'].upper()}** | `{issue['location']}`\n"
            report_content += f"  {issue['description']}\n\n"
    else:
        report_content += "✅ Geen issues gevonden. Alle validaties geslaagd.\n"
    
    write_report(report_path, "Validatie Rapport", report_content)
    
    # Log output
    log_agent_action("publicatie-steward", aangemaakt=[str(report_path)])
    
    print(f"[INFO] Validatiestatus: {status}")
    print(f"[SUCCESS] Rapport geschreven: {report_path}")
    
    # Return code
    if status == "FAIL" or (strict_mode and status == "WARNINGS"):
        return 1
    return 0


def intent_actualiseer_mkdocs_configuratie(workspace_root: Path, params: Dict) -> int:
    """Implementeert intent: actualiseer-mkdocs-configuratie.
    
    Args:
        workspace_root: Root van workspace
        params: Parameters uit input.md
        
    Returns:
        Exit code (0 = success)
    """
    print("[INFO] Intent: actualiseer-mkdocs-configuratie")
    print("[WARN] Deze functionaliteit is nog niet volledig geïmplementeerd")
    print("[INFO] Voor nu: gebruik schrijf-publicatiestructuur voor complete regeneratie")
    
    # Placeholder implementation
    mkdocs_path_str = params.get("mkdocs-yml-path", "mkdocs.yml")
    mkdocs_path = workspace_root / mkdocs_path_str
    
    log_agent_action("publicatie-steward", gelezen=[str(mkdocs_path)])
    
    datum = datetime.now().strftime("%Y%m%d-%H%M")
    report_path = workspace_root / "artefacten" / "publicatie-steward" / f"actualisatie-rapport-{datum}.md"
    
    report_content = "## Status\n\nFunctionaliteit in ontwikkeling.\n"
    write_report(report_path, "Actualisatie Rapport", report_content)
    
    log_agent_action("publicatie-steward", aangemaakt=[str(report_path)])
    
    return 0


def intent_rapporteer_publicatiestatus(workspace_root: Path, params: Dict) -> int:
    """Implementeert intent: rapporteer-publicatiestatus.
    
    Args:
        workspace_root: Root van workspace
        params: Parameters uit input.md
        
    Returns:
        Exit code (0 = success)
    """
    print("[INFO] Intent: rapporteer-publicatiestatus")
    
    # Extract parameters
    mkdocs_path_str = params.get("mkdocs-yml-path", "mkdocs.yml")
    mkdocs_path = workspace_root / mkdocs_path_str
    scan_folders = params.get("scan-folders", ["docs/", "governance/", "artefacten/"])
    include_stats = params.get("include-stats", True)
    
    # Lees gepubliceerde content
    gepubliceerd = set()
    if mkdocs_path.exists():
        try:
            with mkdocs_path.open("r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                if "nav" in config:
                    gepubliceerd = extract_paths_from_nav(config["nav"])
        except Exception as e:
            print(f"[WARN] Kan mkdocs.yml niet lezen: {e}")
    
    log_agent_action("publicatie-steward", gelezen=[str(mkdocs_path)])
    
    # Scan alle content
    alle_bestanden = scan_workspace_content(workspace_root, scan_folders, ["**/temp/", "**/.git/"])
    
    # Vergelijk
    gepubliceerd_bestanden = []
    niet_gepubliceerd_bestanden = []
    
    for file_path in alle_bestanden:
        rel_path = file_path.relative_to(workspace_root).as_posix()
        if rel_path in gepubliceerd:
            gepubliceerd_bestanden.append(rel_path)
        else:
            niet_gepubliceerd_bestanden.append(rel_path)
    
    # Schrijf rapport
    datum = datetime.now().strftime("%Y%m%d-%H%M")
    report_path = workspace_root / "artefacten" / "publicatie-steward" / f"publicatiestatus-rapport-{datum}.md"
    
    report_content = f"## Samenvatting\n\n"
    report_content += f"- **Totaal bestanden**: {len(alle_bestanden)}\n"
    report_content += f"- **Gepubliceerd**: {len(gepubliceerd_bestanden)}\n"
    report_content += f"- **Niet gepubliceerd**: {len(niet_gepubliceerd_bestanden)}\n\n"
    
    report_content += f"## Gepubliceerde content\n\n"
    for path in sorted(gepubliceerd_bestanden)[:20]:  # Top 20
        report_content += f"- {path}\n"
    if len(gepubliceerd_bestanden) > 20:
        report_content += f"\n_...en {len(gepubliceerd_bestanden) - 20} meer_\n"
    
    report_content += f"\n## Niet-gepubliceerde content\n\n"
    for path in sorted(niet_gepubliceerd_bestanden)[:20]:  # Top 20
        report_content += f"- {path}\n"
    if len(niet_gepubliceerd_bestanden) > 20:
        report_content += f"\n_...en {len(niet_gepubliceerd_bestanden) - 20} meer_\n"
    
    write_report(report_path, "Publicatiestatus Rapport", report_content)
    
    log_agent_action("publicatie-steward", aangemaakt=[str(report_path)])
    
    print(f"[SUCCESS] Rapport geschreven: {report_path}")
    
    return 0


def main() -> int:
    """Main entry point for publicatie-steward runner.
    
    Returns:
        Exit code (0 = success, non-zero = error)
    """
    parser = argparse.ArgumentParser(
        description="Publicatie Steward Runner - Beheert mkdocs.yml en publicatiestructuur",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    args = parser.parse_args()
    
    # Bepaal workspace root
    workspace_root = Path.cwd()
    
    # Lees input.md
    input_path = workspace_root / "input" / "input.md"
    
    try:
        print(f"[INFO] Lezen van input: {input_path}")
        input_data = read_input_file(input_path)
        
        # Log input
        log_agent_action("publicatie-steward", gelezen=[str(input_path)])
        
    except Exception as e:
        print(f"[ERROR] Kan input niet lezen: {e}", file=sys.stderr)
        return 1
    
    # Extract intent
    intent = input_data.get("intent")
    if not intent:
        print("[ERROR] Geen 'intent' gevonden in input.md", file=sys.stderr)
        return 1
    
    print(f"[INFO] Intent: {intent}")
    
    # Route naar juiste intent handler
    if intent == "schrijf-publicatiestructuur":
        return intent_schrijf_publicatiestructuur(workspace_root, input_data)
    elif intent == "valideer-publicatiestructuur":
        return intent_valideer_publicatiestructuur(workspace_root, input_data)
    elif intent == "actualiseer-mkdocs-configuratie":
        return intent_actualiseer_mkdocs_configuratie(workspace_root, input_data)
    elif intent == "rapporteer-publicatiestatus":
        return intent_rapporteer_publicatiestatus(workspace_root, input_data)
    else:
        print(f"[ERROR] Onbekende intent: {intent}", file=sys.stderr)
        print("[INFO] Geldige intents: schrijf-publicatiestructuur, valideer-publicatiestructuur, "
              "actualiseer-mkdocs-configuratie, rapporteer-publicatiestatus")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```
