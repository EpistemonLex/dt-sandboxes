"""Python controller for the Minetest Lua Harvester."""

from pathlib import Path
from typing import TYPE_CHECKING

from dt_contracts.sandboxes.minetest import BlockEvent, MinetestState
from pydantic import TypeAdapter

if TYPE_CHECKING:
    from dt_contracts.sandboxes.base import SandboxTelemetry

class MinetestHarvester:
    """Manages the Lua mod injection and telemetry parsing for Minetest."""

    def __init__(self) -> None:
        """Initialize the minetest harvester."""
        self.mod_dir = Path(__file__).parent / "static" / "mod"

    def get_mod_path(self) -> Path:
        """Return the path to the Lua mod directory for injection."""
        return self.mod_dir

    def parse_telemetry(self, telemetry: SandboxTelemetry) -> MinetestState | BlockEvent | None:
        """Map raw sandbox telemetry to specific Minetest contracts."""
        if telemetry.event_name == "state_update":
            return TypeAdapter(MinetestState).validate_python(telemetry.payload)

        if telemetry.event_name == "block_event":
            return TypeAdapter(BlockEvent).validate_python(telemetry.payload)

        return None
