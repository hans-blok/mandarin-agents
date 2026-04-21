"""Centrale service voor tokenbewust contextbeheer in mandarin-agents.

Implementeert het normatieve kader uit implementatienotitie-tokenbewust-contextbeheer.md.
Drie toegestane meetstatussen: exact | schatting | onbekend.
Nooit een exacte waarde claimen zonder expliciete meetbron.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal, Optional

MeetwijzeType = Literal["exact", "schatting", "onbekend"]
RisicoType = Literal["laag", "middel", "hoog", "kritiek"]

# --- Drempelwaarden (overschrijfbaar via config) ---
_DREMPEL_MIDDEL = 0.60
_DREMPEL_HOOG = 0.80
_DREMPEL_KRITIEK = 0.95

# --- Tekens per token (ruwe schatting) ---
_TEKENS_PER_TOKEN = 4


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ContextEvent:
    event_type: Literal[
        "preflight_warning",
        "context_loss_known",
        "context_loss_suspected",
        "compression_event",
        "token_measurement",
    ]
    timestamp: str
    meetwijze: MeetwijzeType
    bron: str
    detail: str
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    context_window_tokens: Optional[int] = None


@dataclass
class ContextStatus:
    model_name: str
    context_window_tokens: Optional[int]
    context_window_meetwijze: MeetwijzeType
    input_tokens: Optional[int]
    input_tokens_meetwijze: MeetwijzeType
    output_tokens: Optional[int]
    output_tokens_meetwijze: MeetwijzeType
    context_pressure_level: RisicoType
    hard_signaal_contextverlies: bool = False
    contextverlies_bekend: bool = False
    vermoed_contextverlies: bool = False
    events: list[ContextEvent] = field(default_factory=list)


@dataclass
class ProviderUsageSnapshot:
    input_tokens: Optional[int]
    output_tokens: Optional[int]
    context_window_tokens: Optional[int]
    meetwijze: MeetwijzeType
    hard_signaal_contextverlies: bool
    compression_detected: bool
    raw_signal_source: str


# ---------------------------------------------------------------------------
# Tokenschatting
# ---------------------------------------------------------------------------

def estimate_tokens(text: str) -> tuple[int, MeetwijzeType]:
    """Schat het aantal tokens in text.

    Probeert tiktoken te laden voor een betere schatting. Valt terug op
    tekengebaseerde schatting (~4 tekens per token). Altijd label 'schatting' —
    nooit 'exact' zonder provider-bevestiging.
    """
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        count = len(enc.encode(text))
        return count, "schatting"
    except Exception:
        count = max(1, len(text) // _TEKENS_PER_TOKEN)
        return count, "schatting"


# ---------------------------------------------------------------------------
# Drukbepaling
# ---------------------------------------------------------------------------

def determine_pressure(
    input_tokens: int,
    context_window: int,
    warn_threshold: float = _DREMPEL_HOOG,
    critical_threshold: float = _DREMPEL_KRITIEK,
) -> RisicoType:
    """Bepaal risiconiveau op basis van verhouding input / context-window."""
    if context_window <= 0:
        return "onbekend"  # type: ignore[return-value]
    ratio = input_tokens / context_window
    if ratio >= critical_threshold:
        return "kritiek"
    if ratio >= warn_threshold:
        return "hoog"
    if ratio >= _DREMPEL_MIDDEL:
        return "middel"
    return "laag"


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Preflight (Moment A + B)
# ---------------------------------------------------------------------------

def build_preflight_status(
    prompt_text: str,
    model_name: str,
    config: dict,
) -> ContextStatus:
    """Schat tokens en bepaal contextdruk vóór modelaanroep.

    Moment A+B uit de implementatienotitie: werkt op samengestelde prompt.
    """
    budget_cfg = config.get("context_budget", {}) if config else {}
    warn_threshold = budget_cfg.get("warn_threshold", _DREMPEL_HOOG)
    critical_threshold = budget_cfg.get("critical_threshold", _DREMPEL_KRITIEK)

    # Context-window opzoeken in config
    model_cfg = budget_cfg.get("models", {}).get(model_name, {})
    context_window = model_cfg.get("context_window_tokens")
    context_window_meetwijze: MeetwijzeType = "schatting" if context_window else "onbekend"

    input_tokens, input_meetwijze = estimate_tokens(prompt_text)

    pressure: RisicoType
    if context_window:
        pressure = determine_pressure(
            input_tokens, context_window, warn_threshold, critical_threshold
        )
    else:
        pressure = "onbekend"  # type: ignore[assignment]

    events: list[ContextEvent] = [
        ContextEvent(
            event_type="token_measurement",
            timestamp=_now_iso(),
            meetwijze=input_meetwijze,
            bron="runner-tokenizer",
            detail=f"Preflight schatting: {input_tokens} tokens",
            input_tokens=input_tokens,
            context_window_tokens=context_window,
        )
    ]

    if pressure in ("hoog", "kritiek"):
        events.append(
            ContextEvent(
                event_type="preflight_warning",
                timestamp=_now_iso(),
                meetwijze=input_meetwijze,
                bron="runner-tokenizer",
                detail=(
                    f"Contextdruk {pressure}: {input_tokens} geschatte tokens"
                    + (f" van {context_window}" if context_window else "")
                ),
                input_tokens=input_tokens,
                context_window_tokens=context_window,
            )
        )

    return ContextStatus(
        model_name=model_name,
        context_window_tokens=context_window,
        context_window_meetwijze=context_window_meetwijze,
        input_tokens=input_tokens,
        input_tokens_meetwijze=input_meetwijze,
        output_tokens=None,
        output_tokens_meetwijze="onbekend",
        context_pressure_level=pressure,
        events=events,
    )


# ---------------------------------------------------------------------------
# Post-call normalisatie (Moment C)
# ---------------------------------------------------------------------------

def normalize_openai_usage(usage) -> ProviderUsageSnapshot:
    """Extraheer usage uit een OpenAI CompletionUsage-object.

    Altijd 'exact' — OpenAI geeft werkelijke token-aantallen terug.
    """
    if usage is None:
        return ProviderUsageSnapshot(
            input_tokens=None,
            output_tokens=None,
            context_window_tokens=None,
            meetwijze="onbekend",
            hard_signaal_contextverlies=False,
            compression_detected=False,
            raw_signal_source="openai-usage-ontbreekt",
        )
    return ProviderUsageSnapshot(
        input_tokens=getattr(usage, "prompt_tokens", None),
        output_tokens=getattr(usage, "completion_tokens", None),
        context_window_tokens=None,
        meetwijze="exact",
        hard_signaal_contextverlies=False,
        compression_detected=False,
        raw_signal_source="openai-usage",
    )


def build_post_call_status(
    snapshot: ProviderUsageSnapshot,
    model_name: str,
    config: dict,
) -> ContextStatus:
    """Verwerk provider-usage na modelaanroep (Moment C)."""
    budget_cfg = config.get("context_budget", {}) if config else {}
    warn_threshold = budget_cfg.get("warn_threshold", _DREMPEL_HOOG)
    critical_threshold = budget_cfg.get("critical_threshold", _DREMPEL_KRITIEK)

    model_cfg = budget_cfg.get("models", {}).get(model_name, {})
    context_window = snapshot.context_window_tokens or model_cfg.get("context_window_tokens")

    pressure: RisicoType = "laag"
    if snapshot.input_tokens and context_window:
        pressure = determine_pressure(
            snapshot.input_tokens, context_window, warn_threshold, critical_threshold
        )

    events: list[ContextEvent] = [
        ContextEvent(
            event_type="token_measurement",
            timestamp=_now_iso(),
            meetwijze=snapshot.meetwijze,
            bron=snapshot.raw_signal_source,
            detail=(
                f"Input: {snapshot.input_tokens}, output: {snapshot.output_tokens}"
            ),
            input_tokens=snapshot.input_tokens,
            output_tokens=snapshot.output_tokens,
            context_window_tokens=context_window,
        )
    ]

    if snapshot.compression_detected:
        events.append(
            ContextEvent(
                event_type="compression_event",
                timestamp=_now_iso(),
                meetwijze=snapshot.meetwijze,
                bron=snapshot.raw_signal_source,
                detail="Provider signaleerde compressie of samenvatting",
            )
        )

    return ContextStatus(
        model_name=model_name,
        context_window_tokens=context_window,
        context_window_meetwijze="schatting" if context_window else "onbekend",
        input_tokens=snapshot.input_tokens,
        input_tokens_meetwijze=snapshot.meetwijze,
        output_tokens=snapshot.output_tokens,
        output_tokens_meetwijze=snapshot.meetwijze,
        context_pressure_level=pressure,
        hard_signaal_contextverlies=snapshot.hard_signaal_contextverlies,
        contextverlies_bekend=snapshot.hard_signaal_contextverlies,
        events=events,
    )


# ---------------------------------------------------------------------------
# Gebruikersmeldingen
# ---------------------------------------------------------------------------

_MELDINGEN = {
    "hoog": (
        "Waarschuwing: de samengestelde context nadert waarschijnlijk de limiet "
        "van het context-window.\n"
        "Meetwijze: schatting.\n"
        "Bron: runner-tokenizer."
    ),
    "kritiek": (
        "Waarschuwing: de samengestelde context overschrijdt waarschijnlijk de "
        "limiet van het context-window.\n"
        "Meetwijze: schatting.\n"
        "Bron: runner-tokenizer."
    ),
    "context_loss_suspected": (
        "Let op: eerdere context is mogelijk niet meer volledig actief.\n"
        "Meetwijze: onbekend.\n"
        "Bron: provider-signaal ontbreekt, runner ziet verhoogde contextdruk."
    ),
    "context_loss_known": (
        "Let op: eerdere context is aantoonbaar gecomprimeerd of weggevallen.\n"
        "Meetwijze: exact.\n"
        "Bron: provider usage / runner event."
    ),
}


def format_user_warning(status: ContextStatus) -> Optional[str]:
    """Geef standaard-waarschuwingstekst of None bij laag/middel risico."""
    if status.contextverlies_bekend:
        return _MELDINGEN["context_loss_known"]
    if status.vermoed_contextverlies:
        return _MELDINGEN["context_loss_suspected"]
    if status.context_pressure_level == "kritiek":
        return _MELDINGEN["kritiek"]
    if status.context_pressure_level == "hoog":
        return _MELDINGEN["hoog"]
    return None


# ---------------------------------------------------------------------------
# Serialisatie voor YAML-trace
# ---------------------------------------------------------------------------

def events_to_dicts(events: list[ContextEvent]) -> list[dict]:
    """Serialiseer events naar dicts voor yaml.dump."""
    result = []
    for e in events:
        d: dict = {
            "event_type": e.event_type,
            "timestamp": e.timestamp,
            "meetwijze": e.meetwijze,
            "bron": e.bron,
            "detail": e.detail,
        }
        if e.input_tokens is not None:
            d["input_tokens"] = e.input_tokens
        if e.output_tokens is not None:
            d["output_tokens"] = e.output_tokens
        if e.context_window_tokens is not None:
            d["context_window_tokens"] = e.context_window_tokens
        result.append(d)
    return result


# ---------------------------------------------------------------------------
# Config laden
# ---------------------------------------------------------------------------

def load_config(workspace_root: str | None = None) -> dict:
    """Laad context_budget.yaml uit workspace root. Geeft lege dict bij afwezigheid."""
    root = workspace_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(root, "context_budget.yaml")
    if not os.path.exists(config_path):
        return {}
    try:
        import yaml
        with open(config_path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}
