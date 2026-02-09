"""
Charter-Acknowledgement Automator
Automatiseert het toevoegen van charter-acknowledgement secties aan prompt bestanden.

Workflow:
1. Scan alle .prompt.md bestanden
2. Filter degene zonder charter-acknowledgement sectie  
3. Extracteer charter informatie uit bijbehorende charter files
4. Voeg charter-acknowledgement toe aan prompt bestanden
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CharterAcknowledgementAutomator:
    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
        self.prompt_files = []
        self.processed_charts = {}
        self.results = {
            'success': [],
            'failed': [],
            'charter_not_found': [],
            'already_has_acknowledgement': []
        }

    def scan_prompt_files(self) -> List[Path]:
        """Scan alle .prompt.md bestanden in de workspace"""
        logger.info("Scanning voor prompt bestanden...")
        files = list(self.workspace_path.rglob("*.prompt.md"))
        logger.info(f"Gevonden {len(files)} prompt bestanden")
        return files

    def has_charter_acknowledgement(self, file_path: Path) -> bool:
        """Check of prompt bestand al charter-acknowledgement sectie heeft"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return 'charter-acknowledgement:' in content
        except Exception as e:
            logger.error(f"Fout bij lezen {file_path}: {e}")
            return True  # Assume het heeft er al een om veiligheid

    def extract_frontmatter(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Extracteer frontmatter uit prompt bestand"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Split frontmatter - hanteren verschillende formaten
            if content.startswith('```prompt\n---\n'):
                parts = content.split('---\n', 2)
                if len(parts) >= 2:
                    yaml_content = parts[1]
                    try:
                        parsed = yaml.safe_load(yaml_content)
                        logger.debug(f"Parsed YAML for {file_path.name}: {parsed}")
                        return parsed
                    except yaml.YAMLError as e:
                        logger.error(f"YAML fout in {file_path}: {e}")
                        return None
            # Alternatief formaat zonder newline na ```prompt  
            elif content.startswith('```prompt\n---'):
                # Split op --- en pak alles tussen eerste en tweede ---
                lines = content.split('\n')
                yaml_lines = []
                in_yaml = False
                yaml_end = False
                for i, line in enumerate(lines):
                    if line.strip() == '---' and not in_yaml:
                        in_yaml = True
                        continue
                    elif line.strip() == '---' and in_yaml:
                        yaml_end = True
                        break
                    elif in_yaml:
                        yaml_lines.append(line)
                
                if yaml_end:
                    yaml_content = '\n'.join(yaml_lines)
                    try:
                        parsed = yaml.safe_load(yaml_content)
                        logger.debug(f"Parsed YAML for {file_path.name}: {parsed}")
                        return parsed
                    except yaml.YAMLError as e:
                        logger.error(f"YAML fout in {file_path}: {e}")
                        return None
            else:
                logger.debug(f"Geen herkenbaar frontmatter format in {file_path}")
                        
        except Exception as e:
            logger.error(f"Fout bij extracten frontmatter uit {file_path}: {e}")
            return None

    def resolve_charter_path(self, charter_ref: str, prompt_file_path: Path) -> Optional[Path]:
        """Resolve charter_ref naar absoluut pad"""
        # Verwijder @main: prefix als aanwezig
        charter_ref = charter_ref.replace('@main:', '')
        
        # Probeer relatief ten opzichte van workspace root
        charter_path = self.workspace_path / charter_ref
        if charter_path.exists():
            return charter_path
            
        # Probeer relatief ten opzichte van prompt file
        charter_path = prompt_file_path.parent / charter_ref
        if charter_path.exists():
            return charter_path
            
        # Kijk in agent-charters directory
        charter_name = Path(charter_ref).name
        charter_path = self.workspace_path / "agent-charters" / charter_name
        if charter_path.exists():
            return charter_path
            
        logger.warning(f"Charter niet gevonden voor ref: {charter_ref}")
        return None

    def extract_charter_info(self, charter_path: Path) -> Dict[str, str]:
        """Extracteer informatie uit charter bestand"""
        try:
            with open(charter_path, 'r', encoding='utf-8') as f:
                content = f.read()

            info = {
                'charter-id': '<onbekend>',
                'charter-versie': '<onbekend>',
                'value-stream': '<onbekend>',
                'canon-resolved-ref': '<wordt-achteraf-gevuld>',
                'kritieke-grens': '<wordt-achteraf-gevuld>',
                'kritieke-output-eis': '<wordt-achteraf-gevuld>',
                'charter-evidence': '<wordt-achteraf-gevuld>'
            }

            # Extract Bootstrap-Header info
            if '# Bootstrap-Header' in content:
                header_section = content.split('# Bootstrap-Header')[1].split('---')[0]
                
                # Extract Value Stream
                value_stream_match = re.search(r'- Value Stream:\s*(.+)', header_section)
                if value_stream_match:
                    value_stream = value_stream_match.group(1).strip()
                    # Extract value stream code (bijv. "sfw" uit "softwareontwikkeling (SFW, fase 02 - Werkvoorbereiding)")
                    if '(' in value_stream:
                        code_match = re.search(r'\(([A-Z]{3})', value_stream)
                        if code_match:
                            info['value-stream'] = code_match.group(1).lower()
                    else:
                        info['value-stream'] = value_stream.lower()

                # Extract Actor versie
                versie_match = re.search(r'- Versie:\s*(.+)', header_section)
                if versie_match:
                    info['charter-versie'] = versie_match.group(1).strip()

                # Extract Actor naam voor charter-id
                naam_match = re.search(r'- Naam/ID:\s*(.+)', header_section)
                if naam_match:
                    info['charter-id'] = naam_match.group(1).strip()

            # Extract Capability boundary (sectie 2)
            capability_match = re.search(r'## 2\. Capability boundary\s*\n\s*(.+?)(?=\n\n|\n##|$)', content, re.DOTALL)
            if capability_match:
                capability = capability_match.group(1).strip()
                # Clean up text
                capability = re.sub(r'\n\s*', ' ', capability)
                capability = re.sub(r'\s+', ' ', capability)
                info['kritieke-grens'] = capability

            # Extract eerste kerntaak (sectie 4)
            kerntaken_match = re.search(r'## 4\. Kerntaken\s*\n\s*1\.\s*\*\*([^*]+)\*\*\s*\n\s*(.+?)(?=\n\s*2\.|$)', content, re.DOTALL)
            if kerntaken_match:
                taak_titel = kerntaken_match.group(1).strip()
                taak_beschrijving = kerntaken_match.group(2).strip()
                # Clean up text
                taak_beschrijving = re.sub(r'\n\s*', ' ', taak_beschrijving)
                taak_beschrijving = re.sub(r'\s+', ' ', taak_beschrijving)
                info['kritieke-output-eis'] = f"{taak_titel}: {taak_beschrijving}"

            return info

        except Exception as e:
            logger.error(f"Fout bij extracten charter info uit {charter_path}: {e}")
            return {}

    def add_charter_acknowledgement(self, file_path: Path, charter_info: Dict[str, str]) -> bool:
        """Voeg charter-acknowledgement toe aan prompt bestand"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Construct charter-acknowledgement YAML
            acknowledgement = f"""charter-acknowledgement:
  charter-id: {charter_info['charter-id']}
  charter-versie: {charter_info['charter-versie']}
  value-stream: {charter_info['value-stream']}
  canon-resolved-ref: {charter_info['canon-resolved-ref']}
  kritieke-grens: "{charter_info['kritieke-grens']}"
  kritieke-output-eis: "{charter_info['kritieke-output-eis']}"
  charter-evidence: {charter_info['charter-evidence']}"""

            # Find insertion point (na charter_ref line)
            if '```prompt\n---\n' in content:
                parts = content.split('---\n', 2)
                if len(parts) >= 3:
                    frontmatter = parts[1]
                    rest = parts[2]
                    
                    # Voeg acknowledgement toe aan frontmatter
                    new_frontmatter = frontmatter.rstrip() + '\n' + acknowledgement + '\n'
                    new_content = '```prompt\n---\n' + new_frontmatter + '---\n' + rest
                    
                    # Write back
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    return True
                    
        except Exception as e:
            logger.error(f"Fout bij toevoegen charter-acknowledgement aan {file_path}: {e}")
            return False

        return False

    def process_prompt_file(self, file_path: Path) -> bool:
        """Process één prompt bestand"""
        logger.info(f"Processing {file_path.relative_to(self.workspace_path)}")
        
        # Check of al charter-acknowledgement heeft
        if self.has_charter_acknowledgement(file_path):
            self.results['already_has_acknowledgement'].append(str(file_path))
            return True

        # Extract frontmatter
        frontmatter = self.extract_frontmatter(file_path)
        if not frontmatter or 'charter_ref' not in frontmatter:
            logger.warning(f"Geen charter_ref gevonden in {file_path}")
            self.results['failed'].append(str(file_path))
            return False

        # Resolve charter path
        charter_ref = frontmatter['charter_ref']
        charter_path = self.resolve_charter_path(charter_ref, file_path)
        if not charter_path:
            self.results['charter_not_found'].append(f"{file_path}: {charter_ref}")
            return False

        # Extract charter info
        charter_info = self.extract_charter_info(charter_path)
        if not charter_info:
            logger.error(f"Kon geen charter info extracten uit {charter_path}")
            self.results['failed'].append(str(file_path))
            return False

        # Add charter-acknowledgement
        success = self.add_charter_acknowledgement(file_path, charter_info)
        if success:
            self.results['success'].append(str(file_path))
            logger.info(f"✓ Charter-acknowledgement toegevoegd aan {file_path.name}")
        else:
            self.results['failed'].append(str(file_path))
            logger.error(f"✗ Fout bij toevoegen charter-acknowledgement aan {file_path.name}")

        return success

    def run_test_batch(self, max_files: int = 5) -> Dict[str, List]:
        """Run test batch met beperkt aantal bestanden"""
        logger.info(f"=== TEST RUN: Max {max_files} bestanden ===")
        
        prompt_files = self.scan_prompt_files()
        
        # Prioriteer bestanden uit artefacten directory
        artefacten_files = [f for f in prompt_files if 'artefacten' in str(f)]
        other_files = [f for f in prompt_files if 'artefacten' not in str(f)]
        
        # Sort zodat we eerst artefacten files proberen
        sorted_files = artefacten_files + other_files
        
        # Filter bestanden zonder charter-acknowledgement
        files_to_process = []
        for file_path in sorted_files:
            if not self.has_charter_acknowledgement(file_path):
                files_to_process.append(file_path)
                if len(files_to_process) >= max_files:
                    break
        
        logger.info(f"Gevonden {len(files_to_process)} bestanden voor processing")
        for fp in files_to_process:
            logger.info(f"  - {fp.relative_to(self.workspace_path)}")
        
        # Process bestanden
        for file_path in files_to_process:
            self.process_prompt_file(file_path)

        return self.results

    def generate_report(self) -> str:
        """Genereer rapport van resultaten"""
        report = f"""
# Charter-Acknowledgement Automation Report

## Samenvatting
- ✅ Succesvol: {len(self.results['success'])}
- ❌ Gefaald: {len(self.results['failed'])}
- 📁 Charter niet gevonden: {len(self.results['charter_not_found'])}
- ✓ Had al acknowledgement: {len(self.results['already_has_acknowledgement'])}

## Succesvolle updates
"""
        for file_path in self.results['success']:
            report += f"- {file_path}\n"

        if self.results['failed']:
            report += "\n## Gefaalde updates\n"
            for file_path in self.results['failed']:
                report += f"- {file_path}\n"

        if self.results['charter_not_found']:
            report += "\n## Charter bestanden niet gevonden\n"
            for entry in self.results['charter_not_found']:
                report += f"- {entry}\n"

        return report

def main():
    """Main functie voor test run"""
    workspace_path = r"c:\git\mandarin-agents"
    
    automator = CharterAcknowledgementAutomator(workspace_path)
    
    # Test run met 5 bestanden
    results = automator.run_test_batch(5)
    
    # Genereer rapport
    report = automator.generate_report()
    
    print(report)
    
    # Save rapport
    with open(workspace_path + "/temp/charter-acknowledgement-test-report.md", 'w', encoding='utf-8') as f:
        f.write(report)

if __name__ == "__main__":
    main()