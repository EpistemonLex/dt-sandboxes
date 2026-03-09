"""Python controller for the BeepBox Harvester."""

from pathlib import Path
from typing import TYPE_CHECKING

from dt_contracts.sandboxes.base import SandboxTelemetry
from pydantic import TypeAdapter

from dt_contracts.sandboxes.music import MusicState

class BeepBoxHarvester:
    """Manages URL-based state harvesting for the BeepBox chiptune engine."""

    def __init__(self) -> None:
        """Initialize the BeepBox harvester."""
        self.static_dir = Path(__file__).parent / "static"
        self._js_cache: str | None = None

    def get_injection_js(self) -> str:
        """Return the JavaScript string to be injected into the sandbox."""
        if not self._js_cache:
            bridge_path = Path(__file__).parents[1] / "static" / "bridge.js"
            harvester_path = self.static_dir / "beepbox_harvester.js"
            
            bridge_js = bridge_path.read_text(encoding="utf-8")
            harvester_js = harvester_path.read_text(encoding="utf-8")
            
            self._js_cache = f"{bridge_js}\n\n{harvester_js}"
        return self._js_cache

    def parse_telemetry(self, telemetry: SandboxTelemetry) -> MusicState | dict[str, object] | None:
        """Map raw sandbox telemetry to specific BeepBox contracts."""
        if telemetry.event_name == "state_update":
            return TypeAdapter(MusicState).validate_python(telemetry.payload)
        
        if telemetry.event_name == "hash_update":
            return telemetry.payload
            
        return None
