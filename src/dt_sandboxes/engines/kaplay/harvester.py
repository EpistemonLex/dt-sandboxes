"""Python controller for the Kaplay.js Harvester."""

from pathlib import Path
from typing import TYPE_CHECKING

from dt_contracts.sandboxes.base import SandboxTelemetry
from dt_contracts.sandboxes.kaplay import KaplayCompilationError, KaplayState
from pydantic import TypeAdapter


class KaplayHarvester:
    """Manages the JS harvester injection and telemetry parsing for Kaplay."""

    def __init__(self) -> None:
        """Initialize the harvester."""
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

    def parse_telemetry(self, telemetry: SandboxTelemetry) -> KaplayState | KaplayCompilationError | None:
        """Map raw sandbox telemetry to specific Kaplay contracts."""
        if telemetry.event_name == "state_update":
            return TypeAdapter(KaplayState).validate_python(telemetry.payload)

        if telemetry.event_name == "compilation_error":
            return TypeAdapter(KaplayCompilationError).validate_python(telemetry.payload)

        return None
