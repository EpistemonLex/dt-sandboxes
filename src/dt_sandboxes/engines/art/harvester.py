"""Python controller for the Art (Piskel) Harvester."""

from pathlib import Path
from typing import TYPE_CHECKING

from dt_contracts.sandboxes.base import SandboxTelemetry, SandboxType
from pydantic import TypeAdapter

class ArtHarvester:
    """Manages JS harvester injection and telemetry parsing for Art engines."""

    def __init__(self, engine_type: SandboxType) -> None:
        """Initialize the art harvester."""
        self.engine_type = engine_type
        self.static_dir = Path(__file__).parent / "static"
        self._js_cache: str | None = None

    def get_injection_js(self) -> str:
        """Return the JavaScript string to be injected into the sandbox."""
        if not self._js_cache:
            bridge_path = Path(__file__).parents[1] / "static" / "bridge.js"
            
            if self.engine_type == SandboxType.PISKEL:
                harvester_path = self.static_dir / "piskel_harvester.js"
            else:
                harvester_path = self.static_dir / "piskel_harvester.js"
            
            bridge_js = bridge_path.read_text(encoding="utf-8")
            harvester_js = harvester_path.read_text(encoding="utf-8")
            
            self._js_cache = f"{bridge_js}\n\n{harvester_js}"
        return self._js_cache

    def parse_telemetry(self, telemetry: SandboxTelemetry) -> object | None: # architectural: allowed-object (Art State)
        """Map raw sandbox telemetry to specific Art contracts."""
        return telemetry.payload
