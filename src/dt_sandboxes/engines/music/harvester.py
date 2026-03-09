"""Python controller for the Strudel (Music) Harvester."""

from pathlib import Path
from typing import TYPE_CHECKING

from dt_contracts.sandboxes.base import SandboxTelemetry
from dt_contracts.sandboxes.music import MusicState
from pydantic import TypeAdapter

class MusicHarvester:
    """Manages the JS harvester injection and telemetry parsing for Strudel."""

    def __init__(self) -> None:
        """Initialize the strudel harvester."""
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

    def parse_telemetry(self, telemetry: SandboxTelemetry) -> MusicState | None:
        """Map raw sandbox telemetry to specific Music contracts."""
        if telemetry.event_name == "rhythm_stats":
            # Map Strudel's stats to MusicState
            # bpm is directly available
            # CPS (cycles per second) is also there
            return TypeAdapter(MusicState).validate_python({
                "bpm": telemetry.payload.get("bpm", 120.0),
                "key": "C", # Strudel doesn't always expose key easily
                "tracks_count": 1,
                "active_pattern": []
            })
        return None
