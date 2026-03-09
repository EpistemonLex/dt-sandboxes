"""Python controller for the Snap! Harvester."""

from pathlib import Path
from typing import TYPE_CHECKING

from dt_contracts.sandboxes.base import SandboxTelemetry
from dt_contracts.sandboxes.snap import SnapBlock, SnapState
from pydantic import TypeAdapter


class SnapHarvester:
    """Manages the JS harvester injection and telemetry parsing for Snap!."""

    def __init__(self) -> None:
        """Initialize the Snap! harvester."""
        self.static_dir = Path(__file__).parent / "static"
        self._js_cache: str | None = None

    def get_injection_js(self) -> str:
        """Return the JavaScript string to be injected into the sandbox."""
        if not self._js_cache:
            bridge_path = Path(__file__).parents[1] / "static" / "bridge.js"
            harvester_path = self.static_dir / "harvester.js"
            
            bridge_js = bridge_path.read_text(encoding="utf-8")
            harvester_js = harvester_path.read_text(encoding="utf-8")
            
            self._js_cache = f"{bridge_js}\n\n{harvester_js}"
        return self._js_cache

    def parse_telemetry(self, telemetry: SandboxTelemetry) -> SnapState | SnapBlock | None:
        """Map raw sandbox telemetry to specific Snap! contracts."""
        if telemetry.event_name == "state_update":
            return TypeAdapter(SnapState).validate_python(telemetry.payload)

        if telemetry.event_name == "block_added":
            return TypeAdapter(SnapBlock).validate_python(telemetry.payload)

        return None
