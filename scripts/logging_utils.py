"""Logging utilities voor mandarin-agents.

Deze module biedt een gedeelde helper voor handmatige initialisatie
(conform Norm 10.4 uit de agent-charter-doctrine):

- Schrijf per handmatige start een logbestand in de `logs/` folder.
- Bestandsnaam: `logs/yyyyddmm.HHmm {agent-naam}.log`.
- Inhoud: opsomming van gelezen, aangepaste en aangemaakte bestanden.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List


@dataclass
class ManualStartLog:
    """Structuur voor een handmatige start-log.

    Attributes:
        agent_naam: Canonieke naam van de agent (bijv. "workspace-steward").
        gelezen: Paden van bestanden die zijn gelezen.
        aangepast: Paden van bestanden die zijn aangepast.
        aangemaakt: Paden van bestanden die zijn aangemaakt.
    """

    agent_naam: str
    gelezen: List[str]
    aangepast: List[str]
    aangemaakt: List[str]

    def to_markdown(self) -> str:
        """Render de log-inhoud als Markdown-tekst."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        lines: List[str] = []
        lines.append(f"# Handmatige start log — {self.agent_naam}\n")
        lines.append(f"**Datum/tijd**: {timestamp}\n")
        lines.append("")

        def add_section(title: str, items: Iterable[str]) -> None:
            lines.append(f"## {title}")
            items_list = list(items)
            if not items_list:
                lines.append("(geen)")
            else:
                for item in items_list:
                    lines.append(f"- {item}")
            lines.append("")

        add_section("Bestanden gelezen", self.gelezen)
        add_section("Bestanden aangepast", self.aangepast)
        add_section("Bestanden aangemaakt", self.aangemaakt)

        return "\n".join(lines).rstrip() + "\n"


def log_manual_start(
    agent_naam: str,
    gelezen: Iterable[str] | None = None,
    aangepast: Iterable[str] | None = None,
    aangemaakt: Iterable[str] | None = None,
) -> Path:
    """Schrijf een logbestand voor een handmatige agent-start.

    De log wordt geschreven naar:

        logs/yyyyddmm.HHmm {agent-naam}.log

    waarbij `yyyyddmm.HHmm` het huidige moment is in lokale tijd.

    Args:
        agent_naam: Canonieke naam van de agent.
        gelezen: Iterable met paden van gelezen bestanden.
        aangepast: Iterable met paden van aangepaste bestanden.
        aangemaakt: Iterable met paden van aangemaakte bestanden.

    Returns:
        Het pad naar het geschreven logbestand.
    """

    # Normaliseer inputs
    gelezen_list = list(gelezen or [])
    aangepast_list = list(aangepast or [])
    aangemaakt_list = list(aangemaakt or [])

    # Bepaal logmap en bestandsnaam
    workspace_root = Path.cwd()
    logs_dir = workspace_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d.%H%M")
    safe_agent_name = agent_naam.strip().replace("/", "-").replace("\\", "-")
    filename = f"{timestamp} {safe_agent_name}.log"
    log_path = logs_dir / filename

    log = ManualStartLog(
        agent_naam=agent_naam,
        gelezen=gelezen_list,
        aangepast=aangepast_list,
        aangemaakt=aangemaakt_list,
    )

    content = log.to_markdown()
    log_path.write_text(content, encoding="utf-8")

    return log_path
