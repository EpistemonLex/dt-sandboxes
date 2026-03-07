"""Python controller for the Chemistry Harvester."""

from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import TypeAdapter

if TYPE_CHECKING:
    from dt_contracts.sandboxes.base import SandboxTelemetry
    from dt_contracts.sandboxes.chemistry import ChemistryState, ReactionEvent


class ChemistryHarvester:
    """Manages the JS harvester injection and telemetry parsing for Chemistry engines."""

    def __init__(self) -> None:
        """Initialize the chemistry harvester."""
        self.static_dir = Path(__file__).parent / "static"
        self._js_cache: str | None = None

    def get_injection_js(self) -> str:
        """Return the JavaScript string to be injected into the sandbox."""
        if not self._js_cache:
            js_path = self.static_dir / "harvester.js"
            self._js_cache = js_path.read_text(encoding="utf-8")
        return self._js_cache

    def parse_telemetry(self, telemetry: SandboxTelemetry) -> ChemistryState | ReactionEvent | None:
        """Map raw sandbox telemetry to specific Chemistry contracts."""
        from dt_contracts.sandboxes.chemistry import (  # noqa: PLC0415 # architectural: allowed-object
            ChemistryState,
            ReactionEvent,
        )


        if telemetry.event_name == "state_update":
            return TypeAdapter(ChemistryState).validate_python(telemetry.payload)

        if telemetry.event_name == "reaction":
            return TypeAdapter(ReactionEvent).validate_python(telemetry.payload)

        return None
