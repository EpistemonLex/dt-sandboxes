"""Python controller for the Logic (MakeCode) Harvester."""

from pathlib import Path
from typing import TYPE_CHECKING

from dt_contracts.sandboxes.base import SandboxTelemetry, SandboxType
from pydantic import TypeAdapter

class LogicHarvester:
    """Manages JS harvester injection and telemetry parsing for Logic engines."""

    def __init__(self, engine_type: SandboxType) -> None:
        """Initialize the logic harvester."""
        self.engine_type = engine_type
        self.static_dir = Path(__file__).parent / "static"
        self._js_cache: str | None = None

    def get_injection_js(self) -> str:
        """Return the JavaScript string to be injected into the sandbox."""
        if not self._js_cache:
            bridge_path = Path(__file__).parents[1] / "static" / "bridge.js"
            
            if self.engine_type == SandboxType.MAKECODE:
                harvester_path = self.static_dir / "makecode_harvester.js"
            else:
                # Fallback to snap if needed or generic
                harvester_path = self.static_dir / "makecode_harvester.js"
            
            bridge_js = bridge_path.read_text(encoding="utf-8")
            harvester_js = harvester_path.read_text(encoding="utf-8")
            
            self._js_cache = f"{bridge_js}\n\n{harvester_js}"
        return self._js_cache

    def parse_telemetry(self, telemetry: SandboxTelemetry) -> object | None: # architectural: allowed-object (Logic State)
        """Map raw sandbox telemetry to specific Logic contracts."""
        return telemetry.payload
