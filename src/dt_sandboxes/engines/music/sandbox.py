"""Music sandbox implementation."""

from dt_contracts.sandboxes.base import SandboxType

from dt_sandboxes.base import BaseSandbox
from dt_sandboxes.schemas import BaseTelemetry

from .harvester import MusicHarvester


class MusicSandbox(BaseSandbox[BaseTelemetry]):
    """Sandbox environment for BeepBox."""

    def __init__(self, sandbox_id: str) -> None:
        """Initialize the music sandbox.

        Args:
            sandbox_id: Unique identifier for the sandbox.

        """
        super().__init__(sandbox_id, SandboxType.BEEPBOX)
        self.harvester = MusicHarvester()

    async def start(self) -> None:
        """Start the music environment."""
        self.is_running = True

    async def stop(self) -> None:
        """Stop the music environment."""
        self.is_running = False
