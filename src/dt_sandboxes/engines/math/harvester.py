"""Python controller for the Math (Mathigon, GeoGebra) Harvester."""

from pathlib import Path
from typing import TYPE_CHECKING

from dt_contracts.sandboxes.base import SandboxTelemetry, SandboxType
from pydantic import TypeAdapter

class MathHarvester:
    """Manages JS harvester injection and telemetry parsing for Math engines."""

    def __init__(self, engine_type: SandboxType) -> None:
        """Initialize the math harvester.

        Args:
            engine_type: The specific engine (MATHIGON or GEOGEBRA).
        """
        self.engine_type = engine_type
        self.static_dir = Path(__file__).parent / "static"
        self._js_cache: str | None = None

    def get_injection_js(self) -> str:
        """Return the JavaScript string to be injected into the sandbox."""
        if not self._js_cache:
            bridge_path = Path(__file__).parents[1] / "static" / "bridge.js"
            
            if self.engine_type == SandboxType.MATHIGON:
                harvester_path = self.static_dir / "mathigon_harvester.js"
            else:
                harvester_path = self.static_dir / "geogebra_harvester.js"
            
            bridge_js = bridge_path.read_text(encoding="utf-8")
            harvester_js = harvester_path.read_text(encoding="utf-8")
            
            self._js_cache = f"{bridge_js}\n\n{harvester_js}"
        return self._js_cache

    def parse_telemetry(self, telemetry: SandboxTelemetry) -> object | None: # architectural: allowed-object (Math State)
        """Map raw sandbox telemetry to specific Math contracts."""
        return telemetry.payload
