"""Python controller for the Starboard Notebook Harvester."""

from pathlib import Path
from typing import TYPE_CHECKING

from dt_contracts.sandboxes.base import SandboxTelemetry
from pydantic import TypeAdapter

class StarboardHarvester:
    """Manages cell-level state harvesting for Starboard literate notebooks."""

    def __init__(self) -> None:
        """Initialize the Starboard harvester."""
        # Create directory if it doesn't exist
        self.static_dir = Path(__file__).parent / "static"
        self.static_dir.mkdir(parents=True, exist_ok=True)
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

    def parse_telemetry(self, telemetry: SandboxTelemetry) -> object | None: # architectural: allowed-object (Notebook State)
        """Map raw sandbox telemetry to specific Starboard contracts."""
        if telemetry.event_name == "notebook_update":
            return telemetry.payload
        return None
