"""Mandarin Agent Runner - Logging helper voor handmatige agent-starts.

Dit script registreert bestanden die een agent leest, wijzigt of aanmaakt,
conform Norm 10.4 uit doctrine-agent-charter-normering.md.

Gebruik:
    python scripts/runners/mandarin_agent_runner.py <agent-naam> \\
        --gelezen <pad1> <pad2> ... \\
        --aangepast <pad1> <pad2> ... \\
        --aangemaakt <pad1> <pad2> ...

Voorbeeld:
    python scripts/runners/mandarin_agent_runner.py workspace-steward \\
        --gelezen governance/beleid.md \\
        --aangepast .gitignore \\
        --aangemaakt logs/20260206.1430 workspace-steward.log
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Voeg scripts folder toe aan Python path voor import
scripts_dir = Path(__file__).parent.parent
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

from logging_utils import log_manual_start


def main() -> int:
    """Parse argumenten en roep log_manual_start aan."""
    parser = argparse.ArgumentParser(
        description="Log handmatige agent-start conform Norm 10.4",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "agent_naam",
        help="Canonieke naam van de agent (bijv. workspace-steward)"
    )
    parser.add_argument(
        "--gelezen",
        nargs="*",
        default=[],
        help="Paden van bestanden die zijn gelezen"
    )
    parser.add_argument(
        "--aangepast",
        nargs="*",
        default=[],
        help="Paden van bestanden die zijn aangepast"
    )
    parser.add_argument(
        "--aangemaakt",
        nargs="*",
        default=[],
        help="Paden van bestanden die zijn aangemaakt"
    )
    
    args = parser.parse_args()
    
    # Roep logging_utils.py aan
    try:
        log_path = log_manual_start(
            agent_naam=args.agent_naam,
            gelezen=args.gelezen,
            aangepast=args.aangepast,
            aangemaakt=args.aangemaakt
        )
        print(f"✓ Log geschreven naar: {log_path}")
        return 0
    except Exception as e:
        print(f"✗ Fout bij schrijven log: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())