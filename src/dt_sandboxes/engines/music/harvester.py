"""Python controller for the BeepBox/Music Harvester."""

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dt_contracts.sandboxes.base import SandboxTelemetry
    from dt_contracts.sandboxes.music import MusicState


class MusicHarvester:
    """Manages the JS harvester injection and telemetry parsing for Music engines."""

    def __init__(self) -> None:
        """Initialize the music harvester."""
        self.static_dir = Path(__file__).parent / "static"
        self._js_cache: str | None = None

    def get_injection_js(self) -> str:
        """Return the JavaScript string to be injected into the sandbox."""
        if not self._js_cache:
            js_path = self.static_dir / "harvester.js"
            self._js_cache = js_path.read_text(encoding="utf-8")
        return self._js_cache

    def parse_telemetry(self, telemetry: SandboxTelemetry) -> MusicState | None:
        """Map raw sandbox telemetry to specific Music contracts."""
        if telemetry.event_name == "state_update":
            # For BeepBox, we might need a parser for the URL hash in the future.
            # For now, we validate the basic structure.
            return None  # Placeholder until hash parser is implemented
        return None
