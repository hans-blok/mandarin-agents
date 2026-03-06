#!/usr/bin/env python3

"""
{runner-naam}.py - {Korte beschrijving van wat deze runner doet}

Runner voor agent {agent-naam}, intent {intent-naam}.
Voert run_prompt.py aan met voorgedefinieerde parameters en handelt agent-specifieke workflow af.

Usage:
    python {runner-naam}.py [OPTIONS]
    
Exit Codes:
    0: Success
    1: Validation error (input ontbreekt of ongeldig)
    2: Execution error (run_prompt.py of agent gefaald)
    3: Dependency unavailable (bestand niet gevonden, omgeving niet klaar)

Architecture:
    Runner -> run_prompt.py -> bootstrap_canon_consult.py + agent.md -> LLM execution
    
    Deze runner is NIET de agent zelf, maar bereidt execution voor en valideert.
    Echte "intelligentie" zit in de LLM die de gegenereerde instructies uitvoert.

Governance:
    - Volgt doctrine-agent-charter-normering.md Principe 7 (Transparante Verantwoording)
    - Logt naar audit/{runner-naam}.log.md
    - Parameters worden gevalideerd voor run_prompt.py wordt aangeroepen
    
Template versie: 1.0.0
Gegenereerd: {YYYY-MM-DD}
"""

# Template Metadata
__template_metadata__ = {
    "agent": "*",  # Generiek template voor alle agents
    "intent": "agent-runner",
    "versie": "1.0.0",
    "beschrijving": "Python runner skeleton voor agent execution workflow"
}

import argparse
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


# =============================================================================
# CONFIGURATION (pas aan voor specifieke runner)
# =============================================================================

RUNNER_NAME = "{runner-naam}"
AGENT_NAME = "{agent-naam}"
INTENT_NAME = "{intent-kortschrift}"
VALUE_STREAM_FASE = "{value-stream-code}.{fase-nummer}"
PROMPT_FILE = "artefacten/{value-stream-code}/{value-stream-code}.{fase-nummer}.{agent-naam}/mandarin.{agent-naam}.{intent-kortschrift}.prompt.md"

# Default input file (kan worden overschreven via CLI)
DEFAULT_INPUT_FILE = "input/input.md"

# Audit logging
AUDIT_DIR = Path("audit")
AUDIT_LOG_FILE = AUDIT_DIR / f"{RUNNER_NAME}.log.md"


# =============================================================================
# COMMAND-LINE INTERFACE
# =============================================================================

def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line argumenten.
    
    Voeg hier runner-specifieke argumenten toe onder "Runner-specific parameters".
    Houd standaard argumenten (--input-file, --method, --verbose) intact.
    
    Returns:
        argparse.Namespace: Geparseerde argumenten
    """
    parser = argparse.ArgumentParser(
        description=f"Runner voor {AGENT_NAME} - {INTENT_NAME}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basis uitvoering
  python {runner-naam}.py
  
  # Met custom input file
  python {runner-naam}.py --input-file input/custom-input.md
  
  # Met verbose logging
  python {runner-naam}.py --verbose

Exit Codes:
  0: Success
  1: Validation error
  2: Execution error  
  3: Dependency unavailable
        """
    )
    
    # -------------------------------------------------------------------------
    # Runner-specific parameters (PAS AAN VOOR JOUW AGENT)
    # -------------------------------------------------------------------------
    parser.add_argument(
        "--{param1}",
        type=str,
        required=False,  # Maak required=True indien verplicht
        help="{Beschrijving van parameter 1}"
    )
    
    parser.add_argument(
        "--{param2}",
        type=str,
        required=False,
        help="{Beschrijving van parameter 2}"
    )
    
    # Voeg meer parameters toe zoals nodig...
    
    # -------------------------------------------------------------------------
    # Standard parameters (LAAT INTACT)
    # -------------------------------------------------------------------------
    parser.add_argument(
        "--input-file",
        type=str,
        default=DEFAULT_INPUT_FILE,
        help=f"Pad naar input-bestand met meerregelige tekst (default: {DEFAULT_INPUT_FILE})"
    )
    
    parser.add_argument(
        "--method",
        type=str,
        default="runner",
        choices=["manual", "runner", "pipeline"],
        help="Methode van uitvoering (default: runner)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Toon uitgebreide logging"
    )
    
    return parser.parse_args()


# =============================================================================
# INPUT VALIDATION (Input Quality Gate)
# =============================================================================

def validate_inputs(args: argparse.Namespace) -> Tuple[bool, List[str]]:
    """
    Valideer alle inputs voordat run_prompt.py wordt aangeroepen.
    
    Dit is de Input Quality Gate: de runner start ALLEEN als alle checks slagen.
    
    Args:
        args: Geparseerde command-line argumenten
        
    Returns:
        Tuple[bool, List[str]]: (succes, lijst van foutmeldingen)
        
    Implementatie:
        Pas deze functie aan voor agent-specifieke validaties:
        - Controleer of verplichte parameters aanwezig zijn
        - Valideer formaten (email, URL, datum, etc.)
        - Controleer of bestanden/paden bestaan
        - Valideer business rules (max lengte, toegestane waarden, etc.)
    """
    errors = []
    
    # -------------------------------------------------------------------------
    # Standard validations (LAAT INTACT)
    # -------------------------------------------------------------------------
    
    # Check prompt file bestaat
    prompt_path = Path(PROMPT_FILE)
    if not prompt_path.exists():
        errors.append(f"Prompt-bestand niet gevonden: {PROMPT_FILE}")
    
    # Check input file bestaat (als opgegeven)
    if args.input_file:
        input_path = Path(args.input_file)
        if not input_path.exists():
            errors.append(f"Input-bestand niet gevonden: {args.input_file}")
    
    # -------------------------------------------------------------------------
    # Agent-specific validations (PAS AAN)
    # -------------------------------------------------------------------------
    
    # Voorbeeld: valideer verplichte parameter
    # if not args.param1:
    #     errors.append("Parameter --param1 is verplicht")
    
    # Voorbeeld: valideer formaat
    # if args.param2 and not args.param2.endswith('.md'):
    #     errors.append("Parameter --param2 moet een .md bestand zijn")
    
    # Voorbeeld: valideer business rule
    # if args.param1 and len(args.param1) > 100:
    #     errors.append("Parameter --param1 mag maximaal 100 karakters zijn")
    
    # TODO: Voeg agent-specifieke validaties toe
    
    return (len(errors) == 0, errors)


# =============================================================================
# PARAMETER MAPPING
# =============================================================================

def build_run_prompt_params(args: argparse.Namespace) -> List[str]:
    """
    Bouw lijst van -p parameters voor run_prompt.py.
    
    run_prompt.py verwacht parameters in het formaat: -p key=value
    Deze functie mapt command-line argumenten naar run_prompt.py parameters.
    
    Args:
        args: Geparseerde command-line argumenten
        
    Returns:
        List[str]: Lijst van ['-p', 'key1=value1', '-p', 'key2=value2', ...]
        
    Implementatie:
        Pas aan voor agent-specifieke parameter mapping.
        Parameters worden gebruikt voor placeholder replacement in prompt en agent.md.
    """
    params = []
    
    # -------------------------------------------------------------------------
    # Standard parameters (altijd meegeven)
    # -------------------------------------------------------------------------
    params.extend(['-p', f'agent_naam={AGENT_NAME}'])
    params.extend(['-p', f'value_stream_fase={VALUE_STREAM_FASE}'])
    params.extend(['-p', f'intent={INTENT_NAME}'])
    
    # -------------------------------------------------------------------------
    # Agent-specific parameters (PAS AAN)
    # -------------------------------------------------------------------------
    
    # Voorbeeld: map CLI argument naar run_prompt parameter
    # if args.param1:
    #     params.extend(['-p', f'doelparameter={args.param1}'])
    
    # Voorbeeld: conditionele parameter
    # if args.param2:
    #     params.extend(['-p', f'optioneel={args.param2}'])
    
    # TODO: Voeg agent-specifieke parameter mapping toe
    
    return params


# =============================================================================
# RUNNER EXECUTION
# =============================================================================

def run_agent(args: argparse.Namespace) -> int:
    """
    Voer run_prompt.py uit met voorgedefinieerde parameters.
    
    Dit is de kern van de runner: roept run_prompt.py aan die op zijn beurt:
    1. Canon consulteert via bootstrap_canon_consult.py
    2. Agent.md inlaadt
    3. Charter inlaadt (indien aanwezig)
    4. Placeholders vervangt
    5. Instructies logt naar audit/agent-instructions.log.md
    6. Volledige instructies print voor LLM execution
    
    Args:
        args: Geparseerde command-line argumenten
        
    Returns:
        int: Exit code (0=success, 2=execution error)
    """
    # Bouw commando
    cmd = [
        'python',
        'scripts/run_prompt.py',
        PROMPT_FILE,
    ]
    
    # Voeg parameters toe
    cmd.extend(build_run_prompt_params(args))
    
    # Voeg input file toe
    if args.input_file:
        cmd.extend(['--input-file', args.input_file])
    
    # Voeg method toe
    cmd.extend(['--method', args.method])
    
    # Logging
    if args.verbose:
        print("=" * 80)
        print(f"RUNNER: {RUNNER_NAME}")
        print("=" * 80)
        print(f"Command: {' '.join(cmd)}")
        print()
    
    # Voer uit
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except FileNotFoundError as e:
        print(f"ERROR: run_prompt.py niet gevonden: {e}", file=sys.stderr)
        return 3  # Dependency unavailable
    except Exception as e:
        print(f"ERROR: Onverwachte fout tijdens uitvoering: {e}", file=sys.stderr)
        return 2  # Execution error


# =============================================================================
# AUDIT LOGGING
# =============================================================================

def log_execution(
    args: argparse.Namespace,
    exit_code: int,
    start_time: datetime,
    end_time: datetime
) -> None:
    """
    Log runner execution naar audit log.
    
    Voldoet aan Principe 7 (Transparante Verantwoording) uit 
    doctrine-agent-charter-normering.md.
    
    Args:
        args: Geparseerde argumenten
        exit_code: Exit code van execution
        start_time: Start timestamp
        end_time: Eind timestamp
    """
    # Maak audit dir aan als die niet bestaat
    AUDIT_DIR.mkdir(exist_ok=True)
    
    # Maak header als log nog niet bestaat
    if not AUDIT_LOG_FILE.exists():
        header = f"""# Runner Execution Log - {RUNNER_NAME}

Dit logbestand registreert alle executions van de {RUNNER_NAME} runner.

**Runner**: {RUNNER_NAME}  
**Agent**: {AGENT_NAME}  
**Intent**: {INTENT_NAME}  
**Value Stream Fase**: {VALUE_STREAM_FASE}  
**Formaat**: Markdown  
**Update methode**: Append-only

---

"""
        with open(AUDIT_LOG_FILE, 'w', encoding='utf-8') as f:
            f.write(header)
    
    # Build parameter summary
    params_text = "  (geen agent-specifieke parameters)"
    # TODO: Pas aan om agent-specifieke parameters te loggen
    # params_text = "\n".join([f"  - `{k}`: {v}" for k, v in {...}.items()])
    
    # Duration
    duration = (end_time - start_time).total_seconds()
    
    # Status
    status = "✓ SUCCESS" if exit_code == 0 else f"✗ FAILED (exit code {exit_code})"
    
    # Build log entry
    log_entry = f"""
---

## Execution — {start_time.isoformat()}

- **Status**: {status}
- **Duration**: {duration:.2f}s
- **Start**: {start_time.isoformat()}
- **End**: {end_time.isoformat()}
- **Method**: {args.method}
- **Input File**: `{args.input_file}`
- **Parameters**:
{params_text}

"""
    
    # Append naar log
    with open(AUDIT_LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry)
    
    if args.verbose:
        print(f"\n✓ Execution gelogd naar: {AUDIT_LOG_FILE}")


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main() -> int:
    """
    Main execution flow.
    
    Flow:
        1. Parse argumenten
        2. Valideer inputs (Input Quality Gate)
        3. Voer run_prompt.py uit
        4. Log execution naar audit
        5. Return exit code
        
    Returns:
        int: Exit code voor sys.exit()
    """
    start_time = datetime.now()
    
    # Parse argumenten
    args = parse_arguments()
    
    if args.verbose:
        print(f"Starting {RUNNER_NAME}...")
        print()
    
    # Input Quality Gate
    valid, errors = validate_inputs(args)
    if not valid:
        print("ERROR: Validatie gefaald:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1  # Validation error
    
    if args.verbose:
        print("✓ Input validatie geslaagd")
        print()
    
    # Execute runner
    exit_code = run_agent(args)
    
    # Log execution
    end_time = datetime.now()
    try:
        log_execution(args, exit_code, start_time, end_time)
    except Exception as e:
        print(f"WARNING: Logging gefaald: {e}", file=sys.stderr)
        # Don't fail the run because of logging issues
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())


# =============================================================================
# INVULINSTRUCTIES VOOR AGENT-SMEDER / ENGINEER-STEWARD
# =============================================================================
"""
VERWIJDER DEZE SECTIE NA INVULLING

1. CONFIGURATION (regel 33-45)
   - Vul {runner-naam} in (kebab-case, bijv. "hypothese-vormer-runner")
   - Vul {agent-naam} in (bijv. "hypothese-vormer")
   - Vul {intent-kortschrift} in (bijv. "formuleer-hypothese")
   - Vul {value-stream-code}.{fase-nummer} in (bijv. "sfw.01")
   - Pas PROMPT_FILE pad aan naar juiste locatie

2. PARSE_ARGUMENTS (regel 56-122)
   - Voeg runner-specifieke parameters toe onder "Runner-specific parameters"
   - Voorbeeld: --thema, --probleemruimte, --status-quo, etc.
   - Gebruik type=str, type=int, type=Path waar gepast
   - Markeer vereiste parameters met required=True

3. VALIDATE_INPUTS (regel 128-175)
   - Voeg agent-specifieke validaties toe onder "Agent-specific validations"
   - Check of verplichte parameters aanwezig zijn
   - Valideer formaten (email, URL, datum, lengte, etc.)
   - Check business rules (toegestane waarden, relaties tussen params)
   - Gebruik duidelijke error messages

4. BUILD_RUN_PROMPT_PARAMS (regel 181-218)
   - Map CLI argumenten naar run_prompt.py parameters (-p key=value)
   - Deze keys worden gebruikt in prompt en agent.md als [KEY] placeholders
   - Voorbeeld: args.thema -> '-p', 'thema_epic={args.thema}'

5. LOG_EXECUTION (regel 283-345)
   - Pas params_text aan om agent-specifieke parameters te loggen
   - Dit maakt executions traceerbaar voor monitoring

6. USAGE PATTERNS

   Verplichte parameter:
   ```python
   parser.add_argument('--naam', type=str, required=True, help="...")
   if not args.naam:
       errors.append("Parameter --naam is verplicht")
   params.extend(['-p', f'agent_naam={args.naam}'])
   ```
   
   Optionele parameter met default:
   ```python
   parser.add_argument('--optie', type=str, default="standaard", help="...")
   if args.optie != "standaard":
       params.extend(['-p', f'custom_optie={args.optie}'])
   ```
   
   File path parameter:
   ```python
   parser.add_argument('--bestand', type=Path, required=True, help="...")
   if not args.bestand.exists():
       errors.append(f"Bestand niet gevonden: {args.bestand}")
   params.extend(['-p', f'input_bestand={args.bestand}'])
   ```

7. EXIT CODES
   - 0: Success (run_prompt.py + agent succesvol)
   - 1: Validation error (input quality gate gefaald)
   - 2: Execution error (run_prompt.py of agent gefaald)
   - 3: Dependency unavailable (bestand/tool niet gevonden)

8. TESTEN
   - Test happy path: alle inputs correct -> exit code 0
   - Test validation errors: missing params -> exit code 1
   - Test file not found: verkeerd pad -> exit code 1 of 3
   - Check audit log wordt correct geschreven

9. NAAMGEVING
   Bestandsnaam: {agent-naam}-{intent-kortschrift}.runner.py
   Voorbeeld: hypothese-vormer-formuleer.runner.py

10. DOCTRINE COMPLIANCE
    ✓ Principe 7 (Transparante Verantwoording): audit logging ingebakken
    ✓ Input Quality Gate: geen "best effort", stop bij ongeldige input
    ✓ Separation of Concerns: runner bereidt voor, LLM voert uit
    ✓ Expliciete error handling: geen silent failures

Template versie: 1.0.0
Gebaseerd op: run_prompt.py, bootstrap_canon_consult.py, engineer-steward charter
"""
