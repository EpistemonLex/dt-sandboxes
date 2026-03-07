"""Python controller for the CAD (BlocksCAD/OpenJSCAD) Harvester."""

from pathlib import Path
from typing import TYPE_CHECKING

from dt_contracts.sandboxes.base import SandboxTelemetry

if TYPE_CHECKING:
    from dt_contracts.sandboxes.base import SandboxTelemetry

class CADHarvester:
    """Manages telemetry parsing for 3D modeling sandboxes."""

    def __init__(self) -> None:
        """Initialize the CAD harvester."""
        self.static_dir = Path(__file__).parent / "static"
        self._js_cache: str | None = None

    def get_injection_js(self) -> str:
        """Return the JavaScript string to be injected into the sandbox."""
        if not self._js_cache:
            js_path = self.static_dir / "harvester.js"
            self._js_cache = js_path.read_text(encoding="utf-8")
        return self._js_cache

    def parse_telemetry(self, _telemetry: SandboxTelemetry) -> object | None: # architectural: allowed-object (CAD State)
        """Map raw sandbox telemetry to specific CAD contracts."""
        # Note: We will use a generic placeholder until we define
        # the specific 3D entity models in dt-contracts.
        return None
