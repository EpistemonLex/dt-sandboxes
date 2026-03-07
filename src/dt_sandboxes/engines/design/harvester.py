"""Python controller for the Design (tldraw) Harvester."""

from pathlib import Path
from typing import TYPE_CHECKING

from dt_contracts.sandboxes.base import SandboxTelemetry
from dt_contracts.sandboxes.design import DesignState
from pydantic import TypeAdapter

if TYPE_CHECKING:
    from dt_contracts.sandboxes.base import SandboxTelemetry

class DesignHarvester:
    """Manages telemetry parsing for visual thinking canvases."""

    def __init__(self) -> None:
        """Initialize the design harvester."""
        self.static_dir = Path(__file__).parent / "static"
        self._js_cache: str | None = None

    def get_injection_js(self) -> str:
        """Return the JavaScript string to be injected into the sandbox."""
        if not self._js_cache:
            js_path = self.static_dir / "harvester.js"
            self._js_cache = js_path.read_text(encoding="utf-8")
        return self._js_cache

    def parse_telemetry(self, telemetry: SandboxTelemetry) -> DesignState | None:
        """Map raw sandbox telemetry to specific Design contracts."""
        if telemetry.event_name == "state_update":
            return TypeAdapter(DesignState).validate_python(telemetry.payload)
        return None
