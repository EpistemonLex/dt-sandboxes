"""Art sandbox implementation (Piskel)."""

from dt_contracts.sandboxes.base import SandboxType

from dt_sandboxes.base import BaseSandbox
from dt_sandboxes.schemas import BaseTelemetry

from .harvester import ArtHarvester


class ArtSandbox(BaseSandbox[BaseTelemetry]):
    """Sandbox environment for Raster Art (Piskel)."""

    def __init__(self, sandbox_id: str, engine_type: SandboxType = SandboxType.PISKEL) -> None:
        """Initialize the art sandbox.

        Args:
            sandbox_id: Unique identifier for the sandbox.
            engine_type: The specific engine (PISKEL).

        """
        super().__init__(sandbox_id, engine_type)
        self.harvester = ArtHarvester(engine_type)

    async def start(self) -> None:
        """Start the art environment."""
        self.is_running = True

    async def stop(self) -> None:
        """Stop the art environment."""
        self.is_running = False
