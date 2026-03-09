"""Python controller for the PhET Harvester."""

from pathlib import Path
from typing import TYPE_CHECKING

from dt_contracts.sandboxes.base import SandboxTelemetry
from dt_contracts.sandboxes.phet import PhetState
from pydantic import TypeAdapter

class PhetHarvester:
    """Manages JS harvester injection and telemetry parsing for PhET simulations."""

    def __init__(self) -> None:
        """Initialize the PhET harvester."""
        self.static_dir = Path(__file__).parent / "static"
        self._js_cache: str | None = None

    def get_injection_js(self) -> str:
        """Return the JavaScript string to be injected into the sandbox."""
        if not self._js_cache:
            # Note: Assuming bridge.js is one level up in engines/static/
            bridge_path = Path(__file__).parents[1] / "static" / "bridge.js"
            harvester_path = self.static_dir / "phet_harvester.js"
            
            bridge_js = bridge_path.read_text(encoding="utf-8")
            harvester_js = harvester_path.read_text(encoding="utf-8")
            
            self._js_cache = f"{bridge_js}\n\n{harvester_js}"
        return self._js_cache

    def parse_telemetry(self, telemetry: SandboxTelemetry) -> PhetState | None:
        """Map raw sandbox telemetry to specific PhET contracts."""
        if telemetry.event_name == "phet_state_update":
            return TypeAdapter(PhetState).validate_python(telemetry.payload)
        return None
