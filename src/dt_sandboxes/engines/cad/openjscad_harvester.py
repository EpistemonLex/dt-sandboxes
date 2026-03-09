"""Python controller for the OpenJSCAD Harvester."""

from pathlib import Path
from typing import TYPE_CHECKING

from dt_contracts.sandboxes.base import SandboxTelemetry
from pydantic import TypeAdapter

class OpenJSCADHarvester:
    """Manages JS harvester injection and telemetry parsing for OpenJSCAD programmatic CAD."""

    def __init__(self) -> None:
        """Initialize the OpenJSCAD harvester."""
        self.static_dir = Path(__file__).parent / "static"
        self._js_cache: str | None = None

    def get_injection_js(self) -> str:
        """Return the JavaScript string to be injected into the sandbox."""
        if not self._js_cache:
            bridge_path = Path(__file__).parents[1] / "static" / "bridge.js"
            harvester_path = self.static_dir / "openjscad_harvester.js"
            
            bridge_js = bridge_path.read_text(encoding="utf-8")
            harvester_js = harvester_path.read_text(encoding="utf-8")
            
            self._js_cache = f"{bridge_js}\n\n{harvester_js}"
        return self._js_cache

    def parse_telemetry(self, telemetry: SandboxTelemetry) -> object | None: # architectural: allowed-object (CAD Code)
        """Map raw sandbox telemetry to specific CAD contracts."""
        if telemetry.event_name == "code_update":
            return telemetry.payload
        return None
