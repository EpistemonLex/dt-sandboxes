"""Python controller for the Electronics (CircuitJS, Q.js) Harvester."""

from pathlib import Path
from typing import TYPE_CHECKING

from dt_contracts.sandboxes.base import SandboxTelemetry, SandboxType
from pydantic import TypeAdapter

class ElectronicsHarvester:
    """Manages JS harvester injection and telemetry parsing for Electronics engines."""

    def __init__(self, engine_type: SandboxType) -> None:
        """Initialize the electronics harvester.

        Args:
            engine_type: The specific engine (CIRCUITJS or QJS).
        """
        self.engine_type = engine_type
        self.static_dir = Path(__file__).parent / "static"
        self._js_cache: str | None = None

    def get_injection_js(self) -> str:
        """Return the JavaScript string to be injected into the sandbox."""
        if not self._js_cache:
            bridge_path = Path(__file__).parents[1] / "static" / "bridge.js"
            
            if self.engine_type == SandboxType.CIRCUITJS:
                harvester_path = self.static_dir / "circuitjs_harvester.js"
            else:
                harvester_path = self.static_dir / "qjs_harvester.js"
            
            bridge_js = bridge_path.read_text(encoding="utf-8")
            harvester_js = harvester_path.read_text(encoding="utf-8")
            
            self._js_cache = f"{bridge_js}\n\n{harvester_js}"
        return self._js_cache

    def parse_telemetry(self, telemetry: SandboxTelemetry) -> object | None: # architectural: allowed-object (Electronics State)
        """Map raw sandbox telemetry to specific Electronics contracts."""
        # For now, we pass the raw JSON.
        # Future: Use contracts from dt_contracts.sandboxes.electronics.
        return telemetry.payload
